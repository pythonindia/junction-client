# -*- coding: utf-8 -*-

from requests import Session

from .base import RequestHandlerMixin
from .models import Conference
from .constants import URI_PARTS


__all__ = ['JunctionClient']


class JunctionClient(RequestHandlerMixin):
    def __init__(self, base_url="https://in.pycon.org/cfp/"):
        """
        :param str base_url: Junction server base url with slug.
        """
        self.base_url = base_url
        if not self.base_url.endswith('/'):
            self.base_url = self.base_url + '/'
        self.request = Session()

    @property
    def conferences(self):
        data = self.make_request(url=URI_PARTS['conference'], method='get')
        confs = []
        for datum in data:
            kwargs = {'base_url': self.base_url}
            kwargs.update(datum)
            confs.append(Conference(**kwargs))
        return confs
