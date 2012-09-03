#!/bin/bash

NOTIFY_ADDRESS="gwpc114@gmail.com"
SUBJECT="There is a problem with www.icnfnt.com"
MESSAGE_BODY=`mktemp`
LOG_FILE=/var/log/tornado/tornado.5000.log
LOG_LINES=40

start() {
        python /srv/icnfont/cyclone.py
	status
}

stop() {
        kill `ps aux | grep python | grep cyclone | awk '{print $2}'`
}

status() {
        PID=`ps aux | grep python | grep cyclone | awk '{print $2}'`
        if [ "$PID" = "" ]; then
                echo "Tornado server not running."
        else
                echo "Tornado server is running. pid = $PID"
        fi
}

status
STATUS=$(status)
if [ "$STATUS" = "Tornado server not running." ]; then
        echo "The application is not running. Restarting."
	STATUS=$(start)
	LOG_TAIL=`tail --lines $LOG_LINES $LOG_FILE`
	echo "Hello," >> $MESSAGE_BODY
	echo "There was an issue with www.icnfnt.com, I tried restarting it and this is the current status:" >> $MESSAGE_BODY
	echo "$STATUS" >> $MESSAGE_BODY
	echo "" >> $MESSAGE_BODY
	echo "Here are the last $LOG_LINES from the log file for the application:" >> $MESSAGE_BODY
	echo "=================================================" >> $MESSAGE_BODY
	echo "$LOG_TAIL" >> $MESSAGE_BODY
	echo "=================================================" >> $MESSAGE_BODY
	echo "" >> $MESSAGE_BODY
	echo "Sorry about the problems. Hope you figure it out :-)" >> $MESSAGE_BODY
	mail -s "$SUBJECT" "$NOTIFY_ADDRESS" < $MESSAGE_BODY
	
	echo "Mail sent."
fi

echo "Done."
