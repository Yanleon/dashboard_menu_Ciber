import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ========== CONFIGURACIÓN INICIAL ==========
st.set_page_config(
    page_title="Defense Center 1 - Data Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== ESTILOS CSS PERSONALIZADOS ==========
st.markdown("""
<style>
    /* Estilos generales */
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px 0;
        margin-bottom: 20px;
        border-bottom: 3px solid #3B82F6;
    }
    
    /* Sidebar estilizado */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E3A8A 0%, #2563EB 100%);
        padding-top: 20px;
    }
    
    [data-testid="stSidebar"] .stButton button {
        width: 100%;
        margin: 5px 0;
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 10px;
        transition: all 0.3s;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
    }
    
    /* Tarjetas de métricas */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.2);
    }
    
    /* Badges de severidad */
    .badge-critical {
        display: inline-block;
        background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
    }
    
    .badge-high {
        display: inline-block;
        background: linear-gradient(135deg, #FFA726 0%, #FF9800 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
    }
    
    /* Pestañas estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #F8F9FA;
        padding: 8px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: 1px solid #E9ECEF;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        color: white !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== SIDEBAR - MENÚ PRINCIPAL ==========
with st.sidebar:
    # Logo y título
    st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 30px;'>🛡️ Defense Center</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #BFDBFE; margin-bottom: 40px;'>Data Center</h3>", unsafe_allow_html=True)
    
    # Línea divisoria
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2); margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Estado del sistema
    st.markdown("### 📊 Estado del Sistema")
    col_status1, col_status2 = st.columns(2)
    with col_status1:
        st.markdown("""
        <div style='background: rgba(34, 197, 94, 0.2); padding: 10px; border-radius: 8px; text-align: center;'>
            <div style='color: #22C55E; font-weight: bold;'>🟢 Online</div>
            <div style='color: #D1D5DB; font-size: 0.8em;'>Sistema</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_status2:
        st.markdown("""
        <div style='background: rgba(59, 130, 246, 0.2); padding: 10px; border-radius: 8px; text-align: center;'>
            <div style='color: #3B82F6; font-weight: bold;'>📊 3.2K</div>
            <div style='color: #D1D5DB; font-size: 0.8em;'>Hallazgos</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Navegación principal
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2); margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown("### 🚀 Navegación")
    
    # Botones de navegación
    menu_options = {
        "🏠 Inicio": "inicio",
        "⚠️ TC - Vulnerabilidades": "vulnerabilidades",
        "🔍 TC - Persistencias": "persistencias",
        "📄 Resumen ejecutivo pg 1": "resumen1",
        "📄 Resumen ejecutivo pg 2": "resumen2"
    }
    
    # Inicializar estado de navegación
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "inicio"
    
    # Crear botones de navegación
    for label, page_id in menu_options.items():
        if st.button(label, key=page_id, type="secondary"):
            st.session_state.current_page = page_id
    
    # Filtros (solo para página de vulnerabilidades)
    if st.session_state.current_page == "vulnerabilidades":
        st.markdown("<hr style='border-color: rgba(255,255,255,0.2); margin: 30px 0;'>", unsafe_allow_html=True)
        st.markdown("### 🔍 Filtros")
        
        # Filtro de fechas
        periodo = st.selectbox(
            "📅 Período",
            ["Últimos 7 días", "Último mes", "Abril 2024", "Marzo 2024", "Febrero 2024", "Personalizado"],
            key="filtro_periodo"
        )
        
        # Filtro de severidad
        severidades = st.multiselect(
            "⚠️ Nivel de severidad",
            ["Crítica", "Alta", "Media", "Baja", "Informativa"],
            default=["Crítica", "Alta", "Media"],
            key="filtro_severidad"
        )
        
        # Filtro de segmentos de red
        segmentos = st.multiselect(
            "🌐 Segmentos de red",
            ["172.22.11.0/24", "172.22.134.0/24", "172.22.1.0/24", "172.22.113.0/24", "172.22.114.0/24"],
            default=["172.22.11.0/24", "172.22.134.0/24"],
            key="filtro_segmentos"
        )
    
    # Pie de página en sidebar
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2); margin-top: 50px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='color: #94A3B8; font-size: 0.8em; text-align: center;'>
        <div>🔄 Última actualización</div>
        <div>{datetime.now().strftime("%d/%m/%Y %H:%M")}</div>
        <div style='margin-top: 10px;'>v2.1.4 • © 2024 Defense Center</div>
    </div>
    """, unsafe_allow_html=True)

# ========== CONTENIDO PRINCIPAL ==========
# Mostrar contenido según la página seleccionada

if st.session_state.current_page == "inicio":
    # PÁGINA DE INICIO
    st.markdown("<h1 class='main-header'>🏠 Panel de Control - Defense Center</h1>", unsafe_allow_html=True)
    
    # Métricas rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #BFDBFE; font-size: 1em;'>Total Activos</h3>
            <div style='font-size: 2.5em; font-weight: bold;'>489</div>
            <div style='color: #BFDBFE;'>+12 esta semana</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #BFDBFE; font-size: 1em;'>Vulnerabilidades</h3>
            <div style='font-size: 2.5em; font-weight: bold;'>3,240</div>
            <div style='color: #BFDBFE;'>-5% vs mes anterior</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #BFDBFE; font-size: 1em;'>Activos en Riesgo</h3>
            <div style='font-size: 2.5em; font-weight: bold;'>42</div>
            <div style='color: #BFDBFE;'>3 críticos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #BFDBFE; font-size: 1em;'>Escaneos Hoy</h3>
            <div style='font-size: 2.5em; font-weight: bold;'>24</div>
            <div style='color: #BFDBFE;'>3 en progreso</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos de resumen
    st.markdown("<br>", unsafe_allow_html=True)
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📈 Tendencias Mensuales")
        # Gráfico de tendencias
        meses = ['Ene', 'Feb', 'Mar', 'Abr']
        vulnerabilidades = [2850, 2540, 2529, 3240]
        
        fig_trend = go.Figure(data=go.Scatter(
            x=meses,
            y=vulnerabilidades,
            mode='lines+markers',
            line=dict(color='#3B82F6', width=4),
            marker=dict(size=10)
        ))
        fig_trend.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=0, b=0)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col_chart2:
        st.subheader("🎯 Distribución por Tipo")
        # Gráfico de pastel
        labels = ['Servidores', 'Workstations', 'Network', 'IoT', 'Otros']
        values = [45, 30, 15, 7, 3]
        
        fig_pie = px.pie(
            values=values,
            names=labels,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Acciones rápidas
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🚀 Acciones Rápidas")
    
    col_act1, col_act2, col_act3 = st.columns(3)
    
    with col_act1:
        if st.button("📊 Generar Reporte Completo", use_container_width=True):
            st.success("Reporte generado exitosamente")
    
    with col_act2:
        if st.button("🔄 Ejecutar Escaneo Completo", use_container_width=True):
            st.info("Escaneo programado para ejecutarse en 5 minutos")
    
    with col_act3:
        if st.button("📧 Enviar Alertas", use_container_width=True):
            st.success("Alertas enviadas a los equipos correspondientes")

elif st.session_state.current_page == "vulnerabilidades":
    # PÁGINA DE VULNERABILIDADES (tu dashboard original)
    st.markdown("<h1 class='main-header'>⚠️ TC - Vulnerabilidades Detectadas</h1>", unsafe_allow_html=True)
    
    # Mostrar filtros activos
    if 'filtro_severidad' in st.session_state and st.session_state.filtro_severidad:
        badges = " | ".join([f"<span class='badge-high'>{s}</span>" for s in st.session_state.filtro_severidad])
        st.markdown(f"**Filtros activos:** {badges}", unsafe_allow_html=True)
    
    # Métricas principales
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #BFDBFE; font-size: 1em;'>Equipos Afectados</h3>
            <div style='font-size: 2.5em; font-weight: bold;'>270</div>
            <div style='color: #BFDBFE;'>14 segmentos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #BFDBFE; font-size: 1em;'>Críticas</h3>
            <div style='font-size: 2.5em; font-weight: bold; color: #FF6B6B;'>2</div>
            <div style='color: #BFDBFE;'>0.7% del total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #BFDBFE; font-size: 1em;'>Altas</h3>
            <div style='font-size: 2.5em; font-weight: bold; color: #FFA726;'>18</div>
            <div style='color: #BFDBFE;'>6.7% del total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #BFDBFE; font-size: 1em;'>Total Hallazgos</h3>
            <div style='font-size: 2.5em; font-weight: bold;'>3,000</div>
            <div style='color: #BFDBFE;'>+471 este mes</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos y tablas (aquí iría el resto de tu dashboard original)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Pestañas para diferentes vistas
    tab1, tab2, tab3 = st.tabs(["📈 Tendencias", "🔝 Top Hallazgos", "🌍 Distribución"])
    
    with tab1:
        st.subheader("Tendencia de Vulnerabilidades Acumuladas")
        
        # Gráfico de tendencias
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=['Febrero', 'Marzo', 'Abril'],
            y=[2540, 2529, 3000],
            mode='lines+markers',
            name='Total',
            line=dict(color='#3B82F6', width=4)
        ))
        
        fig.update_layout(
            height=400,
            xaxis_title="Mes",
            yaxis_title="Cantidad",
            plot_bgcolor='rgba(0,0,0,0.05)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Top 10 Hallazgos Más Repetidos")
        
        # Datos de ejemplo para la tabla
        data = {
            'Vulnerabilidad': [
                'Apache 2.4.x < 2.4.55 Multiple Vulnerabilities',
                'IP Forwarding Enabled',
                'DCOM Services Enumeration',
                'Nessus TCP Scanner',
                'Service Detection',
                'Common Platform Enumeration',
                'Device Type Detection',
                'OS Identification',
                'Additional DNS Hostname',
                'Alert Standard Format'
            ],
            'Cantidad': [310, 307, 760, 479, 451, 174, 101, 101, 101, 500],
            'Severidad': ['Alta', 'Media', 'Alta', 'Media', 'Baja', 'Baja', 'Info', 'Info', 'Info', 'Media']
        }
        
        df = pd.DataFrame(data)
        st.dataframe(
            df,
            column_config={
                "Vulnerabilidad": st.column_config.TextColumn("Vulnerabilidad", width="large"),
                "Cantidad": st.column_config.NumberColumn("Cantidad", format="%d"),
                "Severidad": st.column_config.TextColumn("Severidad")
            },
            use_container_width=True,
            height=400
        )
    
    with tab3:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Por Severidad")
            severidad_data = pd.DataFrame({
                'Nivel': ['Crítica', 'Alta', 'Media', 'Baja', 'Informativa'],
                'Cantidad': [2, 18, 270, 16, 42]
            })
            
            fig_severidad = px.bar(
                severidad_data,
                x='Nivel',
                y='Cantidad',
                color='Nivel',
                color_discrete_sequence=['#DC2626', '#F97316', '#F59E0B', '#10B981', '#6B7280']
            )
            fig_severidad.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig_severidad, use_container_width=True)
        
        with col_right:
            st.subheader("Por Segmento")
            segmento_data = pd.DataFrame({
                'Segmento': ['172.22.11.x', '172.22.134.x', '172.22.1.x', '172.22.113.x'],
                'Equipos': [14, 256, 3, 15],
                'Vulnerabilidades': [310, 1200, 45, 180]
            })
            
            fig_segmento = px.scatter(
                segmento_data,
                x='Equipos',
                y='Vulnerabilidades',
                size='Vulnerabilidades',
                color='Segmento',
                size_max=50
            )
            fig_segmento.update_layout(height=350)
            st.plotly_chart(fig_segmento, use_container_width=True)

elif st.session_state.current_page == "persistencias":
    # PÁGINA DE PERSISTENCIAS
    st.markdown("<h1 class='main-header'>🔍 TC - Persistencias Detectadas</h1>", unsafe_allow_html=True)
    
    st.warning("Esta sección está en desarrollo. Próximamente disponible.")
    
    # Placeholder para contenido futuro
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Persistencias Activas", "12", "+2")
        st.metric("Tiempo Promedio", "45 días", "+5")
    
    with col2:
        st.metric("IOCs Detectados", "8", "-1")
        st.metric("Contenidos", "3", "0")

elif st.session_state.current_page in ["resumen1", "resumen2"]:
    # PÁGINAS DE RESUMEN EJECUTIVO
    page_num = "1" if st.session_state.current_page == "resumen1" else "2"
    st.markdown(f"<h1 class='main-header'>📄 Resumen Ejecutivo - Página {page_num}</h1>", unsafe_allow_html=True)
    
    # Contenido del resumen ejecutivo
    with st.expander("📋 Resumen General", expanded=True):
        st.markdown("""
        ### Hallazgos Principales
        
        1. **Total de activos monitoreados**: 489 equipos
        2. **Vulnerabilidades críticas**: 2 (requieren atención inmediata)
        3. **Segmentos más afectados**: 172.22.134.x (256 equipos)
        4. **Tendencia**: Incremento del 18.6% en hallazgos este mes
        
        ### Recomendaciones
        - **Prioridad 1**: Parchear servidores con vulnerabilidades críticas
        - **Prioridad 2**: Revisar configuración de segmento 172.22.134.x
        - **Prioridad 3**: Implementar monitoreo continuo
        """)
    
    col_stats1, col_stats2 = st.columns(2)
    
    with col_stats1:
        st.subheader("📊 Métricas de Cumplimiento")
        
        compliance_data = pd.DataFrame({
            'Estándar': ['CIS v8', 'NIST 800-53', 'ISO 27001', 'PCI-DSS'],
            'Cumplimiento': [85, 78, 92, 67],
            'Estado': ['🟢', '🟡', '🟢', '🔴']
        })
        
        st.dataframe(compliance_data, use_container_width=True)
    
    with col_stats2:
        st.subheader("🎯 Objetivos del Mes")
        
        goals_data = pd.DataFrame({
            'Objetivo': [
                'Reducir vulnerabilidades críticas',
                'Mejorar tiempo de respuesta',
                'Actualizar políticas',
                'Capacitar equipo'
            ],
            'Progreso': [30, 75, 100, 60],
            'Fecha': ['30/04', '25/04', '15/04', '28/04']
        })
        
        for _, row in goals_data.iterrows():
            st.progress(row['Progreso']/100, text=f"{row['Objetivo']}: {row['Progreso']}%")

# ========== PIE DE PÁGINA GLOBAL ==========
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption("🛡️ **Defense Center - Data Center**")
    
with footer_col2:
    st.caption(f"📅 {datetime.now().strftime('%d de %B, %Y')}")

with footer_col3:
    if st.session_state.current_page == "vulnerabilidades":
        if st.button("📥 Exportar Reporte", type="secondary"):

            st.success("Reporte exportado exitosamente (simulación)")
