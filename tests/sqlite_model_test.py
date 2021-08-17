import pytest
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from src.sqlalchemy_events import listen_events, on

Base = declarative_base()

class SQLiteEventsTest(TestCase):
    def test_listen_model_events(self):
        @listen_events
        class User(Base):
            __tablename__ = "users"

            id = Column(Integer, primary_key=True, autoincrement=True)
            username = Column(String, nullable=False, unique=True)

            @on("before_insert")
            def lowercase_username(mapper, conn, self):
                self.username = self.username.lower()

        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

        session = Session()
        user_1 = User(username="John")
        user_2 = User(username="Mary")

        session.add(user_1)
        session.add(user_2)
        session.commit()

        john = session.query(User).filter(User.username == "john").first()
        mary = session.query(User).filter(User.username == "mary").first()
        assert john.username == "john"
        assert mary.username == "mary"

        session.close()


