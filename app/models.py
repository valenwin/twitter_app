from functools import partial

from slugify import slugify
from sqlalchemy import Column

from app import db

NotNullColumn = partial(Column, nullable=False)
