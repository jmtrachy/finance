import httplib


class NotificationService():

    @staticmethod
    def notify_slack(summaries):
        f = open('/home/james/finance/security.properties', 'r')
        slack_url = f.readline().strip()
        print(slack_url)
        headers = {'Content-type': 'application/json'}

        for summary_key in summaries:
            summary = summaries[summary_key]
            
            send_notification = False
            if summary.per_off_recent_high > .1:
                send_notification = True
   
            if send_notification:

                send_to_channel = ''
                if summary.per_off_recent_high > .3:
                    send_to_channel = '<!channel> '

                body = '{"text":"' + send_to_channel + 'Ticker = ' + summary.ticker + '; name = ' + summary.name + '; max = ' + str(summary.max_price) + '; min = ' + str(summary.min_price) + '; % down from recent high = {:.2%}'.format(summary.per_off_recent_high) + '"}'

                conn = httplib.HTTPSConnection('hooks.slack.com') 
                conn.request('POST', slack_url, body, headers)
                response = conn.getresponse()
                print response.status, response.reason
