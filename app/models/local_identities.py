# app/models/face.py
from app.config import Base
from sqlalchemy import Column, Integer, String
from app.models.vectorizer import PGVector

class IdentitiesFn512(Base):
    __tablename__ = 'identities_fn512'

    id = Column(Integer, primary_key=True)
    img_name = Column(String(100), nullable=False)
    embedding = Column(PGVector(512), nullable=False)

    def __repr__(self):
        return f"<IdentitiesFn512(img_name={self.img_name}, embedding={self.embedding})>"

class IdentitiesDlib(Base):
    __tablename__ = 'identities_dlib'

    id = Column(Integer, primary_key=True)
    img_name = Column(String(100), nullable=False)
    embedding = Column(PGVector(128), nullable=False)

    def __repr__(self):
        return f"<IdentitiesDlib(img_name={self.img_name}, embedding={self.embedding})>"
