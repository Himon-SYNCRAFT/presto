from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from presto import app


engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

db_session = scoped_session(sessionmaker(
    bind=engine, autoflush=False, autocommit=False))

Base = declarative_base(bind=engine)
Base.query = db_session.query_property()
