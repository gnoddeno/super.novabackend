from django.contrib import admin

# Register your models here.
from .models import User  # User 모델을 import합니다.
from .models import Semester  # Semester 모델을 import합니다.
from .models import Quiz
from .models import TimeSlot

# User 모델을 admin 사이트에 등록합니다.
admin.site.register(User)
admin.site.register(Semester)
admin.site.register(Quiz)
admin.site.register(TimeSlot)
