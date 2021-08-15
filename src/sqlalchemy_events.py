from functools import partial
from sqlalchemy import event

# EVENTS DOCS
# http://docs.sqlalchemy.org/en/rel_1_1/core/event.html
# ORM EVENTS DOCS
# http://docs.sqlalchemy.org/en/rel_1_1/orm/events.html


class _EventObject(object):
    ATTR = "_sqlalchemy_event"

    def __init__(self, field_name, event_name, listen_kwargs=None):
        self.field_name = field_name
        self.event_name = event_name
        self.listen_kwargs = listen_kwargs or {}


def listen_events(*args):
    def wrapper(cls):
        for name, fn in cls.__dict__.items():
            if not name.startswith("__") and hasattr(fn, _EventObject.ATTR):
                e = getattr(fn, _EventObject.ATTR)
                if e.field_name:
                    event.listen(
                        getattr(cls, e.field_name), e.event_name, fn, **e.listen_kwargs
                    )
                else:
                    event.listen(cls, e.event_name, fn, **e.listen_kwargs)
        return cls

    if args and callable(args[0]):
        return wrapper(args[0])
    return wrapper


def on(*args, **listen_kwargs):
    if len(args) == 1:
        field_name, event_name = (None, args[0])
    elif len(args) == 2:
        field_name, event_name = args
    else:
        raise NotImplementedError("@on accepts only one or two positional arguments")

    def wrapper(fn):
        setattr(
            fn, _EventObject.ATTR, _EventObject(field_name, event_name, listen_kwargs)
        )
        return fn

    return wrapper
