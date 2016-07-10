# -*- coding: utf-8 -*-

from requests.compat import urljoin

from .exceptions import ClientException, ServerException


class ReprMixin(object):

    """Provides friendly `__repr__` method for all models to print
       fields mentioned in `__repr_fields__`. Output format is:

       <ModelName(field1=value,.., fieldN=value)>
    """

    def __repr__(self):
        model_name = self.__class__.__name__
        message = ', '.join("{}={}".format(field, getattr(self, field, None))
                            for field in self.__repr_fields__)
        return u"<{}({})>".format(model_name, message)


class RequestHandlerMixin(object):
    def make_request(self, url, method='get', data=None, with_auth=False):
        url = urljoin(self.base_url, url)
        if method == 'get':
            resp = self.request.get(url)
        elif method == 'post':
            if with_auth:
                headers = {'Authorization': 'Token: {}'.format(self.token)}
                resp = self.request.post(url, json=data, headers=headers)
            else:
                resp = self.request.post(url, json=data)
        else:
            raise Exception('Method not supported')

        return self.parse_response(resp)

    def parse_response(self, resp):
        if resp.ok:
            return resp.json()
        elif resp.status_code == 400:
            raise ClientException(resp.json())
        elif resp.status_code in (401, 403):
            raise ClientException(resp.content)
        elif 500 <= resp.status_code <= 504:
            raise ServerException(resp.content)
