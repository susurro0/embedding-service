import json
import os

import numpy as np
from peewee import Model, BigIntegerField, TextField, TimestampField, SQL, AutoField

from app.database.database import Database
from pgvector.peewee import VectorField

from database.database import database_instance


class Embedding(Model):
    DoesNotExist = None
    id = AutoField(primary_key=True)
    text = TextField(null=False)
    embedding = VectorField(dimensions=os.environ.get('DIMENSION', 384 ))
    created_at = TimestampField(null=False, default=SQL('EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)'))
    updated_at = TimestampField(null=False, default=SQL('EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)'))

    class Meta:
        database = database_instance.database
