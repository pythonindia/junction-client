# -*- coding: utf-8 -*-

import uuid
import collections

from datetime import datetime

from requests import Session
from requests.compat import urljoin

from .serializer import FeedbackQuestionSerializer, ScheduleItemSerializer


URI_PARTS = {'conference': 'api/v1/conferences/',
             'room': 'api/v1/rooms/?venue={}',
             'schedule': 'api/v1/schedules/?conference={}',
             'device': 'api/v1/devices/',
             'feedback': 'api/v1/feedback/',
             'feedback_questions': 'api/v1/feedback_questions/?conference_id={}'}  # noqa


__all__ = ['JunctionClient']


Room = collections.namedtuple('Room', 'id name venue note')


class Venue(object):
    def __init__(self, id, name, address, latitude, longitude, base_url):
        self.id = id
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

        self.base_url = base_url
        self.request = Session()

    @property
    def rooms(self):
        url = urljoin(self.base_url, URI_PARTS['room'].format(self.id))
        resp = self.request.get(url)

        if resp.ok:
            data = resp.json()

            rooms = []
            for datum in data:
                rooms.append(Room(**datum))
            return rooms


class Conference(object):
    def __init__(self, id, name, slug, start_date, end_date, status,
                 description, venue, base_url):
        self.id = id
        self.name = name
        self.slug = slug
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.venue_url = venue
        self.status = status
        self.description = description
        self.base_url = base_url

        self.token = None
        self.request = Session()

    @property
    def venue(self):
        if not self.venue_url:
            return None

        resp = self.request.get(self.venue_url)
        if resp.ok:
            data = resp.json()
            if data['latitude']:
                latitude = float(data['latitude'])
            else:
                latitude = None

            if data['longitudes']:
                longitude = float(data['longitudes'])
            else:
                longitude = None

            return Venue(id=data['id'], name=data['name'],
                         address=data['address'],
                         latitude=latitude,
                         longitude=longitude,
                         base_url=self.base_url)

    @property
    def schedule(self):
        url = urljoin(self.base_url, URI_PARTS['schedule'].format(self.id))

        resp = self.request.get(url)

        if resp.ok:
            data = resp.json()
            schedule = {}
            for date, dated_session in data.items():
                schedule[date] = {}
                for timing, timed_sessions in dated_session.items():
                    items = []
                    for session in timed_sessions:
                        session.pop('conference')
                        item = ScheduleItemSerializer(session)
                        item.validate()
                        items.append(item)
                    schedule[date] = {timing: items}
            return schedule

    def get_token(self, force_fetch=False):
        """Get the device token from server. This method should be called
        atleats once before submitting feedback.

        :param bool force_fetch: True will re register the device/client
        """
        if force_fetch or self.token is None:
            url = urljoin(self.base_url, URI_PARTS.get('device'))
            resp = self.request.post(url, json={'uuid': str(uuid.uuid1())})
            if resp.ok:
                self.token = resp.json()['uuid']

    @property
    def feedback_questions(self):
        url = self.base_url + URI_PARTS['feedback_questions'].format(self.id)
        resp = self.request.get(url)

        if resp.ok:
            data = resp.json()
            feedback_questions = {}
            for session_type, questions in data.items():
                serializer = FeedbackQuestionSerializer(questions)
                serializer.validate()
                feedback_questions[session_type] = serializer
            return feedback_questions

    def submit_feedback(self, type, data):
        # TODO
        pass


class JunctionClient(object):
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
        url = self.base_url + URI_PARTS['conference']
        resp = self.request.get(url)
        if resp.ok:
            data = resp.json()
            confs = []
            for datum in data:
                kwargs = {'base_url': self.base_url}
                kwargs.update(datum)
                confs.append(Conference(**kwargs))
            return confs
        return []
