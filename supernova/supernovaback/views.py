import json

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db.models import F
#from drf_yasg import openapi
#from drf_yasg.utils import swagger_auto_schema
from .time_table import loadtable, loadempty
from .models import User, Semester, TimeSlot, Quiz, Answer, Category
import time
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from .timer_checker import get_sec_passed
from .emptycalc import get_weekly_empty_time, get_all_xp_ptg
import pytz

class main(APIView):
    def get(self, request):
        # 1 input data
        data = request.GET
        user_id = data.get('userId')
        is_new_user = False

        # 2 check userId exists
        try:
            user_object = User.objects.get(id=user_id)
        except User.DoesNotExist:
            if "@" not in user_id:
                return Response({"error": "userId not valid"}, status=status.HTTP_400_BAD_REQUEST)

            user_object = User.objects.create(id=user_id)
            is_new_user = True

        empty_time = get_weekly_empty_time(user_id)
        # 3 load semester data
        try:
            semester_object = Semester.objects.first()
            if semester_object is None:
                return Response({"error": "Semester data not found"}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response({"error": "Semester data not found"}, status=status.HTTP_404_NOT_FOUND)
        
        ptg = get_all_xp_ptg(user_object)


        # 4 struct response
        response = {
            "pet_code": user_object.pet_code,
            "pet_xp": user_object.pet_xp,
            "pet_ptg": ptg,
            "is_new_user": is_new_user,
            "year_info": semester_object.year,
            "semester_info": semester_object.semester,
            "empty_time": empty_time,
            "timer_sum": user_object.timer_sum
        }

        # 5 send response
        return Response(response, status=status.HTTP_200_OK)


class timetable(APIView):
    """
    시간표 정보를 받아와서 저장
    """
    def post(self, request):
        # 1 input data
        data = request.data
        user_id = data.get('userId')
        path = data.get('path')
        # 2 load timetable
        # if aleady_exist := TimeSlot.objects.filter(userid=user_id).exists():
        #     TimeSlot.objects.filter(userid=user_id).delete()
        if TimeSlot.objects.filter(userid=user_id).exists():
            return Response({"message": "Time table already exists"}, status=status.HTTP_400_BAD_REQUEST)

        time_table, total_empty_time = loadtable(path)
        TimeSlot.objects.create(userid=user_id, time_table=time_table, empty_time=total_empty_time)
        print(TimeSlot.objects.all().values())

        # 3 struct response
        response = {"empty_time": total_empty_time,
                    "user_Id": user_id
                    }

        # 4 send response
        return Response(response, status=status.HTTP_201_CREATED)

class gettimetable(APIView):
    """
    유저 정보를 바탕으로 시간표 출력
    """
    def get(self, request):
        # 1 input data
        data = request.GET
        user_id = data.get('userId')

        # 2 load timetable
        time_slot_objects = TimeSlot.objects.filter(userid=user_id)
        if not time_slot_objects.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        time_slot_object = time_slot_objects.first()
        time_table = time_slot_object.time_table
        total_empty_time = time_slot_object.empty_time


        # 3 struct response
        response = {"empty_time": total_empty_time,
                    "time_table": time_table,
                    "user_Id": user_id
                    }
        print(response)

        # 4 send response
        return Response(response, status=status.HTTP_200_OK)


class start_timer(APIView):
    def post(self, request):
        try:
            # 1 get user from request
            data = request.data
            user_id = data.get('userId')

            # 2 get user object
            user_object = User.objects.get(id=user_id)

            # 3 check timer is already on
            if user_object.timer_on:
                response = {"message": "Timer is already on"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # 4 get korean utc time
            now_utc = datetime.now(pytz.utc)
            now_seoul = now_utc.astimezone(pytz.timezone('Asia/Seoul'))

            # 5 start timer
            user_object.timer_on = True
            user_object.timer_recent = int(now_seoul.timestamp())

            # 6 save user object
            user_object.save()

            # 7 send response
            return Response({"message": "Timer started"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class stop_timer(APIView):
    def post(self, request):
        try:
            # 1 get user from request
            data = request.data
            user_id = data.get('userId')

            # 2 get user object
            user_object = User.objects.get(id=user_id)

            # 3 check timer is already off
            if not user_object.timer_on:
                response = {"message": "Timer is already off"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # 4 stop timer
            user_object.timer_on = False
            time_added = int(time.time()) - user_object.timer_recent
            user_object.pet_xp += time_added
            if user_object.pet_xp >= 374400:
                user_object.pet_xp = 374400
            user_object.timer_sum += time_added

            ptg = get_all_xp_ptg(user_object)
            added_ptg = ptg - user_object.pet_ptg
            user_object.pet_ptg = ptg

            # 5 save user object
            user_object.save()

            # 6 send response
            return Response({"added_ptg": added_ptg}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class timer(APIView):
    def get(self, request):
        try:
            # 1 get user from request
            data = request.GET
            user_id = data.get('userId')

            # 2 get user object
            user_object = User.objects.get(id=user_id)

            # 3 get korean utc time
            now_utc = datetime.now(pytz.utc)
            now_seoul = now_utc.astimezone(pytz.timezone('Asia/Seoul'))
            weekday = now_seoul.weekday()
            formatted_time = now_seoul.strftime("%H:%M:%S")
            print(f"현재 한국 시간: {formatted_time}")
            print(f"오늘의 요일(정수): {weekday}")

            # 4 get timetable
            time_slot_object = TimeSlot.objects.get(userid=user_id)
            time_table = time_slot_object.time_table

            if isinstance(time_table, str):
                schedule = json.loads(time_table)
            else:
                schedule = time_table
            today_time_table = schedule[weekday]


            # 5 get number of "0" between first "1" and last "1"
            sum_empty_time = 0
            continuous_empty_time = 0
            arrived_school = False
            for i in range(len(today_time_table)):

                if today_time_table[i] == 1:
                    arrived_school = True
                    if continuous_empty_time > 0:
                        sum_empty_time += continuous_empty_time
                        continuous_empty_time = 0
                elif today_time_table[i] == 0 and arrived_school:
                    continuous_empty_time += 5

            today_total_min = sum_empty_time

            unix_time = get_sec_passed(user_object, today_time_table)

            # 6 check timer is not on
            if not user_object.timer_on:
                return Response({"unix_time": 0,
                                 "today_total_min": today_total_min
                                 }, status=status.HTTP_200_OK)


            # 7 send response
            return Response({"unix_time": unix_time,
                             "today_total_min": today_total_min
                             }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        except TimeSlot.DoesNotExist:
            return Response({"message": "TimeSlot not found"}, status=status.HTTP_404_NOT_FOUND)


class quiz(APIView):
    def get(self, request):
        try:
            # 1 get quiz object
            quiz_object = Quiz.objects.first()
            if quiz_object is None:
                return Response({"message": "No Quiz Found"}, status=status.HTTP_404_NOT_FOUND)

            # 2 send response
            return Response({"title": quiz_object.title,
                             "content": quiz_object.content
                             }, status=status.HTTP_200_OK)

        except Quiz.DoesNotExist:
            return Response({"message": "No Quiz Found"}, status=status.HTTP_404_NOT_FOUND)


class submit(APIView):
    def post(self, request):
        try:
            # 1 get user from request
            data = request.data
            user_id = data.get('userId')
            answer = data.get('answer')

            # 2 get current quiz object
            quiz_object = Quiz.objects.first()

            # 3 create answer object for above quiz
            Answer.objects.create(user_id=user_id, quiz_id=quiz_object.id)

            # 4 return response check answer is correct
            if answer == quiz_object.answer:
                return Response({"is_correct": True}, status=status.HTTP_200_OK)
            else:
                return Response({"is_correct": False}, status=status.HTTP_200_OK)

        except Quiz.DoesNotExist:
            return Response({"message": "No Quiz found"}, status=status.HTTP_404_NOT_FOUND)


class pet_select(APIView):
    def post(self, request):
        try:
            # 1 get user from request
            data = request.data
            user_id = data.get('userId')
            pet_code = data.get('pet_code')

            # 2 get user object
            user_object = User.objects.get(id=user_id)

            # 3 check pet code is initial value
            if user_object.pet_code > 0:
                response = {"change_valid": False}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # 4 check pet code is valid
            if pet_code < 1 or pet_code > 4:
                response = {"change_valid": False}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # 5 update pet code
            user_object.pet_code = pet_code
            user_object.save()

            # 6 send response
            return Response({"message": "Pet code updated"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class createquiz(APIView):
    """
    문제 출제 기능
    """
    def post(self, request):
        data = request.data
        title = data.get('title')
        content = data.get('content')
        answer = data.get('answer')
        password = data.get('password')
        if password != Semester.objects.first().password:
            return Response({"message": "Password not correct"}, status=status.HTTP_400_BAD_REQUEST)
        Quiz.objects.create(title=title, content=content, answer=answer)
        print(data)
        return Response({"message": "Quiz created"}, status=status.HTTP_200_OK)

class top10(APIView):
    """
    상위 10명의 유저 정보 출력
    """
    def get(self, request):
        user_objects = User.objects.all().order_by('-pet_ptg')[:10]
        response = []
        for user_object in user_objects:
            response.append({"user_id": user_object.id,
                             "pet_ptg": user_object.pet_ptg
                             })
        return Response(response, status=status.HTTP_200_OK)


class getempty(APIView):
    """
    요일별 공강시간
    """
    def get(self, request):
        # 1 input data
        data = request.GET
        user_id = data.get('userId')
        day = data.get('day')

        # 2 load timetable
        time_slot_objects = TimeSlot.objects.filter(userid=user_id)
        if not time_slot_objects.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        time_slot_object = time_slot_objects.first()
        time_table = time_slot_object.time_table

        day_empty_time = loadempty(day, time_table)


        # 3 struct response
        response = {"empty_time": day_empty_time,
                    "user_Id": user_id
                    }
        print(response)

        # 4 send response
        return Response(response, status=status.HTTP_200_OK)
    
class choiceCategory(APIView):
    def patch(self, request):
        data = request.data
        choice_data = data.get('category')
        if Category.objects.count() == 0:
            Category.objects.create()
        category_instance = Category.objects.first()
        if choice_data =="read":
            category_instance.read += 1
        elif choice_data =="walk":
            category_instance.walk += 1
        elif choice_data =="movie":
            category_instance.movie += 1
        elif choice_data =="workout":
            category_instance.workout += 1  
        elif choice_data =="study":
            category_instance.study += 1    
        elif choice_data =="sleep":
            category_instance.sleep += 1
        else:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        category_instance.save()
        return Response({"message": "Category updated"}, status=status.HTTP_200_OK)

    
class rankCategory(APIView):
    def get(self, request):
        if Category.objects.count() == 0:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        category_instance = Category.objects.first()
        response = {
            "read": category_instance.read,
            "walk": category_instance.walk,
            "movie": category_instance.movie,
            "workout": category_instance.workout,
            "study": category_instance.study,
            "sleep": category_instance.sleep
        }
        sorted_response = dict(sorted(response.items(), key=lambda item: item[1], reverse=True))
        return Response(sorted_response, status=status.HTTP_200_OK)
