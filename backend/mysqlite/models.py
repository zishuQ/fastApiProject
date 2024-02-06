from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Defect(Base):
    __tablename__ = 'Defect'
    DefectNo = Column(Integer, primary_key=True)
    DefectName = Column(String(255))


class ProductLine(Base):
    __tablename__ = 'ProductLine'
    LineNo = Column(Integer, primary_key=True)
    LineName = Column(String(255))


class TireInfo(Base):
    __tablename__ = 'TireInfo'
    TireNo = Column(Integer, primary_key=True, autoincrement=True)
    LineNo = Column(Integer, ForeignKey('ProductLine.LineNo'))
    TireName = Column(String(255), unique=True)
    ProduceDate = Column(DATETIME)


class DefectInfo(Base):
    __tablename__ = 'DefectInfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    TireName = Column(Integer, ForeignKey('TireInfo.TireName'), unique=True)
    Info = Column(JSON)
    DefectDate = Column(DATETIME)
