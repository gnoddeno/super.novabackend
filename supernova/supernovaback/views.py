from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
#from drf_yasg import openapi
#from drf_yasg.utils import swagger_auto_schema
from .models import User
from .models import Semester

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

