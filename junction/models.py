# -*- coding: utf-8 -*-

import uuid
import collections

from datetime import datetime

from requests import Session
from schematics.exceptions import ModelConversionError, ModelValidationError


from .base import ReprMixin, RequestHandlerMixin
from .serializers import FeedbackQuestionSerializer, ScheduleItemSerializer
from .constants import URI_PARTS
from .exceptions import ValidationException


Room = collections.namedtuple('Room', 'id name venue note')


class Venue(ReprMixin, RequestHandlerMixin):
    __repr_fields__ = ['id', 'name']

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
        data = self.make_request(url=URI_PARTS['room'].format(self.id))
        rooms = []
        for datum in data:
            rooms.append(Room(**datum))
        return rooms


class VenueMixin(object):
    @property
    def venue(self):
        if not self.venue_url:
            return None

        data = self.make_request(self.venue_url)
        return self.parse_venue(data)

    def parse_venue(self, data):
        if data:
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


class ScheduleMixin(object):
    @property
    def schedule(self):
        data = self.make_request(URI_PARTS['schedule'].format(self.id))
        return self.parse_schedule(data)

    def parse_schedule(self, data):
        if data:
            return self.parse_session(data)
        return data

    def parse_session(self, sessions):
        schedule = {}
        for date, dated_session in sessions.items():
            schedule[date] = {}
            for timing, timed_sessions in dated_session.items():
                items = []
                for session in timed_sessions:
                    items.append(self.validate_session(session))
                schedule[date][timing] = items
        return schedule

    def validate_session(self, session):
        try:
            session.pop('conference')
            item = ScheduleItemSerializer(session)
            item.validate()
            return item
        except (ModelConversionError, ModelValidationError) as e:
            raise ValidationException(e.messages)


class FeedbackMixin(object):
    @property
    def feedback_questions(self):
        data = self.make_request(
            URI_PARTS['feedback_questions'].format(self.id))

        if data:
            feedback_questions = {}
            for session_type, questions in data.items():
                serializer = FeedbackQuestionSerializer(questions)
                serializer.validate()
                feedback_questions[session_type] = serializer
            self._feedback_questions = feedback_questions
            return feedback_questions
        return data

    def submit_feedback(self, data):
        """Submit the feedback to server.

        :param dict data: Dictionary item containing all the feedback question
        ids and value.

        Samplae:
        {'text': [{'text': 'Ok', 'id': 1}], 'schedule_item_id': 1,
        'choices': [{'id': 1, 'value_id': 1}]}
        """
        # TODO: Add validation for data
        data = self.make_request(
            URI_PARTS['feedback'].format(self.id),
            method='post',
            with_auth=True)
        return data


class Conference(ReprMixin, RequestHandlerMixin, VenueMixin, ScheduleMixin,
                 FeedbackMixin):
    __repr_fields__ = ['id', 'name', 'start_date', 'end_date']

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

        # Cache
        self._feedback_questions = None

    def get_token(self, force_fetch=False):
        """Get the device token from server. This method should be called
        atleats once before submitting feedback.

        :param bool force_fetch: True will re register the device/client
        """
        if force_fetch or self.token is None:
            data = self.make_request(URI_PARTS.get('device'), method='post',
                                     data={'uuid': str(uuid.uuid1())})
            self.token = data['uuid']
        return self.token
