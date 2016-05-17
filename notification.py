import httplib
import random
import socket
import time


class NotificationService():

    @staticmethod
    def check_notification_type(summary):
        notify_type = None

        if summary.per_off_recent_high > .1 and summary.per_off_recent_high <= .3:
            notify_type = 1
        elif summary.per_off_recent_high > .3:
            notify_type = 2

        return notify_type

    @staticmethod
    def notify_slack(summaries):
        f = open('/home/james/finance/security.properties', 'r')
        slack_url = f.readline().strip()
        headers = {'Content-type': 'application/json'}

        for summary_key in summaries:
            summary = summaries[summary_key]
  
            send_notification = NotificationService.check_notification_type(summary)          
   
            if send_notification is not None:

                send_to_channel = ''
                if send_notification == 2:
                    send_to_channel = '<!channel> '

                body = '{"text":"' + send_to_channel + 'Ticker = ' + summary.ticker + '; name = ' + summary.name + '; max = ' + str(summary.max_price) + '; min = ' + str(summary.min_price) + '; % down from recent high = {:.2%}'.format(summary.per_off_recent_high) + '"}'

                conn = httplib.HTTPSConnection('hooks.slack.com') 
                conn.request('POST', slack_url, body, headers)
                response = conn.getresponse()
                print response.status, response.reason

    @staticmethod
    def notify_irc(summaries, act_human = True):
        if summaries:
            network = 'www.orangeshovel.com'
            port = 6667
            irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            irc.connect((network, port))

            irc.send('NICK analyst\r\n')
            irc.send('USER analyst analyst analyst :Python IRC\r\n')
            irc.send('JOIN #pynerds\r\n')
            irc.send('PRIVMSG #pynerds :Hey nerds, thought you would like to be alerted to following trends:\r\n')
            if act_human:
                time.sleep(5)
            else:
                time.sleep(0.15)

            for summary_key in summaries:
                summary = summaries[summary_key]

                send_notification = NotificationService.check_notification_type(summary)
               
                if send_notification is not None: 
                    irc_string = 'PRIVMSG #pynerds :Ticker = ' + summary.ticker + '; name = ' + summary.name + '; max = ' + str(summary.max_price) + '; min = ' + str(summary.min_price) + '; % down from recent high = {:.2%}'.format(summary.per_off_recent_high) + ('!!!' if send_notification == 2 else '') + '\r\n'

                    print('sending ' + summary.ticker + ' to IRC')
                    irc.send(irc_string)
                    if act_human:
                        time.sleep(random.randint(3, 5))

            irc.send('QUIT Goodbye\r\n')
