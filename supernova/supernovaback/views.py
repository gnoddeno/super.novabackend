from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
#from drf_yasg import openapi
#from drf_yasg.utils import swagger_auto_schema
from .time_talbe import loadtalbe
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