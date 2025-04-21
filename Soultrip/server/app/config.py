import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config:
    SQLALCHEMY_DATABASE_URI =os.getenv("DATABASE_URL",f"sqlite:///{os.path.join(basedir,'soultrip.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY",'dev-secret-key')
