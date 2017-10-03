import http.client
import json


default_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
METHOD_GET = 'GET'
METHOD_POST = 'POST'
METHOD_PATCH = 'PATCH'


class HTTPRequest():
    def __init__(self, domain, port, path, method=METHOD_GET, headers=default_headers, body=None):
        self.domain = domain
        self.port = port
        self.path = path
        self.method = method
        self.headers = headers
        self.body = body

    def send_request(self):
        conn = http.client.HTTPConnection(self.domain, self.port)
        conn.request(self.method, self.path, self.body, self.headers)
        raw_response = conn.getresponse()

        print('Call to http://{}:{}{} received response code of {}'.format(self.domain, self.port, self.path, raw_response.status))

        response_json = {}
        response_str = raw_response.read().decode('utf-8')
        if raw_response.status > 199 and raw_response.status < 300:
            response_json = json.loads(response_str)
        print('response_str = {}'.format(response_str))

        return response_json