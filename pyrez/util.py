from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def engine_and_session(url, **kw):
  engine = create_engine(url)
  Session = sessionmaker()
  Session.configure(bind=engine, **kw)
  session = Session()
  return engine, session