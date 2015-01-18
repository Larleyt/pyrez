from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship as Relationship, backref as Backref

from .protocols import make_protocol

__all__ = ["Base", "Track", "Repo"]

Base = declarative_base()

class Track(Base):
  __tablename__ = 'tracks'
  id = Column(String, primary_key=True)
  title = Column(String)
  artist = Column(String)
  uri = Column(String)

  repo_id = Column(String, ForeignKey('repos.id'))
  repo = Relationship("Repo", backref=Backref("tracks"))

class Repo(Base):
  __tablename__ = 'repos'
  id = Column(String, primary_key=True)
  uri = Column(String)
  active = Column(Boolean)
  # last_updated = Column(DateTime)

  def get_tracks(self):
    return make_protocol(self.uri).get_tracks()

  def __init__(self, uri, activate=True):
    self.uri = uri
    meta = make_protocol(self.uri).get_meta()
    self.id = meta['id']
    self.active = activate