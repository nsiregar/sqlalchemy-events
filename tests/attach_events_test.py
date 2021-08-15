from unittest import TestCase
from sqlalchemy import event
from src.sqlalchemy_events import listen_events, on


class MockEvent(event.Events):
    def mock_event_one(self):
        pass

    def mock_event_two(self):
        pass


class MockClass(object):
    dispatch = event.dispatcher(MockEvent)


class AttachEventsTest(TestCase):
    def test_wrap_to_class(self):
        @listen_events
        class Target(MockClass):
            @on("mock_event_one")
            def sample_method(self):
                pass

        target = Target()
        assert len(target.dispatch.mock_event_one) == 1
        assert len(target.dispatch.mock_event_two) == 0
