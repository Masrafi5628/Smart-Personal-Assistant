import csv
import datetime
from gtts import gTTS
from playsound import playsound
import time
import schedule

def control():
    evt_name = []
    evt_date = []
    evt_time = []
    alarm_list = []
    evt = []

    with open("event_data.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            evt.append((row[1], row[0], row[2]))
        file.close()

    evt.sort()
    #print(evt)
    # print(evt_date)

    for i in range(len(evt)):
        evt_name.append(evt[i][1])
        evt_date.append(evt[i][0])
        evt_time.append(evt[i][2])
    #print(evt_time)

    cur_time = datetime.datetime.now()
    # print(cur_time)

    for i in range(len(evt_time)):

        n = evt_time[i]
        a = n.split()
        tm, day = a[0], a[1]
        sagor = tm.split(':')
        hr = int(sagor[0])
        mn = int(sagor[1])
        # print(a)
        # print(hr, mn)
        mn = mn - 10
        alarm_mn = int(mn)
        alarm_hr = int(hr)

        if (alarm_mn < 0):
            alarm_hr -= 1
            alarm_mn = 60 + (alarm_mn)

        if day == 'PM' and alarm_hr != 12:
            alarm_hr += 12

        alarm_hr_str = str(alarm_hr)
        if len(alarm_hr_str) == 1:
            alarm_hr_str = str(0) + alarm_hr_str

        alarm_mn_str = str(alarm_mn)
        if len(alarm_mn_str) == 1:
            alarm_mn_str = str(0) + alarm_mn_str

        alarm_time = f"{alarm_hr_str}{':'}{alarm_mn_str}"
        #print(alarm_time, end=' ')
        alarm_list.append(alarm_time)
    return alarm_list,evt_name,evt_date,evt_time

    '''
    date_set = cur_time.strftime("%m/%d/%y")
    time_set = cur_time.strftime("%H:%M")

    cur_alarm_time = alarm_list[0]
    cur_alarm_date = evt_date[0]
    cur_alarm_name = evt_name[0]
    cur_event_time = evt_time[0]

    # print(cur_alarm_name,cur_alarm_date,cur_alarm_time)
    print(time_set)
    print(date_set)

    if date_set == cur_alarm_date and time_set == cur_alarm_time:
        my_text = f"Your event {cur_alarm_name} is scheduled at {cur_event_time}"
        tts = gTTS(text=my_text, lang='en')
        filename = 'alarm.mp3'
        tts.save(filename)
        playsound('alarm.mp3')
    '''