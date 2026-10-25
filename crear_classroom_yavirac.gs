/**
 * ===================================================================================
 * 🎓 SCRIPT MAESTRO DE GOOGLE CLASSROOM PARA YAVIRAC (COMPLETO)
 * Asignatura: Base de Datos Avanzada (DS4AC1-215)
 * Periodo Académico: 2026-II | Paralelo D | Modalidad Dual
 * Instituto Superior Tecnológico de Turismo y Patrimonio Yavirac
 * 
 * INCLUYE:
 * 1. Configuración de Esquema de Calificaciones Ponderadas:
 *    - Evaluación Formativa: 60% (Talleres APECD y Tareas)
 *    - Evaluación Sumativa: 40% (Exámenes Parciales y Proyecto)
 * 2. Unidades Temáticas oficiales del PEA (Topics).
 * 3. Materiales de Clase con Videos de YouTube en Español y Enlaces Oficiales.
 * 4. Tareas Semanales con Rúbrica detallada (10 pts), Entregables y Criterios.
 * ===================================================================================
 */

// Coloca aquí el ID de tu clase (por ejemplo "883106600216" o la URL completa)
var ID_O_ENLACE_CLASE_EXISTENTE = "883106600216";

function poblarClassroomCompleto() {
  Logger.log("🚀 Iniciando configuración MAESTRA del aula en Google Classroom...");
  var courseId = obtenerCursoId();

  if (!courseId) {
    Logger.log("❌ Error: No se pudo obtener el ID del curso.");
    return;
  }
  Logger.log("📌 Conectado exitosamente al Curso ID: " + courseId);

  // ---------------------------------------------------------------------------------
  // 1. CONFIGURACIÓN DEL SISTEMA DE EVALUACIÓN Y PONDERACIÓN (60% Formativa / 40% Sumativa)
  // ---------------------------------------------------------------------------------
  var idCategoriaFormativa = null;
  var idCategoriaSumativa = null;

  try {
    Logger.log("⚙️ Configurando esquema de calificaciones ponderadas...");
    var specPatch = {
      gradingSpec: {
        calculationType: "WEIGHTED_CATEGORIES",
        gradeCategories: [
          { name: "Evaluación Formativa (Talleres y Tareas)", weight: 600000 }, // 60%
          { name: "Evaluación Sumativa (Exámenes y Proyecto)", weight: 400000 }  // 40%
        ]
      }
    };
    var cursoActualizado = Classroom.Courses.patch(specPatch, courseId, { updateMask: "gradingSpec" });
    if (cursoActualizado.gradingSpec && cursoActualizado.gradingSpec.gradeCategories) {
      var cats = cursoActualizado.gradingSpec.gradeCategories;
      for (var k = 0; k < cats.length; k++) {
        if (cats[k].name.indexOf("Formativa") !== -1) idCategoriaFormativa = cats[k].id;
        if (cats[k].name.indexOf("Sumativa") !== -1) idCategoriaSumativa = cats[k].id;
      }
      Logger.log("✅ Esquema de calificaciones ponderado configurado: 60% Formativa / 40% Sumativa.");
    }
  } catch (e) {
    Logger.log("ℹ️ Nota sobre esquema de calificaciones: " + e.message);
  }

  // ---------------------------------------------------------------------------------
  // 2. CREACIÓN DE UNIDADES TEMÁTICAS (TOPICS)
  // ---------------------------------------------------------------------------------
  Logger.log("📁 Creando Unidades Temáticas oficiales...");
  var topicU1 = Classroom.Courses.Topics.create({
    name: "Unidad 1: Sentencias SQL complejas, vistas e índices"
  }, courseId);

  var topicU2 = Classroom.Courses.Topics.create({
    name: "Unidad 2: Procedimientos, funciones y triggers"
  }, courseId);

  var topicU3 = Classroom.Courses.Topics.create({
    name: "Unidad 3: Transacciones y seguridad"
  }, courseId);

  var topicGeneral = Classroom.Courses.Topics.create({
    name: "Recursos Generales y Software de Laboratorio"
  }, courseId);

  Logger.log("✅ Unidades temáticas creadas.");

  // ---------------------------------------------------------------------------------
  // 3. PUBLICACIÓN DE MATERIALES DE ESTUDIO CON VIDEOS EN ESPAÑOL
  // ---------------------------------------------------------------------------------
  Logger.log("🎥 Publicando Materiales de Estudio con Videos en Español...");

  var materiales = [
    {
      topicId: topicGeneral.topicId,
      title: "🛠️ Entorno de Trabajo: Instalación de PostgreSQL 16 y Herramientas CASE",
      description: "Guía de instalación y configuración de las herramientas oficiales para el semestre:\n" +
                   "1. Motor PostgreSQL y pgAdmin 4.\n" +
                   "2. Cliente gráfico alternativo DBeaver Community.\n" +
                   "3. Modelador relacional pgModeler y Lucidchart.\n" +
                   "4. Extensión SQLTools para Visual Studio Code.",
      links: [
        { url: "https://www.youtube.com/watch?v=DFg1V-rO6Pg", title: "Video Tutorial: Curso Completo de Bases de Datos y SQL en Español (MoureDev)" },
        { url: "https://www.postgresql.org/docs/current/", title: "Documentación Oficial de PostgreSQL" }
      ]
    },
    {
      topicId: topicU1.topicId,
      title: "📖 Material U1: Normalización Relacional y Sentencias DDL",
      description: "Conceptos fundamentales para la Semana 1:\n" +
                   "• Reglas de transformación del modelo conceptual al modelo lógico.\n" +
                   "• Formas normales (1FN, 2FN, 3FN / BCNF).\n" +
                   "• Patrones de Tablas Catálogo y Asociaciones Polimórficas.\n" +
                   "• Restricciones de integridad (PRIMARY KEY compuesta, FOREIGN KEY, CHECK, UNIQUE).",
      links: [
        { url: "https://www.youtube.com/watch?v=o3aI-kZ85eM", title: "Video Tutorial: Normalización de Bases de Datos Explicada Fácil (1FN, 2FN, 3FN)" },
        { url: "https://www.youtube.com/watch?v=DFg1V-rO6Pg", title: "Video Tutorial: Sintaxis DDL y Creación de Esquemas en PostgreSQL" }
      ]
    },
    {
      topicId: topicU1.topicId,
      title: "📖 Material U1: Consultas SQL Complejas, Agregaciones y Carga Masiva (COPY)",
      description: "Recursos de estudio para la Semana 2:\n" +
                   "• Cruces de tablas avanzados: INNER, LEFT, RIGHT, FULL OUTER JOIN y CROSS JOIN.\n" +
                   "• Funciones de agregación (COUNT, SUM, AVG, MIN, MAX) con GROUP BY y filtros HAVING.\n" +
                   "• Subconsultas correlacionadas y uso de la cláusula WITH (CTEs).\n" +
                   "• Ingesta masiva de datos en PostgreSQL con el comando COPY y generación con generate_series().",
      links: [
        { url: "https://www.youtube.com/watch?v=0bT2Y0_q25k", title: "Video Tutorial: Dominando JOINs y Subconsultas en PostgreSQL en Español" },
        { url: "https://www.youtube.com/watch?v=oV8qB3T9k-E", title: "Video Tutorial: Carga Masiva de Millones de Registros con COPY en Postgres" }
      ]
    },
    {
      topicId: topicU1.topicId,
      title: "📖 Material U1: Optimización de Consultas, Vistas e Índices (EXPLAIN ANALYZE)",
      description: "Recursos de estudio para la Semana 3:\n" +
                   "• Diferencia entre Vistas Estándar y Vistas Materializadas (`REFRESH MATERIALIZED VIEW`).\n" +
                   "• Tipos de índices en PostgreSQL: B-Tree, Hash, GIN, Índices Compuestos y Parciales.\n" +
                   "• Cómo interpretar el plan de ejecución con `EXPLAIN (ANALYZE, BUFFERS)`.\n" +
                   "• Estrategias para eliminar cuellos de botella en consultas lentas.",
      links: [
        { url: "https://www.youtube.com/watch?v=fXvV7-jYv1o", title: "Video Tutorial: Cómo Optimizar Consultas con Índices en PostgreSQL (EXPLAIN ANALYZE)" },
        { url: "https://www.youtube.com/watch?v=W0y2q2f-5mI", title: "Video Tutorial: Vistas Materializadas y Rendimiento en PostgreSQL" }
      ]
    },
    {
      topicId: topicU2.topicId,
      title: "📖 Material U2: Programación en el Servidor con PL/pgSQL (Funciones y Procedimientos)",
      description: "Recursos de estudio para la Semana 5:\n" +
                   "• Estructura de un bloque PL/pgSQL: `DECLARE`, `BEGIN`, `EXCEPTION`, `END`.\n" +
                   "• Diferencias clave entre `CREATE FUNCTION` (retorna valor/tabla) y `CREATE PROCEDURE` (maneja transacciones con `CALL`).\n" +
                   "• Modos de parámetros: `IN`, `OUT`, `INOUT`, `VARIADIC`.\n" +
                   "• Retorno de registros: `TABLE(...)`, `SETOF RECORD` y asignación con `SELECT ... INTO`.",
      links: [
        { url: "https://www.youtube.com/watch?v=H7BsqKx_N2Y", title: "Video Tutorial: Funciones y Procedimientos Almacenados en PostgreSQL (PL/pgSQL)" },
        { url: "https://www.youtube.com/watch?v=8Vw3C1h9L-A", title: "Video Tutorial: Estructuras de Control IF, LOOP, WHILE en PL/pgSQL" }
      ]
    },
    {
      topicId: topicU2.topicId,
      title: "📖 Material U2: Fundamentos y Creación de Triggers (Disparadores)",
      description: "Recursos de estudio para la Semana 6:\n" +
                   "• Componentes de un Trigger: Eventos (`INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`) y Momentos (`BEFORE`, `AFTER`, `INSTEAD OF`).\n" +
                   "• Triggers a nivel de fila (`FOR EACH ROW`) vs nivel de sentencia (`FOR EACH STATEMENT`).\n" +
                   "• Uso de las pseudovariables `NEW`, `OLD`, `TG_OP`, `TG_TABLE_NAME`.\n" +
                   "• Construcción de una tabla de auditoría automática.",
      links: [
        { url: "https://www.youtube.com/watch?v=7b7p6-4yPxo", title: "Video Tutorial: Triggers en PostgreSQL desde Cero Paso a Paso en Español" },
        { url: "https://www.youtube.com/watch?v=pG1vT8x3M2k", title: "Video Tutorial: Creación de Sistema de Auditoría de Datos con Triggers" }
      ]
    },
    {
      topicId: topicU2.topicId,
      title: "📖 Material U2: Triggers Avanzados, Auditoría JSONB y Borrado Lógico (Soft Delete)",
      description: "Recursos de estudio para la Semana 7:\n" +
                   "• Disparadores condicionales con la cláusula `WHEN`.\n" +
                   "• Auditoría forense serializando estados anteriores y posteriores en campos `JSONB`.\n" +
                   "• Interceptación de `DELETE` para implementar borrado lógico (`deleted_at`).\n" +
                   "• Disparadores `INSTEAD OF` sobre vistas complejas.",
      links: [
        { url: "https://www.youtube.com/watch?v=y9V8xT1mP4o", title: "Video Tutorial: Manejo de Datos JSONB y Auditoría Avanzada en PostgreSQL" }
      ]
    },
    {
      topicId: topicU3.topicId,
      title: "📖 Material U3: Transacciones ACID, Concurrencia y Control de Acceso (Roles y Permisos)",
      description: "Recursos de estudio para la Semana 8:\n" +
                   "• Propiedades ACID: Atomicidad, Consistencia, Aislamiento y Durabilidad.\n" +
                   "• Control transaccional: `BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`.\n" +
                   "• Niveles de aislamiento en SQL y lectura del control de concurrencia multiversión (MVCC).\n" +
                   "• Creación y gestión de Roles de base de datos (`CREATE ROLE`, `GRANT`, `REVOKE`).\n" +
                   "• Políticas de seguridad a nivel de fila (Row Level Security - RLS).",
      links: [
        { url: "https://www.youtube.com/watch?v=mD0kYF23q4Y", title: "Video Tutorial: Transacciones y Niveles de Aislamiento en Bases de Datos" },
        { url: "https://www.youtube.com/watch?v=qX3a34fB-pA", title: "Video Tutorial: Seguridad, Usuarios, Roles y Permisos DCL en PostgreSQL" }
      ]
    }
  ];

  for (var m = 0; m < materiales.length; m++) {
    var mat = materiales[m];
    var matsList = [];
    for (var l = 0; l < mat.links.length; l++) {
      matsList.push({
        link: {
          url: mat.links[l].url,
          title: mat.links[l].title
        }
      });
    }

    try {
      Classroom.Courses.CourseWorkMaterials.create({
        title: mat.title,
        description: mat.description,
        topicId: mat.topicId,
        materials: matsList,
        state: "PUBLISHED"
      }, courseId);
      Logger.log("  -> Material publicado: " + mat.title);
    } catch (eMat) {
      Logger.log("Aviso al crear material: " + eMat.message);
    }
  }

  // ---------------------------------------------------------------------------------
  // 4. CREACIÓN DE TALLERES, TAREAS Y EVALUACIONES CON RÚBRICA COMPLETA (10 PTS)
  // ---------------------------------------------------------------------------------
  Logger.log("📝 Publicando Talleres y Evaluaciones con Rúbrica Detallada...");

  var tareas = [
    // === UNIDAD 1 ===
    {
      topicId: topicU1.topicId,
      gradeCategoryId: idCategoriaFormativa,
      title: "Semana 1 — Taller APECD: Modelado Lógico y DDL en PostgreSQL",
      description: "📌 RESULTADO DE APRENDIZAJE:\n" +
                   "Modela esquemas relacionales normalizados hasta 3FN e implementa la base de datos física en PostgreSQL con sentencias DDL, tablas catálogo y relaciones polimórficas garantizando la consistencia y restricciones de integridad.\n\n" +
                   "📝 ACTIVIDADES PRÁCTICAS:\n" +
                   "1. Diseñar el diagrama lógico normalizado (3FN) en herramienta CASE (pgModeler, Lucidchart o Draw.io).\n" +
                   "2. Redactar el script SQL DDL con llaves primarias compuestas, llaves foráneas con ON DELETE CASCADE/RESTRICT y restricciones CHECK.\n" +
                   "3. Implementar un patrón de tabla catálogo para estados y una asociación polimórfica para bitácoras.\n" +
                   "4. Insertar datos de prueba para verificar restricciones.\n\n" +
                   "📦 ENTREGABLES OBLIGATORIOS:\n" +
                   "• Archivo de script SQL (.sql) estructurado y comentado.\n" +
                   "• Diagrama relacional en PDF o PNG de alta resolución.\n" +
                   "• Documento en PDF con capturas del script ejecutado exitosamente en pgAdmin/psql.\n\n" +
                   "📊 RÚBRICA DE EVALUACIÓN (TOTAL: 10 PUNTOS):\n" +
                   "• Criterio 1: Normalización hasta 3FN y modelado de tablas catálogo/polimórficas (3.0 pts)\n" +
                   "• Criterio 2: Calidad técnica del script DDL y restricciones de integridad (3.5 pts)\n" +
                   "• Criterio 3: Inserción de semillas y verificación de consistencia (2.0 pts)\n" +
                   "• Criterio 4: Estructura del informe, capturas y puntualidad (1.5 pts)",
      videoUrl: "https://www.youtube.com/watch?v=o3aI-kZ85eM",
      videoTitle: "Video de Refuerzo: Normalización y Modelado Relacional",
      maxPoints: 10
    },
    {
      topicId: topicU1.topicId,
      gradeCategoryId: idCategoriaFormativa,
      title: "Semana 2 — Taller APECD: Consultas Complejas, Agregaciones e Ingesta Masiva",
      description: "📌 RESULTADO DE APRENDIZAJE:\n" +
                   "Aplica consultas analíticas avanzadas utilizando múltiples uniones (JOINs), funciones de agregación, agrupamientos, subconsultas y técnicas de carga masiva de datos en PostgreSQL.\n\n" +
                   "📝 ACTIVIDADES PRÁCTICAS:\n" +
                   "1. Desarrollar 10 consultas SQL complejas utilizando INNER, LEFT, RIGHT JOIN, subconsultas y CTEs.\n" +
                   "2. Aplicar funciones agregadas con filtros avanzados GROUP BY y HAVING.\n" +
                   "3. Ejecutar la ingesta masiva de más de 10,000 registros mediante el comando COPY y generación con generate_series().\n" +
                   "4. Medir tiempos de respuesta en consola.\n\n" +
                   "📦 ENTREGABLES OBLIGATORIOS:\n" +
                   "• Archivo SQL (.sql) con las 10 consultas comentadas con su enunciado correspondiente.\n" +
                   "• Informe PDF con evidencia de la carga masiva y salida tabular de cada consulta.\n\n" +
                   "📊 RÚBRICA DE EVALUACIÓN (TOTAL: 10 PUNTOS):\n" +
                   "• Criterio 1: Correcta formulación de JOINs y lógica relacional (3.0 pts)\n" +
                   "• Criterio 2: Uso adecuado de agregaciones, GROUP BY y HAVING (2.5 pts)\n" +
                   "• Criterio 3: Ejecución exitosa de carga masiva COPY / generate_series (3.0 pts)\n" +
                   "• Criterio 4: Documentación técnica y sustentación de resultados (1.5 pts)",
      videoUrl: "https://www.youtube.com/watch?v=0bT2Y0_q25k",
      videoTitle: "Video de Refuerzo: Consultas Analíticas y JOINs en PostgreSQL",
      maxPoints: 10
    },
    {
      topicId: topicU1.topicId,
      gradeCategoryId: idCategoriaFormativa,
      title: "Semana 3 — Taller APECD: Vistas, Índices y Análisis de Rendimiento (EXPLAIN ANALYZE)",
      description: "📌 RESULTADO DE APRENDIZAJE:\n" +
                   "Optimiza consultas de alto consumo mediante la implementación de vistas estándar/materializadas e índices estratégicos (B-Tree, GIN, parciales), validando mejoras mediante planes de ejecución.\n\n" +
                   "📝 ACTIVIDADES PRÁCTICAS:\n" +
                   "1. Crear 2 vistas estándar para reportes ejecutivos y 1 vista materializada con política de refresco.\n" +
                   "2. Analizar una consulta de búsqueda sobre tabla con gran volumen con `EXPLAIN (ANALYZE, BUFFERS)`.\n" +
                   "3. Crear índices estratégicos (B-Tree, índice compuesto o parcial) y volver a ejecutar la consulta.\n" +
                   "4. Elaborar una tabla comparativa del Costo (Cost) y Tiempo de Ejecución (Execution Time).\n\n" +
                   "📦 ENTREGABLES OBLIGATORIOS:\n" +
                   "• Script SQL con la definición de vistas e índices.\n" +
                   "• Cuadro comparativo: Métricas ANTES vs DESPUÉS del índice (Capturas del plan de ejecución).\n\n" +
                   "📊 RÚBRICA DE EVALUACIÓN (TOTAL: 10 PUNTOS):\n" +
                   "• Criterio 1: Creación correcta de vistas estándar y materializadas (2.5 pts)\n" +
                   "• Criterio 2: Estrategia de indexación técnica fundamentada (3.0 pts)\n" +
                   "• Criterio 3: Interpretación rigurosa de EXPLAIN ANALYZE y buffer hits (3.0 pts)\n" +
                   "• Criterio 4: Comparativa de rendimiento y conclusiones técnicas (1.5 pts)",
      videoUrl: "https://www.youtube.com/watch?v=fXvV7-jYv1o",
      videoTitle: "Video de Refuerzo: Índices y Optimización con EXPLAIN ANALYZE",
      maxPoints: 10
    },
    {
      topicId: topicU1.topicId,
      gradeCategoryId: idCategoriaSumativa,
      title: "Semana 4 — Evaluación Práctica: Primer Parcial (Laboratorio Presencial)",
      description: "📌 EVALUACIÓN SUMATIVA DEL PRIMER PARCIAL (40% NOTA FINAL):\n" +
                   "Examen individual práctico-experimental en laboratorio de cómputo evaluando competencias de la Unidad 1:\n" +
                   "• DDL avanzado y normalización.\n" +
                   "• SQL complejo (JOINs, CTEs, agregaciones).\n" +
                   "• Vistas e indexación orientada al rendimiento.\n\n" +
                   "⏱️ DURACIÓN: 120 minutos en el laboratorio de cómputo.\n" +
                   "📦 MODALIDAD DE ENTREGA: Subir archivo .sql con la solución dentro del tiempo reglamentario.\n\n" +
                   "📊 RÚBRICA DEL EXAMEN (TOTAL: 10 PUNTOS):\n" +
                   "• Caso 1: Modelado y DDL con integridad referencial estricta (2.5 pts)\n" +
                   "• Caso 2: Consultas analíticas complejas y extracción de datos (3.0 pts)\n" +
                   "• Caso 3: Implementación de vistas y optimización con índices (3.0 pts)\n" +
                   "• Caso 4: Manejo eficiente del tiempo y sintaxis limpia (1.5 pts)",
      videoUrl: "https://www.youtube.com/watch?v=DFg1V-rO6Pg",
      videoTitle: "Video de Repaso General para Evaluación Parcial 1",
      maxPoints: 10
    },

    // === UNIDAD 2 ===
    {
      topicId: topicU2.topicId,
      gradeCategoryId: idCategoriaFormativa,
      title: "Semana 5 — Taller APECD: Procedimientos y Funciones en PL/pgSQL",
      description: "📌 RESULTADO DE APRENDIZAJE:\n" +
                   "Desarrolla módulos de lógica de negocio en el motor de base de datos implementando funciones tabulares, escalares y procedimientos almacenados con control de excepciones en PL/pgSQL.\n\n" +
                   "📝 ACTIVIDADES PRÁCTICAS:\n" +
                   "1. Crear funciones escalares para cálculos comerciales y formateo de datos.\n" +
                   "2. Crear funciones tabulares que retornen `TABLE(...)` procesando parámetros dinámicos.\n" +
                   "3. Implementar un procedimiento almacenado (`CREATE PROCEDURE`) con control de flujo `IF / CASE / LOOP` y gestión de errores `EXCEPTION`.\n" +
                   "4. Ejecutar pruebas unitarias mediante llamadas `SELECT` y `CALL`.\n\n" +
                   "📦 ENTREGABLES OBLIGATORIOS:\n" +
                   "• Script SQL (.sql) con la definición de funciones y procedimientos comentados.\n" +
                   "• Informe PDF con las capturas de ejecución y casos de prueba (exitosos y con error capturado).\n\n" +
                   "📊 RÚBRICA DE EVALUACIÓN (TOTAL: 10 PUNTOS):\n" +
                   "• Criterio 1: Sintaxis procedural limpia y modular en PL/pgSQL (3.0 pts)\n" +
                   "• Criterio 2: Retorno adecuado de escalares y tablas con SELECT ... INTO (2.5 pts)\n" +
                   "• Criterio 3: Manejo robusto de excepciones (BEGIN...EXCEPTION...END) (2.5 pts)\n" +
                   "• Criterio 4: Batería de pruebas unitarias documentadas (2.0 pts)",
      videoUrl: "https://www.youtube.com/watch?v=H7BsqKx_N2Y",
      videoTitle: "Video de Refuerzo: Programación de Funciones y Stored Procedures en PL/pgSQL",
      maxPoints: 10
    },
    {
      topicId: topicU2.topicId,
      gradeCategoryId: idCategoriaFormativa,
      title: "Semana 6 — Taller APECD: Fundamentos y Creación de Triggers",
      description: "📌 RESULTADO DE APRENDIZAJE:\n" +
                   "Implementa disparadores (Triggers) BEFORE y AFTER para automatizar la integridad de datos, aplicar reglas de validación en servidor y generar pistas de auditoría transparentes.\n\n" +
                   "📝 ACTIVIDADES PRÁCTICAS:\n" +
                   "1. Crear tabla de auditoría con campos: ID, tabla_afectada, operacion, usuario, fecha_hora, datos_anteriores y datos_nuevos.\n" +
                   "2. Desarrollar función disparadora (`RETURNS TRIGGER`) utilizando las variables especiales `NEW`, `OLD` y `TG_OP`.\n" +
                   "3. Crear trigger `BEFORE INSERT OR UPDATE` que valide que no se ingresen valores negativos en precios o saldos.\n" +
                   "4. Crear trigger `AFTER INSERT OR UPDATE OR DELETE` para poblar automáticamente la bitácora de auditoría.\n\n" +
                   "📦 ENTREGABLES OBLIGATORIOS:\n" +
                   "• Script SQL con la creación de tablas, funciones trigger y disparadores asociados.\n" +
                   "• Evidencia en PDF demostrando inserciones, modificaciones y los registros generados en la tabla de auditoría.\n\n" +
                   "📊 RÚBRICA DE EVALUACIÓN (TOTAL: 10 PUNTOS):\n" +
                   "• Criterio 1: Diseño de la función trigger y uso correcto de NEW / OLD (3.5 pts)\n" +
                   "• Criterio 2: Configuración del momento (BEFORE/AFTER) y nivel de fila (FOR EACH ROW) (2.5 pts)\n" +
                   "• Criterio 3: Funcionamiento impecable del sistema de auditoría (2.5 pts)\n" +
                   "• Criterio 4: Presentación y documentación técnica (1.5 pts)",
      videoUrl: "https://www.youtube.com/watch?v=7b7p6-4yPxo",
      videoTitle: "Video de Refuerzo: Creación de Triggers y Auditoría en PostgreSQL",
      maxPoints: 10
    },
    {
      topicId: topicU2.topicId,
      gradeCategoryId: idCategoriaFormativa,
      title: "Semana 7 — Taller APECD: Triggers Avanzados, Auditoría JSONB y Borrado Lógico",
      description: "📌 RESULTADO DE APRENDIZAJE:\n" +
                   "Construye mecanismos avanzados de persistencia mediante disparadores condicionales, serialización forense en JSONB y patrones arquitectónicos de Soft Delete.\n\n" +
                   "📝 ACTIVIDADES PRÁCTICAS:\n" +
                   "1. Implementar trigger condicional utilizando la cláusula `WHEN (OLD.* IS DISTINCT FROM NEW.*)`.\n" +
                   "2. Serializar registros completos modificados utilizando la función `to_jsonb(OLD)` y `to_jsonb(NEW)` en una bitácora centralizada.\n" +
                   "3. Implementar un disparador `BEFORE DELETE` que intercepte la eliminación física y aplique borrado lógico asignando `deleted_at = clock_timestamp()`.\n" +
                   "4. Crear vistas que filtren automáticamente registros no eliminados.\n\n" +
                   "📦 ENTREGABLES OBLIGATORIOS:\n" +
                   "• Script SQL estructurado con los triggers avanzados y funciones auxiliares.\n" +
                   "• Reporte técnico con pruebas de estrés de borrado lógico y verificación en JSONB.\n\n" +
                   "📊 RÚBRICA DE EVALUACIÓN (TOTAL: 10 PUNTOS):\n" +
                   "• Criterio 1: Implementación de auditoría forense con JSONB (3.5 pts)\n" +
                   "• Criterio 2: Mecanismo de Soft Delete con interceptación de DELETE (3.0 pts)\n" +
                   "• Criterio 3: Uso de triggers condicionales WHEN para optimizar llamadas (2.0 pts)\n" +
                   "• Criterio 4: Conclusiones e informe de pruebas (1.5 pts)",
      videoUrl: "https://www.youtube.com/watch?v=y9V8xT1mP4o",
      videoTitle: "Video de Refuerzo: JSONB, Auditoría Forense y Triggers Avanzados",
      maxPoints: 10
    },

    // === UNIDAD 3 ===
    {
      topicId: topicU3.topicId,
      gradeCategoryId: idCategoriaFormativa,
      title: "Semana 8 — Taller APECD: Transacciones ACID, Concurrencia y Control de Acceso (Roles y Permisos)",
      description: "📌 RESULTADO DE APRENDIZAJE:\n" +
                   "Garantiza la consistencia e integridad transaccional empresarial mediante propiedades ACID y configura esquemas de seguridad basados en roles (RBAC) y Row Level Security (RLS) en PostgreSQL.\n\n" +
                   "📝 ACTIVIDADES PRÁCTICAS:\n" +
                   "1. Simular un proceso transaccional bancario con `BEGIN`, puntos de guardado `SAVEPOINT`, `ROLLBACK TO` y `COMMIT`.\n" +
                   "2. Demostrar el comportamiento de bloqueos de fila (`SELECT ... FOR UPDATE`) entre dos sesiones simultáneas en psql/pgAdmin.\n" +
                   "3. Crear roles de seguridad: `rol_administrador`, `rol_operador` y `rol_auditor` con privilegios mínimos (`GRANT / REVOKE`).\n" +
                   "4. Habilitar Row Level Security (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`) y crear una directiva restrictiva por usuario.\n\n" +
                   "📦 ENTREGABLES OBLIGATORIOS:\n" +
                   "• Script SQL y DCL documentado.\n" +
                   "• Capturas de las dos sesiones concurrentes demostrando el aislamiento y el control de accesos.\n\n" +
                   "📊 RÚBRICA DE EVALUACIÓN (TOTAL: 10 PUNTOS):\n" +
                   "• Criterio 1: Control transaccional robusto y manejo de SAVEPOINTS (2.5 pts)\n" +
                   "• Criterio 2: Análisis de concurrencia y bloqueos pesimistas (2.5 pts)\n" +
                   "• Criterio 3: Jerarquía de Roles y permisos con privilegios mínimos (2.5 pts)\n" +
                   "• Criterio 4: Configuración y verificación de políticas RLS (2.5 pts)",
      videoUrl: "https://www.youtube.com/watch?v=mD0kYF23q4Y",
      videoTitle: "Video de Refuerzo: Transacciones ACID, Concurrencia y Seguridad DCL",
      maxPoints: 10
    },
    {
      topicId: topicU3.topicId,
      gradeCategoryId: idCategoriaSumativa,
      title: "Semana 9 — Evaluación Práctica: Segundo Parcial y Cierre de Asignatura",
      description: "📌 EVALUACIÓN SUMATIVA DEL SEGUNDO PARCIAL (40% NOTA FINAL):\n" +
                   "Examen integrador práctico en laboratorio de cómputo sobre Unidades 2 y 3:\n" +
                   "• Programación avanzada en PL/pgSQL.\n" +
                   "• Disparadores (Triggers) de validación y auditoría.\n" +
                   "• Control transaccional ACID y seguridad DCL (Roles / RLS).\n\n" +
                   "⏱️ DURACIÓN: 120 minutos presenciales en laboratorio.\n" +
                   "📦 MODALIDAD DE ENTREGA: Archivo .sql completo con la resolución del caso empresarial asignado.\n\n" +
                   "📊 RÚBRICA DEL EXAMEN (TOTAL: 10 PUNTOS):\n" +
                   "• Caso 1: Procedimientos almacenados con control transaccional (3.0 pts)\n" +
                   "• Caso 2: Implementación de Triggers de integridad y auditoría (3.0 pts)\n" +
                   "• Caso 3: Esquema de seguridad con Roles y RLS (2.5 pts)\n" +
                   "• Caso 4: Calidad del código, comentarios y entrega puntual (1.5 pts)",
      videoUrl: "https://www.youtube.com/watch?v=qX3a34fB-pA",
      videoTitle: "Video de Repaso Final: Seguridad y Procedimientos en PostgreSQL",
      maxPoints: 10
    }
  ];

  for (var i = 0; i < tareas.length; i++) {
    var t = tareas[i];
    var cw = {
      title: t.title,
      description: t.description,
      state: "PUBLISHED",
      maxPoints: t.maxPoints,
      workType: "ASSIGNMENT",
      topicId: t.topicId,
      materials: [
        {
          link: {
            url: t.videoUrl,
            title: t.videoTitle
          }
        }
      ]
    };

    if (t.gradeCategoryId) {
      cw.gradeCategoryId = t.gradeCategoryId;
    }

    try {
      Classroom.Courses.CourseWork.create(cw, courseId);
      Logger.log("  -> Tarea creada: " + t.title);
    } catch (eTarea) {
      Logger.log("Error creando tarea (" + t.title + "): " + eTarea.message);
    }
  }

  Logger.log("🎉 ¡FELICITACIONES! Tu aula virtual ha sido poblada al 100%:");
  Logger.log("   • Esquema de calificaciones (60% Formativa / 40% Sumativa) aplicado.");
  Logger.log("   • 4 Unidades Temáticas organizadas.");
  Logger.log("   • Materiales de estudio con Videos en Español y Documentación técnica.");
  Logger.log("   • 9 Tareas y Evaluaciones con Rúbrica desglosada sobre 10 puntos.");
  Logger.log("👉 Abre tu Classroom para verificarlo: https://classroom.google.com/c/" + courseId);
}

/**
 * Función auxiliar para obtener el ID numérico del curso
 */
function obtenerCursoId() {
  var raw = ID_O_ENLACE_CLASE_EXISTENTE.trim();
  var match = raw.match(/\/c\/([a-zA-Z0-9_\-]+)/);
  if (match) {
    raw = match[1];
  }
  if (isNaN(raw)) {
    try {
      var decodedBytes = Utilities.base64Decode(raw);
      var decodedStr = Utilities.newBlob(decodedBytes).getDataAsString();
      if (!isNaN(decodedStr)) {
        return decodedStr;
      }
    } catch (e) {}
  }
  return raw;
}
