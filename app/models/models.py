from peewee import Model, BigIntegerField, TextField, FloatField, TimestampField, SQL

from app.database.database import Database


class Embedding(Model):
    id = BigIntegerField(primary_key=True)
    text = TextField(null=False)
    embedding = TextField(null=False)  # Store as text (JSON string)
    created_at = TimestampField(null=False, default=SQL('CURRENT_TIMESTAMP'))
    updated_at = TimestampField(null=False, default=SQL('CURRENT_TIMESTAMP'))

    class Meta:
        database = Database().db
