/**
 * ===================================================================================
 * 🎓 SCRIPT DE AUTOMATIZACIÓN DE GOOGLE CLASSROOM PARA YAVIRAC
 * Asignatura: Base de Datos Avanzada (DS4AC1-215)
 * Periodo Académico: 2026-II | Paralelo D | Modalidad Dual
 * Instituto Superior Tecnológico de Turismo y Patrimonio Yavirac
 * ===================================================================================
 */

// URL o ID numérico de tu clase en Yavirac:
var ID_O_ENLACE_CLASE_EXISTENTE = "895643328206"; // ID de https://classroom.google.com/u/4/c/ODk1NjQzMzI4MjA2

function poblarClassroom() {
  Logger.log("Iniciando estructuración de la clase en Google Classroom...");
  var courseId = obtenerCursoId();

  if (!courseId) {
    Logger.log("❌ No se pudo identificar el curso. Revisa el ID.");
    return;
  }

  Logger.log("📌 Trabajando sobre el Curso ID: " + courseId);

  // 1. Crear las Unidades Temáticas (Topics)
  Logger.log("Creando unidades temáticas (Topics)...");
  var topicUnidad1 = Classroom.Courses.Topics.create({
    name: "Unidad 1: Sentencias SQL complejas, vistas e índices"
  }, courseId);
  
  var topicUnidad2 = Classroom.Courses.Topics.create({
    name: "Unidad 2: Procedimientos, funciones y triggers"
  }, courseId);
  
  var topicUnidad3 = Classroom.Courses.Topics.create({
    name: "Unidad 3: Transacciones y seguridad"
  }, courseId);

  Logger.log("✅ Unidades creadas: Unidad 1, Unidad 2, Unidad 3.");

  // 2. Definición de Tareas y Talleres con base en el PEA
  var tareas = [
    // --- UNIDAD 1 ---
    {
      topicId: topicUnidad1.topicId,
      title: "Semana 1 — Taller APECD: Modelado Lógico y DDL en PostgreSQL",
      description: "📌 OBJETIVO:\n" +
                   "Transformar modelos conceptuales en esquemas relacionales normalizados hasta 3FN e implementar físicamente en PostgreSQL con sentencias DDL, tablas catálogo y asociaciones polimórficas.\n\n" +
                   "📝 ACTIVIDADES:\n" +
                   "1. Diseñar el diagrama relacional en herramienta CASE (pgModeler / Lucidchart).\n" +
                   "2. Implementar el script DDL con llaves primarias compuestas, foráneas, restricciones CHECK y arcos exclusivos.\n" +
                   "3. Insertar registros semilla de prueba.\n\n" +
                   "📦 ENTREGABLES:\n" +
                   "• Archivo .sql con el script DDL documentado.\n" +
                   "• Diagrama relacional exportado en formato PDF/PNG.\n" +
                   "• Informe técnico con capturas de ejecución exitosa en PostgreSQL.",
      maxPoints: 10
    },
    {
      topicId: topicUnidad1.topicId,
      title: "Semana 2 — Taller APECD: Consultas Complejas, Agregaciones e Ingesta Masiva",
      description: "📌 OBJETIVO:\n" +
                   "Aplicar consultas SQL avanzadas con múltiples JOINs, funciones de agregación, GROUP BY, HAVING, subconsultas y técnicas de carga masiva de datos.\n\n" +
                   "📝 ACTIVIDADES:\n" +
                   "1. Resolver los 10 ejercicios de consultas analíticas sobre el esquema de ventas/académico.\n" +
                   "2. Realizar la carga masiva de al menos 10,000 registros mediante el comando COPY y generate_series().\n" +
                   "3. Comparar tiempos de respuesta de consultas analíticas.\n\n" +
                   "📦 ENTREGABLES:\n" +
                   "• Script SQL con las consultas resueltas y comentadas.\n" +
                   "• Capturas de pantalla de la ingesta masiva y salida de datos.",
      maxPoints: 10
    },
    {
      topicId: topicUnidad1.topicId,
      title: "Semana 3 — Taller APECD: Vistas, Índices y Análisis de Rendimiento (EXPLAIN ANALYZE)",
      description: "📌 OBJETIVO:\n" +
                   "Optimizar el rendimiento de bases de datos mediante el diseño de Vistas estándar/materializadas y la implementación de Índices B-Tree, Hash y GIN.\n\n" +
                   "📝 ACTIVIDADES:\n" +
                   "1. Crear 3 vistas estándar y 1 vista materializada con refresco programado.\n" +
                   "2. Ejecutar EXPLAIN ANALYZE sobre tablas con gran volumen de datos antes de indexar.\n" +
                   "3. Crear índices estratégicos y documentar la reducción del Costo y Tiempo de Ejecución.\n\n" +
                   "📦 ENTREGABLES:\n" +
                   "• Script SQL con la definición de vistas e índices.\n" +
                   "• Tabla comparativa de métricas de rendimiento (Antes vs Después del índice).",
      maxPoints: 10
    },
    {
      topicId: topicUnidad1.topicId,
      title: "Semana 4 — Evaluación Práctica: Primer Parcial (Unidad 1)",
      description: "📌 EVALUACIÓN PRIMER PARCIAL:\n" +
                   "Aplicación práctica individual en laboratorio de cómputo sobre sentencias SQL complejas, normalización DDL, vistas e índices.\n\n" +
                   "⏱️ Duración: 120 minutos en laboratorio.\n" +
                   "📊 Rúbrica: Criterios técnicos de integridad, normalización y optimización.",
      maxPoints: 10
    },

    // --- UNIDAD 2 ---
    {
      topicId: topicUnidad2.topicId,
      title: "Semana 5 — Taller APECD: Procedimientos y Funciones en PL/pgSQL",
      description: "📌 OBJETIVO:\n" +
                   "Desarrollar lógica de negocio en el motor de base de datos implementando funciones escalares, tabulares y procedimientos almacenados con control de flujo.\n\n" +
                   "📝 ACTIVIDADES:\n" +
                   "1. Crear funciones escalares y funciones que retornen TABLE / SETOF RECORD.\n" +
                   "2. Implementar procedimientos almacenados con parámetros IN, OUT, INOUT para operaciones transaccionales.\n" +
                   "3. Gestionar excepciones y validaciones con bloques BEGIN ... EXCEPTION ... END.\n\n" +
                   "📦 ENTREGABLES:\n" +
                   "• Script .sql con el código PL/pgSQL y casos de prueba (CALL / SELECT).",
      maxPoints: 10
    },
    {
      topicId: topicUnidad2.topicId,
      title: "Semana 6 — Taller APECD: Fundamentos y Creación de Triggers",
      description: "📌 OBJETIVO:\n" +
                   "Implementar triggers BEFORE y AFTER a nivel de fila y sentencia para automatización de validaciones y pistas de auditoría.\n\n" +
                   "📝 ACTIVIDADES:\n" +
                   "1. Crear una función disparadora que capture eventos INSERT, UPDATE y DELETE.\n" +
                   "2. Utilizar las variables especiales NEW y OLD para validar reglas de negocio antes de la persistencia.\n" +
                   "3. Registrar cambios en una tabla de auditoría dedicada.\n\n" +
                   "📦 ENTREGABLES:\n" +
                   "• Script SQL con la tabla de auditoría, función trigger y disparador asociado.",
      maxPoints: 10
    },
    {
      topicId: topicUnidad2.topicId,
      title: "Semana 7 — Taller APECD: Triggers Avanzados, Auditoría JSONB y Borrado Lógico",
      description: "📌 OBJETIVO:\n" +
                   "Construir mecanismos avanzados de integridad empresarial con triggers condicionales (WHEN), auditoría histórica en JSONB y gestión de Soft Delete.\n\n" +
                   "📝 ACTIVIDADES:\n" +
                   "1. Implementar disparadores INSTEAD OF sobre vistas complejas.\n" +
                   "2. Crear trigger de Soft Delete que intercepte sentencias DELETE y actualice la columna deleted_at.\n" +
                   "3. Probar el flujo completo simulando transacciones de producción.\n\n" +
                   "📦 ENTREGABLES:\n" +
                   "• Script SQL estructurado y reporte de verificación funcional.",
      maxPoints: 10
    },

    // --- UNIDAD 3 ---
    {
      topicId: topicUnidad3.topicId,
      title: "Semana 8 — Taller APECD: Transacciones ACID, Concurrencia y Seguridad (Roles y Permisos)",
      description: "📌 OBJETIVO:\n" +
                   "Garantizar la consistencia e integridad transaccional mediante ACID y configurar esquemas de seguridad basados en roles (RBAC) y Row Level Security (RLS).\n\n" +
                   "📝 ACTIVIDADES:\n" +
                   "1. Implementar bloques transaccionales con BEGIN, COMMIT, SAVEPOINT y ROLLBACK.\n" +
                   "2. Crear roles de base de datos (administrador, analista, operador) y asignar privilegios mínimos con GRANT/REVOKE.\n" +
                   "3. Habilitar y probar políticas de seguridad a nivel de fila (Row Level Security - RLS).\n\n" +
                   "📦 ENTREGABLES:\n" +
                   "• Script DCL y SQL con pruebas de transaccionalidad y control de accesos.",
      maxPoints: 10
    },
    {
      topicId: topicUnidad3.topicId,
      title: "Semana 9 — Evaluación Práctica: Segundo Parcial y Examen Final",
      description: "📌 EVALUACIÓN SEGUNDO PARCIAL:\n" +
                   "Evaluación práctico-experimental en laboratorio sobre Unidades 2 y 3 (PL/pgSQL, Triggers, Transacciones y Seguridad DCL).\n\n" +
                   "⏱️ Duración: 120 minutos en laboratorio de cómputo.\n" +
                   "📊 Rúbrica: Calidad técnica del código procedural, manejo de excepciones y control transaccional.",
      maxPoints: 10
    }
  ];

  // 3. Crear cada tarea en el curso
  for (var i = 0; i < tareas.length; i++) {
    var t = tareas[i];
    var courseWork = {
      title: t.title,
      description: t.description,
      state: "PUBLISHED",
      maxPoints: t.maxPoints,
      workType: "ASSIGNMENT",
      topicId: t.topicId
    };

    Classroom.Courses.CourseWork.create(courseWork, courseId);
    Logger.log("  -> Tarea creada: " + t.title);
  }

  Logger.log("🎉 ¡ÉXITO TOTAL! Las 3 unidades y las 9 semanas de tareas han sido creadas en tu Classroom.");
}

/**
 * Función auxiliar para obtener el ID numérico del curso
 */
function obtenerCursoId() {
  var raw = ID_O_ENLACE_CLASE_EXISTENTE.trim();

  // Si pegó una URL completa tipo https://classroom.google.com/u/4/c/ODk1NjQzMzI4MjA2
  var match = raw.match(/\/c\/([a-zA-Z0-9_\-]+)/);
  if (match) {
    raw = match[1];
  }

  // Si está codificado en Base64 (las URLs de Classroom codifican el número en base64)
  if (isNaN(raw)) {
    try {
      var decodedBytes = Utilities.base64Decode(raw);
      var decodedStr = Utilities.newBlob(decodedBytes).getDataAsString();
      if (!isNaN(decodedStr)) {
        Logger.log("Decodificado ID Base64 (" + raw + ") a ID numérico: " + decodedStr);
        return decodedStr;
      }
    } catch (e) {
      Logger.log("No fue necesario decodificar Base64: " + e.message);
    }
  }

  return raw;
}

