from datetime import datetime, timezone, timedelta
from pytz import timezone


def get_sec_passed(user_object, today_time_table):
    dt_seoul = datetime.now(timezone('Asia/Seoul'))
    start_time = user_object.timer_recent
    midnight = dt_seoul.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    examined_time = int(midnight)
    prev_flag = 0
    flag_count = 0
    maximum_empty_sec = 0

    for i in range(len(today_time_table)):
        examined_time += 5 * 60
        if today_time_table[i] == 1 and prev_flag == 0:
            flag_count += 1
            prev_flag = 1
            if flag_count == 1 and start_time < examined_time:
                return 0

            if flag_count >= 2 and start_time < examined_time:
                maximum_empty_sec = examined_time - start_time
                break
        elif today_time_table[i] == 0 and prev_flag == 1:
            prev_flag = 0

    print(flag_count)
    original_time = int(dt_seoul.timestamp()) - user_object.timer_recent
    sec_passed = maximum_empty_sec

    # midnight = dt_seoul.replace(hour=0, minute=0, second=0, microsecond=0)
    # minutes_since_midnight = (dt_seoul - midnight).seconds // 60
    # offset_seconds = (dt_seoul - midnight).seconds % 60
    # start_index = minutes_since_midnight // 5
    # offset_minutes = minutes_since_midnight % 5



    # free_time = 0
    # if start_index < arrived_school:
    #     return 0
    # else:
    #     max_index = len(today_time_table)
    #
    #     for i in range(start_index, max_index):
    #         if today_time_table[i] == 0:
    #             free_time += 1
    #         else:
    #             break

    # sec_passed = (free_time * 5 + offset_minutes) * 60 + offset_seconds
    #sec_passed = free_time * 5 * 60
    print(f"original_time: {original_time}, sec_passed: {sec_passed}")
    return min(sec_passed, original_time)