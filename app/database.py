from peewee import SqliteDatabase

# SQLite database file
db = SqliteDatabase("embeddings.db")

def initialize_db():
    from app.models import Embedding
    db.connect()
    db.create_tables([Embedding], safe=True)
