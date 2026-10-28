# -*- coding: utf-8 -*-
"""
Script maestro para incrustar reproductores de video YouTube (iframes interactivos)
en Moodle (https://baseavanzada.milaulas.com/course/view.php?id=2)
y actualizar los archivos markdown del repositorio.
"""
import sys
import re
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

VIDEOS = {
    "w1_c1": {
        "id": "kvt2wE-q-yY",
        "canal": "TodoCode",
        "titulo": "Normalización en Bases de Datos (1FN, 2FN, 3FN)",
        "duracion": "~28 min",
        "desc": "Reglas de transformación a relacional, atomicidad, dependencias funcionales y 3FN."
    },
    "w1_c2": {
        "id": "FRT38sQeZ-w",
        "canal": "PicaCódigo",
        "titulo": "PostgreSQL: Creación de Tablas DDL, Primary Key y Foreign Keys",
        "duracion": "~32 min",
        "desc": "Sentencias DDL, CREATE TABLE, PRIMARY KEY, FOREIGN KEY, CHECK y IDENTITY."
    },
    "w2_c3": {
        "id": "FprFu75BoE4",
        "canal": "Fazt Code",
        "titulo": "Consultas SQL y Relaciones con JOINs (INNER, LEFT, RIGHT, FULL)",
        "duracion": "~35 min",
        "desc": "Operadores lógicos, funciones escalares y cruce de tablas con JOINs."
    },
    "w2_c4": {
        "id": "Uu2hUZumPxY",
        "canal": "PicaCódigo",
        "titulo": "PostgreSQL: GROUP BY, HAVING, Subconsultas e Ingesta Masiva",
        "duracion": "~40 min",
        "desc": "Agrupamiento analítico, filtros HAVING, subconsultas y COPY CSV."
    },
    "w3_c5": {
        "id": "9CxEgOEVJt8",
        "canal": "SystemGuards",
        "titulo": "Vistas y Vistas Materializadas en PostgreSQL con REFRESH",
        "duracion": "~25 min",
        "desc": "Vistas estándar vs materializadas, índices subyacentes y REFRESH CONCURRENTLY."
    },
    "w3_c6": {
        "id": "scA1Mahdgvw",
        "canal": "Mauro Bernal",
        "titulo": "Optimización de Consultas, Índices B-Tree y EXPLAIN ANALYZE",
        "duracion": "~30 min",
        "desc": "Estructuras de índices (B-Tree, GIN) y análisis de costos con EXPLAIN ANALYZE."
    },
    "w4_c7": {
        "id": "TP9gg2vICGM",
        "canal": "BettaTech",
        "titulo": "Los Errores más Comunes al Escribir Consultas SQL",
        "duracion": "~22 min",
        "desc": "Anti-patrones frecuentes, mala utilización de índices y optimización de consultas."
    },
    "w4_c8": {
        "id": "5fxcSskfgxE",
        "canal": "La Geekipedia de Ernesto",
        "titulo": "Resolución Práctica de Examen y Ejercicios de Base de Datos",
        "duracion": "~45 min",
        "desc": "Resolución paso a paso de casos de laboratorio y modelado relacional."
    },
    "w5_c9": {
        "id": "_ccMbzh9Ji0",
        "canal": "Jesús Conde",
        "titulo": "Curso PostgreSQL: Programación con PL/pgSQL y Funciones",
        "duracion": "~26 min",
        "desc": "Estructura de bloques anónimos, variables, condicionales y funciones escalares."
    },
    "w5_c10": {
        "id": "ZJz-8IPP0ks",
        "canal": "PicaCódigo",
        "titulo": "Procedimientos Almacenados (STORED PROCEDURES) en PostgreSQL",
        "duracion": "~34 min",
        "desc": "CREATE PROCEDURE, control transaccional con CALL, COMMIT y parámetros INOUT."
    },
    "w6_c11": {
        "id": "obVLJxvLAOA",
        "canal": "Jesús Conde",
        "titulo": "Curso PostgreSQL: Triggers y Disparadores en PL/pgSQL",
        "duracion": "~24 min",
        "desc": "Fundamentos de triggers, timing BEFORE/AFTER, y variables NEW y OLD."
    },
    "w6_c12": {
        "id": "rzML_5HqnhI",
        "canal": "Tutoriales de Programación",
        "titulo": "Implementación Práctica de Triggers para Auditoría y Stock",
        "duracion": "~35 min",
        "desc": "Disparador para actualizar stock en compras/ventas y tabla de auditoría automática."
    },
    "w7_c13": {
        "id": "kN_mD0tWPbE",
        "canal": "El Laboratorio de Rafa",
        "titulo": "Triggers Avanzados en PostgreSQL: Cláusula WHEN y Variables NEW/OLD",
        "duracion": "~28 min",
        "desc": "Condiciones de activación con WHEN, control de estados y validaciones complejas."
    },
    "w7_c14": {
        "id": "PF4J64WP5Fc",
        "canal": "SystemGuards",
        "titulo": "Auditoría Completa con Triggers y formato JSONB en PostgreSQL",
        "duracion": "~38 min",
        "desc": "Captura dinámica de columnas modificadas en formato JSONB para trazabilidad."
    },
    "w8_c15": {
        "id": "0tAqp3w_K2o",
        "canal": "BettaTech",
        "titulo": "Transacciones ACID, Aislamiento y Concurrencia en Bases de Datos",
        "duracion": "~25 min",
        "desc": "Atomicidad, consistencia, aislamiento, durabilidad y control de concurrencia MVCC."
    },
    "w8_c16": {
        "id": "l60FP1gHtJE",
        "canal": "PicaCódigo",
        "titulo": "Seguridad en PostgreSQL: Roles, Usuarios, Permisos y RLS",
        "duracion": "~36 min",
        "desc": "Gestión de roles (ROLE), privilegios GRANT/REVOKE y Row-Level Security."
    },
    "w9_c17": {
        "id": "cHGaDfzJyY4",
        "canal": "Fazt Code",
        "titulo": "PostgreSQL y Buenas Prácticas de Arquitectura de Bases de Datos",
        "duracion": "~30 min",
        "desc": "Repaso general de optimización, índices, seguridad y diseño escalable."
    },
    "w9_c18": {
        "id": "b8BSf5SV7to",
        "canal": "La Geekipedia de Ernesto",
        "titulo": "Cómo Defender y Presentar un Proyecto de Software y Base de Datos",
        "duracion": "~27 min",
        "desc": "Guía práctica para exposición técnica, defensa de arquitectura y sustentación oral."
    }
}

def render_video_embed(key):
    v = VIDEOS[key]
    return f"""
    <div style="margin-top: 10px; border-top: 1px solid #e2e8f0; padding-top: 8px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-weight: 700; color: #dc2626; font-size: 0.78rem;">📺 Video Tutorial en Español ({v['duracion']}):</span>
            <a href="https://www.youtube.com/watch?v={v['id']}" target="_blank" style="font-size: 0.74rem; color: #2563eb; font-weight: 600; text-decoration: underline;">Abrir en YouTube ↗</a>
        </div>
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.12); background: #000;">
            <iframe src="https://www.youtube.com/embed/{v['id']}" title="{v['titulo']}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
        </div>
        <div style="font-size: 0.74rem; color: #475569; margin-top: 5px; line-height: 1.3;">
            <strong>{v['canal']}:</strong> {v['titulo']}
        </div>
    </div>
    """

print("Generando HTML completo de Secciones Moodle con reproductores incrustados...")

# ============================================================================
# SECCIÓN 1: UNIDAD 1
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
                <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff; margin: 4px 0 2px 0;">Ing. Byron Moreno</div>
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
SEC1_HTML = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">

    <!-- CABECERA DE UNIDAD 1 -->
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #0284c7 100%); color: #ffffff; border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15);">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px;">
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
    <div style="display: grid; grid-template-columns: 1fr; gap: 20px;">

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
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; font-size: 0.85rem;">
                <!-- Clase 1 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #0369a1; font-size: 0.92rem;">Clase 1 (Lunes 26/10 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 3px;">Transformación conceptual a lógico, normalización (1FN-3FN), catálogo unificado vs tipos ENUM, arcos exclusivos polimórficos y DDL con <code>IDENTITY</code>.</div>
                    {render_video_embed('w1_c1')}
                </div>
                <!-- Clase 2 -->
                <div style="background: #f8fafc; border-left: 3px solid #16a34a; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #15803d; font-size: 0.92rem;">Clase 2 (Miércoles 28/10 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 3px;">Taller en pgModeler/Lucidchart e implementación DDL de la plataforma turística <em>KunturGo</em> con pruebas de restricciones y solucionario.</div>
                    {render_video_embed('w1_c2')}
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
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; font-size: 0.85rem;">
                <!-- Clase 3 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #0369a1; font-size: 0.92rem;">Clase 3 (Lunes 02/11 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 3px;">Orden léxico vs lógico en SQL, operadores relacionales/lógicos, funciones escalares (numéricas, texto, fecha), cruce de tablas con JOINs y DISTINCT asistidos por IA.</div>
                    {render_video_embed('w2_c3')}
                </div>
                <!-- Clase 4 -->
                <div style="background: #f8fafc; border-left: 3px solid #16a34a; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #15803d; font-size: 0.92rem;">Clase 4 (Miércoles 04/11 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 3px;">Taller de agregaciones (<code>GROUP BY</code>, <code>HAVING</code>, <code>FILTER</code>), subconsultas, CTEs múltiples (<code>WITH</code>) e ingesta masiva (<code>COPY</code>, <code>generate_series</code>).</div>
                    {render_video_embed('w2_c4')}
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
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; font-size: 0.85rem;">
                <!-- Clase 5 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #0369a1; font-size: 0.92rem;">Clase 5 (Lunes 09/11 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 3px;">Vistas estándar y materializadas (<code>REFRESH CONCURRENTLY</code>), estructura de índices (B-Tree, Hash, GIN), lectura de planes de ejecución con <code>EXPLAIN ANALYZE</code>.</div>
                    {render_video_embed('w3_c5')}
                </div>
                <!-- Clase 6 -->
                <div style="background: #f8fafc; border-left: 3px solid #16a34a; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #15803d; font-size: 0.92rem;">Clase 6 (Miércoles 11/11 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 3px;">Creación y eliminación de vistas, creación de índices parciales y compuestos, comparativa de métricas de rendimiento con y sin índice.</div>
                    {render_video_embed('w3_c6')}
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
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; font-size: 0.85rem;">
                <!-- Clase 7 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #0369a1; font-size: 0.92rem;">Clase 7 (Lunes 16/11 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 3px;">Retroalimentación académica, síntesis de la Unidad 1, clínica de dudas y análisis de los 6 errores más frecuentes en exámenes.</div>
                    {render_video_embed('w4_c7')}
                </div>
                <!-- Clase 8 -->
                <div style="background: #f8fafc; border-left: 3px solid #dc2626; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #b91c1c; font-size: 0.92rem;">Clase 8 (Miércoles 18/11 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 3px;"><strong>Examen Práctico Oficial del Primer Parcial:</strong> Caso empresarial integrador <em>Yavirac Heritage Stays</em> en laboratorio.</div>
                    {render_video_embed('w4_c8')}
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
SEC2_HTML = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">

    <!-- CABECERA DE UNIDAD 2 -->
    <div style="background: linear-gradient(135deg, #065f46 0%, #059669 100%); color: #ffffff; border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(6, 95, 70, 0.15);">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px;">
            <div>
                <span style="background: rgba(255,255,255,0.2); border-radius: 4px; padding: 3px 10px; font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">
                    ID Unidad: 347553 • Carga: 15 Horas • Semanas 5 a 7
                </span>
                <h3 style="margin: 8px 0 4px 0; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
                    Unidad 2: Procedimientos, funciones y triggers
                </h3>
                <p style="margin: 0; color: #d1fae5; font-size: 0.92rem;">
                    <strong>Competencia:</strong> Automatizar la lógica de negocio y reglas de integridad transaccional dentro del motor de base de datos utilizando programación procedural en PostgreSQL.
                </p>
            </div>
            <div style="text-align: right; font-size: 0.85rem; color: #a7f3d0;">
                <div>Evaluación: <strong>Talleres & Triggers</strong></div>
                <div>Fechas: <strong>23 Nov — 11 Dic 2026</strong></div>
            </div>
        </div>
    </div>

    <!-- TARJETAS SEMANALES UNIDAD 2 -->
    <div style="display: grid; grid-template-columns: 1fr; gap: 20px;">

        <!-- SEMANA 5 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #065f46; font-weight: 700; font-size: 1.05rem;">
                    📘 Semana 5: Programación en el Motor: Funciones y Procedimientos en PL/pgSQL (5 Horas)
                </h5>
                <span style="background: #d1fae5; color: #065f46; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">23 & 25 Nov 2026</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultado de Aprendizaje:</strong> Implementa funciones y procedimientos almacenados en PL/pgSQL incorporando parámetros, estructuras de control, manejo de excepciones y transacciones autónomas.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; font-size: 0.85rem;">
                <!-- Clase 9 -->
                <div style="background: #f8fafc; border-left: 3px solid #059669; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #047857; font-size: 0.92rem;">Clase 9 (Lunes 23/11 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 3px;">Arquitectura de PL/pgSQL, bloques anónimos (<code>DO</code>), variables, tipos de datos, estructuras condicionales (<code>IF-THEN-ELSE</code>) y bucles (<code>LOOP</code>, <code>WHILE</code>, <code>FOR</code>).</div>
                    {render_video_embed('w5_c9')}
                </div>
                <!-- Clase 10 -->
                <div style="background: #f8fafc; border-left: 3px solid #10b981; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #065f46; font-size: 0.92rem;">Clase 10 (Miércoles 25/11 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 3px;">Taller de creación de funciones escalares y con retorno de tablas (<code>RETURNS TABLE</code>), procedimientos almacenados (<code>CREATE PROCEDURE</code>) y gestión de excepciones.</div>
                    {render_video_embed('w5_c10')}
                </div>
            </div>
        </div>

        <!-- SEMANA 6 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #065f46; font-weight: 700; font-size: 1.05rem;">
                    📘 Semana 6: Fundamentos y Creación de Triggers (Disparadores) (5 Horas)
                </h5>
                <span style="background: #d1fae5; color: #065f46; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">30 Nov & 02 Dic 2026</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultado de Aprendizaje:</strong> Construye triggers en PostgreSQL para auditar modificaciones de datos y forzar restricciones de negocio complejas antes o después de operaciones DML.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; font-size: 0.85rem;">
                <!-- Clase 11 -->
                <div style="background: #f8fafc; border-left: 3px solid #059669; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #047857; font-size: 0.92rem;">Clase 11 (Lunes 30/11 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 3px;">Concepto de trigger, ciclo de vida, eventos (<code>INSERT</code>, <code>UPDATE</code>, <code>DELETE</code>), momentos (<code>BEFORE</code>, <code>AFTER</code>), registros especiales <code>NEW</code> y <code>OLD</code>.</div>
                    {render_video_embed('w6_c11')}
                </div>
                <!-- Clase 12 -->
                <div style="background: #f8fafc; border-left: 3px solid #10b981; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #065f46; font-size: 0.92rem;">Clase 12 (Miércoles 02/12 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 3px;">Taller de triggers para actualización de stock en tiempo real y diseño de tablas de auditoría de movimientos con captura de usuario y timestamp.</div>
                    {render_video_embed('w6_c12')}
                </div>
            </div>
        </div>

        <!-- SEMANA 7 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #065f46; font-weight: 700; font-size: 1.05rem;">
                    📘 Semana 7: Implementación Avanzada de Triggers y Procedimientos (5 Horas)
                </h5>
                <span style="background: #d1fae5; color: #065f46; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">07 & 09 Dic 2026</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultado de Aprendizaje:</strong> Integra triggers avanzados con cláusulas condicionales WHEN, transacciones y estructuras JSONB para auditoría forense empresarial.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; font-size: 0.85rem;">
                <!-- Clase 13 -->
                <div style="background: #f8fafc; border-left: 3px solid #059669; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #047857; font-size: 0.92rem;">Clase 13 (Lunes 07/12 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 3px;">Triggers a nivel de fila vs sentencia (<code>FOR EACH ROW</code> vs <code>STATEMENT</code>), cláusula <code>WHEN</code>, prevención de mutaciones y recursividad en cascada.</div>
                    {render_video_embed('w7_c13')}
                </div>
                <!-- Clase 14 -->
                <div style="background: #f8fafc; border-left: 3px solid #10b981; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #065f46; font-size: 0.92rem;">Clase 14 (Miércoles 09/12 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 3px;">Taller de auditoría forense con almacenamiento de snapshots en <code>JSONB</code>, simulación de ataques de inyección y trazabilidad de eventos.</div>
                    {render_video_embed('w7_c14')}
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
SEC3_HTML = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">

    <!-- CABECERA DE UNIDAD 3 -->
    <div style="background: linear-gradient(135deg, #7c2d12 0%, #c2410c 100%); color: #ffffff; border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(124, 45, 18, 0.15);">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px;">
            <div>
                <span style="background: rgba(255,255,255,0.2); border-radius: 4px; padding: 3px 10px; font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">
                    ID Unidad: 347554 • Carga: 10 Horas • Semanas 8 y 9
                </span>
                <h3 style="margin: 8px 0 4px 0; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
                    Unidad 3: Transacciones y Seguridad
                </h3>
                <p style="margin: 0; color: #ffedd5; font-size: 0.92rem;">
                    <strong>Competencia:</strong> Garantizar la integridad transaccional ACID, la concurrencia y la seguridad perimetral y granular de bases de datos relacionales en entornos de producción.
                </p>
            </div>
            <div style="text-align: right; font-size: 0.85rem; color: #fed7aa;">
                <div>Evaluación: <strong>Examen Parcial 2 & PIS</strong></div>
                <div>Fechas: <strong>14 Dic 2026 — 06 Ene 2027</strong></div>
            </div>
        </div>
    </div>

    <!-- TARJETAS SEMANALES UNIDAD 3 -->
    <div style="display: grid; grid-template-columns: 1fr; gap: 20px;">

        <!-- SEMANA 8 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #7c2d12; font-weight: 700; font-size: 1.05rem;">
                    📘 Semana 8: Transacciones, Concurrencia (ACID) y Seguridad en PostgreSQL (5 Horas)
                </h5>
                <span style="background: #ffedd5; color: #7c2d12; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">14 & 16 Dic 2026</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultado de Aprendizaje:</strong> Configura transacciones concurrentes con propiedades ACID y aplica políticas de seguridad mediante roles, privilegios y Row-Level Security (RLS) en PostgreSQL.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; font-size: 0.85rem;">
                <!-- Clase 15 -->
                <div style="background: #f8fafc; border-left: 3px solid #c2410c; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #9a3412; font-size: 0.92rem;">Clase 15 (Lunes 14/12 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 3px;">Propiedades ACID, control de concurrencia multiversión (MVCC), anomalías de concurrencia y niveles de aislamiento SQL.</div>
                    {render_video_embed('w8_c15')}
                </div>
                <!-- Clase 16 -->
                <div style="background: #f8fafc; border-left: 3px solid #ea580c; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #c2410c; font-size: 0.92rem;">Clase 16 (Miércoles 16/12 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 3px;">Taller de simulación de bloqueos (<code>pg_locks</code>), gestión de roles (<code>CREATE ROLE</code>), permisos granulares y políticas de seguridad por fila (<code>RLS</code>).</div>
                    {render_video_embed('w8_c16')}
                </div>
            </div>
        </div>

        <!-- SEMANA 9 -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.03); border-left: 5px solid #dc2626;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <h5 style="margin: 0; color: #b91c1c; font-weight: 700; font-size: 1.05rem;">
                    🎓 Semana 9: Repaso General, Evaluación del Segundo Parcial y Recuperación (5 Horas)
                </h5>
                <span style="background: #fee2e2; color: #991b1b; font-size: 0.78rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">04 & 06 Ene 2027</span>
            </div>
            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 10px 0;">
                <strong>Resultado de Aprendizaje:</strong> Resuelve escenarios complejos de bases de datos integrando procedimientos, triggers, concurrencia transaccional y seguridad para la evaluación sumativa final.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 14px; font-size: 0.85rem;">
                <!-- Clase 17 -->
                <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #0369a1; font-size: 0.92rem;">Clase 17 (Lunes 04/01 — 2h ACD / Aula)</div>
                    <div style="color: #334155; margin-top: 3px;">Sesión integradora de síntesis: resolución de dudas en PL/pgSQL, triggers, transacciones y preparación para la defensa del Proyecto Integrador.</div>
                    {render_video_embed('w9_c17')}
                </div>
                <!-- Clase 18 -->
                <div style="background: #f8fafc; border-left: 3px solid #dc2626; padding: 12px 14px; border-radius: 6px;">
                    <div style="font-weight: 700; color: #b91c1c; font-size: 0.92rem;">Clase 18 (Miércoles 06/01 — 3h APECD / Laboratorio)</div>
                    <div style="color: #334155; margin-top: 3px;"><strong>Examen Práctico Oficial del Segundo Parcial:</strong> Caso integrador en laboratorio de PL/pgSQL, triggers y transacciones, cierre de actas y examen de recuperación.</div>
                    {render_video_embed('w9_c18')}
                </div>
            </div>
        </div>

    </div>
</div>
"""

# ============================================================================
# SECCIÓN 4 / ID=5: PROYECTO INTEGRADOR (LIMPIO)
# ============================================================================
SEC4_NAME = "🏆 Proyecto Integrador de Saberes (PIS), Datasets y Evaluaciones"
SEC4_HTML = """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">

    <div style="background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%); color: #ffffff; border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(67, 56, 202, 0.2);">
        <h3 style="margin: 0 0 6px 0; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
            Proyecto Integrador de Saberes (PIS) & Recursos Oficiales
        </h3>
        <p style="margin: 0; color: #e0e7ff; font-size: 0.92rem;">
            Espacio de entrega de entregables de arquitectura de datos, scripts DDL/DML, datasets reales y defensas orales.
        </p>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px;">
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            <h5 style="color: #4338ca; font-weight: 700; margin: 0 0 6px 0;">📦 Entregable Parcial 1: Modelo y DDL</h5>
            <p style="font-size: 0.84rem; color: #64748b; margin: 0 0 8px 0;">Entrega del script DDL estructurado, diccionario de datos y diagrama entidad-relación en pgModeler/Lucidchart.</p>
            <span style="background: #ede9fe; color: #5b21b6; font-size: 0.75rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">Semana 4 • Peso: 2.0 pts</span>
        </div>

        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            <h5 style="color: #4338ca; font-weight: 700; margin: 0 0 6px 0;">⚙️ Entregable Parcial 2: Lógica y Triggers</h5>
            <p style="font-size: 0.84rem; color: #64748b; margin: 0 0 8px 0;">Entrega de funciones analíticas, procedimientos transaccionales y triggers de auditoría con JSONB.</p>
            <span style="background: #ede9fe; color: #5b21b6; font-size: 0.75rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">Semana 8 • Peso: 2.5 pts</span>
        </div>

        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            <h5 style="color: #b91c1c; font-weight: 700; margin: 0 0 6px 0;">🎯 Defensa Final del Proyecto PIS</h5>
            <p style="font-size: 0.84rem; color: #64748b; margin: 0 0 8px 0;">Sustentación oral, demostración técnica en vivo, consulta de métricas y evaluación de rúbrica.</p>
            <span style="background: #fee2e2; color: #991b1b; font-size: 0.75rem; font-weight: 700; border-radius: 4px; padding: 2px 8px;">Semana 9 • Peso: 3.5 pts</span>
        </div>
    </div>

</div>
"""

# 2. Conexión y subida a Moodle
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
s = requests.Session()
s.headers.update(headers)

print("\nIniciando sesión en Moodle...")
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

# Actualizar Secciones con reproductores incrustados
update_section(1, SEC0_NAME, SEC0_HTML)
update_section(2, SEC1_NAME, SEC1_HTML)
update_section(3, SEC2_NAME, SEC2_HTML)
update_section(4, SEC3_NAME, SEC3_HTML)
update_section(5, SEC4_NAME, SEC4_HTML)

print("\n¡Todas las secciones de Moodle han sido actualizadas con reproductores incrustados!")
