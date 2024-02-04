import uuid
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Integer, String, Date, Float, Text

Base = declarative_base()

class Netflix(Base):
    __tablename__ = "Netflix"
    
    uuid = Column(String, nullable=False, primary_key=True)
    week = Column(Date, nullable=True)
    category = Column(String, nullable=True)
    weekly_rank = Column(Integer, nullable=True)
    show_title = Column(String, nullable=True)
    season_title = Column(String, nullable=True)
    weekly_hours_viewed = Column(Integer, nullable=True)
    runtime = Column(Float, nullable=True)
    weekly_views = Column(Integer, nullable=True)
    cumulative_weeks_in_top_10 = Column(Integer, nullable=True)
    is_staggered_launch = Column(Boolean, nullable=True)
    episode_launch_detail = Column(Text, nullable=True)

def transform_netflix_data(data_location):
    df = pd.read_csv(data_location, delimiter=',', encoding='ISO-8859-1', index_col=None)
    df['week'] = pd.to_datetime(df['week'])
    df['uuid'] = [uuid.uuid4() for _ in range(len(df))]
    df['uuid'] = df['uuid'].astype(str)
    return df

def prepare_netflix_data(data_location: str, database_location: str) -> None:
    print("## Ingesting SQLite database with Netflix data. ##")
    engine = create_engine(f"sqlite:///{database_location}", echo=True)
    Netflix.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    netflix_data = transform_netflix_data(data_location)
    session.bulk_insert_mappings(Netflix, netflix_data.to_dict(orient="records"))
    session.commit()
    session.close()
    print("## Completed ingestion of SQLite database. ##")