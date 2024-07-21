from datetime import time
import requests
import json
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

class Everytime:
    def __init__(self, path):
        url = urlparse(path)
        if url.netloc == "everytime.kr":
            self.path = url.path.replace("/@", "")
            return
        self.path = path

    def get_timetable(self):
        return requests.post(
            "https://api.everytime.kr/find/timetable/table/friend",
            data={
                "identifier": self.path,
                "friendInfo": 'true'
            },
            headers={
                "Accept": "*/*",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Host": "api.everytime.kr",
                "Origin": "https://everytime.kr",
                "Referer": "https://everytime.kr/",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
            }).text

def loadtable(path):
    time_table = [[0 for i in range(0,288)] for i in range(0,5)]
    root = ET.fromstring(Everytime(path).get_timetable())
    for subject in root.findall('table/subject'):
        for data in subject.findall('time/data'):
            day = int(data.get('day'))
            starttime = int(data.get('starttime'))
            endtime = int(data.get('endtime'))
            for time in range(starttime, endtime):
                time_table[day][time] += 1
    total_empty_time = 0
    for day in range(5):
        following = False
        endday = 0
        for time in range(0, 288):
            if time_table[day][time]==1:
                endday = time   
        for time in range(0, endday):
            if time_table[day][time]==1:
                following = True
            if time_table[day][time]==0 and following:
                total_empty_time += 1
    return time_table, total_empty_time

def loadempty(day,time_table):
    starttime = 0
    endtime = 0
    print(time_table)
    day_empty_time = []
    day = int(day)
    time_table = json.loads(time_table)
    time_table = [list(map(int, i)) for i in time_table]
    for time in range(0, 288):
        if time_table[day][time]==1:
            endday = time   
    for time in range(0, endday):
        if time_table[day][time]==1 and time_table[day][time+1]==0 and time != endday:
            starttime = time + 1
        if time_table[day][time]==0 and time_table[day][time+1]==1:
            endtime = time + 1
            if starttime != 0 and endtime != 0:
                day_empty_time.append((starttime,endtime))
    return day_empty_time