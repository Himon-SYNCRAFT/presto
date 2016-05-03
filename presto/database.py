from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://postgres:Awarene$4@localhost/presto')

db_session = scoped_session(sessionmaker(
    bind=engine, autoflush=False, autocommit=False))

Base = declarative_base(bind=engine)
Base.query = db_session.query_property()
