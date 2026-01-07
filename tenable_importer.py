"""
Módulo para importar datos desde Tenable Security Center
Simula la integración con Tenable API
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class TenableDataImporter:
    """Clase para importar y procesar datos de Tenable"""
    
    def __init__(self):
        self.connected = False
        self.last_scan_date = None
        
    def connect(self, api_key, secret_key, url="https://cloud.tenable.com"):
        """Simula conexión a Tenable API"""
        # En un caso real, aquí iría la lógica de autenticación
        self.connected = True
        self.api_key = api_key
        self.url = url
        return True
    
    def simulate_scan_data(self, days_back=30, num_assets=100):
        """Genera datos de escaneo simulados"""
        
        np.random.seed(42)
        
        # Generar fechas
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        assets = []
        vulnerabilities = []
        
        # Generar activos
        for i in range(num_assets):
            asset_id = f"ASSET-{i:04d}"
            ip = f"172.22.{np.random.randint(1, 200)}.{np.random.randint(1, 255)}"
            
            asset = {
                'asset_id': asset_id,
                'ip_address': ip,
                'hostname': f"SVR-{np.random.choice(['DB', 'WEB', 'APP', 'FILE'])}-{i:03d}",
                'os': np.random.choice(['Windows Server 2022', 'Ubuntu 22.04', 'CentOS 7', 'Windows 11']),
                'last_scanned': (end_date - timedelta(days=np.random.randint(0, days_back))).strftime('%Y-%m-%d'),
                'status': np.random.choice(['Active', 'Inactive', 'Quarantined'], p=[0.8, 0.15, 0.05])
            }
            assets.append(asset)
            
            # Generar vulnerabilidades para cada activo
            num_vulns = np.random.randint(0, 50)
            for v in range(num_vulns):
                severity = np.random.choice(['Critical', 'High', 'Medium', 'Low', 'Info'], 
                                           p=[0.05, 0.15, 0.30, 0.40, 0.10])
                
                vulnerability = {
                    'asset_id': asset_id,
                    'cve_id': f"CVE-202{np.random.randint(3, 5)}-{np.random.randint(1000, 9999)}",
                    'severity': severity,
                    'cvss_score': round(np.random.uniform(0, 10), 1),
                    'plugin_id': f"PLUGIN-{np.random.randint(10000, 99999)}",
                    'description': self._generate_vuln_description(),
                    'discovery_date': (end_date - timedelta(days=np.random.randint(0, days_back))).strftime('%Y-%m-%d'),
                    'remediated': np.random.choice([True, False], p=[0.3, 0.7])
                }
                vulnerabilities.append(vulnerability)
        
        return {
            'assets': pd.DataFrame(assets),
            'vulnerabilities': pd.DataFrame(vulnerabilities),
            'scan_metadata': {
                'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_assets': num_assets,
                'total_vulnerabilities': len(vulnerabilities),
                'critical_count': len([v for v in vulnerabilities if v['severity'] == 'Critical'])
            }
        }
    
    def _generate_vuln_description(self):
        """Genera descripciones de vulnerabilidades realistas"""
        templates = [
            "Remote Code Execution vulnerability in {} service",
            "Privilege Escalation via {}",
            "SQL Injection in {} endpoint",
            "Cross-Site Scripting (XSS) in {}",
            "Buffer Overflow in {} component",
            "Information Disclosure via {}",
            "Denial of Service in {} service"
        ]
        
        components = ['HTTP', 'SSH', 'Database', 'Web Application', 'API', 'File System', 'Network']
        
        template = np.random.choice(templates)
        component = np.random.choice(components)
        
        return template.format(component)
    
    def export_to_csv(self, data, output_dir='./exports'):
        """Exporta datos a CSV"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Exportar activos
        assets_file = f"{output_dir}/tenable_assets_{timestamp}.csv"
        data['assets'].to_csv(assets_file, index=False)
        
        # Exportar vulnerabilidades
        vulns_file = f"{output_dir}/tenable_vulnerabilities_{timestamp}.csv"
        data['vulnerabilities'].to_csv(vulns_file, index=False)
        
        # Exportar metadatos
        metadata_file = f"{output_dir}/tenable_metadata_{timestamp}.json"
        with open(metadata_file, 'w') as f:
            json.dump(data['scan_metadata'], f, indent=2)
        
        return {
            'assets_file': assets_file,
            'vulnerabilities_file': vulns_file,
            'metadata_file': metadata_file
        }
    
    def generate_report(self, data):
        """Genera un reporte de análisis"""
        
        vuln_df = data['vulnerabilities']
        
        report = {
            'summary': {
                'total_assets': len(data['assets']),
                'total_vulnerabilities': len(vuln_df),
                'critical_assets': len(vuln_df[vuln_df['severity'] == 'Critical']['asset_id'].unique()),
                'remediation_rate': f"{vuln_df['remediated'].mean() * 100:.1f}%"
            },
            'severity_distribution': vuln_df['severity'].value_counts().to_dict(),
            'top_vulnerabilities': vuln_df['cve_id'].value_counts().head(10).to_dict(),
            'assets_at_risk': data['assets'][data['assets']['status'] == 'Active'].shape[0]
        }
        
        return report