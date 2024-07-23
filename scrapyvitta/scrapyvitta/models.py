from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ScrapedItem(Base):
    __tablename__ = 'scraped_items'

    id = Column(Integer, primary_key=True)
    author = Column(String)
    tags = Column(String)
    about = Column(String)


# crear la base de datos
engine = create_engine('sqlite:///scraped_data.db')
Base.metadata.create_all(engine)
