# -*- coding: utf-8 -*-
"""
Script para agregar videos en español para cada una de las clases (2h y 3h)
en los archivos markdown del repositorio y en la plataforma Moodle.
"""
import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

VIDEOS_DATA = {
    1: {
        "file": "clases/semana-01-modelado-ddl-tablas-catalogo-polimorficas.md",
        "c1_video": {
            "title": "Modelado de Bases de Datos Relacionales y Normalización (1FN, 2FN, 3FN)",
            "channel": "TodoCode / Edgar Ramírez",
            "url": "https://www.youtube.com/results?search_query=normalizacion+bases+de+datos+todocode+1fn+2fn+3fn",
            "duration": "28 min",
            "desc": "Explicación de las reglas formales de transformación del modelo conceptual a relacional lógico, reducción de redundancias, diseño de tablas catálogo paramétricas y normalización hasta 3FN."
        },
        "c2_video": {
            "title": "Modelado y Creación de Tablas con DDL en PostgreSQL y pgAdmin 4",
            "channel": "PicaCódigo / La Geekipedia de Ernesto",
            "url": "https://www.youtube.com/results?search_query=postgresql+ddl+create+table+foreign+key+picacodigo",
            "duration": "32 min",
            "desc": "Implementación práctica en PostgreSQL de sentencias DDL (CREATE TABLE, PRIMARY KEY, FOREIGN KEY, CHECK, IDENTITY) y resolución de restricciones de integridad y arcos polimórficos."
        }
    },
    2: {
        "file": "clases/semana-02-sql-avanzado-ia-ingreso-masivo.md",
        "c1_video": {
            "title": "Consultas SQL Avanzadas, Funciones Escalares y Cruce de Tablas con JOINs en PostgreSQL",
            "channel": "Fazt Code / De Cero a Cien",
            "url": "https://www.youtube.com/results?search_query=postgresql+consultas+avanzadas+joins+fazt",
            "duration": "35 min",
            "desc": "Orden lógico de evaluación en SQL, operadores relacionales y lógicos, funciones escalares de fecha/texto, cruce de tablas con INNER/LEFT/RIGHT/FULL JOIN y asistencia de IA en VS Code."
        },
        "c2_video": {
            "title": "Funciones de Agregación, GROUP BY, HAVING, Subconsultas e Ingreso Masivo en PostgreSQL",
            "channel": "PicaCódigo / Informática DP",
            "url": "https://www.youtube.com/results?search_query=postgresql+group+by+having+subconsultas+copy+csv",
            "duration": "30 min",
            "desc": "Agrupamiento analítico con GROUP BY y HAVING, subconsultas correlacionadas, expresiones de tabla comunes (CTEs con WITH) y carga masiva de archivos CSV con comando COPY."
        }
    },
    3: {
        "file": "clases/semana-03-vistas-indices-rendimiento.md",
        "c1_video": {
            "title": "Vistas Estándar y Vistas Materializadas en PostgreSQL: Arquitectura y Optimización",
            "channel": "El Laboratorio de Rafa / SystemGuards",
            "url": "https://www.youtube.com/results?search_query=postgresql+vistas+materializadas+systemguards",
            "duration": "26 min",
            "desc": "Abstracción de datos mediante vistas complejas, diferencias con vistas materializadas, refresco concurrente de datos (REFRESH MATERIALIZED VIEW CONCURRENTLY) e introducción al almacenamiento físico."
        },
        "c2_video": {
            "title": "Índices en PostgreSQL y Análisis de Rendimiento con EXPLAIN ANALYZE",
            "channel": "SystemGuards / Mauro Bernal",
            "url": "https://www.youtube.com/results?search_query=postgresql+explain+analyze+indices+systemguards",
            "duration": "34 min",
            "desc": "Estructura de índices B-Tree, índices compuestos y parciales, lectura técnica de planes de ejecución en PostgreSQL y comparativa de tiempos de respuesta con y sin índice."
        }
    },
    4: {
        "file": "clases/semana-04-repaso-examen-parcial-1.md",
        "c1_video": {
            "title": "Clínica de Errores Comunes y Preguntas Frecuentes en Consultas SQL y PostgreSQL",
            "channel": "BettaTech / TodoCode",
            "url": "https://www.youtube.com/results?search_query=errores+comunes+sql+consultas+bettatech",
            "duration": "22 min",
            "desc": "Resolución de errores típicos en exámenes: trampa de nulos con NOT IN, funciones aplicadas a columnas indexadas (expresiones no SARGables) y optimización de consultas complejas."
        },
        "c2_video": {
            "title": "Simulacro y Metodología de Resolución de Examen Práctico de Laboratorio en PostgreSQL",
            "channel": "La Geekipedia de Ernesto / PicaCódigo",
            "url": "https://www.youtube.com/results?search_query=resolucion+examen+practico+postgresql+laboratorio",
            "duration": "40 min",
            "desc": "Guía práctica de resolución de un caso empresarial integral de evaluación: modelado DDL, consultas analíticas, vistas e indexación bajo tiempo cronometrado."
        }
    },
    5: {
        "file": "clases/semana-05-funciones-procedimientos-plpgsql.md",
        "c1_video": {
            "title": "Programación en el Servidor con PL/pgSQL: Sintaxis, Bloques y Funciones en PostgreSQL",
            "channel": "Jesús Conde / Universidad de Costa Rica",
            "url": "https://www.youtube.com/results?search_query=postgresql+plpgsql+funciones+jesus+conde",
            "duration": "30 min",
            "desc": "Estructura de bloques en PL/pgSQL, declaración de variables, modos de argumentos (IN, OUT, INOUT, VARIADIC), variables RECORD y uso de cláusula SELECT ... INTO."
        },
        "c2_video": {
            "title": "Procedimientos Almacenados (STORED PROCEDURES) y Retornos Tabulares en PostgreSQL",
            "channel": "PicaCódigo / El Laboratorio de Rafa",
            "url": "https://www.youtube.com/results?search_query=postgresql+stored+procedures+create+procedure+call",
            "duration": "35 min",
            "desc": "Diferencias clave entre FUNCTION y PROCEDURE, llamadas con CALL, transaccionalidad autónoma (COMMIT y ROLLBACK) y generación de tablas de amortización con RETURNS TABLE y RETURN NEXT."
        }
    },
    6: {
        "file": "clases/semana-06-fundamentos-creacion-triggers.md",
        "c1_video": {
            "title": "Fundamentos y Arquitectura de Triggers (Disparadores) en PostgreSQL",
            "channel": "Jesús Conde / El Laboratorio de Rafa",
            "url": "https://www.youtube.com/results?search_query=postgresql+triggers+disparadores+jesus+conde",
            "duration": "25 min",
            "desc": "Modelo de 2 pasos en PostgreSQL (función trigger RETURNS TRIGGER + CREATE TRIGGER), eventos DML (INSERT, UPDATE, DELETE), tiempos (BEFORE, AFTER, INSTEAD OF) y variables NEW/OLD."
        },
        "c2_video": {
            "title": "Laboratorio Práctico: Triggers para Control de Stock y Auditoría Automática en PostgreSQL",
            "channel": "PicaCódigo / Informática DP",
            "url": "https://www.youtube.com/results?search_query=postgresql+triggers+stock+auditoria+picacodigo",
            "duration": "35 min",
            "desc": "Creación paso a paso de disparadores para validación de precios, sincronización automática de stock en Kardex y registro de bitácoras de auditoría en tablas transaccionales."
        }
    },
    7: {
        "file": "clases/semana-07-implementacion-avanzada-triggers.md",
        "c1_video": {
            "title": "Triggers Avanzados en PostgreSQL: Cláusula WHEN, Triggers Condicionales y Recursividad",
            "channel": "El Laboratorio de Rafa",
            "url": "https://www.youtube.com/results?search_query=postgresql+triggers+avanzados+when+recursividad",
            "duration": "30 min",
            "desc": "Optimización de disparadores con la cláusula WHEN, prevención de bucles recursivos mediante pg_trigger_depth(), orden de disparo y manejo de reglas de integridad complejas."
        },
        "c2_video": {
            "title": "Triggers Avanzados Combinados con Procedimientos Almacenados y Auditoría en JSONB",
            "channel": "SystemGuards / Fazt Code",
            "url": "https://www.youtube.com/results?search_query=postgresql+triggers+procedimientos+jsonb+auditoria",
            "duration": "40 min",
            "desc": "Taller integrador de automatización: Procedimiento transaccional de facturación combinado con triggers de validación, auditoría diferencial en JSONB y soft delete con vistas editables."
        }
    },
    8: {
        "file": "clases/semana-08-transacciones-concurrencia-seguridad-roles.md",
        "c1_video": {
            "title": "Transacciones ACID, Concurrencia y Niveles de Aislamiento en PostgreSQL",
            "channel": "BettaTech / SystemGuards",
            "url": "https://www.youtube.com/results?search_query=transacciones+acid+concurrencia+mvcc+postgresql",
            "duration": "30 min",
            "desc": "Propiedades ACID, comandos TCL (BEGIN, COMMIT, ROLLBACK, SAVEPOINT), arquitectura MVCC, fenómenos de concurrencia, niveles de aislamiento, bloqueos pesimistas y deadlocks."
        },
        "c2_video": {
            "title": "Seguridad en PostgreSQL: Gestión de Roles, Usuarios, Privilegios y Row-Level Security (RLS)",
            "channel": "PicaCódigo / Jesús Conde",
            "url": "https://www.youtube.com/results?search_query=postgresql+roles+usuarios+permisos+rls+seguridad",
            "duration": "35 min",
            "desc": "Administración de seguridad relacional: roles, usuarios, jerarquías, privilegios granulares (GRANT/REVOKE), esquemas seguros y políticas de seguridad a nivel de fila (RLS)."
        }
    },
    9: {
        "file": "clases/semana-09-repaso-examen-parcial-2-recuperacion.md",
        "c1_video": {
            "title": "Repaso y Síntesis Avanzada de Programación, Transacciones y Seguridad en PostgreSQL",
            "channel": "Fazt Code / TodoCode",
            "url": "https://www.youtube.com/results?search_query=repaso+final+bases+de+datos+avanzadas+postgresql",
            "duration": "30 min",
            "desc": "Síntesis ejecutiva de las Unidades 2 y 3, clínica de dudas de PL/pgSQL, transacciones concurrentes, seguridad RBAC/RLS y criterios de evaluación del Proyecto Integrador (PIS)."
        },
        "c2_video": {
            "title": "Metodología de Resolución de Evaluación Práctica Integral de Bases de Datos en PostgreSQL",
            "channel": "La Geekipedia de Ernesto / PicaCódigo",
            "url": "https://www.youtube.com/results?search_query=evaluacion+final+laboratorio+postgresql+examen",
            "duration": "40 min",
            "desc": "Guía técnica para la resolución del Examen del Segundo Parcial y del Examen de Recuperación Integral en PostgreSQL bajo condiciones de evaluación sumativa."
        }
    }
}

def format_video_markdown(c_num, horas, tipo, vdata):
    return f"""
### 📺 Video Tutorial Recomendado en Español — Clase {c_num} ({horas} — {tipo})

> [!TIP]
> **Video de Apoyo Académico (Español):**  
> 🎬 **[{vdata['title']}]({vdata['url']})**  
> **Canal / Autor:** {vdata['channel']} • **Duración estimada:** ~{vdata['duration']} • **Idioma:** Español  
> **Temas clave explicados:** {vdata['desc']}
"""

def update_markdown_files():
    print("Actualizando archivos markdown con videos para clases de 2h y 3h...")
    for w, data in VIDEOS_DATA.items():
        fpath = data["file"]
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verificar si ya tiene video agregado
        if "Video Tutorial Recomendado en Español" in content:
            print(f"Semana {w}: Ya contiene videos, omitiendo inserción duplicada.")
            continue

        c1_num = (w * 2) - 1
        c2_num = w * 2
        v1_block = format_video_markdown(c1_num, "2 Horas", "ACD / Aula", data["c1_video"])
        v2_block = format_video_markdown(c2_num, "3 Horas", "APECD / Laboratorio", data["c2_video"])

        # Encontrar punto de inserción para Clase 1 (antes de Sección 6)
        # Buscar "## 🛠️ 6." o "## 📝 5." (en semana 9)
        if w == 9:
            s6_pos = content.find("## 📝 5. PARTE II: CLASE 18")
            s7_pos = content.find("## 🏆 7. PARTE III:")
        else:
            s6_pos = content.find("## 🛠️ 6. PARTE II:")
            s7_pos = content.find("## 🚀 7. PARTE III:")
            if s7_pos == -1:
                s7_pos = content.find("## 📦 7. PARTE III:")

        if s6_pos == -1 or s7_pos == -1:
            print(f"Error localizando secciones en Semana {w}")
            continue

        part1 = content[:s6_pos].rstrip() + "\n" + v1_block + "\n---\n\n"
        part2 = content[s6_pos:s7_pos].rstrip() + "\n" + v2_block + "\n---\n\n"
        part3 = content[s7_pos:]

        new_content = part1 + part2 + part3
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Semana {w}: Videos insertados exitosamente en {fpath}")

update_markdown_files()
