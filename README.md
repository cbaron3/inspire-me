# Inspire.Me
Service that you sign up and receive a daily inspirational quote
Need two endpoints:

1) /subscribe/[number]
    endpoint when user subscribes to the service
    results:
        add number to NewUsers
        send text

2) /receive/[number]?[content]
    connected with twillo so triggered on every text received
    results:

        1) if number is in NewUsers
            if content says YES
                remove from NewUsers
                add to ConfirmedUsers
                respond with "Thanks you are confirmed"
            else
                nothing or tell user to send something
                respond with something

        2) if number is in ConfirmedUsers
            if content says STOP
                remove from ConfirmedUsers
                respond with thanks message

        3) Else, number in neither table
            respond with "Please subscribe at https://..."

        instead of using two tables, use one table called Users that has PhoneNumber, Confirmed, TimeZone

Also need a process to run every 24 hours to send a message to all subcribers. also can add timezone

How the schedule will work is as follows:

1) have clock process do something every X amount of time
https://devcenter.heroku.com/articles/clock-processes-python
2) when that clock process is triggered, dont do actual work in that function but schedule a background task instead
https://devcenter.heroku.com/articles/scheduled-jobs-custom-clock-processes#overview
3) background task will query database for all confirmed users and send them a text
https://devcenter.heroku.com/articles/python-rq

also need the whole api access

also need table to store quotes to make sure no duplicates. If duplicate query random table element and resend

predicted files:
init
    init app
config
    app configuration
model
    database oom
clock
    used for scheduled processes
routes
    hold routes for app
quotes
    api access
manage
    db migrations
run
    run app