from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = "postgresql://postgres.dykuwaztmcfmcxdxgrqx:Ymu6Efu45UKczuW1@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DATABASE_URL)
SESSION: Session = sessionmaker(bind=engine)()


#Ymu6Efu45UKczuW1