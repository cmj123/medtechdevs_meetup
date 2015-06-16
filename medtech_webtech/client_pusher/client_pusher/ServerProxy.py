import requests
import json

class ServerProxy(object):
    URL = 'someurl.com'
    USERNAME = 'user'
    PASSWORD = 'pass'

    def __init__(self):
        pass

    def send_data(self, data):
        result = requests.post(self.URL, data, auth=(self.USERNAME, self.PASSWORD))