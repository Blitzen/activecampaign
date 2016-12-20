import requests
from urllib.parse import quote
import re
import json

class ActiveCampaignError(Exception):
    def __init__(self, response):
        self.response = response

class ActiveCampaign():
    '''

    '''
    def __init__(self, url, api_key, *args, **kwargs):
        self.base_url = url
        self.api_key = api_key
        if self.base_url != 'https://www.activecampaign.com':
            self.base_suffix  = '/admin'
        if self.base_url[-1] == '/':
            self.base_url = self.base_url[:-1]
        self.url = '{0}/admin/api.php'.format(self.base_url)
        self._request_method = {
            'POST': requests.post,
            'GET': requests.get,
            'PUT': requests.put,
            'DELETE': requests.delete
        }

    def call(self, method='GET', api_action=None, data=None, params=None, headers=None, *args, **kwargs):
        request_params = {'api_action': api_action, 'api_output': 'json', 'api_key': self.api_key}
        request_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        if api_action:
            request_params.update(params) if params else request_params
            request_headers.update(headers) if headers else request_headers
            return self._request(self.url,
                                data,
                                method=method,
                                headers=request_headers,
                                params=request_params)

    def _request(self, endpoint, data, method='GET', headers=None, params=None):
        '''
        _request will actually make the request, and return the response json if the code is
        successful.
        This function will return the json from the response
        If an error occurs, it will raise a requests raise_for_status exception
        '''
        if type(data) == dict:
            data = json.dumps(data)
        try:
            request = self._request_method[method]
        except KeyError as e:
            raise ActiveCampaignError(e.value)
        response = request(endpoint,
                           data=data,
                           params=params,
                           headers=headers)
        if response.status_code < 400:
            if response.text != '':
                return response.json()
            else:
                return response.text
        else:
            response.raise_for_status()

    def make_request(self, api_action='list_view', params=None):
        resp = self.call(api_action=api_action, params=params)
        return resp

    def test_credentials(self):
        resp = self.call(api_action='user_me', params=params)
