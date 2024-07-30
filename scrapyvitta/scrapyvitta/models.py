from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ScrapedItem(Base):
    __tablename__ = 'scraped_items'

    id = Column(Integer, primary_key=True)
    author = Column(String)
    tags = Column(String)
    about = Column(Text)  # Cambiado a Text para permitir contenido más largo
    text = Column(Text)   # Nueva columna para la cita


# crear la base de datos
engine = create_engine('sqlite:///scraped_data.db', connect_args={'timeout': 15})
Base.metadata.create_all(engine)
