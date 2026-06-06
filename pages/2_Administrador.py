# LIBRERÍAS
import streamlit as st
import os
import pandas as pd
from scripts import utils
from services import alta_registros
from dotenv import load_dotenv
import time

# CONFIGURACIÓN
st.set_page_config(
    page_title="Administrador",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Logo en la parte superior de la barra lateral
st.sidebar.image('./static/img/logo_rgv.png', width=150)

# VARIABLES DE ENTORNO
load_dotenv()
# google_maps_api_key = os.getenv('')

# INICIO DE SESIÓN
if 'login_admin' not in st.session_state:
    st.session_state['login_admin'] = False

# AUTENTICACIÓN
login = st.empty()
with login.form(key='login_form_admin'):
        st.header('Login administrador')
        st.write('Ingresa las credenciales para cargar los resultados de los juegos')
        usuario = st.text_input('Usuario', key='user_admin')
        password = st.text_input('Contraseña', type='password', key='password_admin')
        submit_button = st.form_submit_button(label='Ingresar')

if submit_button:
    if utils.validacion_credenciales_admin(usuario, password):
        st.session_state['login_admin'] = True

        st.session_state.pop('user_admin', None)
        st.session_state.pop('password_admin', None)

        st.rerun()

    else:
        st.error('Usuario o contraseña incorrectos')

        st.session_state['login_admin'] = False

        st.session_state.pop('user_admin', None)
        st.session_state.pop('password_admin', None)

if st.session_state['login_admin']:
    
    # SECCIONES
    st.title('Administrador')

    with st.container(border=True):

        st.header('Carga de resultados')

        # =====================================
        # CARGA PARTIDOS
        # =====================================

        dict_partidos = utils.carga_dict_partidos(
            './static/sql/partidos_jugados.sql'
        )

        # =====================================
        # SELECTBOX
        # =====================================

        partido_interes = st.selectbox(
            'Carga los resultados de los partidos',
            options=list(dict_partidos.keys()),
            format_func=lambda x: dict_partidos[x],
            placeholder='Selecciona una opción'
        )

        # =====================================
        # INPUTS
        # =====================================

        col1, col2 = st.columns(2)

        with col1:

            resultado_1 = st.number_input(
                'Goles equipo 1',
                min_value=0,
                step=1,
                key='resultado_1' 
            )

        with col2:

            resultado_2 = st.number_input(
                'Goles equipo 2',
                min_value=0,
                step=1,
                key='resultado_2'
            )

        # =====================================
        # BOTONES
        # =====================================
        
        guardar, cancelar = st.columns(2)
            
        if guardar.button('Guardar', type='primary'):

            resultado = alta_registros.guardar_resultado_partido(
                id_partido=partido_interes,
                resultado_1=resultado_1,
                resultado_2=resultado_2
            )

            if resultado['success']:

                equipo_1, equipo_2 = (
                    dict_partidos[
                        partido_interes
                    ].split(' vs ')
                )

                st.success(f'Resultado guardado correctamente: {equipo_1} {resultado_1} - {equipo_2} {resultado_2}')

                time.sleep(3)
                    
                st.session_state['login_admin'] = False
                st.session_state.pop('user_admin', None)
                st.session_state.pop('password_admin', None)
                st.session_state.pop('resultado_1', 0)
                st.session_state.pop('resultado_2', 0)
                
                st.rerun()

            else:

                st.error(
                    resultado['message']
                )
        
        if cancelar.button('Cancelar', type='primary'):
            st.session_state['login_admin'] = False
            st.session_state.pop('resultado_1', 0)
            st.session_state.pop('resultado_2', 0)
        
            st.rerun()

    # st.write(st.session_state)