from django.http import HttpResponse
from .models import User

def index(request):
    return HttpResponse("배포 test입니다.")

def create(request):
    name = request.GET.get('name')
    id = request.GET.get('id')
    user = User.objects.create(name=name, id=id)
    user.save()
    

def login(request):
    name = request.GET.get('name')
    id = request.GET.get('id')
    