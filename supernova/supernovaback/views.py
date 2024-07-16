from django.http import HttpResponse

def index(request):
    return HttpResponse("배포 test입니다.")