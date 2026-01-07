import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import json
import time
import io
from pathlib import Path

# ========== CONFIGURACIÓN INICIAL ==========
st.set_page_config(
    page_title="Defense Center - Security Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://example.com/help',
        'Report a bug': 'https://example.com/bug',
        'About': '# Defense Center v3.0\nSistema de Monitoreo de Seguridad'
    }
)

# ========== ESTILOS CSS PROFESIONAL ==========
st.markdown("""
<style>
    /* Estilos generales */
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 15px;
        margin-bottom: 30px;
        border-bottom: 4px solid;
        border-image: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%) 1;
    }
    
    /* Sidebar profesional */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        padding-top: 30px;
    }
    
    /* Botones de navegación */
    .nav-button {
        width: 100%;
        margin: 8px 0;
        background: linear-gradient(90deg, rgba(30, 58, 138, 0.7) 0%, rgba(37, 99, 235, 0.7) 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 20px;
        font-size: 1em;
        transition: all 0.3s;
        text-align: left;
        position: relative;
        overflow: hidden;
    }
    
    .nav-button:hover {
        transform: translateX(10px);
        box-shadow: 0 5px 15px rgba(37, 99, 235, 0.4);
    }
    
    .nav-button.active {
        background: linear-gradient(90deg, #3B82F6 0%, #1D4ED8 100%);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
        border-left: 4px solid #60A5FA;
    }
    
    /* Tarjetas de métricas mejoradas */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.9) 0%, rgba(37, 99, 235, 0.9) 100%);
        border-radius: 15px;
        padding: 25px;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transition: all 0.3s;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
    }
    
    .metric-card.critical {
        background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
    }
    
    .metric-card.high {
        background: linear-gradient(135deg, #EA580C 0%, #9A3412 100%);
    }
    
    .metric-card.medium {
        background: linear-gradient(135deg, #D97706 0%, #92400E 100%);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75em;
        font-weight: bold;
        margin: 2px;
    }
    
    .badge-critical { background: linear-gradient(135deg, #EF4444, #B91C1C); color: white; }
    .badge-high { background: linear-gradient(135deg, #F97316, #C2410C); color: white; }
    .badge-medium { background: linear-gradient(135deg, #F59E0B, #B45309); color: white; }
    .badge-low { background: linear-gradient(135deg, #10B981, #047857); color: white; }
    
    /* Progress bars */
    .progress-container {
        width: 100%;
        background-color: #E5E7EB;
        border-radius: 10px;
        overflow: hidden;
        height: 20px;
        margin: 10px 0;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 12px;
        line-height: 20px;
        transition: width 0.5s ease;
    }
    
    /* Tabs mejorados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: #1E293B;
        padding: 5px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #334155;
        color: #94A3B8;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #3B82F6 0%, #1D4ED8 100%);
        color: white !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    /* Tablas estilizadas */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Tooltips */
    [data-tooltip] {
        position: relative;
        cursor: help;
    }
    
    [data-tooltip]:hover::before {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: #1E293B;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        white-space: nowrap;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# ========== INICIALIZACIÓN DE SESIÓN ==========
if 'current_page' not in st.session_state:
    st.session_state.current_page = "inicio"

if 'tenable_data' not in st.session_state:
    st.session_state.tenable_data = None

if 'imported_files' not in st.session_state:
    st.session_state.imported_files = []

# ========== FUNCIONES AUXILIARES ==========
def generate_vulnerability_data():
    """Genera datos simulados de vulnerabilidades"""
    np.random.seed(42)
    
    # Datos de tendencias
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    vulnerabilities = [2800, 2540, 2529, 3240, 3100, 3350]
    
    # Top vulnerabilidades
    top_vulns = [
        {'name': 'CVE-2024-1234: Apache 2.4.x < 2.4.55', 'count': 310, 'severity': 'Alta', 'cvss': 8.5},
        {'name': 'CVE-2023-4567: IP Forwarding Enabled', 'count': 307, 'severity': 'Media', 'cvss': 6.5},
        {'name': 'CVE-2023-7890: DCOM Services Enum', 'count': 760, 'severity': 'Alta', 'cvss': 7.8},
        {'name': 'CVE-2024-5678: SSL/TLS Weak Ciphers', 'count': 215, 'severity': 'Media', 'cvss': 5.9},
        {'name': 'CVE-2024-3456: Default Credentials', 'count': 189, 'severity': 'Crítica', 'cvss': 9.8}
    ]
    
    # Activos críticos
    critical_assets = [
        {'ip': '172.22.134.12', 'hostname': 'SRV-DB-PROD-01', 'vulns': 81, 'last_seen': '2024-04-15'},
        {'ip': '172.22.134.51', 'hostname': 'SRV-WEB-01', 'vulns': 72, 'last_seen': '2024-04-14'},
        {'ip': '172.22.114.12', 'hostname': 'WS-ADMIN-45', 'vulns': 58, 'last_seen': '2024-04-10'},
        {'ip': '172.22.111.14', 'hostname': 'SRV-FILE-02', 'vulns': 53, 'last_seen': '2024-04-12'}
    ]
    
    return {
        'trends': {'months': months, 'vulnerabilities': vulnerabilities},
        'top_vulnerabilities': top_vulns,
        'critical_assets': critical_assets
    }

def simulate_tenable_scan():
    """Simula un escaneo de Tenable"""
    import random
    
    assets = []
    for i in range(1, 101):
        ip = f"172.22.{random.randint(1, 200)}.{random.randint(1, 255)}"
        severity = random.choice(['Crítica', 'Alta', 'Media', 'Baja'])
        assets.append({
            'asset_id': f"ASSET-{i:04d}",
            'ip_address': ip,
            'hostname': f"SRV-{random.choice(['DB', 'WEB', 'APP', 'FILE'])}-{i:03d}",
            'vulnerabilities': random.randint(1, 100),
            'severity': severity,
            'last_scanned': datetime.now().strftime("%Y-%m-%d"),
            'status': random.choice(['Active', 'Inactive', 'Quarantined'])
        })
    
    return assets

# ========== PÁGINAS ==========
def pagina_inicio():
    """Página de inicio del dashboard"""
    st.markdown("<h1 class='main-header'>🏠 Panel de Control - Defense Center</h1>", unsafe_allow_html=True)
    
    # Banner de estado
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.info("📊 **Estado del Sistema**: Todos los servicios operativos | Último escaneo: Hace 2 horas")
    
    with col2:
        if st.button("🔄 Ejecutar Escaneo", use_container_width=True):
            with st.spinner("Ejecutando escaneo..."):
                time.sleep(2)
                st.success("Escaneo completado exitosamente")
                st.rerun()
    
    with col3:
        if st.button("📊 Generar Reporte", use_container_width=True):
            st.success("Reporte generado y enviado a los administradores")
    
    # Métricas principales
    st.subheader("📈 Métricas Clave")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 0.9em; color: #BFDBFE;'>Total Activos</div>
            <div style='font-size: 2.5em; font-weight: bold;'>489</div>
            <div style='font-size: 0.8em; color: #BFDBFE;'>↗️ +12 esta semana</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 0.9em; color: #BFDBFE;'>Vulnerabilidades</div>
            <div style='font-size: 2.5em; font-weight: bold;'>3,240</div>
            <div style='font-size: 0.8em; color: #BFDBFE;'>↘️ -5% vs mes anterior</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card critical'>
            <div style='font-size: 0.9em; color: #FECACA;'>Críticas</div>
            <div style='font-size: 2.5em; font-weight: bold;'>5</div>
            <div style='font-size: 0.8em; color: #FECACA;'>⚠️ Requieren atención inmediata</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card high'>
            <div style='font-size: 0.9em; color: #FED7AA;'>Altas</div>
            <div style='font-size: 2.5em; font-weight: bold;'>24</div>
            <div style='font-size: 0.8em; color: #FED7AA;'>📅 Remediar en 72 horas</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos de resumen
    st.markdown("<br>", unsafe_allow_html=True)
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📊 Tendencias Mensuales")
        data = generate_vulnerability_data()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data['trends']['months'],
            y=data['trends']['vulnerabilities'],
            mode='lines+markers',
            line=dict(color='#3B82F6', width=4),
            marker=dict(size=10, color='#1E40AF'),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.1)'
        ))
        
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=30, b=30),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_chart2:
        st.subheader("🎯 Distribución por Tipo")
        
        types = ['Servidores', 'Workstations', 'Dispositivos de Red', 'IoT', 'Cloud']
        counts = [45, 30, 15, 7, 3]
        
        fig = px.pie(
            values=counts,
            names=types,
            color_discrete_sequence=px.colors.sequential.Blues_r,
            hole=0.4
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hoverinfo='label+percent',
            marker=dict(line=dict(color='#1E293B', width=2))
        )
        
        fig.update_layout(
            height=300,
            showlegend=False,
            margin=dict(t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Alertas recientes
    st.subheader("🚨 Alertas Recientes")
    
    alerts = [
        {'time': 'Hace 2h', 'asset': 'SRV-DB-PROD-01', 'description': 'Vulnerabilidad crítica detectada', 'severity': 'Crítica'},
        {'time': 'Hace 4h', 'asset': '172.22.134.51', 'description': 'Puerto no autorizado abierto', 'severity': 'Alta'},
        {'time': 'Hace 6h', 'asset': 'WS-USER-045', 'description': 'Software desactualizado', 'severity': 'Media'},
        {'time': 'Hace 1d', 'asset': 'VPN-Gateway', 'description': 'Configuración insegura detectada', 'severity': 'Alta'},
    ]
    
    for alert in alerts:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.markdown(f"**{alert['time']}**")
        with col2:
            st.write(f"{alert['asset']} - {alert['description']}")
        with col3:
            if alert['severity'] == 'Crítica':
                st.markdown('<span class="badge badge-critical">Crítica</span>', unsafe_allow_html=True)
            elif alert['severity'] == 'Alta':
                st.markdown('<span class="badge badge-high">Alta</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge badge-medium">Media</span>', unsafe_allow_html=True)

def pagina_detalle():
    """Página detallada de vulnerabilidades"""
    st.markdown("<h1 class='main-header'>📊 Dashboard Detallado de Vulnerabilidades</h1>", unsafe_allow_html=True)
    
    # Filtros avanzados
    with st.expander("🔍 Filtros Avanzados", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            date_range = st.date_input(
                "Rango de Fechas",
                value=(datetime.now() - timedelta(days=30), datetime.now()),
                max_value=datetime.now()
            )
        
        with col2:
            severity_filter = st.multiselect(
                "Severidad",
                ["Crítica", "Alta", "Media", "Baja", "Información"],
                default=["Crítica", "Alta", "Media"]
            )
        
        with col3:
            asset_type = st.multiselect(
                "Tipo de Activo",
                ["Servidores", "Workstations", "Network", "Cloud", "IoT"],
                default=["Servidores", "Workstations"]
            )
        
        with col4:
            cvss_score = st.slider("Puntuación CVSS mínima", 0.0, 10.0, 5.0, 0.1)
    
    # Métricas principales
    st.subheader("📈 Métricas de Vulnerabilidades")
    
    metric_cols = st.columns(5)
    
    metrics = [
        {"label": "Total", "value": "3,240", "delta": "+12%", "class": ""},
        {"label": "Críticas", "value": "5", "delta": "-2", "class": "critical"},
        {"label": "Altas", "value": "24", "delta": "+3", "class": "high"},
        {"label": "Medias", "value": "189", "delta": "+15", "class": "medium"},
        {"label": "Tiempo Promedio", "value": "45d", "delta": "-5d", "class": ""}
    ]
    
    for i, metric in enumerate(metrics):
        with metric_cols[i]:
            st.markdown(f"""
            <div class='metric-card {metric["class"]}'>
                <div style='font-size: 0.9em; color: #BFDBFE;'>{metric['label']}</div>
                <div style='font-size: 2.2em; font-weight: bold;'>{metric['value']}</div>
                <div style='font-size: 0.8em; color: #BFDBFE;'>{metric['delta']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Gráficos detallados
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Tendencias", "🔝 Top Vulnerabilidades", "📍 Distribución", "📋 Detalles"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Tendencia Acumulada")
            
            months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
            vulnerabilities = [2800, 2540, 2529, 3240, 3100, 3350]
            critical = [8, 5, 3, 5, 4, 6]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=months, y=vulnerabilities,
                name='Total',
                line=dict(color='#3B82F6', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=months, y=critical,
                name='Críticas',
                line=dict(color='#EF4444', width=3)
            ))
            
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', y=1.1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Distribución por Severidad")
            
            labels = ['Crítica', 'Alta', 'Media', 'Baja', 'Información']
            values = [5, 24, 189, 450, 2572]
            colors = ['#EF4444', '#F97316', '#F59E0B', '#10B981', '#94A3B8']
            
            fig = px.bar(
                x=labels,
                y=values,
                color=labels,
                color_discrete_map=dict(zip(labels, colors))
            )
            
            fig.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="",
                yaxis_title="Cantidad"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Top 10 Vulnerabilidades Más Críticas")
        
        data = [
            {"CVE": "CVE-2024-1234", "Descripción": "Apache 2.4.x Multiple Vulnerabilities", "CVSS": 9.8, "Activos": 310, "Días": 45},
            {"CVE": "CVE-2023-4567", "Descripción": "Remote Code Execution", "CVSS": 9.5, "Activos": 289, "Días": 120},
            {"CVE": "CVE-2024-5678", "Descripción": "Privilege Escalation", "CVSS": 8.8, "Activos": 215, "Días": 30},
            {"CVE": "CVE-2023-7890", "Descripción": "SQL Injection", "CVSS": 8.5, "Activos": 187, "Días": 90},
            {"CVE": "CVE-2024-3456", "Descripción": "Cross-Site Scripting", "CVSS": 8.2, "Activos": 165, "Días": 15},
        ]
        
        df = pd.DataFrame(data)
        
        # Añadir colores según CVSS
        def cvss_color(score):
            if score >= 9.0: return '#EF4444'
            elif score >= 7.0: return '#F97316'
            elif score >= 4.0: return '#F59E0B'
            else: return '#10B981'
        
        # Mostrar tabla con estilo
        st.dataframe(
            df,
            column_config={
                "CVE": st.column_config.TextColumn("CVE ID", width="small"),
                "Descripción": st.column_config.TextColumn("Descripción", width="large"),
                "CVSS": st.column_config.NumberColumn(
                    "CVSS",
                    format="%.1f",
                    help="Puntuación CVSS v3.1"
                ),
                "Activos": st.column_config.NumberColumn("Activos Afectados"),
                "Días": st.column_config.NumberColumn("Días Expuesto")
            },
            hide_index=True,
            use_container_width=True,
            height=300
        )
    
    with tab3:
        st.subheader("Mapa de Distribución por Segmento")
        
        # Datos de segmentos
        segments = pd.DataFrame({
            'Segmento': ['172.22.11.0/24', '172.22.134.0/24', '172.22.1.0/24', '172.22.113.0/24'],
            'Activos': [14, 256, 3, 15],
            'Vulnerabilidades': [310, 1200, 45, 180],
            'Críticas': [1, 3, 0, 1]
        })
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de dispersión
            fig = px.scatter(
                segments,
                x='Activos',
                y='Vulnerabilidades',
                size='Críticas',
                color='Segmento',
                size_max=60,
                hover_name='Segmento'
            )
            
            fig.update_layout(
                height=400,
                title="Vulnerabilidades vs Activos por Segmento",
                xaxis_title="Número de Activos",
                yaxis_title="Vulnerabilidades Detectadas"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Resumen por Segmento")
            for _, row in segments.iterrows():
                with st.expander(f"📡 {row['Segmento']}"):
                    st.metric("Activos", row['Activos'])
                    st.metric("Vulnerabilidades", row['Vulnerabilidades'])
                    st.metric("Críticas", row['Críticas'])
    
    with tab4:
        st.subheader("Detalle Completo de Activos")
        
        # Generar datos de ejemplo para tabla detallada
        np.random.seed(42)
        assets_data = []
        for i in range(50):
            assets_data.append({
                'IP': f'172.22.{np.random.randint(1, 200)}.{np.random.randint(1, 255)}',
                'Hostname': f'SVR-{np.random.choice(["DB", "WEB", "APP"])}-{i:03d}',
                'Vulns': np.random.randint(1, 100),
                'Críticas': np.random.randint(0, 5),
                'Altas': np.random.randint(0, 10),
                'Último Scan': (datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d'),
                'Estado': np.random.choice(['🟢 Seguro', '🟡 Riesgo', '🔴 Crítico'], p=[0.6, 0.3, 0.1])
            })
        
        df_assets = pd.DataFrame(assets_data)
        
        # Filtro rápido
        search = st.text_input("🔍 Buscar por IP o Hostname")
        if search:
            df_assets = df_assets[df_assets['IP'].str.contains(search) | df_assets['Hostname'].str.contains(search)]
        
        # Mostrar tabla
        st.dataframe(
            df_assets,
            column_config={
                "IP": "Dirección IP",
                "Hostname": "Nombre",
                "Vulns": "Total Vulnerabilidades",
                "Críticas": "Críticas",
                "Altas": "Altas",
                "Último Scan": "Último Escaneo",
                "Estado": "Estado"
            },
            use_container_width=True,
            height=400
        )

def pagina_importar_datos():
    """Página para importar datos desde Tenable"""
    st.markdown("<h1 class='main-header'>📁 Importar Datos desde Tenable</h1>", unsafe_allow_html=True)
    
    # Información del sistema
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        ### 📋 Información del Sistema
        - **Conector**: Tenable Security Center
        - **Versión**: v2.1.4
        - **Última sincronización**: Hace 2 horas
        - **Estado**: 🟢 Conectado
        """)
    
    with col2:
        st.info("""
        ### ⚙️ Configuración
        - **Formato soportado**: CSV, JSON, Nessus
        - **Límite de registros**: 10,000 por importación
        - **Frecuencia de escaneo**: Cada 24 horas
        - **Almacenamiento**: Base de datos segura
        """)
    
    st.markdown("---")
    
    # Pestañas para diferentes métodos de importación
    tab1, tab2, tab3 = st.tabs(["📤 Subir Archivo", "🔗 Conexión API", "🔄 Sincronización Automática"])
    
    with tab1:
        st.subheader("Subir Archivo de Exportación")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Formatos Soportados:
            
            1. **CSV Export** (Tenable.io)
            2. **Nessus (.nessus)**
            3. **JSON Export**
            4. **Excel (.xlsx)**
            
            ### Instrucciones:
            1. Exporta los datos desde Tenable
            2. Selecciona el formato adecuado
            3. Sube el archivo aquí
            4. Procesa los datos
            """)
        
        with col2:
            uploaded_file = st.file_uploader(
                "Selecciona archivo para importar",
                type=['csv', 'json', 'nessus', 'xlsx'],
                help="Sube archivos de exportación de Tenable"
            )
            
            if uploaded_file is not None:
                # Mostrar información del archivo
                file_details = {
                    "Nombre": uploaded_file.name,
                    "Tipo": uploaded_file.type,
                    "Tamaño": f"{uploaded_file.size / 1024:.1f} KB"
                }
                
                st.write("📄 **Detalles del archivo:**")
                for key, value in file_details.items():
                    st.write(f"- {key}: {value}")
                
                # Opciones de procesamiento
                st.markdown("---")
                st.subheader("Opciones de Procesamiento")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    process_mode = st.selectbox(
                        "Modo de procesamiento",
                        ["Importación completa", "Solo nuevas vulnerabilidades", "Actualización incremental"]
                    )
                
                with col_b:
                    deduplicate = st.checkbox("Eliminar duplicados", value=True)
                    validate_cves = st.checkbox("Validar CVE con base de datos", value=True)
                
                # Botón para procesar
                if st.button("🚀 Procesar Archivo", type="primary", use_container_width=True):
                    with st.spinner("Procesando archivo..."):
                        # Simular procesamiento
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i in range(100):
                            progress_bar.progress(i + 1)
                            status_text.text(f"Procesando... {i+1}%")
                            time.sleep(0.02)
                        
                        # Simular resultados
                        st.success("✅ Archivo procesado exitosamente!")
                        
                        # Mostrar estadísticas simuladas
                        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
                        
                        with stats_col1:
                            st.metric("Registros importados", "1,245")
                        with stats_col2:
                            st.metric("Vulnerabilidades únicas", "89")
                        with stats_col3:
                            st.metric("Activos nuevos", "12")
                        with stats_col4:
                            st.metric("Críticas detectadas", "3")
                        
                        # Guardar en sesión
                        st.session_state.tenable_data = {
                            'filename': uploaded_file.name,
                            'records': 1245,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        st.session_state.imported_files.append({
                            'name': uploaded_file.name,
                            'date': datetime.now().strftime("%Y-%m-%d"),
                            'records': 1245
                        })
    
    with tab2:
        st.subheader("Conexión API a Tenable")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Configuración API
            
            Para conectarse a Tenable.io o Tenable.sc:
            
            1. **Access Key**: Clave de acceso de la API
            2. **Secret Key**: Clave secreta de la API
            3. **URL**: Endpoint del servicio
            4. **Scan ID**: ID del escaneo (opcional)
            """)
        
        with col2:
            api_url = st.text_input(
                "URL de Tenable",
                value="https://cloud.tenable.com",
                placeholder="https://cloud.tenable.com o https://tenable.sc"
            )
            
            access_key = st.text_input(
                "Access Key",
                type="password",
                placeholder="Ingresa tu Access Key"
            )
            
            secret_key = st.text_input(
                "Secret Key", 
                type="password",
                placeholder="Ingresa tu Secret Key"
            )
            
            scan_id = st.text_input(
                "Scan ID (opcional)",
                placeholder="Dejar vacío para todos los escaneos"
            )
            
            # Configuración de consulta
            with st.expander("⚙️ Configuración Avanzada"):
                days_back = st.slider("Días hacia atrás", 1, 365, 30)
                limit_results = st.number_input("Límite de resultados", 100, 10000, 1000)
                include_plugins = st.checkbox("Incluir detalles de plugins", value=False)
            
            if st.button("🔗 Probar Conexión", type="secondary"):
                if access_key and secret_key:
                    with st.spinner("Probando conexión..."):
                        time.sleep(2)
                        st.success("✅ Conexión exitosa a Tenable API")
                        
                        # Simular información de la cuenta
                        st.info(f"""
                        **Información de la cuenta:**
                        - Cuenta: Security Team
                        - Escaneos disponibles: 24
                        - Activos: 489
                        - Último escaneo: Hace 2 horas
                        """)
                else:
                    st.error("❌ Por favor ingresa Access Key y Secret Key")
            
            if st.button("📥 Importar desde API", type="primary"):
                if access_key and secret_key:
                    with st.spinner("Importando datos desde Tenable API..."):
                        progress = st.progress(0)
                        
                        for i in range(100):
                            progress.progress(i + 1)
                            time.sleep(0.03)
                        
                        st.success("✅ Datos importados exitosamente desde Tenable API")
                        
                        # Mostrar estadísticas
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Escaneos importados", "15")
                        with col_b:
                            st.metric("Vulnerabilidades", "3,245")
                        with col_c:
                            st.metric("Activos", "489")
                else:
                    st.error("❌ Por favor ingresa las credenciales de API primero")
    
    with tab3:
        st.subheader("Sincronización Automática")
        
        st.info("""
        ### ⚡ Configuración de Sincronización Automática
        
        Configura sincronizaciones periódicas con Tenable para mantener
        tu dashboard actualizado automáticamente.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            frequency = st.selectbox(
                "Frecuencia de sincronización",
                ["Cada 24 horas", "Cada 12 horas", "Cada 6 horas", "Cada hora", "Manual"]
            )
            
            time_of_day = st.time_input(
                "Hora de sincronización",
                value=datetime.strptime("02:00", "%H:%M").time()
            )
            
            retention_days = st.slider(
                "Retención de datos (días)",
                7, 365, 90
            )
        
        with col2:
            notifications = st.checkbox("Enviar notificaciones por email", value=True)
            if notifications:
                email = st.text_input("Email para notificaciones", "security-team@company.com")
            
            auto_remediate = st.checkbox("Crear tickets automáticamente para críticas", value=True)
            
            if st.button("💾 Guardar Configuración", type="primary"):
                st.success("✅ Configuración de sincronización guardada")
        
        st.markdown("---")
        
        # Historial de sincronizaciones
        st.subheader("📋 Historial de Sincronizaciones")
        
        history_data = [
            {"Fecha": "2024-04-15 02:00", "Estado": "✅", "Registros": "1,245", "Duración": "45s"},
            {"Fecha": "2024-04-14 02:00", "Estado": "✅", "Registros": "1,230", "Duración": "42s"},
            {"Fecha": "2024-04-13 02:00", "Estado": "⚠️", "Registros": "890", "Duración": "38s"},
            {"Fecha": "2024-04-12 02:00", "Estado": "✅", "Registros": "1,210", "Duración": "40s"},
            {"Fecha": "2024-04-11 02:00", "Estado": "✅", "Registros": "1,195", "Duración": "39s"},
        ]
        
        df_history = pd.DataFrame(history_data)
        st.dataframe(df_history, use_container_width=True, hide_index=True)
    
    # Sección de archivos importados
    st.markdown("---")
    st.subheader("📁 Archivos Importados")
    
    if st.session_state.imported_files:
        for file in st.session_state.imported_files:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"📄 **{file['name']}**")
            with col2:
                st.write(f"📅 {file['date']} | 📊 {file['records']} registros")
            with col3:
                if st.button("🗑️", key=f"delete_{file['name']}"):
                    st.session_state.imported_files.remove(file)
                    st.rerun()
    else:
        st.info("No hay archivos importados todavía")

# ========== SIDEBAR - MENÚ PRINCIPAL ==========
with st.sidebar:
    # Logo y título
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <div style='font-size: 2em; color: white;'>🛡️</div>
        <h1 style='color: white; margin: 10px 0;'>Defense Center</h1>
        <div style='color: #94A3B8; font-size: 0.9em;'>Security Operations Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Línea divisoria
    st.markdown("<hr style='border-color: #334155; margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Estado del sistema
    st.markdown("### 📊 Estado del Sistema")
    
    system_status = {
        "Database": {"status": "🟢", "color": "#22C55E"},
        "API Services": {"status": "🟢", "color": "#22C55E"},
        "Scanner": {"status": "🟡", "color": "#F59E0B"},
        "Notifications": {"status": "🟢", "color": "#22C55E"}
    }
    
    for service, info in system_status.items():
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; margin: 8px 0;'>
            <span style='color: #D1D5DB;'>{service}</span>
            <span style='color: {info["color"]}; font-weight: bold;'>{info["status"]}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Navegación principal
    st.markdown("<hr style='border-color: #334155; margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown("### 🚀 Navegación")
    
    # Definir páginas y sus íconos
    pages = [
        {"icon": "🏠", "name": "Inicio", "id": "inicio"},
        {"icon": "📊", "name": "Dashboard Detalle", "id": "detalle"},
        {"icon": "⚠️", "name": "TC - Vulnerabilidades", "id": "vulnerabilidades"},
        {"icon": "🔍", "name": "TC - Persistencias", "id": "persistencias"},
        {"icon": "📁", "name": "Importar Datos", "id": "importar"},
        {"icon": "📄", "name": "Resumen Ejecutivo", "id": "resumen"},
    ]
    
    # Crear botones de navegación
    for page in pages:
        is_active = st.session_state.current_page == page["id"]
        button_class = "nav-button active" if is_active else "nav-button"
        
        if st.button(
            f"{page['icon']} {page['name']}",
            key=f"nav_{page['id']}",
            use_container_width=True
        ):
            st.session_state.current_page = page["id"]
            st.rerun()
    
    # Filtros para la página de vulnerabilidades
    if st.session_state.current_page == "vulnerabilidades":
        st.markdown("<hr style='border-color: #334155; margin: 30px 0;'>", unsafe_allow_html=True)
        st.markdown("### 🔍 Filtros")
        
        with st.form("filters_form"):
            periodo = st.selectbox(
                "📅 Período",
                ["Últimas 24 horas", "Últimos 7 días", "Último mes", "Abril 2024", "Marzo 2024", "Febrero 2024"],
                key="filtro_periodo"
            )
            
            severidades = st.multiselect(
                "⚠️ Nivel de severidad",
                ["Crítica", "Alta", "Media", "Baja", "Informativa"],
                default=["Crítica", "Alta", "Media"],
                key="filtro_severidad"
            )
            
            segmentos = st.multiselect(
                "🌐 Segmentos de red",
                ["172.22.11.0/24", "172.22.134.0/24", "172.22.1.0/24", "172.22.113.0/24", "172.22.114.0/24"],
                default=["172.22.11.0/24", "172.22.134.0/24"],
                key="filtro_segmentos"
            )
            
            if st.form_submit_button("Aplicar Filtros", use_container_width=True):
                st.success("Filtros aplicados")
    
    # Pie de página en sidebar
    st.markdown("<hr style='border-color: #334155; margin-top: 50px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='color: #64748B; font-size: 0.8em; text-align: center;'>
        <div>🔄 Última actualización</div>
        <div>{datetime.now().strftime("%d/%m/%Y %H:%M")}</div>
        <div style='margin-top: 10px; display: flex; justify-content: center; gap: 10px;'>
            <span>v3.0.1</span>
            <span>•</span>
            <span>© 2024</span>
        </div>
        <div style='margin-top: 5px; font-size: 0.7em;'>
            <i>Defense Center - Data Center</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========== CONTENIDO PRINCIPAL ==========
# Mostrar contenido según la página seleccionada
if st.session_state.current_page == "inicio":
    pagina_inicio()

elif st.session_state.current_page == "detalle":
    pagina_detalle()

elif st.session_state.current_page == "vulnerabilidades":
    # Esta es la página original de vulnerabilidades (simplificada)
    st.markdown("<h1 class='main-header'>⚠️ TC - Vulnerabilidades Detectadas</h1>", unsafe_allow_html=True)
    
    # Mostrar filtros activos
    if 'filtro_severidad' in st.session_state:
        st.info(f"Filtros activos: {', '.join(st.session_state.filtro_severidad)}")
    
    # Métricas rápidas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Equipos afectados", "270", "+12")
    with col2:
        st.metric("Vulnerabilidades críticas", "2", "-1", delta_color="inverse")
    with col3:
        st.metric("Total hallazgos", "3,000", "+471")
    
    # Gráfico de tendencias
    st.subheader("Tendencia de Vulnerabilidades")
    
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

elif st.session_state.current_page == "persistencias":
    st.markdown("<h1 class='main-header'>🔍 TC - Persistencias Detectadas</h1>", unsafe_allow_html=True)
    
    st.warning("Esta sección está en desarrollo. Próximamente disponible.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Persistencias Activas", "12", "+2")
        st.metric("Tiempo Promedio", "45 días", "+5")
    with col2:
        st.metric("IOCs Detectados", "8", "-1")
        st.metric("Contenidos", "3", "0")

elif st.session_state.current_page == "importar":
    pagina_importar_datos()

elif st.session_state.current_page == "resumen":
    st.markdown("<h1 class='main-header'>📄 Resumen Ejecutivo</h1>", unsafe_allow_html=True)
    
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Métricas de Cumplimiento")
        compliance_data = pd.DataFrame({
            'Estándar': ['CIS v8', 'NIST 800-53', 'ISO 27001', 'PCI-DSS'],
            'Cumplimiento': [85, 78, 92, 67],
            'Estado': ['🟢', '🟡', '🟢', '🔴']
        })
        st.dataframe(compliance_data, use_container_width=True)
    
    with col2:
        st.subheader("Objetivos del Mes")
        goals_data = pd.DataFrame({
            'Objetivo': ['Reducir vulnerabilidades críticas', 'Mejorar tiempo de respuesta', 'Actualizar políticas'],
            'Progreso': [30, 75, 100],
            'Fecha': ['30/04', '25/04', '15/04']
        })
        for _, row in goals_data.iterrows():
            st.progress(row['Progreso']/100, text=f"{row['Objetivo']}: {row['Progreso']}%")

# ========== PIE DE PÁGINA ==========
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption("🛡️ **Defense Center - Security Dashboard**")
    
with footer_col2:
    st.caption(f"📅 {datetime.now().strftime('%d de %B, %Y')}")

with footer_col3:
    if st.button("🔄 Actualizar Datos", type="secondary"):
        st.rerun()