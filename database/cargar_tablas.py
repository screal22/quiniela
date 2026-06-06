import pandas as pd
import uuid

from database.connection import SessionLocal, Base
from database.models import Partidos, Pronosticos, ResultadosPartidos

# NOTE Correr con python -m database.cargar_tablas

# Sesión
db = SessionLocal()

# Recrear tablas
Base.metadata.drop_all(bind=db.bind)
Base.metadata.create_all(bind=db.bind)

# Leer CSV
df_partidos = pd.read_csv('data/partidos.csv', encoding='latin-1')
df_pronosticos = pd.read_csv('data/pronosticos.csv', encoding='latin-1')
df_resultados_partidos = pd.read_csv('data/resultados_partidos.csv', encoding='latin-1')

# Convertimos los nulls en -1
df_pronosticos[['pronostico_1','pronostico_2']] = df_pronosticos[['pronostico_1','pronostico_2']].fillna(-1)
df_resultados_partidos[['resultado_1','resultado_2']] = df_resultados_partidos[['resultado_1','resultado_2']].fillna(-1)

df_pronosticos[['pronostico_1','pronostico_2']] = df_pronosticos[['pronostico_1','pronostico_2']].astype(int)
df_resultados_partidos[['resultado_1','resultado_2']] = df_resultados_partidos[['resultado_1','resultado_2']].astype(int)

# Convertir fecha
df_partidos['fecha_partido'] = pd.to_datetime(df_partidos['fecha_partido'], format='%d/%m/%Y %H:%M')

# Crear objetos
partidos = [
    Partidos(
        id=row['id'],
        nom_partido=row['nom_partido'],
        fecha_partido=row['fecha_partido'],
    )
    for _, row in df_partidos.iterrows()
]

pronosticos = [
    Pronosticos(
        id=uuid.uuid4(),
        id_partido=row['id_partido'],
        pronostico_1=row['pronostico_1'],
        pronostico_2=row['pronostico_2'],
        participante=row['participante'],
    )
    for _, row in df_pronosticos.iterrows()
]

resultados_partidos = [
    ResultadosPartidos(
        id=uuid.uuid4(),
        id_partido=row['id_partido'],
        resultado_1=row['resultado_1'],
        resultado_2=row['resultado_2'],
    )
    for _, row in df_resultados_partidos.iterrows()
]

# Insert masivo
try:

    db.bulk_save_objects(partidos)
    db.bulk_save_objects(pronosticos)
    db.bulk_save_objects(resultados_partidos)

    db.commit()

    print('Datos cargados correctamente')

except Exception as e:

    db.rollback()

    print(f'Error: {e}')

finally:

    db.close()