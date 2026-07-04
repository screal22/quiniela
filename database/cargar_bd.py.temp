from scripts import utils
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime

load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

PATH_BD = os.getenv('PATH_BD')

# TODO Para partidos solo incluir los que no se han subido
TABLA = 'partidos'

secret = {
    "username": DB_USER,
    "password": DB_PASSWORD,
    "engine": "postgres",
    "host": DB_HOST,
    "port": DB_PORT,
    "dbname": DB_NAME
}

df_carga = pd.read_csv(PATH_BD, encoding='latin-1')

# Convertir fecha
df_carga['fecha_partido'] = pd.to_datetime(df_carga['fecha_partido'], format='%d/%m/%Y %H:%M')
df_carga['added_date'] = datetime.today()

query = f'INSERT INTO {TABLA} ({", ".join(df_carga.columns.tolist())}) VALUES %s'
utils.cargar_bd(secret, f'{TABLA}', df_carga, query, borrar_tabla=False)