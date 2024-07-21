from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
#from drf_yasg import openapi
#from drf_yasg.utils import swagger_auto_schema
from .time_table import loadtable
from .models import User
from .models import Semester
import time
from .models import TimeSlot
from .models import Quiz

class main(APIView):
    def get(self, request):

        # 1 input data
        data = request.GET
        user_id = data.get('userId')
        is_new_user = False

        # 2 check userId exists
        user_objects = User.objects.filter(id=user_id)
        if not user_objects.exists():
            User.objects.create(id=user_id)
            is_new_user = True


        # 3 load semester data
        semester_object = Semester.objects.first()

        # 4 struct response
        print(user_id)
        user_object = User.objects.get(id=user_id)
        response = {"pet_code": user_object.pet_code,
                    "pet_xp": user_object.pet_xp,
                    "is_new_user": is_new_user,
                    "year_info": semester_object.year,
                    "semester_info": semester_object.semester
                    }

        # 5 send response
        return Response(response, status=status.HTTP_200_OK)


class timetable(APIView):
    """
    시간표 정보를 받아와서 저장
    """
    def get(self, request):
        # 1 input data
        data = request.GET
        user_id = data.get('userid')
        path = data.get('path')
        print(path)
        # 2 load timetable
        time_table, total_empty_time = loadtable(path)
        TimeSlot.objects.create(userid=user_id, time_table=time_table, empty_time=total_empty_time)
        print(TimeSlot.objects.all().values())

        # 3 struct response
        response = {"empty_time": total_empty_time,
                    "time_table": time_table,
                    "user_id": user_id
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
        user_id = data.get('userid')

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
                    "user_id": user_id
                    }

        # 4 send response
        return Response(response, status=status.HTTP_200_OK)



'''
@api_view(['PATCH'])    
def loadtimetalbe(request):
    if request.method == 'PATCH':
        userid = request.data.get('userid')
        path = request.data.get('path')
        time_table, total_empty_time = loadtalbe(path)
        TimeSlot.objects.create(userid=userid, time_table=time_table, empty_time=total_empty_time)
        if total_empty_time > 0:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
'''
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

            # 4 start timer
            user_object.timer_on = True
            user_object.timer_recent = int(time.time())

            # 5 save user object
            user_object.save()

            # 6 send response
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
            user_object.pet_xp += int(time.time()) - user_object.timer_recent

            # 5 save user object
            user_object.save()

            # 6 send response
            return Response({"message": "Timer stopped"}, status=status.HTTP_200_OK)

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

            # 3 check timer is on
            if not user_object.timer_on:
                return Response({"remaining_time": 0}, status=status.HTTP_200_OK)

            # 4 calculate remaining time
            time_passed = int(time.time()) - user_object.timer_recent

            # 5 send response
            return Response({"time_passed": time_passed}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class quiz(APIView):
    def get(self, request):
        try:
            # 1 get quiz object
            quiz_object = Quiz.objects.first()

            # 2 send response
            return Response({"title": quiz_object.title,
                             "content": quiz_object.content,
                             "answer": quiz_object.answer
                             }, status=status.HTTP_200_OK)

        except Quiz.DoesNotExist:
            return Response({"message": "No Quiz Found"}, status=status.HTTP_404_NOT_FOUND)
