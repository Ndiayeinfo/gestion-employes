from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class Employe(Base):
    __tablename__ = "employes"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False, index=True)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    telephone = Column(String)
    poste = Column(String, nullable=False)
    salaire = Column(Float)
    date_embauche = Column(Date)
    departement = Column(String)

