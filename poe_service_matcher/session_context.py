from contextlib import contextmanager
from sqlalchemy.orm import scoped_session, sessionmaker

@contextmanager
def create_session(engine):
    
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        Session.remove()