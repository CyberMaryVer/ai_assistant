from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, ForeignKey, create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
engine = create_engine("postgresql+asyncpg://postgres:Password!@10.254.159.15/assistan")

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

    keys = relationship('Keys', backref='customer')

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
        return f'{self.__class__.__name__} (id={self.id}, name={self.name})'
