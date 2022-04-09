from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from config import DATABASE_URL


SQLALCHEMY_DATABASE_URL = "postgresql://faozuispekgops" \
                          ":49e44fdedf916d54c5d562385a7677a6f387af7111403befac06fa0b2f96c73b@ec2-176-34-116-203.eu" \
                          "-west-1.compute.amazonaws.com:5432/d1gec1g9j9v7sr"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()