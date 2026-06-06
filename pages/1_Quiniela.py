# LIBRERÍAS
import streamlit as st
import pandas as pd
from scripts import utils
from services import alta_registros
from dotenv import load_dotenv
import time

# CONFIGURACIÓN
st.set_page_config(
    page_title='Quiniela mundialista 2026',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# Logo en la parte superior de la barra lateral
st.sidebar.image('./static/img/logo_rgv.png', width=150)

# VARIABLES DE ENTORNO
load_dotenv()

# INICIO DE SESIÓN
if 'login' not in st.session_state:
    st.session_state['login'] = False

# SECCIONES
st.title('Quiniela mundialista RGV ⚽')

## RESULTADOS DE LA QUINIELA
with st.container(border=True):
    
    st.markdown('#### **Resultados de la quiniela**')
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            # TABLA GENERAL
            st.markdown('#### **Tabla general**')
            st.bar_chart(utils.ejecutar_query_sql('./static/sql/puntos.sql'), x='total_puntos', y='participante', sort='total_puntos')
        
        with col2:
            # MARCADORES EXACTOS
            st.markdown('#### **Marcadores exactos**')
            st.bar_chart(utils.ejecutar_query_sql('./static/sql/puntos.sql'), x='total_aciertos', y='participante', sort='total_puntos')


    # PARTIDOS DEL DÍA
    df_partidos_hoy = utils.ejecutar_query_sql('./static/sql/partidos_hoy.sql')
    
    # Configuración del layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('#### **Partidos del día**')
        with st.container(border=True):

            if len(df_partidos_hoy) > 0:

                for _, row in df_partidos_hoy.iterrows(): 
                    with st.container(border=True):
                        if row['resultado']:
                            st.success(f'{row['nom_partido']} ({row['resultado']})') 
                        else:
                            st.write(f'{row['nom_partido']}') 
            
            else:
                st.markdown(f':red[**Sin partidos programados**]')
    
    with col2:
        st.markdown('#### **Resultados pendientes por subir**')
        with st.container(border=True):
            resultados_pendientes = len(utils.ejecutar_query_sql('./static/sql/resultados_pendientes.sql'))

            if resultados_pendientes == 0:
                st.success(0)
            else:
                st.error(resultados_pendientes)


    # RESULTADOS POR PARTIDO
    st.markdown('#### **Resultados por partido**')

    dict_resultados = utils.carga_dict_resultados('./static/sql/partidos_con_resultados.sql')
    partido_interes = st.selectbox('Consulta los resultados por partido', dict_resultados.keys(), placeholder='Selecciona una opción')
    st.markdown(f'**Resultado del partido: {dict_resultados[partido_interes]}**')
    
    if len(utils.carga_resultado_partido('./static/sql/detalle_puntos.sql', partido_interes)) > 0:
        # TODO Incluir formato colores puntos
        st.dataframe(utils.carga_resultado_partido('./static/sql/detalle_puntos.sql', partido_interes), hide_index=True)
    else:
        st.markdown(f':red[**Sin resultados por mostrar**]')

## CARGA DE PRONÓSTICOS

### AUTENTICACIÓN PARA CARGA DE RESULTADOS
login = st.empty()
with login.form(key='login_form'):
        st.header('Login pronósticos')
        st.write('Ingresa las credenciales para cargar tus pronósticos')
        usuario = st.text_input('Usuario', key='user')
        password = st.text_input('Contraseña', type='password', key='password')
        submit_button = st.form_submit_button(label='Ingresar')

if submit_button:
    if utils.validacion_credenciales(usuario, password):
        st.session_state['login'] = True

        st.session_state.pop('user', None)
        st.session_state.pop('password', None)

        st.rerun()

    else:
        st.error('Usuario o contraseña incorrectos')

        st.session_state['login'] = False

        st.session_state.pop('user', None)
        st.session_state.pop('password', None)

# validacion = utils.validacion_credenciales(usuario, password)

if st.session_state['login']:
    
    with st.container(border=True):

        st.header('Carga de pronósticos')

        uploaded_file = st.file_uploader(
            'Carga tu archivo',
            type='csv',
            key='carga_pronosticos'
        )

        if uploaded_file:

            df_pronosticos = utils.validacion_pronosticos(uploaded_file)

            if len(df_pronosticos) > 0:

                st.write(
                    '''
                    Vista preliminar.
                    Revisa la carga
                    de tus pronósticos
                    '''
                )

                st.dataframe(
                    df_pronosticos,
                    hide_index=True
                )

                st.markdown(f':red[**Los resultados incompletos no se cargarán**]')
            
            else:
                st.error(f'Carga de pronósticos vacía. Llena los resultados y vuelvelos a cargar')

                time.sleep(3)

                st.session_state['login'] = False
                st.session_state.pop('carga_pronosticos', None)
                st.session_state.pop('user', None)
                st.session_state.pop('password', None)
                    
                st.rerun()

            guardar, cancelar = st.columns(2)

            if guardar.button('Guardar', type='primary'):

                resultado = alta_registros.guardar_pronosticos(
                    df_pronosticos
                )

                if resultado['success']:

                    st.success(
                        resultado['message']
                    )

                    time.sleep(5)
                    
                    st.session_state['login'] = False
                    st.session_state.pop('carga_pronosticos', None)
                    st.session_state.pop('user', None)
                    st.session_state.pop('password', None)
                    
                    st.rerun()

                else:

                    st.error(
                        resultado['message']
                    )
            
            if cancelar.button('Cancelar', type='primary'):
                if 'carga_pronosticos' in st.session_state:
                    st.session_state['login'] = False
                    st.session_state.pop('carga_pronosticos', None)
                
                st.rerun()

# st.write(st.session_state)