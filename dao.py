import config
import domain
import json
import webtest


class DAO:
    def __init__(self):
        self.host = config.finance_api_host
        self.port = config.finance_api_port
        self.equities_root = config.finance_api_equity_path
        self.snapshots_root = config.finance_api_snapshot_path

    #################### CRUD for snapshots ########################
    def create_snapshot(self, snapshot):
        req = webtest.HttpRequest()
        req.host = self.host + ':' + str(self.port)
        req.method = webtest._method_POST
        req.url = self.snapshots_root

        req.headers = {webtest._header_content_type: webtest._accept_JSON}

        req.body = json.dumps(snapshot.__dict__)
        print('About to send ' + req.body + ' to ' + self.host + ":" + str(self.port) + self.snapshots_root)

        resp = webtest.WebService.send_request(req)
        print('response = ' + resp)

    ##################### CRUD for equities ########################
    def get_all_equities(self):
        req = webtest.HttpRequest()
        req.host = self.host + ':' + str(self.port)
        req.method = webtest._method_GET
        req.url = self.equities_root

        req.headers = {webtest._header_accept: webtest._accept_JSON}

        resp = webtest.WebService.send_request(req)
        print('response = ' + resp)

        equities_json = json.loads(resp)
        equities = []

        for e in equities_json:
            equities.append(domain.Equity(e['id'], e['ticker'], e['name'], e['exchange'], e['industry'], e['dow']))

        return equities

    def create_equity(self, equity):
        req = webtest.HttpRequest()
        req.host = self.host + ':' + str(self.port)
        req.method = webtest._method_POST
        req.url = self.equities_root

        req.headers = {
            webtest._header_content_type: webtest._accept_JSON,
            webtest._header_accept: webtest._accept_JSON
        }

        del equity.equity_id
        del equity.snapshots
        del equity.aggregates

        print("Equity to delete = " + json.dumps(equity.__dict__))