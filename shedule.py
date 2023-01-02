import schedule
import time

def job():
    s=0
    for i in range(10):
       s+=i
    print(s)

schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)