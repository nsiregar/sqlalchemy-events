import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from src.sqlalchemy_events import listen_events, on

Base = declarative_base()


class BaseModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return self.username


@pytest.fixture(scope="function")
def setup_database():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_before_commit(setup_database):
    @listen_events
    class User(BaseModel):
        @on("before_insert")
        def lowercase_username(mapper, conn, self):
            self.username = self.username.lower()

    session = setup_database
    user_1 = User(username="John")
    user_2 = User(username="Mary")

    session.add(user_1)
    session.add(user_2)
    session.commit()

    john = session.query(User).filter(User.username == "john").first()
    mary = session.query(User).filter(User.username == "mary").first()
    assert john.username == "john"
    assert mary.username == "mary"
