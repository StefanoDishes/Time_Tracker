from sqlalchemy import create_engine,URL
from sqlalchemy.orm import Session
from Scripts.Queries import loginRisorsa
import configparser
import os

dir=os.path.dirname(__file__)
config_path=os.path.join(dir,'config.ini')

config=configparser.ConfigParser()
config.read(config_path)

db_config=config['db']
URL_CONN = URL.create(drivername=db_config["drivername"],
                     username=db_config["username"],
                     password=db_config["password"],
                     host=db_config["host"],
                     database=db_config["database"],
                     query={"driver": db_config["driver"],"TrustServerCertificate": db_config["TrustServerCertificate"]})

ENGINE = create_engine(URL_CONN)

def getSession() -> Session:
    return Session(ENGINE)






