from sqlalchemy import Column, Integer, String
from database import Base

class URLModel(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    longURL = Column(String(120), unique=True)
    shortURL = Column(String(50), unique=True)

    def __init__(self, longURL=None, shortURL=None):
        self.longURL = longURL
        self.shortURL = shortURL

    def __repr__(self):
        return '<URL %r>' % (self.longURL)