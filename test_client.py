# -*- coding: utf-8 -*-

import unittest

from junction_client import JunctionClient

BASE_URL = 'http://junctiondemo.herokuapp.com'


class TestClient:
    def test_conferences(self):
        client = JunctionClient(BASE_URL)
        confs = client.conferences

        assert len(confs) > 0


class TestConference(unittest.TestCase):
    def setUp(self):
        client = JunctionClient(BASE_URL)
        self.confs = client.conferences

    def test_venue(self):
        for conf in self.confs:
            if conf.venue_url:
                break

        venue = conf.venue

        assert venue.id
        assert venue.address
        assert venue.longitude
        assert venue.latitude

    def test_missing_venue(self):
        conf = self.confs[0]

        assert conf.venue is None

    def test_get_venue_rooms(self):
        for conf in self.confs:
            if conf.venue_url:
                break

        room = conf.venue.rooms[0]

        assert room.id
        assert room.note

    def test_schedule(self):
        conf = self.confs[-1]
        schedule = conf.schedule

        for date, date_session in schedule.items():
            for _, val in date_session.items():
                assert val[0].id
                assert val[0].type

                assert val[0].session
                assert val[0].session.id
                assert val[0].session.author

    def test_get_token(self):
        conf = self.confs[-1]

        conf.get_token()

        assert conf.token

    def test_get_token_cache(self):
        conf = self.confs[-1]

        conf.get_token()
        token = conf.token
        conf.get_token()

        assert conf.token == token

    def test_force_get_token(self):
        conf = self.confs[-1]

        conf.get_token()
        token = conf.token
        conf.get_token(force_fetch=True)

        assert conf.token != token
