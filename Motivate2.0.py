import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y TEMA STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Pausa y Progreso | Motivación para Atletas",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. INYECCIÓN DE CUSTOM CSS (PALETA CORPORATIVA)
# ==========================================
custom_css = """
<style>
    /* Fondo principal de la app */
    .stApp {
        background-color: #F5F8FA;
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Estilo de la Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #C1CCD4;
    }

    /* Títulos e Historiales */
    h1, h2, h3 {
        color: #557D96 !important;
        font-weight: 700;
    }

    /* Estilos para Tarjetas / KPI Cards */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #C1CCD4;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        text-align: center;
        transition: transform 0.2s ease-in-out;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #5CB0CF;
    }

    .kpi-title {
        color: #557D96;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #5CB0CF;
        font-size: 1.8rem;
        font-weight: 700;
    }

    /* Estilos de Contenedores de Banner y Tarjetas de Historias */
    .hero-banner {
        background: linear-gradient(135deg, #557D96 0%, #5CB0CF 100%);
        color: #FFFFFF;
        padding: 40px;
        border-radius: 16px;
        margin-bottom: 25px;
    }

    .hero-banner h1 {
        color: #FFFFFF !important;
        font-size: 2.8rem;
        margin-bottom: 10px;
    }

    .hero-banner p {
        font-size: 1.2rem;
        opacity: 0.95;
    }

    .quote-box {
        background-color: #FFFFFF;
        border-left: 5px solid #5CB0CF;
        border-top: 1px solid #C1CCD4;
        border-right: 1px solid #C1CCD4;
        border-bottom: 1px solid #C1CCD4;
        padding: 25px;
        border-radius: 0 12px 12px 0;
        margin: 20px 0;
        font-style: italic;
        font-size: 1.2rem;
        color: #557D96;
    }

    .story-card {
        background-color: #FFFFFF;
        border: 1px solid #C1CCD4;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
    }

    .story-tag {
        background-color: #F5F8FA;
        color: #557D96;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        border: 1px solid #C1CCD4;
    }

    /* Estilización de Botones */
    .stButton > button {
        background-color: #5CB0CF !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background-color: #557D96 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }

    /* Personalización de Pestañas (st.tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 2px solid #C1CCD4;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #FFFFFF;
        border-radius: 8px 8px 0px 0px;
        border: 1px solid #C1CCD4;
        border-bottom: none;
        color: #557D96;
        font-weight: 600;
        padding: 0px 20px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #5CB0CF !important;
        color: #FFFFFF !important;
        border-color: #5CB0CF !important;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 3. FUNCIONES AUXILIARES DE MANEJO DE DATOS
# ==========================================
@st.cache_data
def cargar_datos_csv(file):
    """
    Carga y procesa de forma segura el archivo CSV subido por el usuario.
    """
    try:
        df = pd.read_csv(file)
        df.columns = [str(col).strip() for col in df.columns]
        return df, None
    except Exception as e:
        return None, f"Error al leer el archivo CSV: {str(e)}"

def generar_datos_ejemplo():
    """
    Genera un DataFrame temporal para tendencias de rendimiento/recuperación
    en caso de que el CSV cargado no contenga columnas numéricas para st.line_chart.
    """
    dates = pd.date_range(start="2026-01-01", periods=30, freq="D")
    df_demo = pd.DataFrame({
        "Fecha": dates,
        "Nivel de Movilidad (%)": np.linspace(30, 85, 30) + np.random.normal(0, 2, 30),
        "Bienestar Mental (1-10)": np.random.choice(range(5, 10), size=30),
        "Sesiones de Fisioterapia": np.random.poisson(lam=1.5, size=30)
    })
    df_demo.set_index("Fecha", inplace=True)
    return df_demo

# ==========================================
# 4. BARRA LATERAL (CARGA DE DATOS & ACCIONES)
# ==========================================
st.sidebar.image("https://img.icons8.com/isometric-line/100/5CB0CF/sports.png", width=70)
st.sidebar.title("Ajustes del Sistema")
st.sidebar.markdown("---")

st.sidebar.subheader("📁 Base de Datos CSV")
uploaded_file = st.sidebar.file_uploader(
    "Sube tu archivo CSV de atletas o seguimiento", 
    type=["csv"], 
    help="El archivo debe estar en formato CSV."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Acciones Rápidas")
if st.sidebar.button("🔄 Restablecer Estado", use_container_width=True):
    st.rerun()

# ==========================================
# 5. CONTROLADOR PRINCIPAL Y DATOS
# ==========================================
df = None
error_msg = None

if uploaded_file is not None:
    df, error_msg = cargar_datos_csv(uploaded_file)

# ==========================================
# 6. ESTRUCTURA DASHBOARD (PESTAÑAS)
# ==========================================
tab_inicio, tab_motivacion, tab_historias, tab_apoyo, tab_recursos, tab_proyecto = st.tabs([
    "🏠 Inicio", 
    "✨ Motivación Diaria", 
    "📖 Historias", 
    "🤝 Espacio de Apoyo", 
    "📚 Recursos", 
    "ℹ️ Acerca del Proyecto"
])

# ------------------------------------------
# PESTAÑA 1: INICIO & DASHBOARD DE DATOS
# ------------------------------------------
with tab_inicio:
    st.markdown(
        """
        <div class="hero-banner">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-weight: 600; font-size: 0.9rem;">
                Un espacio para seguir a tu ritmo
            </p>
            <h1>Volver también es avanzar.</h1>
            <p>Si una lesión cambió tus planes, aquí hay lugar para la paciencia, la frustración y la esperanza.<br>
            Tu valor no depende de cuándo vuelvas a competir.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    if uploaded_file is None:
        st.info("👋 **Bienvenido/a.** Para explorar estadísticas o analíticas del programa, sube tu archivo CSV en la barra lateral izquierda.")
    elif error_msg:
        st.error(f"❌ {error_msg}")
    else:
        st.success("✅ ¡Base de datos CSV cargada correctamente!")

        st.subheader("📊 Resumen General del Sistema")
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

        with col_kpi1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Total Registros</div>
                    <div class="kpi-value">{len(df)}</div>
                </div>
                """, unsafe_allow_html=True
            )

        with col_kpi2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Columnas Analizadas</div>
                    <div class="kpi-value">{len(df.columns)}</div>
                </div>
                """, unsafe_allow_html=True
            )

        with col_kpi3:
            num_cols = df.select_dtypes(include=[np.number]).shape[1]
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Variables Numéricas</div>
                    <div class="kpi-value">{num_cols}</div>
                </div>
                """, unsafe_allow_html=True
            )

        with col_kpi4:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Estado Sistema</div>
                    <div class="kpi-value">Activo</div>
                </div>
                """, unsafe_allow_html=True
            )

        st.markdown("---")
        st.subheader("📈 Tendencias y Modulación del Progreso")

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_cols) > 0:
            selected_metrics = st.multiselect(
                "Selecciona las métricas que deseas graficar:", 
                options=numeric_cols, 
                default=numeric_cols[:2] if len(numeric_cols) >= 2 else numeric_cols
            )

            if selected_metrics:
                st.line_chart(df[selected_metrics], height=350)
            else:
                st.warning("Selecciona al menos una columna numérica para visualizar el gráfico.")
        else:
            st.write("Tu archivo CSV no cuenta con columnas numéricas directas. Visualizando tendencia de progreso estándar:")
            df_demo = generar_datos_ejemplo()
            st.line_chart(df_demo[["Nivel de Movilidad (%)", "Bienestar Mental (1-10)"]], height=350)

        with st.expander("🔍 Explorar Vista Previa de la Base de Datos CSV"):
            st.dataframe(df, use_container_width=True)

# ------------------------------------------
# PESTAÑA 2: MOTIVACIÓN DIARIA
# ------------------------------------------
with tab_motivacion:
    st.markdown("#### 01 / MOTIVACIÓN DIARIA")
    st.title("Tu pausa no borra tu progreso.")
    st.write("No hace falta sentirse fuerte todos los días. Descansar, reconocer un pequeño avance o pedir compañía también pueden ser formas de cuidarte.")

    col_quote, col_cards = st.columns([1.2, 1])

    frases = [
        "Hoy también cuenta, aunque hoy necesites descansar.",
        "Un paso cuenta: Compara tu avance contigo, no con el ritmo de alguien más.",
        "Descansar importa: Una pausa necesaria no es un fracaso.",
        "Tu valor como atleta va más allá de tus marcas y competencias.",
        "La paciencia también es entrenamiento."
    ]

    if "quote_index" not in st.session_state:
        st.session_state.quote_index = 0

    with col_quote:
        st.markdown(
            f"""
            <div class="quote-box">
                "{frases[st.session_state.quote_index]}"
            </div>
            """, 
            unsafe_allow_html=True
        )

        if st.button("🔄 Mostrar otra frase", key="btn_quote"):
            st.session_state.quote_index = (st.session_state.quote_index + 1) % len(frases)
            st.rerun()

    with col_cards:
        col_sub1, col_sub2 = st.columns(2)
        with col_sub1:
            st.markdown(
                """
                <div class="story-card">
                    <span class="story-tag">Un paso cuenta</span>
                    <h4 style="margin-top:10px; color:#557D96;">Comparación Propia</h4>
                    <p style="font-size:0.9rem;">Compara tu avance contigo, no con el ritmo de alguien más.</p>
                </div>
                """, unsafe_allow_html=True
            )
        with col_sub2:
            st.markdown(
                """
                <div class="story-card">
                    <span class="story-tag">Descansar importa</span>
                    <h4 style="margin-top:10px; color:#557D96;">Pausa Reconstituyente</h4>
                    <p style="font-size:0.9rem;">Una pausa necesaria no es un fracaso en tu carrera.</p>
                </div>
                """, unsafe_allow_html=True
            )

# ------------------------------------------
# PESTAÑA 3: HISTORIAS DE SUPERACIÓN
# ------------------------------------------
with tab_historias:
    st.markdown("#### 02 / HISTORIAS DE SUPERACIÓN")
    st.title("Cada historia tiene su propio ritmo.")
    st.write("Estas escenas muestran emociones posibles durante una lesión, sin presentar un camino único ni prometer un resultado. *Relatos ficticios e ilustrativos.*")

    col_h1, col_h2, col_h3 = st.columns(3)

    with col_h1:
        st.markdown(
            """
            <div class="story-card">
                <span class="story-tag">EJEMPLO FICTICIO · ATLETISMO</span>
                <h3 style="margin-top:10px;">Aprender a bajar el ritmo</h3>
                <p>Una corredora descubre que la frustración y la paciencia pueden convivir mientras su cuerpo sana.</p>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Leer historia completa", key="h1"):
            st.info("📖 **Aprender a bajar el ritmo:** Reducir la intensidad no significa rendirse, sino reprogramar las expectativas para permitirle al tejido sanar con seguridad.")

    with col_h2:
        st.markdown(
            """
            <div class="story-card">
                <span class="story-tag">EJEMPLO FICTICIO · NATACIÓN</span>
                <h3 style="margin-top:10px;">El valor de la pausa</h3>
                <p>Un nadador comprende que el descanso programado es parte esencial del rendimiento a largo plazo.</p>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Leer historia completa", key="h2"):
            st.info("📖 **El valor de la pausa:** Entender que el descanso físico y mental previene recaídas y fortalece la disciplina interna.")

    with col_h3:
        st.markdown(
            """
            <div class="story-card">
                <span class="story-tag">EJEMPLO FICTICIO · CICLISMO</span>
                <h3 style="margin-top:10px;">Reencontrar el propósito</h3>
                <p>Un ciclista revalora su identidad más allá de los podios y tiempos de competencia.</p>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Leer historia completa", key="h3"):
            st.info("📖 **Reencontrar el propósito:** Tu identidad deportiva no se apaga por estar fuera de pista; evoluciona hacia una perspectiva más madura.")

# ------------------------------------------
# PESTAÑA 4: ESPACIO DE APOYO
# ------------------------------------------
with tab_apoyo:
    st.markdown("#### 03 / ESPACIO DE APOYO")
    st.title("No tienes que atravesar esto a solas.")
    st.write("Comparte cómo te sientes o lee reflexiones compartidas por otros atletas en proceso de recuperación.")

    col_form, col_feed = st.columns([1, 1])

    with col_form:
        st.subheader("💬 Deja tu reflexión o sentir")
        with st.form("form_apoyo"):
            nombre_atleta = st.text_input("Nombre o Seudónimo (Opcional)")
            deporte = st.selectbox("Disciplina deportiva", ["Atletismo / Running", "Ciclismo", "Natación", "Fútbol / Deportes de Equipo", "Gimnasio / Fuerza", "Otro"])
            mensaje_apoyo = st.text_area("¿Cómo te sientes hoy respecto a tu recuperación?")
            enviar_msg = st.form_submit_button("Compartir mensaje")

            if enviar_msg:
                if mensaje_apoyo.strip() != "":
                    st.success("✨ ¡Gracias por compartir tu sentir! Tu voz forma parte de esta comunidad.")
                else:
                    st.warning("Por favor escribe un mensaje antes de enviar.")

    with col_feed:
        st.subheader("📢 Mural de la Comunidad")
        st.markdown(
            """
            <div class="story-card" style="margin-bottom: 15px;">
                <span class="story-tag">NATACIÓN</span>
                <p style="margin-top: 8px; font-style: italic;">"Hoy logré hacer mi rutina de movilidad completa sin dolor. Hace un mes parecía imposible."</p>
                <small style="color: #557D96;">— Atleta en recuperación</small>
            </div>
            <div class="story-card">
                <span class="story-tag">RUNNING</span>
                <p style="margin-top: 8px; font-style: italic;">"Aceptar caminar en lugar de correr me costó lágrimas, pero hoy entiendo que es parte del proceso."</p>
                <small style="color: #557D96;">— Corredora de fondo</small>
            </div>
            """, 
            unsafe_allow_html=True
        )

# ------------------------------------------
# PESTAÑA 5: RECURSOS
# ------------------------------------------
with tab_recursos:
    st.markdown("#### 04 / RECURSOS Y GUÍAS")
    st.title("Herramientas para tu bienestar")
    st.write("Explora lecturas recomendadas, pautas de salud mental y estrategias de fisioterapia deportiva.")

    col_r1, col_r2 = st.columns(2)

    with col_r1:
        st.markdown("### 🧠 Salud Mental Deportiva")
        st.markdown("""
        - **Gestión de la frustración:** Estrategias cognitivas para deportistas lesionados.
        - **Identidad post-lesión:** Cómo separar tu valía personal de tus marcas deportivas.
        - **Mindfulness para atletas:** Técnicas de respiración y enfoque en momentos de pausa.
        """)

    with col_r2:
        st.markdown("### 🩹 Fisioterapia y Readaptación")
        st.markdown("""
        - **El poder del descanso activo:** Movilidad segura sin comprometer la sanación.
        - **Prevención de recaídas:** Pautas clínicas para un retorno gradual y seguro.
        - **Nutrición durante el reposo:** Ajuste calórico y macronutrientes en etapas de baja actividad.
        """)

# ------------------------------------------
# PESTAÑA 6: ACERCA DEL PROYECTO
# ------------------------------------------
with tab_proyecto:
    st.markdown("#### 05 / INFORMACIÓN")
    st.title("Acerca de Pausa y Progreso")
    
    st.write(
        "**Pausa y Progreso** es una iniciativa concebida para acompañar emocional y analíticamente a atletas "
        "que atraviesan procesos de lesión, rehabilitación o pausas obligatorias en su entrenamiento."
    )
    
    st.write(
        "Nuestro objetivo principal es desestigmatizar el descanso, fomentar la autocompasión y proporcionar "
        "una plataforma interactiva clara y accesible para el seguimiento de métricas personales y de bienestar."
    )
    
    st.info("💡 Desarrollado con Streamlit · Diseñado para atletas que no se rinden, sepan o no correr hoy.")