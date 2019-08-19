from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

sched = BlockingScheduler()

@sched.scheduled_job('cron', minute=0)
def startNotify():
    # TODO: All this task needs to do is enqueue a task
    print (datetime.datetime.now())
    print('This job runs every hour')

sched.start()