from supernovaback.models import TimeSlot


def get_weekly_empty_time(user_id):
    time_slot_objects = TimeSlot.objects.filter(userid=user_id)
    if not time_slot_objects.exists():
        empty_time = 0
    else:
        empty_time = time_slot_objects.first().empty_time

    return empty_time


def get_all_xp_ptg(user_object):
    empty_time = get_weekly_empty_time(user_object.id)
    ptg = 0
    if empty_time > 0:
        ptg = (user_object.pet_xp / (empty_time * 5 * 60 * 15)) * 100

    return ptg