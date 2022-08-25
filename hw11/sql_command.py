from models import Base, Records, Emails, Phones
import sqlite3
# from app import session
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import update
engine = create_engine("sqlite:///myHelper.db", connect_args={"check_same_thread": False}, echo=True)



def execute_query(sql: str,) -> list:
    with sqlite3.connect('myHelper.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


def update_data(data, id, table, column):
    conn = engine.connect()
    if table == 'phones':
        print('\n\nhere\n\n')
        stmt = update(Phones).where(Phones.id == id).values(phone=data).execution_options(synchronize_session="fetch")
        result = conn.execute(stmt)
        conn.execute(stmt)
    elif table == 'emails':
        stmt = update(Emails).where(Emails.id == id).values(email=data).execution_options(synchronize_session="fetch")
        result = conn.execute(stmt)
        conn.execute(stmt)
    conn.close

def newdata(data, id, table, column):
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    if table == 'phones':
        new_data = Phones(phone=data, record_id=id)
        session.add(new_data)
    elif table == 'emails':
        new_data = Emails(email=data, record_id=id)
        session.add(new_data)
    session.commit()
    session.close

def search_contact_data(name):
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    results = session.query(Records).filter_by(name=name).all()
    i = 0
    print('search result:')
    for row in results:
        print (f'{row}')
        i +=1
    print(f'found {i} results')
    return results