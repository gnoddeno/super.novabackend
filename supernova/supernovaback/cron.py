from supernovaback.models import User

def reset_database_values():
    User.objects.update(timer_sum=0)
