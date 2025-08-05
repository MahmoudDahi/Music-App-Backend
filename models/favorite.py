from sqlalchemy import TEXT, Column, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship

class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(TEXT, primary_key=True)
    user_id = Column(TEXT, ForeignKey('users.id'))
    song_id = Column(TEXT, ForeignKey('songs.id'))
    song = relationship('Song')
    