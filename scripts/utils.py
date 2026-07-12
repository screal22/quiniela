import streamlit as st
import time
from dotenv import load_dotenv
import os
from database.connection import engine
import pandas as pd
import numpy as np

load_dotenv()
USER_USER = os.getenv('USER_USER')
USER_PASS = os.getenv('USER_PASS')

ADMIN_USER = os.getenv('ADMIN_USER')
ADMIN_PASS = os.getenv('ADMIN_PASS')

def crear_login():
    # Inicializar el estado de sesión si no existe
    if 'autenticado' not in st.session_state:
        st.session_state['autenticado'] = False
    if 'login_intentado' not in st.session_state:
        st.session_state['login_intentado'] = False
    if 'login_fallido' not in st.session_state:
        st.session_state['login_fallido'] = False

    # Si no se ha autenticado el usuario
    if not st.session_state['autenticado']:
        # Generamos el formulario
        login = st.empty()

        with login.form(key='login_form'):
            st.title('Login')
            usuario = st.text_input('Usuario')
            password = st.text_input('Contraseña', type='password')
            submit_button = st.form_submit_button(label='Ingresar')

        # Solo mostramos advertencia si aún no ha intentado iniciar sesión
        if not st.session_state['login_intentado']:
            login_intentado = st.warning('Por favor, ingresa tus credenciales')
        else:
            login_intentado = st.warning('Por favor, ingresa tus credenciales')
            login_intentado.empty()

        # Solo mostramos error si ya intentó y falló
        if st.session_state['login_fallido']:
            login_fallido = st.error('Usuario o contraseña incorrectos')
        else:
            login_fallido = st.error('Usuario o contraseña incorrectos')
            login_fallido.empty()

        if submit_button:
            st.session_state['login_intentado'] = True
            if validacion_credenciales(usuario, password):
                st.session_state['autenticado'] = True
                st.session_state['login_fallido'] = False
                login_fallido.empty()
                login_intentado.empty()
                login.empty()
                success = st.success('Bienvenido')
                time.sleep(2)
                success.empty()
            else:
                st.session_state['login_fallido'] = True

    return st.session_state['autenticado']

def validacion_credenciales(usuario, password):
    return usuario == USER_USER and password == USER_PASS

def validacion_credenciales_admin(usuario, password):
    return usuario == ADMIN_USER and password == ADMIN_PASS

def ejecutar_query_sql(path_sql):

    with open(path_sql, 'r', encoding='utf-8') as file:

        query = file.read()

    df = pd.read_sql(query, con=engine)

    return df

def carga_dict_resultados(path_sql):
    
    df = ejecutar_query_sql(path_sql)

    dict_resultados = dict(
        zip(
            df['nom_partido'],
            df['resultado']
        )
    )

    return dict_resultados

def carga_resultado_partido(path_sql, partido_interes):
    df = ejecutar_query_sql(path_sql)
    df = df[df['nom_partido'] == partido_interes].reset_index(drop=True)

    df['pronostico_completo'] = np.where(np.logical_or(df['pronostico_1'] == -1, df['pronostico_2'] == -1), 'Sin resultado', df['pronostico_1'].astype(str) + ' - ' + df['pronostico_2'].astype(str))
    return df[['participante','pronostico_completo','total_puntos']]

def carga_dict_partidos(path_sql):
    
    df = ejecutar_query_sql(path_sql)

    dict_partidos = dict(
        zip(
            df['id'],
            df['nom_partido']
        )
    )

    return dict_partidos

def validacion_pronosticos(uploaded_file):
    df_pronosticos = pd.read_csv(uploaded_file, encoding='latin-1')

    # Filtramos los pronósticos vacíos
    df_pronosticos_final = df_pronosticos[
        df_pronosticos[['pronostico_1','pronostico_2','participante']].notna().all(axis=1)
        ].reset_index(drop=True)

    return df_pronosticos_final

