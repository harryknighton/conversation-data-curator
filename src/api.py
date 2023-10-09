"""Create an API to allow access to the database."""

from src import models
from src.crud import count_messages, create_test_messages, read_messages
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

with SessionLocal() as session:
    count = count_messages(session)
    if count == 0:
        create_test_messages(session)

    messages = read_messages(session)
    for msg in messages:
        print(msg[0].id, msg[0].content)
