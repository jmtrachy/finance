import dal
import httplib
import random
import socket
import time


class NotificationService():

    def __init__(self):
        self.equities = dal.EquityDAO.get_equities()
        self.aggregates = {}
        for equity in self.equities:
            aggregate = dal.EquityDAO.get_top_equity_aggregate_by_id(equity.equity_id)
            if aggregate is not None:
                self.aggregates[equity.ticker] = aggregate
                print(str(aggregate.aggregate_id) + ' ticker = ' + equity.ticker)

    def check_notification_type(self, aggregate):
        notify_type = None

        if aggregate.per_off_recent_high > 10 and aggregate.per_off_recent_high <= 30:
            notify_type = 1
        elif aggregate.per_off_recent_high > 30:
            notify_type = 2

        return notify_type

    def notify_slack(self):
        f = open('/home/james/finance/security.properties', 'r')
        slack_url = f.readline().strip()
        headers = {'Content-type': 'application/json'}

        for ticker in self.aggregates:
            aggregate = self.aggregates[ticker]
            send_notification = self.check_notification_type(aggregate)          
   
            if send_notification is not None:

                send_to_channel = ''
                if send_notification == 2:
                    send_to_channel = '<!channel> '

                body = '{"text":"' + send_to_channel + 'Ticker = ' + ticker + '; per off recent high = ' + str(aggregate.per_off_recent_high) + '; per off recent low = ' + str(aggregate.per_off_recent_low) + '; 50 day moving avg = ' + str(aggregate.fifty_day_moving_avg) + '; fifty_day_volatility_avg = ' + str(aggregate.fifty_day_volatility_avg) + '"}'
                print(body)

                conn = httplib.HTTPSConnection('hooks.slack.com') 
                conn.request('POST', slack_url, body, headers)
                response = conn.getresponse()
                print response.status, response.reason

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


if __name__ == '__main__':
    not_service = NotificationService()
    not_service.notify_slack()
