from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    second_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hash_password = Column(String)

    # items = relationship("Item", back_populates="owner")


class Achievements_List(Base):
    __tablename__ = "achievements_list"

    id_ach = Column(Integer, primary_key=True, index=True)
    name_ach = Column(String)
    req_ach = Column(Integer)
    limit_ach = Column(Boolean)
    date_end_if_limit_ach = Column(DateTime, nullable=True)


class Complete_Achievements(Base):
    __tablename__ = "complete_achievements"

    id_comach = Column(Integer, primary_key=True, index=True)
    id_ach = Column(Integer)
    uid = Column(Integer)
    date_receive = Column(DateTime)


class Process_Achievements(Base):
    __tablename__ = "process_achievements"

    id_proach = Column(Integer, primary_key=True, index=True)
    id_ach = Column(Integer)
    pass_ach = Column(Integer)


class Messages(Base):
    __tablename__ = "messages"

    id_mes = Column(Integer, primary_key=True, index=True)
    uid_sender = Column(Integer)
    uid_recipient = Column(Integer)
    text_mes = Column(String)
    time_mes = Column(DateTime)


class Saves(Base):
    __tablename__ = "saves"

    id_save = Column(Integer, primary_key=True, index=True)
    uid = Column(Integer)
    date_save = Column(DateTime)
    name_save = Column(String)


class Coordinators(Base):
    __tablename__ = "coordinators"

    id_coord = Column(Integer, primary_key=True, index=True)
    value_coord = Column(String)
    id_save = Column(Integer)


class Bd_Options(Base):
    __tablename__ = "bd_options"

    id_option = Column(Integer, primary_key=True, index=True)
    name_option = Column(String)
    value_option = Column(String)


