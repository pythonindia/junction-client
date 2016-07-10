### Junction API client.

#### Installation

`pip install git+git://github.com/pythonindia/junction-client.git`

#### API

``` python

In [4]: from junction import JunctionClient

In [5]: client = JunctionClient('https://in.pycon.org/cfp/')

In [6]: client.conferences
Out[6]:
[<Conference(id=5, name=PyCon India 2016, start_date=2016-09-23 00:00:00, end_date=2016-09-25 00:00:00)>,
 <Conference(id=4, name=PyCon India 2015 open spaces, start_date=2015-10-03 00:00:00, end_date=2015-10-04 00:00:00)>,
 <Conference(id=3, name=PyCon India 2015 poster session, start_date=2015-10-03 00:00:00, end_date=2015-10-04 00:00:00)>,
 <Conference(id=1, name=PyCon India 2015, start_date=2015-10-02 00:00:00, end_date=2015-10-04 00:00:00)>,
 <Conference(id=2, name=PyCon India Dev Sprint 2015, start_date=2015-10-02 00:00:00, end_date=2015-10-02 00:00:00)>]

In [7]: conf_2016 = client.conferences[0]


In [8]: conf_2016.venue
Out[8]: <Venue(id=2, name=JNU - Jawahar Lal Nehru University,)>

In [9]: conf_2016.venue.rooms
Out[9]: [Room(id=5, name='Conference Hall', venue='http://in.pycon.org/cfp/api/v1/venues/2/', note='Conference Hall')]

In [10]: conf_2015 = client.conferences[-2]

In [11]: schdeule = conf_2015.schedule

In [12]: schedule = conf_2015.schedule

In [13]: schedule.
schedule.clear       schedule.copy        schedule.fromkeys    schedule.get         schedule.items       schedule.keys        schedule.pop         schedule.popitem     schedule.setdefault  schedule.update      schedule.values

In [14]: schedule.keys()
Out[14]: dict_keys(['2015-10-02', '2015-10-03', '2015-10-04'])

In [15]: schedule['2015-10-02']
Out[15]:
{'09:30:00 - 12:00:00': [<ScheduleItemSerializer instance>,
  <ScheduleItemSerializer instance>,
  <ScheduleItemSerializer instance>],
 '12:30:00 - 13:00:00': [<ScheduleItemSerializer instance>],
 '13:00:00 - 15:30:00': [<ScheduleItemSerializer instance>,
  <ScheduleItemSerializer instance>,
  <ScheduleItemSerializer instance>],
 '16:00:00 - 18:30:00': [<ScheduleItemSerializer instance>,
  <ScheduleItemSerializer instance>,
  <ScheduleItemSerializer instance>]}

In [16]: schedule['2015-10-02']['16:00:00 - 18:30:00']
Out[16]:
[<ScheduleItemSerializer instance>,
 <ScheduleItemSerializer instance>,
 <ScheduleItemSerializer instance>]

In [17]: item = schedule['2015-10-02']['16:00:00 - 18:30:00'][0]

In [18]: item.session
Out[18]: <SessionSerializer instance>

In [19]: item.id
Out[19]: 8

In [20]: item.start_time
Out[20]: datetime.datetime(1900, 1, 1, 16, 0)

In [21]: item.type
Out[21]: 'Workshop'

In [22]: item.session.title
Out[22]: 'Building NextGen IoT solutions using Python and Cloud'

In [23]: item.session.to_native()
Out[23]:
{'author': 'Saurabh Kirtani',
 'content_urls': '...',
 'description': "...",
 'id': 83,
 'prerequisites': '...',
 'section': 'Embedded Python',
 'speaker_info': '..',
 'speaker_links': '...',
 'target_audience': 1,
 'title': 'Building NextGen IoT solutions using Python and Cloud'}

In [24]: questions = conf_2015.feedback_questions

In [25]: questions
Out[25]:
{'Talk': <FeedbackQuestionSerializer instance>,
 'Workshop': <FeedbackQuestionSerializer instance>}

In [26]: questions['Talk']
Out[26]: <FeedbackQuestionSerializer instance>

In [27]: questions['Talk'].text
Out[27]: [<TextFeedbackQuestionSerializer instance>]

In [28]: questions['Talk'].text[0].to_primitive()
Out[28]:
{'id': 1,
 'is_required': False,
 'schedule_item_type': 'Talk',
 'title': 'Any other feedback for the talk ?',
 'type': 'text'}

In [29]: questions['Talk'].choice[0].to_primitive()
Out[29]:
{'allowed_choices': [{'id': 18, 'title': 'Good', 'value': 2},
  {'id': 17, 'title': 'Ok', 'value': 1},
  {'id': 16, 'title': 'Bad', 'value': 0}],
 'id': 6,
 'is_required': True,
 'schedule_item_type': 'Talk',
 'title': 'Does the speaker have experience on the subject?',
 'type': 'choice'}

In [30]: questions['Talk'].choice[1].allowed_choices
Out[30]:
[<AllowedChoiceValidator instance>,
 <AllowedChoiceValidator instance>,
 <AllowedChoiceValidator instance>]

In [31]: questions['Talk'].choice[1].allowed_choices[0].id
Out[31]: 12

In [32]: questions['Talk'].choice[1].is_required
Out[32]: True

In [33]: conf_2016.get_token()
Out[33]: '6a6f531c-4692-11e6-8714-ac87a3379142'

In [34]: conf_2016.get_token()
Out[34]: '6a6f531c-4692-11e6-8714-ac87a3379142'

In [35]: conf_2016.get_token(force_fetch=True)
Out[35]: '77345ad4-4692-11e6-8ad3-ac87a3379142'

```

To submit a feedback, call `conf.submit_feedback(data)`. Before calling `submit_feedback`, call `conf.get_token()`.

The client is still in development mode. HTTP Docs is available in [Junction Repo](https://github.com/pythonindia/junction/blob/master/docs/api.md).
