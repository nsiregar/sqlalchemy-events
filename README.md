# sqlalchemy-events

[![CI](https://github.com/nsiregar/sqlalchemy-events/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/nsiregar/sqlalchemy-events/actions/workflows/ci.yml)

Helper for handling sqlalchemy events

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install sqlalchemy-events.

```bash
pip install sqlalchemy-events
```

## Usage

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_events import listen_events, on

Base = declarative_base()


@listen_events
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)

    @on("before_insert")
    def lowercase_username(mapper, conn, self):
        self.username = self.username.lower()
```

List available mapper events is described at [sqlalchemy docs](https://docs.sqlalchemy.org/en/14/orm/events.html#mapper-events)

## License
[MIT](https://choosealicense.com/licenses/mit/)
