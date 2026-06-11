import pandas as pd
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from database.connection import SessionLocal
from database.models import Pronosticos, ResultadosPartidos, Partidos


# def guardar_pronosticos(df_pronosticos):

#     db = SessionLocal()

#     try:

#         # =====================================
#         # LIMPIEZA
#         # =====================================

#         df_pronosticos[
#             ['pronostico_1', 'pronostico_2']
#         ] = (
#             df_pronosticos[
#                 ['pronostico_1', 'pronostico_2']
#             ]
#             .fillna(-1)
#             .astype(int)
#         )

#         # =====================================
#         # UPSERT
#         # =====================================

#         for _, row in df_pronosticos.iterrows():

#             pronostico_existente = (

#                 db.query(Pronosticos)

#                 .filter(
#                     Pronosticos.participante
#                     == row['participante']
#                 )

#                 .filter(
#                     Pronosticos.id_partido
#                     == row['id_partido']
#                 )

#                 .first()
#             )

#             # ===============================
#             # UPDATE
#             # ===============================

#             if pronostico_existente:

#                 pronostico_existente.pronostico_1 = (
#                     row['pronostico_1']
#                 )

#                 pronostico_existente.pronostico_2 = (
#                     row['pronostico_2']
#                 )

#             # ===============================
#             # INSERT
#             # ===============================

#             else:

#                 nuevo_pronostico = Pronosticos(

#                     id=uuid.uuid4(),

#                     participante=row[
#                         'participante'
#                     ],

#                     id_partido=row[
#                         'id_partido'
#                     ],

#                     pronostico_1=row[
#                         'pronostico_1'
#                     ],

#                     pronostico_2=row[
#                         'pronostico_2'
#                     ]
#                 )

#                 db.add(
#                     nuevo_pronostico
#                 )

#         db.commit()

#         return {
#             'success': True,
#             'message': '''
#                 Pronósticos guardados correctamente
#             '''
#         }

#     except Exception as e:

#         db.rollback()

#         return {
#             'success': False,
#             'message': str(e)
#         }

#     finally:

#         db.close()

def guardar_pronosticos(df_pronosticos):

    db = SessionLocal()

    try:

        # =====================================
        # LIMPIEZA
        # =====================================

        df_pronosticos[
            ['pronostico_1', 'pronostico_2']
        ] = (
            df_pronosticos[
                ['pronostico_1', 'pronostico_2']
            ]
            .fillna(-1)
            .astype(int)
        )

        # =====================================
        # CARGA DE PARTIDOS
        # =====================================

        partidos = {
            p.id: p
            for p in db.query(Partidos).all()
        }

        # Hora actual en la zona de México para comparar contra fecha_partido
        # (la hora límite de carga). El servidor de Streamlit corre en UTC, por
        # lo que datetime.now() sin zona adelantaría el candado ~6 h.
        fecha_actual = datetime.now(
            ZoneInfo('America/Mexico_City')
        ).replace(tzinfo=None)

        partidos_bloqueados = []
        registros_validos = []

        for _, row in df_pronosticos.iterrows():

            partido = partidos.get(
                row['id_partido']
            )

            if not partido:
                continue

            if partido.fecha_partido <= fecha_actual:

                partidos_bloqueados.append(
                    partido.nom_partido
                )

                continue

            registros_validos.append(row)

        # =====================================
        # UPSERT SOLO VÁLIDOS
        # =====================================

        for row in registros_validos:

            pronostico_existente = (

                db.query(Pronosticos)

                .filter(
                    Pronosticos.participante
                    == row['participante']
                )

                .filter(
                    Pronosticos.id_partido
                    == row['id_partido']
                )

                .first()
            )

            if pronostico_existente:

                pronostico_existente.pronostico_1 = (
                    row['pronostico_1']
                )

                pronostico_existente.pronostico_2 = (
                    row['pronostico_2']
                )

            else:

                db.add(
                    Pronosticos(
                        id=uuid.uuid4(),
                        participante=row['participante'],
                        id_partido=row['id_partido'],
                        pronostico_1=row['pronostico_1'],
                        pronostico_2=row['pronostico_2']
                    )
                )

        db.commit()

        # =====================================
        # MENSAJE
        # =====================================

        if partidos_bloqueados:

            partidos_bloqueados = sorted(
                set(partidos_bloqueados)
            )

            return {
                'success': True,
                'message': (
                    'Pronósticos guardados correctamente.\n\n'
                    'No se actualizaron los siguientes partidos '
                    'porque ya iniciaron:\n\n- '
                    + '\n- '.join(partidos_bloqueados)
                )
            }

        return {
            'success': True,
            'message': (
                'Pronósticos guardados correctamente.'
            )
        }

    except Exception as e:

        db.rollback()

        return {
            'success': False,
            'message': str(e)
        }

    finally:

        db.close()


def guardar_resultado_partido(

    id_partido,
    resultado_1,
    resultado_2
):

    db = SessionLocal()

    try:

        # =====================================
        # BUSCAR RESULTADO EXISTENTE
        # =====================================

        resultado_existente = (

            db.query(
                ResultadosPartidos
            )

            .filter(
                ResultadosPartidos.id_partido
                == id_partido
            )

            .first()
        )

        # =====================================
        # UPDATE
        # =====================================

        if resultado_existente:

            resultado_existente.resultado_1 = (
                resultado_1
            )

            resultado_existente.resultado_2 = (
                resultado_2
            )

        # =====================================
        # INSERT
        # =====================================

        else:

            nuevo_resultado = (

                ResultadosPartidos(

                    id=uuid.uuid4(),

                    id_partido=id_partido,

                    resultado_1=resultado_1,

                    resultado_2=resultado_2
                )
            )

            db.add(
                nuevo_resultado
            )

        db.commit()

        return {
            'success': True,
            'message': '''
                Resultado guardado correctamente
            '''
        }

    except Exception as e:

        db.rollback()

        return {
            'success': False,
            'message': str(e)
        }

    finally:

        db.close()