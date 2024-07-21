from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
#from drf_yasg import openapi
#from drf_yasg.utils import swagger_auto_schema
from .time_table import loadtable
from .models import User
from .models import Semester
from .models import TimeSlot

class main(APIView):
    """
    스테이지 생성 후 스테이지 ID 반환
    """
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