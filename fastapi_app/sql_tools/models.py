from sqlalchemy import Column, Integer, String, Boolean

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String)
    website = Column(String)
    is_disabled = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'{self.__class__.__name__} (id={self.id}, name={self.name})'
