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
        