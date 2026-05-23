import databases
import sqlalchemy
from settings import settings

DATABASE_URL = settings.database_url

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)