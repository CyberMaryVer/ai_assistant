from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, ForeignKey, create_engine, ARRAY

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
engine = create_engine("postgresql+asyncpg://")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String)
    website = Column(String)
    telephone = Column(String)
    description = Column(Text)
    created_at = Column(TIMESTAMP)
    is_disabled = Column(Boolean, nullable=False, default=False)

    keys = relationship('Keys', backref='customer', lazy="selectin")

    def __repr__(self):
        return f'{self.__class__.__name__} (id={self.id}, name={self.name})'


class Keys(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    key_id = Column(String, unique=True)
    key_type = Column(String)

    created_at = Column(TIMESTAMP)
    expired_at = Column(TIMESTAMP)

    usages_left = Column(Integer)
    is_disabled = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'{self.__class__.__name__} (id={self.id}, name={self.key_id})'


class Filters(Base):
    __tablename__ = "filtering_rules"

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    created_user_id = Column(String)

    word = Column(String, nullable=False)
    description = Column(Text)

    is_archive = Column(Boolean, default=False)
    archive_at = Column(TIMESTAMP)
    archive_user_id = Column(String)

    def __repr__(self):
        return f'{self.__class__.__name__} (id={self.id}, name={self.word})'


class Requests(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    user_id = Column(String)
    chat_id = Column(String)

    raw_text = Column(Text, nullable=False)
    topic = Column(String)

    filter_id = Column(Integer, ForeignKey('filtering_rules.id'))
    timestamp_filter = Column(TIMESTAMP)
    parent_resp_id = Column(Integer, ForeignKey('responses.id'))
    status = Column(String, nullable=False)



    def __repr__(self):
        return f'{self.__class__.__name__} (id={self.id}, time={self.timestamp}, status={self.status})'


class Responses(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP)
    request_id = Column(Integer, ForeignKey('requests.id'), nullable=False)
    raw_text = Column(Text)
    sources = Column(ARRAY(String))
    status = Column(String, nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__} (id={self.id}, time={self.timestamp}, status={self.status})'


class Feedbacks(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True)
    respons_id = Column(Integer, ForeignKey('requests.id'), nullable=False)
    user_id = Column(String)
    timestamp = Column(TIMESTAMP)
    estimation = Column(Integer, nullable=False)
    note = Column(Text)

    def __repr__(self):
        return f'{self.__class__.__name__} (id={self.id}, respons={self.respons_id}, estimation={self.estimation})'
