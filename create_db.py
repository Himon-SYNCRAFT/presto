from presto import models
from presto.database import Base, db_session


def create_db():
    Base.metadata.reflect()
    Base.metadata.drop_all()
    Base.metadata.create_all()

    user = models.User('danzaw', 'danzaw@mail.pl', "it's a secret")

    db_session.add(user)
    db_session.commit()

    account = models.Account('danzaw', 'danzaw@gmail.com', "it's a secret", 'webapi_key')

    db_session.add(account)
    db_session.commit()


if __name__ == '__main__':
    create_db()
