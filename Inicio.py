import streamlit as st

st.set_page_config(
    page_title="Inicio",
)

# Logo en la parte superior de la barra lateral
st.sidebar.image('./static/img/logo_rgv.png', width=150)

# Encabezado principal
st.write("# ⚽ Bienvenido a la Quiniela")

# Descripción principal
st.markdown("""
Esta aplicación permite registrarlos pronósticos de la quiniela del mundial, así como revisar resultados y posiciones en la tabla general de los participantes.

---

### 🧾 ¿Cómo funciona la quiniela?

La quiniela deberá llenarse por rondas:

- Fase de grupos
- Dieciseisavos
- Octavos
- Cuartos
- Semifinales
- Final

Las plantillas de cada ronda serán enviadas cuando los partidos estén definidos y, participar en cada ronda, será necesario subir los pronóstico en la plantilla correspondiente.

⚠️ IMPORTANTE

- Colocar el **nombre completo** en la columna de "participante" y siempre mantener el mismo formato.
- Los resultados ya subidos a la base de datos se **sobrescribirán** con la última fecha de registro.

---

### 📅 Fechas límite para enviar pronósticos

Los pronósticos para los partidos deberán subirse al sistema **antes de las 10 am** del día en el que está programado el juego.

⚠️ IMPORTANTE

En caso de **no llenar los resultados** para una ronda o partido, **no habrá puntos asignados, sin excepción**.
            
---

### 🏆 Sistema de puntuación

La asignación de puntos se realizará de la siguiente manera:

- ✅ **3 puntos** por acertar exactamente el marcador del partido.
- ✅ **1 punto** por acertar únicamente el resultado del partido (victoria de un equipo o empate).
- ❌ **0 puntos** por un resultado incorrecto o no enviado a tiempo.

---

### ⚽ Reglas para fases eliminatorias

A partir de los **octavos de final**, si un partido llega a penales:

- El marcador considerado será el resultado al finalizar el **tiempo extra**.
- La tanda de penales **no contará** para la asignación de puntos.

---

### 💵 Costo de participación

La entrada para participar en la quiniela será de:

## 💰 $400 MXN

El pago deberá realizarse **a más tardar el 10 de junio** para poder participar.

---

### 🥇 Distribución de premios

Por definir

---

### 🔐 ¿Cómo usar la aplicación?

1. **Ingresa a la plataforma**  
   Accede con tus datos para visualizar la quiniela y registrar tus pronósticos.

2. **Carga tus pronósticos**  
   Sube tu archivo antes de la fecha límite para los partidos del día.

3. **Consulta posiciones y resultados**  
   Revisa la tabla general y el desempeño de los participantes.

---
""")