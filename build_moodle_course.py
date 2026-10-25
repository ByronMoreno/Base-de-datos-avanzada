# -*- coding: utf-8 -*-
"""
Script maestro para la construcción y diseño estético profesional del curso en Moodle,
incorporando los videos en español para cada una de las clases de 2 y 3 horas.
URL: https://baseavanzada.milaulas.com/course/view.php?id=2
"""
import sys
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
s = requests.Session()
s.headers.update(headers)

# 1. Login
print("Iniciando sesión en Moodle...")
r = s.get('https://baseavanzada.milaulas.com/login/index.php')
token = BeautifulSoup(r.text, 'html.parser').find('input', {'name': 'logintoken'})['value']
r_login = s.post('https://baseavanzada.milaulas.com/login/index.php', data={
    'username': 'bmoreno',
    'password': 'Datos2026$',
    'logintoken': token
})

if 'Área personal' in r_login.text or 'bmoreno' in r_login.text:
    print("Login exitoso como Byron Moreno.")
else:
    print("Error en login.")
    sys.exit(1)

def update_section(sec_id, name, summary_html):
    print(f"\n--- Sincronizando Sección ID={sec_id}: '{name}' ---")
    url = f'https://baseavanzada.milaulas.com/course/editsection.php?id={sec_id}'
    r_form = s.get(url)
    soup = BeautifulSoup(r_form.text, 'html.parser')
    form = soup.find('form', class_='mform')
    if not form:
        print(f"Error: no se encontró formulario en {url}")
        return False
    
    post_data = {}
    for inp in form.find_all(['input', 'textarea', 'select']):
        n = inp.get('name')
        if not n: continue
        if inp.name == 'select':
            sel = inp.find('option', selected=True)
            post_data[n] = sel.get('value') if sel else ''
        elif inp.name == 'textarea':
            post_data[n] = inp.text
        else:
            post_data[n] = inp.get('value', '')
            
    if 'cancel' in post_data: del post_data['cancel']
    
    post_data['name'] = name
    post_data['summary_editor[text]'] = summary_html.strip()
    post_data['summary_editor[format]'] = '1'
    
    action_url = form.get('action') or url
    r_res = s.post(action_url, data=post_data)
    if r_res.status_code == 200 and 'course/view.php' in r_res.url:
        print(f"Sección {sec_id} guardada con éxito.")
        return True
    else:
        print(f"Resultado inesperado en sección {sec_id}: status={r_res.status_code}")
        return False

# ============================================================================
# SECCIÓN 0: INFORMACIÓN GENERAL Y PRESENTACIÓN
# ============================================================================
SEC0_NAME = "📌 Información General y Presentación de la Asignatura"

SEC0_HTML = """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">

    <!-- HERO BANNER PRINCIPAL -->
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0369a1 100%); color: #ffffff; border-radius: 14px; padding: 32px 28px; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);">
        <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 20px;">
            <div style="flex: 1 1 500px;">
                <div style="display: inline-block; background: rgba(56, 189, 248, 0.2); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 20px; padding: 5px 14px; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; color: #38bdf8; margin-bottom: 12px;">
                    🏛️ Instituto Superior Tecnológico de Turismo y Patrimonio Yavirac
                </div>
                <h1 style="font-size: 2.2rem; font-weight: 800; margin: 0 0 10px 0; color: #ffffff; line-height: 1.2;">
                    Base de Datos Avanzada <span style="color: #38bdf8; font-weight: 400; font-size: 1.6rem;">(DS4AC1-215)</span>
                </h1>
                <p style="font-size: 1.1rem; color: #e2e8f0; margin: 0 0 18px 0; max-width: 650px; line-height: 1.5;">
                    Tecnología Superior en Desarrollo de Software • Segundo Semestre • <strong>Paralelo D</strong> • Modalidad Dual
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    <span style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 6px; padding: 4px 10px; font-size: 0.82rem; font-weight: 600;">📅 Periodo 2026-II</span>
                    <span style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 6px; padding: 4px 10px; font-size: 0.82rem; font-weight: 600;">⏱️ 48 Horas Formación</span>
                    <span style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 6px; padding: 4px 10px; font-size: 0.82rem; font-weight: 600;">🏢 Régimen Dual</span>
                    <span style="background: rgba(34, 197, 94, 0.25); border: 1px solid rgba(34, 197, 94, 0.4); color: #86efac; border-radius: 6px; padding: 4px 10px; font-size: 0.82rem; font-weight: 600;">🐘 PostgreSQL 16+</span>
                    <span style="background: rgba(239, 68, 68, 0.25); border: 1px solid rgba(239, 68, 68, 0.4); color: #fca5a5; border-radius: 6px; padding: 4px 10px; font-size: 0.82rem; font-weight: 600;">🎬 Videotutoriales en Español (18 Clases)</span>
                </div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(8px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 12px; padding: 18px 22px; min-width: 260px;">
                <div style="font-size: 0.8rem; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Docente de la Asignatura</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff; margin: 4px 0 2px 0;">Ing. Yoli Moya, MSc.</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 10px;">Coordinadora de Carrera / Representante de Colectivo</div>
                <div style="font-size: 0.82rem; color: #e2e8f0; border-top: 1px solid rgba(255,255,255,0.15); padding-top: 8px;">
                    ✉️ Atención académica y tutorías presenciales / virtuales
                </div>
            </div>
        </div>
    </div>

    <!-- TARJETAS DE INFORMACIÓN GENERAL (3 COLUMNAS) -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 24px;">
        
        <!-- Tarjeta 1: Horario de Clases -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #0284c7; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
            <h4 style="color: #0369a1; margin: 0 0 10px 0; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>⏱️</span> Horario Oficial — Paralelo D
            </h4>
            <p style="font-size: 0.9rem; color: #475569; margin: 0 0 12px 0;">
                El proceso formativo se estructura en <strong>2 sesiones presenciales semanales</strong> (5 horas totales):
            </p>
            <ul style="margin: 0; padding-left: 20px; font-size: 0.88rem; color: #334155;">
                <li style="margin-bottom: 6px;"><strong>Lunes (2 Horas — ACD):</strong> Aula presencial. Clase magistral teórica, análisis de sintaxis, arquitectura y videotutorial en español.</li>
                <li><strong>Miércoles (3 Horas — APECD):</strong> Laboratorio de cómputo. Taller práctico-experimental, ejercicios guiados, retos con solucionario y videotutorial práctico.</li>
            </ul>
        </div>

        <!-- Tarjeta 2: Sistema de Evaluación -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #16a34a; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
            <h4 style="color: #15803d; margin: 0 0 10px 0; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>📊</span> Criterios de Evaluación (PEA)
            </h4>
            <div style="margin-bottom: 8px; font-size: 0.88rem; color: #334155;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span><strong>Evaluación Formativa (60%):</strong></span>
                    <span style="color: #15803d; font-weight: 700;">6.0 pts</span>
                </div>
                <div style="font-size: 0.8rem; color: #64748b; margin-bottom: 8px;">Talleres en laboratorio, actividades en aula, refuerzos académicos y trabajo autónomo.</div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span><strong>Evaluación Sumativa (40%):</strong></span>
                    <span style="color: #15803d; font-weight: 700;">4.0 pts</span>
                </div>
                <div style="font-size: 0.8rem; color: #64748b;">Examen Parcial 1 (20%) + Examen Parcial 2 / PIS (20%).</div>
            </div>
            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 6px; padding: 6px 10px; font-size: 0.8rem; color: #166534; font-weight: 600;">
                Nota mínima: 7.00 / 10 • Asistencia mínima: 70%
            </div>
        </div>

        <!-- Tarjeta 3: Herramientas Tecnológicas -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #7c3aed; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
            <h4 style="color: #6d28d9; margin: 0 0 10px 0; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>🛠️</span> Entorno Tecnológico Requerido
            </h4>
            <ul style="margin: 0; padding-left: 20px; font-size: 0.88rem; color: #334155;">
                <li style="margin-bottom: 5px;"><strong>Motor de BD:</strong> PostgreSQL 16+ (Servidor local o Docker).</li>
                <li style="margin-bottom: 5px;"><strong>Gestión Gráfica:</strong> pgAdmin 4 y cliente de terminal <code>psql</code> o DBeaver.</li>
                <li style="margin-bottom: 5px;"><strong>Modelado CASE:</strong> pgModeler o Lucidchart.</li>
                <li><strong>Editor & IA:</strong> Visual Studio Code con extensión de PostgreSQL y asistente de IA (GitHub Copilot / ChatGPT).</li>
            </ul>
        </div>
    </div>

    <!-- RESULTADOS DE APRENDIZAJE INSTITUCIONALES (PEA OFICIAL) -->
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 12px; padding: 22px 24px; margin-bottom: 20px;">
        <h4 style="color: #0f172a; margin: 0 0 14px 0; font-size: 1.15rem; display: flex; align-items: center; gap: 10px;">
            <span>🎯</span> Resultados de Aprendizaje Oficiales de la Asignatura
        </h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px;">
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 16px;">
                <span style="background: #e0f2fe; color: #0369a1; font-size: 0.75rem; font-weight: 700; border-radius: 4px; padding: 2px 6px;">RdA 1</span>
                <p style="margin: 6px 0 0 0; font-size: 0.88rem; color: #334155; line-height: 1.4;">
                    <strong>Brinda</strong> asistencia técnica en el diseño, modelamiento e ilustración del proceso de base de datos relacional.
                </p>
            </div>
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 16px;">
                <span style="background: #e0f2fe; color: #0369a1; font-size: 0.75rem; font-weight: 700; border-radius: 4px; padding: 2px 6px;">RdA 2</span>
                <p style="margin: 6px 0 0 0; font-size: 0.88rem; color: #334155; line-height: 1.4;">
                    <strong>Utiliza</strong> herramientas y tecnologías de programación para llevar a cabo tareas específicas en el desarrollo de software.
                </p>
            </div>
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 16px;">
                <span style="background: #e0f2fe; color: #0369a1; font-size: 0.75rem; font-weight: 700; border-radius: 4px; padding: 2px 6px;">RdA 3</span>
                <p style="margin: 6px 0 0 0; font-size: 0.88rem; color: #334155; line-height: 1.4;">
                    <strong>Brinda</strong> asistencia técnica en el diseño de bases de datos mediante control y seguimiento de operaciones para el manejo adecuado de datos.
                </p>
            </div>
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 16px;">
                <span style="background: #e0f2fe; color: #0369a1; font-size: 0.75rem; font-weight: 700; border-radius: 4px; padding: 2px 6px;">RdA 4</span>
                <p style="margin: 6px 0 0 0; font-size: 0.88rem; color: #334155; line-height: 1.4;">
                    <strong>Realiza</strong> procesos de análisis y verificación de consistencia de datos extraídos de diversas fuentes para generar reportes relevantes.
                </p>
            </div>
        </div>
    </div>

</div>
"""

# ============================================================================
# SECCIÓN 1: UNIDAD 1
# ============================================================================
SEC1_NAME = "🏛️ UNIDAD 1: Sentencias SQL complejas, vistas e índices"

SEC1_HTML = """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">

    <!-- CABECERA DE LA UNIDAD 1 -->
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%); color: #ffffff; border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px;">
            <div>
                <span style="background: rgba(255,255,255,0.2); border-radius: 4px; padding: 3px 10px; font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">
                    ID Unidad: 347552 • Carga: 23 Horas • Semanas 1 a 4
                </span>
                <h3 style="margin: 8px 0 4px 0; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
                    Unidad 1: Sentencias SQL complejas, vistas e índices
                </h3>
                <p style="margin: 0; color: #dbeafe; font-size: 0.92rem;">
                    <strong>Competencia:</strong> Diseñar y modelar bases de datos aplicando principios de modelamiento y estructuras relacionales para apoyar el desarrollo de software.
                </p>
            </div>
            <div style="text-align: right; font-size: 0.85rem; color: #bfdbfe;">
                <div>Evaluación: <strong>Examen Parcial 1</strong></div>
                <div>Fechas: <strong>26 Oct — 18 Nov 2026</strong></div>
            </div>
        </div>
    </div>

    <!-- TARJETAS SEMANALES UNIDAD 1 -->
    <div style="display: grid; grid-template-columns: 1fr; gap: 16px;">

        <!-- SEMANA 1 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #1e3a8a; font-weight: 700; font-size: 1.05rem;">
                    📘 Semana 1: Modelado Lógico, DDL, Tablas Catálogo y Polimórficas (5 Horas)
                </h5>
                <span style="background: #dbeafe; color: #1e40af; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">26 & 28 Oct 2026</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultado de Aprendizaje:</strong> Modela esquemas relacionales normalizados hasta 3FN e implementa la base de datos en PostgreSQL con sentencias DDL, tablas catálogo y relaciones polimórficas garantizando la consistencia de datos.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; font-size: 0.85rem;">
                <!-- Clase 1 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #0369a1;">Clase 1 (Lunes 26/10 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 2px;">Transformación conceptual a lógico, normalización (1FN-3FN), catálogo unificado vs tipos ENUM, arcos exclusivos polimórficos y DDL con <code>IDENTITY</code>.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=normalizacion+bases+de+datos+todocode+1fn+2fn+3fn" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (2h): Modelado y Normalización (1FN, 2FN, 3FN) — TodoCode
                        </a>
                    </div>
                </div>
                <!-- Clase 2 -->
                <div style="background: #f8fafc; border-left: 3px solid #16a34a; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #15803d;">Clase 2 (Miércoles 28/10 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 2px;">Taller en pgModeler/Lucidchart e implementación DDL de la plataforma turística <em>KunturGo</em> con pruebas de restricciones y solucionario.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=postgresql+ddl+create+table+foreign+key+picacodigo" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (3h): Tablas DDL y Claves Foráneas en PostgreSQL — PicaCódigo
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- SEMANA 2 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #1e3a8a; font-weight: 700; font-size: 1.05rem;">
                    📘 Semana 2: SQL Avanzado, Funciones Escalares, Ingreso Masivo e IA en VS Code (8 Horas)
                </h5>
                <span style="background: #dbeafe; color: #1e40af; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">02 & 04 Nov 2026</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultados de Aprendizaje:</strong> Ejecuta consultas analíticas avanzadas sobre múltiples tablas, valida consistencia de datos mediante agrupamiento y subconsultas, y utiliza asistentes de inteligencia artificial para formular consultas en PostgreSQL.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; font-size: 0.85rem;">
                <!-- Clase 3 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #0369a1;">Clase 3 (Lunes 02/11 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 2px;">Orden léxico vs lógico en SQL, operadores relacionales/lógicos, funciones escalares (numéricas, texto, fecha), cruce de tablas con JOINs y DISTINCT asistidos por IA.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=postgresql+consultas+avanzadas+joins+fazt" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (2h): Consultas Complejas y JOINs en PostgreSQL — Fazt Code
                        </a>
                    </div>
                </div>
                <!-- Clase 4 -->
                <div style="background: #f8fafc; border-left: 3px solid #16a34a; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #15803d;">Clase 4 (Miércoles 04/11 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 2px;">Taller de agregaciones (<code>GROUP BY</code>, <code>HAVING</code>, <code>FILTER</code>), subconsultas, CTEs múltiples (<code>WITH</code>) e ingesta masiva (<code>COPY</code>, <code>generate_series</code>).</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=postgresql+group+by+having+subconsultas+copy+csv" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (3h): GROUP BY, HAVING y Carga COPY CSV — PicaCódigo
                        </a>
                    </div>
                </div>
            </div>
            <div style="margin-top: 8px; font-size: 0.8rem; color: #64748b; background: #f1f5f9; padding: 6px 10px; border-radius: 4px;">
                💡 <strong>Horas Autónomas:</strong> APEA (1h — Ingesta masiva de datos en PostgreSQL) + AA (2h — Extensión de IA en Visual Studio Code para Text-to-SQL).
            </div>
        </div>

        <!-- SEMANA 3 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #1e3a8a; font-weight: 700; font-size: 1.05rem;">
                    📘 Semana 3: Vistas, Arquitectura de Índices y Optimización de Rendimiento (5 Horas)
                </h5>
                <span style="background: #dbeafe; color: #1e40af; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">09 & 11 Nov 2026</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultado de Aprendizaje:</strong> Diseña e implementa vistas e índices optimizados, analiza planes de ejecución y compara el rendimiento computacional de consultas SQL en PostgreSQL.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; font-size: 0.85rem;">
                <!-- Clase 5 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #0369a1;">Clase 5 (Lunes 09/11 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 2px;">Vistas estándar y materializadas (<code>REFRESH CONCURRENTLY</code>), estructura de índices (B-Tree, Hash, GIN), lectura de planes de ejecución con <code>EXPLAIN ANALYZE</code>.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=postgresql+vistas+materializadas+systemguards" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (2h): Vistas y Vistas Materializadas en PostgreSQL — SystemGuards
                        </a>
                    </div>
                </div>
                <!-- Clase 6 -->
                <div style="background: #f8fafc; border-left: 3px solid #16a34a; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #15803d;">Clase 6 (Miércoles 11/11 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 2px;">Creación y eliminación de vistas, creación de índices parciales y compuestos, comparativa de métricas de rendimiento con y sin índice.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=postgresql+explain+analyze+indices+systemguards" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (3h): Optimización con Índices y EXPLAIN ANALYZE — Mauro Bernal
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- SEMANA 4 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03); border-left: 5px solid #dc2626;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #b91c1c; font-weight: 700; font-size: 1.05rem;">
                    🎓 Semana 4: Repaso Unidad 1 y Evaluación del Primer Parcial (5 Horas)
                </h5>
                <span style="background: #fee2e2; color: #991b1b; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">16 & 18 Nov 2026</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultado de Aprendizaje:</strong> Resuelve problemas complejos de modelado, extracción y optimización de datos en PostgreSQL demostrando dominio técnico de los contenidos de la Unidad 1.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; font-size: 0.85rem;">
                <!-- Clase 7 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #0369a1;">Clase 7 (Lunes 16/11 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 2px;">Retroalimentación académica, síntesis de la Unidad 1, clínica de dudas y análisis de los 6 errores más frecuentes en exámenes.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=errores+comunes+sql+consultas+bettatech" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (2h): Errores Típicos en Consultas y Trucos SQL — BettaTech
                        </a>
                    </div>
                </div>
                <!-- Clase 8 -->
                <div style="background: #f8fafc; border-left: 3px solid #dc2626; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #b91c1c;">Clase 8 (Miércoles 18/11 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 2px;"><strong>Examen Práctico Oficial del Primer Parcial:</strong> Caso empresarial integrador <em>Yavirac Heritage Stays</em> en laboratorio.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=resolucion+examen+practico+postgresql+laboratorio" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (3h): Resolución de Caso de Examen Práctico — La Geekipedia
                        </a>
                    </div>
                </div>
            </div>
        </div>

    </div>
</div>
"""

# ============================================================================
# SECCIÓN 2: UNIDAD 2
# ============================================================================
SEC2_NAME = "⚙️ UNIDAD 2: Procedimientos, funciones y triggers"

SEC2_HTML = """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">

    <!-- CABECERA DE LA UNIDAD 2 -->
    <div style="background: linear-gradient(135deg, #047857 0%, #059669 100%); color: #ffffff; border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(5, 150, 105, 0.15);">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px;">
            <div>
                <span style="background: rgba(255,255,255,0.2); border-radius: 4px; padding: 3px 10px; font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">
                    ID Unidad: 347553 • Carga: 15 Horas • Semanas 5 a 7
                </span>
                <h3 style="margin: 8px 0 4px 0; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
                    Unidad 2: Procedimientos, funciones y triggers
                </h3>
                <p style="margin: 0; color: #d1fae5; font-size: 0.92rem;">
                    <strong>Competencia:</strong> Aplicar herramientas y tecnologías de bases de datos avanzadas para implementar mecanismos de procesamiento y gestión eficiente de la información en aplicaciones de software.
                </p>
            </div>
            <div style="text-align: right; font-size: 0.85rem; color: #a7f3d0;">
                <div>Evaluación: <strong>Talleres Prácticos Integradores</strong></div>
                <div>Fechas: <strong>23 Nov — 09 Dic 2026</strong></div>
            </div>
        </div>
    </div>

    <!-- TARJETAS SEMANALES UNIDAD 2 -->
    <div style="display: grid; grid-template-columns: 1fr; gap: 16px;">

        <!-- SEMANA 5 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #047857; font-weight: 700; font-size: 1.05rem;">
                    📗 Semana 5: Funciones y Procedimientos Almacenados en PL/pgSQL (5 Horas)
                </h5>
                <span style="background: #d1fae5; color: #065f46; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">23 & 25 Nov 2026</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultado de Aprendizaje:</strong> Desarrolla funciones y procedimientos almacenados en PL/pgSQL aplicando parámetros avanzados, variables de registro y estructuras de control para encapsular lógica de negocio en el motor de base de datos.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; font-size: 0.85rem;">
                <!-- Clase 9 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #0369a1;">Clase 9 (Lunes 23/11 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 2px;">Arquitectura de rutinas (FUNCTION vs PROCEDURE), argumentos (IN, OUT, INOUT, VARIADIC), retornos escalares/tabulares, variables RECORD y cláusula <code>SELECT ... INTO</code>.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=postgresql+plpgsql+funciones+jesus+conde" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (2h): Introducción a PL/pgSQL y Funciones — Jesús Conde
                        </a>
                    </div>
                </div>
                <!-- Clase 10 -->
                <div style="background: #f8fafc; border-left: 3px solid #16a34a; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #15803d;">Clase 10 (Miércoles 25/11 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 2px;">Taller de desarrollo, invocación y eliminación de rutinas; función de amortización crediticia con <code>RETURN NEXT</code> y procedimientos transaccionales.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=postgresql+stored+procedures+create+procedure+call" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (3h): Procedimientos Almacenados en PostgreSQL — PicaCódigo
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- SEMANA 6 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #047857; font-weight: 700; font-size: 1.05rem;">
                    📗 Semana 6: Fundamentos, Arquitectura y Creación de Triggers (5 Horas)
                </h5>
                <span style="background: #d1fae5; color: #065f46; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">30 Nov & 02 Dic 2026</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultado de Aprendizaje:</strong> Construye e implementa disparadores y funciones trigger en PostgreSQL que garantizan la integridad activa de los datos y ejecutan auditorías automáticas ante operaciones DML.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; font-size: 0.85rem;">
                <!-- Clase 11 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #0369a1;">Clase 11 (Lunes 30/11 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 2px;">Modelo de 2 pasos, eventos (INSERT/UPDATE/DELETE/TRUNCATE), momentos (BEFORE/AFTER/INSTEAD OF), variables de contexto (NEW, OLD, TG_*) y cláusula WHEN.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=postgresql+triggers+disparadores+jesus+conde" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (2h): Fundamentos de Disparadores en PostgreSQL — Jesús Conde
                        </a>
                    </div>
                </div>
                <!-- Clase 12 -->
                <div style="background: #f8fafc; border-left: 3px solid #16a34a; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #15803d;">Clase 12 (Miércoles 02/12 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 2px;">Taller de triggers para validación automática de precios, sincronización de existencias de inventario en Kardex y auditoría forense multi-tabla.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=postgresql+triggers+stock+auditoria+picacodigo" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (3h): Triggers para Control de Stock y Auditoría — PicaCódigo
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- SEMANA 7 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #047857; font-weight: 700; font-size: 1.05rem;">
                    📗 Semana 7: Implementación Avanzada de Triggers en Producción (5 Horas)
                </h5>
                <span style="background: #d1fae5; color: #065f46; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">07 & 09 Dic 2026</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultados de Aprendizaje:</strong> Diseña e implementa soluciones automatizadas avanzadas mediante triggers condicionales y procedimientos almacenados en PostgreSQL, garantizando la consistencia y trazabilidad de los datos.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; font-size: 0.85rem;">
                <!-- Clase 13 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #0369a1;">Clase 13 (Lunes 07/12 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 2px;">Patrones avanzados: triggers condicionales, arcos de integridad complejos, prevención de recursividad con <code>pg_trigger_depth()</code>, auditoría diferencial con JSONB y soft delete.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=postgresql+triggers+avanzados+when+recursividad" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (2h): Triggers Avanzados y Cláusula WHEN — El Laboratorio de Rafa
                        </a>
                    </div>
                </div>
                <!-- Clase 14 -->
                <div style="background: #f8fafc; border-left: 3px solid #16a34a; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #15803d;">Clase 14 (Miércoles 09/12 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 2px;">Laboratorio integrador de cierre de Unidad 2: Procedimiento transaccional de facturación combinado con disparadores en la distribuidora <em>TechAndes S.A.</em></div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=postgresql+triggers+procedimientos+jsonb+auditoria" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (3h): Triggers con Procedimientos y Auditoría JSONB — SystemGuards
                        </a>
                    </div>
                </div>
            </div>
        </div>

    </div>
</div>
"""

# ============================================================================
# SECCIÓN 3: UNIDAD 3
# ============================================================================
SEC3_NAME = "🔐 UNIDAD 3: Transacciones y Seguridad"

SEC3_HTML = """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">

    <!-- CABECERA DE LA UNIDAD 3 -->
    <div style="background: linear-gradient(135deg, #b45309 0%, #d97706 100%); color: #ffffff; border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(217, 119, 6, 0.15);">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px;">
            <div>
                <span style="background: rgba(255,255,255,0.2); border-radius: 4px; padding: 3px 10px; font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">
                    ID Unidad: 347554 • Carga: 10 Horas • Semanas 8 y 9
                </span>
                <h3 style="margin: 8px 0 4px 0; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
                    Unidad 3: Transacciones y Seguridad
                </h3>
                <p style="margin: 0; color: #fef3c7; font-size: 0.92rem;">
                    <strong>Competencia:</strong> Administrar y controlar las operaciones de bases de datos mediante mecanismos de seguimiento, integridad y gestión de transacciones que garanticen la confiabilidad de la información.
                </p>
            </div>
            <div style="text-align: right; font-size: 0.85rem; color: #fde68a;">
                <div>Evaluación: <strong>Examen Parcial 2 & Recuperación</strong></div>
                <div>Fechas: <strong>14 Dic — 23 Dic 2026</strong></div>
            </div>
        </div>
    </div>

    <!-- TARJETAS SEMANALES UNIDAD 3 -->
    <div style="display: grid; grid-template-columns: 1fr; gap: 16px;">

        <!-- SEMANA 8 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #b45309; font-weight: 700; font-size: 1.05rem;">
                    📙 Semana 8: Transacciones, Concurrencia y Seguridad (Roles y Usuarios) (5 Horas)
                </h5>
                <span style="background: #fef3c7; color: #92400e; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">14 & 16 Dic 2026</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultado de Aprendizaje:</strong> Describe los conceptos de transaccionalidad y concurrencia y administra roles, privilegios y políticas de seguridad para el control de acceso a la información en PostgreSQL.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; font-size: 0.85rem;">
                <!-- Clase 15 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #0369a1;">Clase 15 (Lunes 14/12 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 2px;">Propiedades ACID, comandos TCL (BEGIN, COMMIT, ROLLBACK, SAVEPOINT), concurrencia MVCC, niveles de aislamiento, bloqueos pesimistas, deadlocks y criterios de seguridad.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=transacciones+acid+concurrencia+mvcc+postgresql" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (2h): Transacciones ACID y Concurrencia MVCC — BettaTech
                        </a>
                    </div>
                </div>
                <!-- Clase 16 -->
                <div style="background: #f8fafc; border-left: 3px solid #16a34a; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #15803d;">Clase 16 (Miércoles 16/12 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 2px;">Laboratorio simultáneo en 2 terminales concurrentes, prevención de Lost Update con <code>FOR UPDATE</code>, matriz de roles RBAC y políticas Row-Level Security (RLS).</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=postgresql+roles+usuarios+permisos+rls+seguridad" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (3h): Roles, Permisos y Seguridad RLS en PostgreSQL — PicaCódigo
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- SEMANA 9 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03); border-left: 5px solid #dc2626;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #b91c1c; font-weight: 700; font-size: 1.05rem;">
                    🎓 Semana 9: Repaso Final, Examen Parcial 2 y Examen de Recuperación (5 Horas)
                </h5>
                <span style="background: #fee2e2; color: #991b1b; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">21 & 23 Dic 2026</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultado de Aprendizaje:</strong> Demuestra dominio integral en el desarrollo de procedimientos, triggers, transacciones seguras y optimización de bases de datos relacionales en PostgreSQL bajo evaluación sumativa.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; font-size: 0.85rem;">
                <!-- Clase 17 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #0369a1;">Clase 17 (Lunes 21/12 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 2px;">Retroalimentación académica final de la asignatura, síntesis de Unidades 2 y 3, clínica de dudas de PL/pgSQL y verificación de rúbricas del PIS.</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=repaso+final+bases+de+datos+avanzadas+postgresql" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (2h): Repaso General y Buenas Prácticas en PostgreSQL — Fazt Code
                        </a>
                    </div>
                </div>
                <!-- Clase 18 -->
                <div style="background: #f8fafc; border-left: 3px solid #dc2626; padding: 10px 14px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #b91c1c;">Clase 18 (Miércoles 23/12 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 2px;"><strong>Examen Práctico Oficial del Segundo Parcial</strong> (<em>CoopYavirac Ltda.</em>) y <strong>Examen de Recuperación Integral</strong> (<em>AndesMed S.A.</em>).</div>
                    <div style="margin-top: 8px;">
                        <a href="https://www.youtube.com/results?search_query=evaluacion+final+laboratorio+postgresql+examen" target="_blank" style="display: inline-flex; align-items: center; gap: 5px; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; border-radius: 4px; padding: 3px 8px; font-size: 0.76rem; font-weight: 700; text-decoration: none;">
                            🎬 Video (3h): Guía de Evaluación y Defensa de Proyecto — La Geekipedia
                        </a>
                    </div>
                </div>
            </div>
        </div>

    </div>
</div>
"""

# ============================================================================
# SECCIÓN 4: PROYECTO INTEGRADOR Y RECURSOS
# ============================================================================
SEC4_NAME = "🏆 Proyecto Integrador de Saberes (PIS), Datasets y Evaluaciones"

SEC4_HTML = """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">

    <!-- CABECERA DE PROYECTO Y RECURSOS -->
    <div style="background: linear-gradient(135deg, #475569 0%, #334155 100%); color: #ffffff; border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(51, 65, 85, 0.15);">
        <h3 style="margin: 0 0 6px 0; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
            🏆 Proyecto Integrador de Saberes (PIS), Datasets Reales y Bibliografía
        </h3>
        <p style="margin: 0; color: #cbd5e1; font-size: 0.92rem;">
            Espacio de integración curricular, especificaciones del proyecto de fin de ciclo, bases de datos de benchmarking a gran escala y referencias bibliográficas oficiales.
        </p>
    </div>

    <!-- TARJETAS DE PIS Y DATASETS -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; margin-bottom: 20px;">
        
        <!-- PIS -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-top: 4px solid #0284c7; border-radius: 10px; padding: 18px 20px;">
            <h5 style="color: #0369a1; margin: 0 0 10px 0; font-size: 1.05rem;">
                🚀 Proyecto de Integración de Saberes (PIS)
            </h5>
            <p style="font-size: 0.88rem; color: #475569; margin-bottom: 12px;">
                Desarrollo de una solución empresarial completa que integra todos los núcleos de aprendizaje del semestre:
            </p>
            <ul style="font-size: 0.85rem; color: #334155; margin: 0; padding-left: 18px; line-height: 1.5;">
                <li>Modelado lógico normalizado (3FN) con tablas catálogo y arcos polimórficos.</li>
                <li>Estrategias de indexación y vistas materializadas analíticas.</li>
                <li>Lógica procedural en PL/pgSQL (funciones y procedimientos almacenados transaccionales).</li>
                <li>Triggers activos para validación de negocio y bitácora de auditoría diferencial con JSONB.</li>
                <li>Seguridad granular con roles empresariales (RBAC) y políticas Row-Level Security (RLS).</li>
            </ul>
        </div>

        <!-- Datasets Reales -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-top: 4px solid #16a34a; border-radius: 10px; padding: 18px 20px;">
            <h5 style="color: #15803d; margin: 0 0 10px 0; font-size: 1.05rem;">
                🗄️ Datasets Estándar para Laboratorios Reales
            </h5>
            <div style="font-size: 0.85rem; color: #334155; line-height: 1.5;">
                <div style="margin-bottom: 8px;">
                    <strong>1. Employees (3.9 Millones de registros):</strong> Utilizado en análisis de rendimiento, escaneos secuenciales vs de índice, y benchmarking con <code>EXPLAIN ANALYZE</code>.
                </div>
                <div style="margin-bottom: 8px;">
                    <strong>2. Pagila (62.322 filas / 33 tablas):</strong> Modelo completo de alquiler de películas para funciones PL/pgSQL, triggers y transacciones concurrentes.
                </div>
                <div>
                    <strong>3. MusicBrainz:</strong> Esquema empresarial de metadatos musicales para estudio de tablas catálogo y relaciones polimórficas a gran escala.
                </div>
            </div>
        </div>

    </div>

    <!-- BIBLIOGRAFÍA OFICIAL PEA -->
    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px;">
        <h5 style="color: #0f172a; margin: 0 0 12px 0; font-size: 1.05rem;">
            📚 Bibliografía Oficial del PEA (Asignatura DS4AC1-215)
        </h5>
        <ol style="margin: 0; padding-left: 20px; font-size: 0.85rem; color: #334155; line-height: 1.6;">
            <li><strong>Obe, R., & Hsu, L. (2014).</strong> <em>PostgreSQL: Up and Running</em> (2da Ed.). EE.UU.: O'Reilly Media. <em>(Disponible en Biblioteca Digital Yavirac)</em>.</li>
            <li><strong>Domínguez Chávez, J. (2019).</strong> <em>Fundamentos de Programación en Lenguaje PL/pgSQL</em>. Aragua: IEASS Editorial. <em>(Disponible en Biblioteca Digital Yavirac)</em>.</li>
            <li><strong>Sánchez, F., Pazmiño, G., Gordón, A., Mera, E., Chipuxi, L., Moya, Y., Páez, R., Mejía, H. (2024).</strong> <em>Guía completa de desarrollo de software</em> (Tomo 2, 1ra Ed.). Quito: Editorial Yavirac. ISBN: 978-9942-48-412-3. <em>(Disponible en Biblioteca Digital Yavirac)</em>.</li>
            <li><strong>Silberschatz, A., Korth, H. F., & Sudarshan, S. (2006).</strong> <em>Fundamentos de Bases de Datos</em> (5ta Ed.). McGraw-Hill.</li>
            <li><strong>Elmasri, R., & Navathe, S. B. (2007).</strong> <em>Fundamentos de Sistemas de Bases de Datos</em> (5ta Ed.). Pearson Educación.</li>
            <li><strong>Zea, M., Molina, J., & Redrován, F. (2017).</strong> <em>Administración de base de datos con PostgreSQL</em>. Alicante: Área de Innovación y Desarrollo, S.L.</li>
        </ol>
    </div>

</div>
"""

# Ejecutar actualizaciones en las 5 secciones
sections_to_update = [
    (1, SEC0_NAME, SEC0_HTML),
    (2, SEC1_NAME, SEC1_HTML),
    (3, SEC2_NAME, SEC2_HTML),
    (4, SEC3_NAME, SEC3_HTML),
    (5, SEC4_NAME, SEC4_HTML)
]

success_count = 0
for sec_id, name, html in sections_to_update:
    ok = update_section(sec_id, name, html)
    if ok:
        success_count += 1

print(f"\n========================================================")
print(f"Resumen de sincronización: {success_count} de 5 secciones actualizadas con videos.")
print(f"URL del curso: https://baseavanzada.milaulas.com/course/view.php?id=2")
print(f"========================================================")
