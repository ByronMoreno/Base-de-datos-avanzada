# ⚙️ Semana 05: Programación en el Servidor con Funciones y Procedimientos Almacenados en PL/pgSQL

---

## 📋 1. Portada y Ficha Técnica de la Sesión

| Campo | Detalle Oficial |
| :--- | :--- |
| **Institución** | Instituto Superior Tecnológico de Turismo y Patrimonio Yavirac |
| **Carrera** | Tecnología Superior en Desarrollo de Software |
| **Asignatura** | Base de Datos Avanzada |
| **Código de Asignatura** | `DS4AC1-215` |
| **Semestre / Periodo** | Segundo Semestre / 2026-II |
| **Modalidad** | Dual |
| **Unidad Didáctica** | Unidad 2: Generación de procedimientos, funciones y triggers |
| **Semana** | Semana 05 de 16 |
| **Carga Horaria Semanal** | **ACD:** 1 hora \| **APECD:** 4 horas \| **Total:** 5 horas |
| **Contenidos (PEA)** | Funciones, procedimientos almacenados; Crea, modifica y elimina función y procedimiento (`PL/pgSQL`, argumentos, tipos de retorno, `RECORD`, `SELECT ... INTO`) |
| **Resultado de Aprendizaje (RdA 2)** | Desarrollo de procedimientos almacenados, funciones o triggers. |
| **Software y Herramientas** | PostgreSQL 16+, pgAdmin 4 / DBeaver, Extensión `plpgsql` (nativa), Git |

---

## 🎯 2. Objetivos de Aprendizaje, Competencias, Evidencias y Habilidades Blandas

### 2.1 Objetivos de la Sesión
1. **Diferenciar arquitectónicamente** las **Funciones (`FUNCTION`)** de los **Procedimientos Almacenados (`PROCEDURE`)** en PostgreSQL, comprendiendo su invocación (`SELECT` vs `CALL`), su capacidad de retorno y el control de transacciones (`COMMIT`/`ROLLBACK`).
2. **Dominar la sintaxis y semántica del lenguaje procedural `PL/pgSQL`**, incluyendo bloques estructurados, declaración de variables escalares, `%TYPE`, `%ROWTYPE` y `RECORD`, asignación con `SELECT ... INTO` (`STRICT` y `FOUND`), estructuras condicionales, bucles y manejo de excepciones (`RAISE`).
3. **Diseñar, crear, modificar y eliminar** funciones escalares, funciones tabulares (`RETURNS TABLE` / `RETURNS SETOF`) y procedimientos transaccionales complejos en un taller práctico de 4 horas.

### 2.2 Matriz de Competencias y Evidencias

| Componente | Descripción Aplicada a la Semana 05 |
| :--- | :--- |
| **Resultado de Aprendizaje (RdA 2)** | Desarrollo de procedimientos almacenados, funciones o triggers para encapsular reglas de negocio críticas dentro del motor de base de datos. |
| **Competencia Específica** | Implementa rutinas modulares en `PL/pgSQL` utilizando modos de parámetros (`IN`, `OUT`, `INOUT`, `VARIADIC`), tipos compuestos (`RECORD`), captura de estado (`SELECT INTO`) y manejo robusto de errores (`EXCEPTION`). |
| **Evidencia de Aprendizaje** | Script de laboratorio `semana05_plpgsql_rutinas.sql` con 6 funciones y procedimientos almacenados probados y documentados. |
| **Habilidades Blandas (PEA)** | **Aprendizaje autónomo:** Realiza ejercicios extras de Funciones y Triggers de forma autónoma; pensamiento algorítmico estructurado y depuración metódica mediante trazas (`RAISE NOTICE`). |

---

## ⏱️ 3. Agenda Detallada de la Sesión (5 Horas)

| Fase | Tiempo | Componente | Actividad Pedagógica |
| :--- | :---: | :---: | :--- |
| **Fase 1** | `00:00 - 00:30` (30 min) | **ACD** | **Fundamentos de Rutinas en PostgreSQL:** `FUNCTION` vs `PROCEDURE`, modos de argumentos (`IN`, `OUT`, `INOUT`, `VARIADIC`) y tipos de retorno (`SCALAR`, `RECORD`, `TABLE`, `SETOF`, `VOID`). |
| **Fase 2** | `00:30 - 01:00` (30 min) | **ACD** | **Anatomía del Lenguaje `PL/pgSQL`:** Estructura de bloques, variables `RECORD`/`%ROWTYPE`, `SELECT ... INTO` (`STRICT`/`FOUND`), control de flujo (`IF`, `CASE`, `FOR`), `RAISE` y ciclo de vida (`CREATE OR REPLACE`, `DROP`). |
| **Fase 3** | `01:00 - 01:45` (45 min) | **APECD** | **Práctica Guiada:** Despliegue del esquema FinTech/Cooperativa y creación paso a paso de nuestras primeras funciones escalares y con `SELECT ... INTO`. |
| **Fase 4** | `01:45 - 03:00` (75 min) | **APECD** | **Taller Experimental (Parte 1):** Desarrollo de funciones con parámetros `OUT`, funciones que retornan tablas (`RETURNS TABLE`), uso de `RECORD` en bucles `FOR` y clasificación de volatilidad. |
| **Fase 5** | `03:00 - 04:30` (90 min) | **APECD** | **Taller Experimental (Parte 2):** Desarrollo de Procedimientos Almacenados (`CREATE PROCEDURE`) con validaciones de negocio, bloques `EXCEPTION` y control transaccional. |
| **Fase 6** | `04:30 - 05:00` (30 min) | **APECD** | **Mantenimiento del Ciclo de Vida y Cierre:** Pruebas de modificación (`CREATE OR REPLACE`), eliminación segura (`DROP FUNCTION/PROCEDURE`) y revisión con rúbrica. |

---

## 📚 4. Desarrollo Teórico-Conceptual Profundo (ACD - 1 Hora)

### 4.1 ¿Por qué llevar Lógica al Motor de Base de Datos con `PL/pgSQL`?

Mientras el SQL estándar (visto en la Unidad 1) es un lenguaje **declarativo** (le decimos al motor *qué* datos queremos obtener), **`PL/pgSQL` (Procedural Language / PostgreSQL)** es un lenguaje **imperativo y procedural** nativo que añade variables, estructuras condicionales, bucles, cursores y control de errores directamente dentro del servidor PostgreSQL.

```mermaid
flowchart LR
    subgraph App["Enfoque Solo Aplicación (Múltiples Viajes de Red)"]
        A1["Backend (Node/Java/Python)"] -- "1. SELECT saldo..." --> DB1[("PostgreSQL")]
        DB1 -- "2. Retorna fila" --> A1
        A1 -- "3. Calcula en app y envía UPDATE..." --> DB1
        A1 -- "4. INSERT auditoría..." --> DB1
    end

    subgraph Stored["Enfoque PL/pgSQL (1 Solo Viaje de Red + Atomicidad)"]
        A2["Backend (Node/Java/Python)"] -- "1. CALL sp_transferir(...)" --> DB2[("PostgreSQL Engine\n(Función / Procedimiento PL/pgSQL)")]
        DB2 -- "2. Resultado final validado" --> A2
    end
```

#### Ventajas clave de `PL/pgSQL`:
1. **Eliminación de latencia de red (*Round-trips*):** Múltiples consultas `SELECT`, `INSERT` y `UPDATE` se ejecutan en la memoria local del motor en microsegundos.
2. **Consistencia y Centralización:** Si cinco aplicaciones distintas (Web, App Móvil, ERP, Batch nocturno, BI) se conectan a la misma base de datos, todas comparten exactamente la misma regla de cálculo o validación.
3. **Seguridad Granular (`SECURITY DEFINER`):** Permite que un usuario sin permisos directos de escritura sobre una tabla sensible ejecute únicamente un procedimiento controlado y auditado.

---

### 4.2 Diferencias Arquitectónicas: `FUNCTION` vs. `PROCEDURE` en PostgreSQL

A partir de PostgreSQL 11 se introdujo `CREATE PROCEDURE` como ciudadano de primera clase, separando claramente las responsabilidades respecto a `CREATE FUNCTION`:

| Característica Técnica | Función (`CREATE FUNCTION`) | Procedimiento Almacenado (`CREATE PROCEDURE`) |
| :--- | :--- | :--- |
| **Propósito Principal** | Cálculos, transformaciones, consultas encapsuladas y funciones de Trigger. | Orquestación de procesos de negocio, cargas por lotes (ETL) y operaciones transaccionales. |
| **Forma de Invocación** | Dentro de expresiones SQL: `SELECT fn_nombre(...);` o en `FROM`, `WHERE`, `JOIN`. | Sentencia independiente: `CALL sp_nombre(...);` (no puede usarse dentro de un `SELECT`). |
| **Valor de Retorno** | **Obligatorio** declarar `RETURNS <tipo>` (puede ser escalar, `TABLE`, `SETOF`, `RECORD`, `VOID` o `TRIGGER`). | **No tiene cláusula `RETURNS`**. Puede devolver valores únicamente mediante parámetros `OUT` o `INOUT`. |
| **Control Transaccional Interno** | **No permite** ejecutar `COMMIT` ni `ROLLBACK` dentro de su cuerpo (corre dentro de la transacción externa). | **Sí permite** ejecutar `COMMIT` y `ROLLBACK` dentro de su cuerpo (si no se invoca dentro de un bloque `BEGIN` explícito). |
| **Uso en Índices Funcionales** | Sí (si se declara como `IMMUTABLE`). | No aplica. |

---

### 4.3 Anatomía de un Bloque `PL/pgSQL` y Delimitadores Dollar-Quoting (`$$`)

En PostgreSQL, el cuerpo de una función o procedimiento es técnicamente un literal de cadena. Para evitar escapar las comillas simples (`'`) dentro del código, se utiliza el estándar de PostgreSQL llamado **Dollar-Quoting (`$$` o `$body$`)**:

```mermaid
flowchart TD
    HEADER["Cabecera: CREATE OR REPLACE FUNCTION / PROCEDURE nombre(argumentos)\nRETURNS tipo_retorno LANGUAGE plpgsql AS $$"] --> DECL["Sección DECLARE (Opcional)\nDeclaración de variables locales, constantes, tipos RECORD, %TYPE y %ROWTYPE"]
    DECL --> BEG["Sección BEGIN (Obligatoria)\nSentencias SQL, SELECT ... INTO, condicionales IF/CASE, bucles LOOP/FOR/WHILE"]
    BEG --> EXC["Sección EXCEPTION (Opcional)\nCaptura y tratamiento de errores (WHEN OTHERS, division_by_zero, unique_violation)"]
    EXC --> ENDB["Cierre: END; $$"]
```

```sql
CREATE OR REPLACE FUNCTION esquema.nombre_funcion(
    p_parametro1 INTEGER,
    p_parametro2 VARCHAR DEFAULT 'VALOR_DEFECTO'
)
RETURNS NUMERIC(12,2)
LANGUAGE plpgsql
AS $$
DECLARE
    -- 1. Declaración de variables locales y constantes
    v_subtotal      NUMERIC(12,2) := 0.00;
    c_iva  CONSTANT NUMERIC(4,2)  := 0.15;
BEGIN
    -- 2. Lógica procedural y consultas SQL
    v_subtotal := p_parametro1 * (1 + c_iva);
    RETURN ROUND(v_subtotal, 2);
EXCEPTION
    -- 3. Manejo de excepciones (opcional pero recomendado)
    WHEN OTHERS THEN
        RAISE WARNING 'Ocurrió un error inesperado: %', SQLERRM;
        RETURN 0.00;
END;
$$;
```

> **📏 Convención de Nombres Profesional (Evita colisiones de nombres):**
> - Prefijo `p_` para **parámetros/argumentos** (ej. `p_cliente_id`).
> - Prefijo `v_` para **variables locales** (ej. `v_saldo_actual`).
> - Prefijo `c_` para **constantes** (ej. `c_tasa_impuesto`).
> - Prefijo `r_` para **registros / filas** (`RECORD` o `%ROWTYPE`, ej. `r_cuenta`).
> *¿Por qué es vital?* Si llamas a un parámetro `cliente_id` igual que la columna `cliente_id` de la tabla, dentro de un `WHERE cliente_id = cliente_id` generarás un error de **referencia ambigua** (`column reference "cliente_id" is ambiguous`).

---

### 4.4 Argumentos y Modos de Parámetros (`IN`, `OUT`, `INOUT`, `VARIADIC`, `DEFAULT`)

| Modo | Dirección | ¿Se puede modificar dentro? | Comportamiento en PostgreSQL |
| :---: | :---: | :---: | :--- |
| **`IN`** *(Por defecto)* | Entrada (`Caller -> Rutina`) | Sí (como variable local en PG) | Recibe el valor enviado por el usuario. Si omites el modo, PostgreSQL asume `IN`. |
| **`OUT`** | Salida (`Rutina -> Caller`) | Sí (inicia en `NULL`) | Define una columna o valor de salida. Si hay varios parámetros `OUT`, la función devuelve automáticamente un registro compuesto (`RECORD`) sin necesidad de escribir `RETURN`. |
| **`INOUT`** | Entrada y Salida (`Bidireccional`) | Sí | Recibe un valor inicial del llamador, se transforma dentro de la rutina y se devuelve modificado al finalizar. |
| **`VARIADIC`** | Entrada de longitud variable | Sí (como `ARRAY`) | Permite pasar un número variable de argumentos del mismo tipo (ej. `VARIADIC p_montos NUMERIC[]`). |

####Formas de Invocar Argumentos:
1. **Notación Posicional:** `SELECT fn_calcular_interes(1000.00, 12, 0.08);`
2. **Notación por Nombre (`=>`):** `SELECT fn_calcular_interes(p_plazo_meses => 12, p_capital => 1000.00, p_tasa => 0.08);` *(Más legible y autodocumentada).*
3. **Notación Mixta:** Primero los posicionales y al final los nombrados.

---

### 4.5 Tipos de Retorno (`RETURNS`) en Funciones PostgreSQL

```mermaid
flowchart LR
    RET["Tipos de Retorno en CREATE FUNCTION"] --> R1["RETURNS tipo_escalar\n(INTEGER, NUMERIC, TEXT, BOOLEAN, JSONB)"]
    RET --> R2["RETURNS VOID\n(Ejecuta acciones sin devolver valor)"]
    RET --> R3["RETURNS RECORD\n(Estructura de fila dinámica o vía parámetros OUT)"]
    RET --> R4["RETURNS TABLE(col1 tipo1, col2 tipo2)\n(Devuelve un conjunto de filas con esquema fijo)"]
    RET --> R5["RETURNS SETOF tabla_o_tipo\n(Devuelve 0..N filas de una tabla existente)"]
    RET --> R6["RETURNS TRIGGER\n(Exclusivo para funciones disparadoras - Semana 06)"]
```

- **En funciones escalares:** Se utiliza `RETURN expresion;` para finalizar y devolver el valor.
- **En funciones `RETURNS TABLE(...)` o `RETURNS SETOF`:**
  - Se utiliza `RETURN QUERY SELECT ...;` para agregar el resultado de una consulta al conjunto de salida sin terminar aún la función.
  - O se utiliza `RETURN NEXT;` dentro de un bucle para emitir fila por fila.

---

### 4.6 El Tipo `RECORD`, `%TYPE`, `%ROWTYPE` y Variables Especiales

En `PL/pgSQL` disponemos de tres mecanismos de tipado dinámico para trabajar con columnas y filas completas sin acoplar el código a tipos rígidos:

| Mecanismo | Declaración en `DECLARE` | Descripción Técnica |
| :--- | :--- | :--- |
| **Anclaje de Columna (`%TYPE`)** | `v_precio productos.precio_unitario%TYPE;` | Copia dinámicamente el tipo de dato exacto de una columna de una tabla. Si mañana la columna cambia de `NUMERIC(8,2)` a `NUMERIC(12,4)`, la función se adapta sola. |
| **Anclaje de Fila (`%ROWTYPE`)** | `r_cliente clientes%ROWTYPE;` | Declara una variable compuesta que tiene **exactamente las mismas columnas** que la tabla `clientes`. Se accede a sus campos con notación punto: `r_cliente.nombre`. |
| **Registro Dinámico (`RECORD`)** | `r_dato RECORD;` | No tiene estructura fija al declararse; **adopta la estructura de la fila que se le asigne** en un `SELECT ... INTO r_dato` o en un bucle `FOR r_dato IN SELECT ... LOOP`. |
| **Registros de Trigger (`NEW` / `OLD`)** | *(Automáticos en funciones `RETURNS TRIGGER`)* | Variables especiales tipo `RECORD` que contienen la fila nueva (`NEW`) o anterior (`OLD`) durante un `INSERT`, `UPDATE` o `DELETE` (se profundizarán en la Semana 06). |

---

### 4.7 Uso de `SELECT ... INTO`, `STRICT` y la Variable Booleana `FOUND`

Dentro de `PL/pgSQL`, un `SELECT` normal sin destino no está permitido (lanza el error `query has no destination for result data`). Para guardar el resultado de una consulta de **una sola fila** en variables o en un `RECORD`, usamos `SELECT ... INTO`:

```sql
-- Variante A: SELECT ... INTO normal + verificación con FOUND
SELECT c.saldo_disponible, c.estado
INTO v_saldo, v_estado
FROM cuentas_ahorro c
WHERE c.cuenta_id = p_cuenta_id;

IF NOT FOUND THEN
    RAISE EXCEPTION 'La cuenta con ID % no existe en el sistema.', p_cuenta_id
        USING ERRCODE = 'P0002', HINT = 'Verifique el número de cuenta antes de reintentar.';
END IF;
```

```sql
-- Variante B: SELECT ... INTO STRICT (Garantiza exactamente 1 fila)
-- Si devuelve 0 filas -> lanza NO_DATA_FOUND
-- Si devuelve >1 filas -> lanza TOO_MANY_ROWS
SELECT c.saldo_disponible, c.estado
INTO STRICT r_cuenta
FROM cuentas_ahorro c
WHERE c.cuenta_id = p_cuenta_id;
```

| Comportamiento cuando la consulta devuelve... | `SELECT ... INTO` (Sin `STRICT`) | `SELECT ... INTO STRICT` |
| :--- | :--- | :--- |
| **0 filas** | Asigna `NULL` a las variables y pone `FOUND = FALSE`. No lanza error. | Lanza excepción inmediata `NO_DATA_FOUND` (`P0002`). |
| **1 fila** | Asigna los valores a las variables y pone `FOUND = TRUE`. | Asigna los valores a las variables y pone `FOUND = TRUE`. |
| **2 o más filas** | Asigna únicamente la **primera fila** encontrada (indeterminista si no hay `ORDER BY`) y descarta el resto. | Lanza excepción inmediata `TOO_MANY_ROWS` (`P0003`). |

---

### 4.8 Estructuras de Control, Mensajes (`RAISE`), Volatilidad y Ciclo de Vida

#### A. Condicionales y Bucles en `PL/pgSQL`
- **Condicional `IF`:** `IF condicion THEN ... ELSIF otra_condicion THEN ... ELSE ... END IF;`
- **Condicional `CASE`:** `CASE WHEN cond1 THEN ... WHEN cond2 THEN ... ELSE ... END CASE;`
- **Bucle `FOR` sobre consulta (el más usado en BD):**
  ```sql
  FOR r_item IN
      SELECT producto_id, stock FROM productos WHERE categoria_id = p_cat_id
  LOOP
      -- Procesar cada fila usando r_item.producto_id y r_item.stock
  END LOOP;
  ```
- **Bucle `FOR` numérico:** `FOR i IN 1..10 LOOP ... END LOOP;` (o `FOR i IN REVERSE 10..1 BY 2 LOOP`).
- **Bucle `WHILE`:** `WHILE v_contador < 100 LOOP ... END LOOP;`

#### B. Niveles de `RAISE` en PostgreSQL
- `RAISE DEBUG 'Mensaje técnico: %', v_var;` (Para trazas internas de bajo nivel).
- `RAISE NOTICE 'Procesando registro ID: %', v_id;` (Informativo en consola, **no aborta** la transacción).
- `RAISE WARNING 'Advertencia: stock bajo (%)', v_stock;` (Alerta al cliente, **no aborta** la transacción).
- `RAISE EXCEPTION 'Saldo insuficiente: disponible % vs solicitado %', v_disp, p_monto;` (**Aborta inmediatamente** la transacción actual y hace rollback de los cambios).

#### C. Categorías de Volatilidad (Optimización del Planificador)
Al declarar una función, debemos indicar su volatilidad para ayudar al optimizador de PostgreSQL:
- **`IMMUTABLE`**: No consulta tablas y para los mismos argumentos **siempre** devuelve el mismo resultado (ej. cálculo matemático o formato de texto). *Puede usarse en índices funcionales.*
- **`STABLE`**: Puede hacer `SELECT` a tablas, pero no modifica datos y dentro de una misma sentencia devuelve resultados consistentes.
- **`VOLATILE`** *(Por defecto)*: Puede modificar tablas (`INSERT`, `UPDATE`, `DELETE`) o devolver valores cambiantes (`NOW()`, `RANDOM()`).

#### D. Ciclo de Vida: Crear, Modificar y Eliminar Rutinas
```sql
-- 1. Crear o Modificar (Reemplazar cuerpo manteniendo la misma firma y tipo de retorno)
CREATE OR REPLACE FUNCTION fn_ejemplo(p_id INT) RETURNS TEXT ...;

-- 2. Si necesitas cambiar el TIPO DE RETORNO o los nombres de parámetros OUT,
--    debes eliminarla primero especificando los tipos de sus argumentos de entrada:
DROP FUNCTION IF EXISTS fn_ejemplo(INT);

-- 3. Eliminar un procedimiento almacenado:
DROP PROCEDURE IF EXISTS sp_cierre_diario(DATE, INTEGER);
```

---

## 💻 5. Ejemplos Guiados Paso a Paso en PostgreSQL / PL/pgSQL

Antes de iniciar el taller de 4 horas, construyamos el entorno empresarial de una **Cooperativa de Ahorro y Crédito / FinTech ("CoopYavirac Digital")** y ejecutemos **4 ejemplos guiados progresivos**.

### 5.1 Script Base del Entorno de Demostración y Taller

```sql
-- =============================================================================
-- ENTORNO BASE SEMANA 05: SISTEMA FINANCIERO "COOPYAVIRAC DIGITAL"
-- =============================================================================
DROP SCHEMA IF EXISTS coop_yavirac CASCADE;
CREATE SCHEMA coop_yavirac;
SET search_path TO coop_yavirac, public;

-- 1. Tabla de Socios / Clientes
CREATE TABLE socios (
    socio_id SERIAL PRIMARY KEY,
    cedula VARCHAR(15) NOT NULL UNIQUE,
    nombres_completos VARCHAR(120) NOT NULL,
    correo VARCHAR(120) NOT NULL UNIQUE,
    score_crediticio SMALLINT NOT NULL DEFAULT 700 CHECK (score_crediticio BETWEEN 300 AND 999),
    segmento VARCHAR(20) NOT NULL DEFAULT 'ESTANDAR' CHECK (segmento IN ('ESTANDAR', 'PREFERENTE', 'VIP')),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_vinculacion DATE NOT NULL DEFAULT CURRENT_DATE
);

-- 2. Tabla de Cuentas de Ahorro
CREATE TABLE cuentas (
    cuenta_id SERIAL PRIMARY KEY,
    numero_cuenta VARCHAR(20) NOT NULL UNIQUE,
    socio_id INTEGER NOT NULL REFERENCES socios(socio_id) ON DELETE RESTRICT,
    tipo_cuenta VARCHAR(20) NOT NULL CHECK (tipo_cuenta IN ('AHORRO_VISTA', 'AHORRO_PROGRAMADO', 'CORRIENTE')),
    saldo_contable NUMERIC(14,2) NOT NULL DEFAULT 0.00 CHECK (saldo_contable >= 0),
    saldo_bloqueado NUMERIC(14,2) NOT NULL DEFAULT 0.00 CHECK (saldo_bloqueado >= 0),
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVA' CHECK (estado IN ('ACTIVA', 'INACTIVA', 'BLOQUEADA', 'CERRADA')),
    ultima_transaccion TIMESTAMPTZ,
    CONSTRAINT chk_bloqueo_menor_contable CHECK (saldo_bloqueado <= saldo_contable)
);

-- 3. Tabla de Movimientos / Transacciones Financieras
CREATE TABLE movimientos (
    movimiento_id BIGSERIAL PRIMARY KEY,
    cuenta_id INTEGER NOT NULL REFERENCES cuentas(cuenta_id) ON DELETE RESTRICT,
    tipo_movimiento VARCHAR(25) NOT NULL CHECK (tipo_movimiento IN ('DEPOSITO', 'RETIRO', 'TRANSFERENCIA_ENV', 'TRANSFERENCIA_REC', 'INTERES', 'COMISION')),
    monto NUMERIC(14,2) NOT NULL CHECK (monto > 0),
    saldo_anterior NUMERIC(14,2) NOT NULL,
    saldo_posterior NUMERIC(14,2) NOT NULL,
    referencia VARCHAR(150) NOT NULL,
    fecha_movimiento TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Tabla de Créditos Otorgados
CREATE TABLE creditos (
    credito_id SERIAL PRIMARY KEY,
    socio_id INTEGER NOT NULL REFERENCES socios(socio_id) ON DELETE RESTRICT,
    monto_aprobado NUMERIC(14,2) NOT NULL CHECK (monto_aprobado > 0),
    tasa_anual_pct NUMERIC(5,2) NOT NULL CHECK (tasa_anual_pct > 0),
    plazo_meses SMALLINT NOT NULL CHECK (plazo_meses BETWEEN 3 AND 120),
    cuota_mensual NUMERIC(14,2) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'VIGENTE' CHECK (estado IN ('VIGENTE', 'CANCELADO', 'VENCIDO')),
    fecha_desembolso DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Poblamiento inicial
INSERT INTO socios (cedula, nombres_completos, correo, score_crediticio, segmento, fecha_vinculacion) VALUES
('1710020031', 'Valeria Andrade Viteri', 'valeria.andrade@yavirac.edu.ec', 890, 'VIP', '2022-03-15'),
('1720030042', 'Mateo Cevallos Paredes', 'mateo.cevallos@yavirac.edu.ec', 745, 'PREFERENTE', '2023-07-10'),
('1730040053', 'Camila Zambrano Rojas', 'camila.zambrano@yavirac.edu.ec', 610, 'ESTANDAR', '2024-11-05'),
('0910050064', 'Diego Montalvo Espinoza', 'diego.montalvo@yavirac.edu.ec', 480, 'ESTANDAR', '2025-02-20');

INSERT INTO cuentas (numero_cuenta, socio_id, tipo_cuenta, saldo_contable, saldo_bloqueado, estado, ultima_transaccion) VALUES
('400-0001-99', 1, 'AHORRO_VISTA', 8500.00, 500.00, 'ACTIVA', NOW() - INTERVAL '2 days'),
('400-0002-88', 1, 'AHORRO_PROGRAMADO', 12000.00, 0.00, 'ACTIVA', NOW() - INTERVAL '15 days'),
('400-0003-77', 2, 'AHORRO_VISTA', 2350.50, 150.50, 'ACTIVA', NOW() - INTERVAL '1 day'),
('400-0004-66', 3, 'AHORRO_VISTA', 420.00, 0.00, 'ACTIVA', NOW() - INTERVAL '5 days'),
('400-0005-55', 4, 'AHORRO_VISTA', 80.00, 80.00, 'BLOQUEADA', NOW() - INTERVAL '60 days');
```

---

### Ejemplo Guiado 1: Función Escalar `IMMUTABLE` con Fórmula Financiera (Cuota Francés)

Crearemos una función que calcule la cuota mensual fija de un préstamo bajo el sistema de amortización francés:
$$C = P \cdot \frac{i (1 + i)^n}{(1 + i)^n - 1}$$
donde $P$ es el capital, $i$ es la tasa mensual ($\text{tasa\_anual} / 12 / 100$) y $n$ el número de meses.

```sql
CREATE OR REPLACE FUNCTION fn_calcular_cuota_francesa(
    p_capital        NUMERIC,
    p_tasa_anual_pct NUMERIC,
    p_plazo_meses    INTEGER
)
RETURNS NUMERIC(14,2)
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    v_tasa_mensual NUMERIC;
    v_factor       NUMERIC;
    v_cuota        NUMERIC(14,2);
BEGIN
    -- Validaciones defensivas de dominio
    IF p_capital <= 0 OR p_plazo_meses <= 0 THEN
        RAISE EXCEPTION 'El capital (%) y el plazo (%) deben ser mayores que cero.', p_capital, p_plazo_meses
            USING ERRCODE = '22023'; -- invalid_parameter_value
    END IF;

    IF p_tasa_anual_pct <= 0 THEN
        RETURN ROUND(p_capital / p_plazo_meses, 2);
    END IF;

    v_tasa_mensual := (p_tasa_anual_pct / 100.0) / 12.0;
    v_factor       := POWER(1 + v_tasa_mensual, p_plazo_meses);
    v_cuota        := p_capital * ((v_tasa_mensual * v_factor) / (v_factor - 1));

    RETURN ROUND(v_cuota, 2);
END;
$$;

-- Prueba posicional y por nombre:
SELECT
    fn_calcular_cuota_francesa(10000.00, 11.50, 36) AS cuota_posicional,
    fn_calcular_cuota_francesa(
        p_plazo_meses    => 36,
        p_capital        => 10000.00,
        p_tasa_anual_pct => 11.50
    ) AS cuota_por_nombre;
```

---

### Ejemplo Guiado 2: Uso de `RECORD`, `SELECT ... INTO` y Parámetros `OUT`

Crearemos una función que reciba el `numero_cuenta`, busque la fila con `SELECT ... INTO` en una variable `RECORD` y devuelva múltiples métricas mediante parámetros `OUT`:

```sql
CREATE OR REPLACE FUNCTION fn_diagnosticar_cuenta(
    IN  p_numero_cuenta    VARCHAR,
    OUT o_titular          VARCHAR,
    OUT o_saldo_disponible NUMERIC(14,2),
    OUT o_estado_cuenta    VARCHAR,
    OUT o_mensaje_alerta   TEXT
)
RETURNS RECORD
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    r_info RECORD; -- Variable dinámica RECORD que adoptará las columnas del SELECT
BEGIN
    SELECT
        s.nombres_completos,
        c.saldo_contable,
        c.saldo_bloqueado,
        (c.saldo_contable - c.saldo_bloqueado) AS disponible_real,
        c.estado
    INTO r_info
    FROM cuentas c
    INNER JOIN socios s ON s.socio_id = c.socio_id
    WHERE c.numero_cuenta = TRIM(p_numero_cuenta);

    -- Verificamos con la variable especial FOUND si el SELECT devolvió una fila
    IF NOT FOUND THEN
        RAISE EXCEPTION 'La cuenta [%] no existe en el catálogo de CoopYavirac.', p_numero_cuenta
            USING ERRCODE = 'P0002', HINT = 'Verifique el formato 400-XXXX-XX.';
    END IF;

    -- Asignamos los parámetros OUT usando los campos del RECORD r_info
    o_titular          := r_info.nombres_completos;
    o_saldo_disponible := r_info.disponible_real;
    o_estado_cuenta    := r_info.estado;

    IF r_info.estado <> 'ACTIVA' THEN
        o_mensaje_alerta := 'ALERTA: La cuenta no está operativa (' || r_info.estado || ').';
    ELSIF r_info.disponible_real < 100.00 THEN
        o_mensaje_alerta := 'AVISO: Saldo disponible inferior al mínimo recomendado ($100.00).';
    ELSE
        o_mensaje_alerta := 'OK: Cuenta operativa y con liquidez saludable.';
    END IF;
END;
$$;

-- Invocación desestructurando el RECORD retornado con SELECT * FROM:
SELECT * FROM fn_diagnosticar_cuenta('400-0001-99');
SELECT * FROM fn_diagnosticar_cuenta('400-0005-55');
```

---

### Ejemplo Guiado 3: Función Tabular (`RETURNS TABLE`) con `RETURN QUERY`

Cuando una aplicación necesita un reporte parametrizado que pueda cruzarse en un `JOIN`, usamos `RETURNS TABLE`:

```sql
CREATE OR REPLACE FUNCTION fn_listar_cuentas_por_segmento(
    p_segmento      VARCHAR DEFAULT 'VIP',
    p_saldo_minimo  NUMERIC DEFAULT 0.00
)
RETURNS TABLE (
    socio_cedula       VARCHAR,
    socio_nombre       VARCHAR,
    numero_cuenta      VARCHAR,
    tipo_cuenta        VARCHAR,
    saldo_disponible   NUMERIC(14,2)
)
LANGUAGE plpgsql
STABLE
AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.cedula,
        s.nombres_completos,
        c.numero_cuenta,
        c.tipo_cuenta,
        (c.saldo_contable - c.saldo_bloqueado)::NUMERIC(14,2) AS disp
    FROM socios s
    INNER JOIN cuentas c ON c.socio_id = s.socio_id
    WHERE s.segmento = UPPER(TRIM(p_segmento))
      AND (c.saldo_contable - c.saldo_bloqueado) >= p_saldo_minimo
      AND s.activo = TRUE
    ORDER BY disp DESC;
END;
$$;

-- Invocación como si fuera una tabla o vista parametrizada:
SELECT * FROM fn_listar_cuentas_por_segmento('VIP', 1000.00);
```

---

### Ejemplo Guiado 4: Procedimiento Almacenado (`CREATE PROCEDURE`) para Transferencias Bancarias Atómicas

Observa cómo un procedimiento almacenado coordina bloqueos de fila (`FOR UPDATE`), validaciones de negocio, actualización de ambas cuentas y registro doble en `movimientos`:

```sql
CREATE OR REPLACE PROCEDURE sp_transferir_fondos(
    IN    p_cuenta_origen   VARCHAR,
    IN    p_cuenta_destino  VARCHAR,
    IN    p_monto           NUMERIC(14,2),
    IN    p_concepto        VARCHAR,
    INOUT io_codigo_estado  VARCHAR DEFAULT NULL,
    INOUT io_mensaje        TEXT    DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    r_origen          cuentas%ROWTYPE;
    r_destino         cuentas%ROWTYPE;
    v_disp_origen     NUMERIC(14,2);
BEGIN
    -- 1. Validaciones básicas de entrada
    IF p_monto <= 0 THEN
        RAISE EXCEPTION 'El monto a transferir debe ser estrictamente positivo (%).', p_monto;
    END IF;

    IF TRIM(p_cuenta_origen) = TRIM(p_cuenta_destino) THEN
        RAISE EXCEPTION 'La cuenta de origen y destino no pueden ser la misma (%).', p_cuenta_origen;
    END IF;

    -- 2. Obtener y bloquear fila de cuenta origen (SELECT ... INTO STRICT)
    SELECT * INTO STRICT r_origen
    FROM cuentas
    WHERE numero_cuenta = TRIM(p_cuenta_origen)
    FOR UPDATE;

    -- 3. Obtener y bloquear fila de cuenta destino
    SELECT * INTO STRICT r_destino
    FROM cuentas
    WHERE numero_cuenta = TRIM(p_cuenta_destino)
    FOR UPDATE;

    -- 4. Validar estados operativos y fondos disponibles
    IF r_origen.estado <> 'ACTIVA' THEN
        RAISE EXCEPTION 'La cuenta origen % se encuentra en estado %.', p_cuenta_origen, r_origen.estado;
    END IF;

    IF r_destino.estado <> 'ACTIVA' THEN
        RAISE EXCEPTION 'La cuenta destino % se encuentra en estado %.', p_cuenta_destino, r_destino.estado;
    END IF;

    v_disp_origen := r_origen.saldo_contable - r_origen.saldo_bloqueado;
    IF v_disp_origen < p_monto THEN
        RAISE EXCEPTION 'Fondos insuficientes en cuenta %. Disponible: $%, Solicitado: $%',
            p_cuenta_origen, v_disp_origen, p_monto;
    END IF;

    -- 5. Debitar cuenta origen y acreditar cuenta destino
    UPDATE cuentas
    SET saldo_contable     = saldo_contable - p_monto,
        ultima_transaccion = NOW()
    WHERE cuenta_id = r_origen.cuenta_id;

    UPDATE cuentas
    SET saldo_contable     = saldo_contable + p_monto,
        ultima_transaccion = NOW()
    WHERE cuenta_id = r_destino.cuenta_id;

    -- 6. Insertar trazabilidad contable en la tabla movimientos
    INSERT INTO movimientos (cuenta_id, tipo_movimiento, monto, saldo_anterior, saldo_posterior, referencia)
    VALUES
    (
        r_origen.cuenta_id, 'TRANSFERENCIA_ENV', p_monto,
        r_origen.saldo_contable, r_origen.saldo_contable - p_monto,
        'Transferencia hacia ' || p_cuenta_destino || ': ' || COALESCE(p_concepto, 'Sin concepto')
    ),
    (
        r_destino.cuenta_id, 'TRANSFERENCIA_REC', p_monto,
        r_destino.saldo_contable, r_destino.saldo_contable + p_monto,
        'Transferencia desde ' || p_cuenta_origen || ': ' || COALESCE(p_concepto, 'Sin concepto')
    );

    io_codigo_estado := 'OK-200';
    io_mensaje       := FORMAT('Transferencia exitosa de $%s desde %s hacia %s.', p_monto, p_cuenta_origen, p_cuenta_destino);
    RAISE NOTICE '%', io_mensaje;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        io_codigo_estado := 'ERR-404';
        io_mensaje       := 'Una de las cuentas especificadas no existe en el sistema.';
        RAISE WARNING '%', io_mensaje;
    WHEN OTHERS THEN
        io_codigo_estado := 'ERR-400';
        io_mensaje       := SQLERRM;
        RAISE WARNING 'Transferencia rechazada: %', SQLERRM;
END;
$$;

-- Invocación del procedimiento con CALL:
CALL sp_transferir_fondos('400-0001-99', '400-0003-77', 250.00, 'Pago de consultoría de software');
```

---

## 🛠️ 6. Taller Práctico-Experimental en Contacto con el Docente (APECD - 4 Horas)

Trabajando sobre el esquema `coop_yavirac` creado en la sección anterior, desarrolla los siguientes **6 ejercicios progresivos** en tu archivo `semana05_plpgsql_rutinas.sql`.

---

### Ejercicio 1: Función de Evaluación de Riesgo y Cupo de Crédito (`SELECT ... INTO` + `CASE`)
**Requerimiento:**
Crea la función `fn_evaluar_cupo_credito(p_cedula VARCHAR)` que retorne un `NUMERIC(14,2)` correspondiente al cupo máximo de crédito preaprobado para un socio según las siguientes reglas:
1. Usa `SELECT ... INTO` sobre una variable `r_socio RECORD` para consultar el `socio_id`, `score_crediticio`, `segmento`, `activo` y la suma del saldo disponible (`saldo_contable - saldo_bloqueado`) de todas sus cuentas activas.
2. Si el socio no existe (`NOT FOUND`), lanza `RAISE EXCEPTION` indicando la cédula buscada.
3. Si `activo = FALSE` o `score_crediticio < 500`, retorna `0.00` y emite un `RAISE NOTICE` explicando el motivo.
4. En caso contrario, calcula el cupo multiplicando su liquidez total por un factor según su `score_crediticio`:
   - `score_crediticio >= 800`: factor `3.5` (y bono adicional de `$2,000.00` si es segmento `'VIP'`).
   - `score_crediticio BETWEEN 650 AND 799`: factor `2.0`.
   - `score_crediticio BETWEEN 500 AND 649`: factor `1.2`.
5. Prueba la función con las cédulas `'1710020031'`, `'1720030042'` y `'0910050064'`.

<details>
<summary>✅ Ver Solución Propuesta — Ejercicio 1</summary>

```sql
CREATE OR REPLACE FUNCTION fn_evaluar_cupo_credito(p_cedula VARCHAR)
RETURNS NUMERIC(14,2)
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    r_socio  RECORD;
    v_factor NUMERIC(4,2);
    v_cupo   NUMERIC(14,2) := 0.00;
BEGIN
    SELECT
        s.socio_id,
        s.nombres_completos,
        s.score_crediticio,
        s.segmento,
        s.activo,
        COALESCE(SUM(c.saldo_contable - c.saldo_bloqueado) FILTER (WHERE c.estado = 'ACTIVA'), 0.00) AS liquidez_total
    INTO r_socio
    FROM socios s
    LEFT JOIN cuentas c ON c.socio_id = s.socio_id
    WHERE s.cedula = TRIM(p_cedula)
    GROUP BY s.socio_id, s.nombres_completos, s.score_crediticio, s.segmento, s.activo;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe ningún socio registrado con la cédula [%].', p_cedula
            USING ERRCODE = 'P0002';
    END IF;

    IF NOT r_socio.activo OR r_socio.score_crediticio < 500 THEN
        RAISE NOTICE 'Socio % no califica para crédito (Activo: %, Score: %).',
            r_socio.nombres_completos, r_socio.activo, r_socio.score_crediticio;
        RETURN 0.00;
    END IF;

    v_factor := CASE
        WHEN r_socio.score_crediticio >= 800 THEN 3.50
        WHEN r_socio.score_crediticio >= 650 THEN 2.00
        ELSE 1.20
    END;

    v_cupo := ROUND(r_socio.liquidez_total * v_factor, 2);

    IF r_socio.score_crediticio >= 800 AND r_socio.segmento = 'VIP' THEN
        v_cupo := v_cupo + 2000.00;
    END IF;

    RETURN v_cupo;
END;
$$;

-- Pruebas de verificación:
SELECT
    cedula,
    nombres_completos,
    score_crediticio,
    fn_evaluar_cupo_credito(cedula) AS cupo_preaprobado
FROM socios;
```

</details>

---

### Ejercicio 2: Función Generadora de Tabla de Amortización (`RETURNS TABLE` + Bucle `FOR` + `RETURN NEXT`)
**Requerimiento:**
Crea la función `fn_simular_tabla_amortizacion(p_capital NUMERIC, p_tasa_anual_pct NUMERIC, p_plazo_meses INTEGER)` que retorne una tabla con las columnas:
- `numero_cuota INTEGER`
- `fecha_vencimiento DATE` (sumando `numero_cuota` meses a `CURRENT_DATE`)
- `saldo_inicial NUMERIC(14,2)`
- `valor_cuota NUMERIC(14,2)` (reutilizando `fn_calcular_cuota_francesa`)
- `interes_mes NUMERIC(14,2)`
- `abono_capital NUMERIC(14,2)`
- `saldo_final NUMERIC(14,2)`

Usa un bucle `FOR v_mes IN 1..p_plazo_meses LOOP` y emite cada fila calculada con `RETURN NEXT;`.

<details>
<summary>✅ Ver Solución Propuesta — Ejercicio 2</summary>

```sql
CREATE OR REPLACE FUNCTION fn_simular_tabla_amortizacion(
    p_capital        NUMERIC,
    p_tasa_anual_pct NUMERIC,
    p_plazo_meses    INTEGER
)
RETURNS TABLE (
    numero_cuota      INTEGER,
    fecha_vencimiento DATE,
    saldo_inicial     NUMERIC(14,2),
    valor_cuota       NUMERIC(14,2),
    interes_mes       NUMERIC(14,2),
    abono_capital     NUMERIC(14,2),
    saldo_final       NUMERIC(14,2)
)
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    v_tasa_mensual NUMERIC;
    v_cuota_fija   NUMERIC(14,2);
    v_saldo_actual NUMERIC(14,2);
BEGIN
    v_cuota_fija   := fn_calcular_cuota_francesa(p_capital, p_tasa_anual_pct, p_plazo_meses);
    v_tasa_mensual := (p_tasa_anual_pct / 100.0) / 12.0;
    v_saldo_actual := ROUND(p_capital, 2);

    FOR v_mes IN 1..p_plazo_meses LOOP
        numero_cuota      := v_mes;
        fecha_vencimiento := (CURRENT_DATE + (v_mes || ' months')::INTERVAL)::DATE;
        saldo_inicial     := v_saldo_actual;
        interes_mes       := ROUND(v_saldo_actual * v_tasa_mensual, 2);

        -- Ajuste de última cuota por redondeo de centavos
        IF v_mes = p_plazo_meses THEN
            abono_capital := v_saldo_actual;
            valor_cuota   := abono_capital + interes_mes;
            saldo_final   := 0.00;
        ELSE
            valor_cuota   := v_cuota_fija;
            abono_capital := valor_cuota - interes_mes;
            saldo_final   := v_saldo_actual - abono_capital;
        END IF;

        v_saldo_actual := saldo_final;
        RETURN NEXT;
    END LOOP;
END;
$$;

-- Prueba: Simular un crédito de $6,000 a 12% anual por 6 meses
SELECT * FROM fn_simular_tabla_amortizacion(6000.00, 12.00, 6);
```

</details>

---

### Ejercicio 3: Función con Argumento `VARIADIC` para Depósito Múltiple de Cheques
**Requerimiento:**
Crea la función `fn_sumar_lote_cheques(p_comision_por_cheque NUMERIC, VARIADIC p_montos_cheques NUMERIC[])` que reciba el costo de comisión por cada cheque y una lista variable de montos de cheques.
- Recorre el arreglo o usa `unnest(p_montos_cheques)` para validar que ningún cheque sea negativo o cero.
- Retorna un `RECORD` mediante parámetros `OUT`: `o_cantidad_cheques INT`, `o_total_bruto NUMERIC(14,2)`, `o_total_comision NUMERIC(14,2)` y `o_total_neto NUMERIC(14,2)`.

<details>
<summary>✅ Ver Solución Propuesta — Ejercicio 3</summary>

```sql
CREATE OR REPLACE FUNCTION fn_sumar_lote_cheques(
    IN       p_comision_por_cheque NUMERIC,
    VARIADIC p_montos_cheques      NUMERIC[],
    OUT      o_cantidad_cheques    INTEGER,
    OUT      o_total_bruto         NUMERIC(14,2),
    OUT      o_total_comision      NUMERIC(14,2),
    OUT      o_total_neto          NUMERIC(14,2)
)
RETURNS RECORD
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    v_monto NUMERIC;
BEGIN
    o_cantidad_cheques := 0;
    o_total_bruto      := 0.00;

    FOREACH v_monto IN ARRAY p_montos_cheques LOOP
        IF v_monto IS NULL OR v_monto <= 0 THEN
            RAISE EXCEPTION 'Monto de cheque inválido (%). Todos los cheques deben ser > 0.', v_monto;
        END IF;
        o_cantidad_cheques := o_cantidad_cheques + 1;
        o_total_bruto      := o_total_bruto + v_monto;
    END LOOP;

    o_total_comision := ROUND(o_cantidad_cheques * COALESCE(p_comision_por_cheque, 0), 2);
    o_total_neto     := ROUND(o_total_bruto - o_total_comision, 2);
END;
$$;

-- Prueba enviando 4 cheques en una sola llamada:
SELECT * FROM fn_sumar_lote_cheques(0.50, 120.00, 350.25, 80.00, 1500.75);
```

</details>

---

### Ejercicio 4: Procedimiento Almacenado de Capitalización Mensual de Intereses (`FOR r_cuenta IN SELECT ... LOOP`)
**Requerimiento:**
Crea el procedimiento almacenado `sp_capitalizar_intereses_mensuales(IN p_tasa_anual_vista NUMERIC DEFAULT 3.50, IN p_tasa_anual_programado NUMERIC DEFAULT 6.00, OUT o_cuentas_procesadas INTEGER, OUT o_monto_total_acreditado NUMERIC(14,2))` que:
1. Recorra con un bucle `FOR r_cuenta IN SELECT ... LOOP` todas las cuentas con `estado = 'ACTIVA'` y `saldo_contable >= 100.00`.
2. Calcule el interés mensual según `tipo_cuenta` (`AHORRO_VISTA` vs `AHORRO_PROGRAMADO`).
3. Si el interés calculado es `>= 0.01`, actualice `saldo_contable` en `cuentas` e inserte el movimiento tipo `'INTERES'` en la tabla `movimientos`.
4. Al finalizar, devuelva en los parámetros `OUT` el total de cuentas beneficiadas y la suma acreditada, emitiendo un `RAISE NOTICE` con el resumen.

<details>
<summary>✅ Ver Solución Propuesta — Ejercicio 4</summary>

```sql
CREATE OR REPLACE PROCEDURE sp_capitalizar_intereses_mensuales(
    IN  p_tasa_anual_vista       NUMERIC DEFAULT 3.50,
    IN  p_tasa_anual_programado  NUMERIC DEFAULT 6.00,
    OUT o_cuentas_procesadas     INTEGER,
    OUT o_monto_total_acreditado NUMERIC(14,2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    r_cuenta  RECORD;
    v_tasa    NUMERIC;
    v_interes NUMERIC(14,2);
BEGIN
    o_cuentas_procesadas     := 0;
    o_monto_total_acreditado := 0.00;

    FOR r_cuenta IN
        SELECT cuenta_id, numero_cuenta, tipo_cuenta, saldo_contable
        FROM cuentas
        WHERE estado = 'ACTIVA'
          AND saldo_contable >= 100.00
          AND tipo_cuenta IN ('AHORRO_VISTA', 'AHORRO_PROGRAMADO')
        FOR UPDATE
    LOOP
        v_tasa := CASE
            WHEN r_cuenta.tipo_cuenta = 'AHORRO_PROGRAMADO' THEN p_tasa_anual_programado
            ELSE p_tasa_anual_vista
        END;

        v_interes := ROUND(r_cuenta.saldo_contable * ((v_tasa / 100.0) / 12.0), 2);

        IF v_interes >= 0.01 THEN
            UPDATE cuentas
            SET saldo_contable     = saldo_contable + v_interes,
                ultima_transaccion = NOW()
            WHERE cuenta_id = r_cuenta.cuenta_id;

            INSERT INTO movimientos (cuenta_id, tipo_movimiento, monto, saldo_anterior, saldo_posterior, referencia)
            VALUES (
                r_cuenta.cuenta_id,
                'INTERES',
                v_interes,
                r_cuenta.saldo_contable,
                r_cuenta.saldo_contable + v_interes,
                FORMAT('Capitalización mensual (%s%% anual)', v_tasa)
            );

            o_cuentas_procesadas     := o_cuentas_procesadas + 1;
            o_monto_total_acreditado := o_monto_total_acreditado + v_interes;
        END IF;
    END LOOP;

    RAISE NOTICE 'Cierre mensual completado: % cuentas capitalizadas por un total de $%.',
        o_cuentas_procesadas, o_monto_total_acreditado;
END;
$$;

-- Invocación con CALL:
CALL sp_capitalizar_intereses_mensuales(3.50, 6.00, NULL, NULL);
```

</details>

---

### Ejercicio 5: Procedimiento de Otorgamiento y Desembolso Automático de Crédito
**Requerimiento:**
Crea el procedimiento `sp_desembolsar_credito(p_cedula VARCHAR, p_numero_cuenta_destino VARCHAR, p_monto NUMERIC, p_tasa_anual NUMERIC, p_plazo_meses SMALLINT)` que:
1. Verifique el cupo preaprobado llamando a tu función `fn_evaluar_cupo_credito(p_cedula)`. Si `p_monto > v_cupo`, lance `RAISE EXCEPTION` indicando el exceso.
2. Verifique con `SELECT ... INTO STRICT` que la cuenta destino pertenezca a ese socio y esté `'ACTIVA'`.
3. Calcule la cuota mensual usando `fn_calcular_cuota_francesa`.
4. Inserte el registro en la tabla `creditos`.
5. Acredite el `p_monto` en la cuenta del socio e inserte el movimiento `'DEPOSITO'` por concepto de desembolso de crédito.

<details>
<summary>✅ Ver Solución Propuesta — Ejercicio 5</summary>

```sql
CREATE OR REPLACE PROCEDURE sp_desembolsar_credito(
    p_cedula                VARCHAR,
    p_numero_cuenta_destino VARCHAR,
    p_monto                 NUMERIC,
    p_tasa_anual            NUMERIC,
    p_plazo_meses           SMALLINT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_socio_id     INTEGER;
    v_cupo_maximo  NUMERIC(14,2);
    v_cuota        NUMERIC(14,2);
    v_credito_id   INTEGER;
    r_cuenta       cuentas%ROWTYPE;
BEGIN
    -- 1. Obtener socio_id
    SELECT socio_id INTO STRICT v_socio_id
    FROM socios
    WHERE cedula = TRIM(p_cedula);

    -- 2. Validar cupo máximo preaprobado
    v_cupo_maximo := fn_evaluar_cupo_credito(p_cedula);
    IF p_monto > v_cupo_maximo THEN
        RAISE EXCEPTION 'Monto solicitado ($%) supera el cupo máximo aprobado ($%) para la cédula %.',
            p_monto, v_cupo_maximo, p_cedula;
    END IF;

    -- 3. Verificar que la cuenta pertenezca al socio y esté activa
    SELECT * INTO STRICT r_cuenta
    FROM cuentas
    WHERE numero_cuenta = TRIM(p_numero_cuenta_destino)
      AND socio_id = v_socio_id
    FOR UPDATE;

    IF r_cuenta.estado <> 'ACTIVA' THEN
        RAISE EXCEPTION 'La cuenta % no está ACTIVA (Estado actual: %).',
            p_numero_cuenta_destino, r_cuenta.estado;
    END IF;

    -- 4. Calcular cuota mensual e insertar crédito
    v_cuota := fn_calcular_cuota_francesa(p_monto, p_tasa_anual, p_plazo_meses);

    INSERT INTO creditos (socio_id, monto_aprobado, tasa_anual_pct, plazo_meses, cuota_mensual, estado)
    VALUES (v_socio_id, p_monto, p_tasa_anual, p_plazo_meses, v_cuota, 'VIGENTE')
    RETURNING credito_id INTO v_credito_id;

    -- 5. Acreditar desembolso en cuenta y registrar movimiento
    UPDATE cuentas
    SET saldo_contable     = saldo_contable + p_monto,
        ultima_transaccion = NOW()
    WHERE cuenta_id = r_cuenta.cuenta_id;

    INSERT INTO movimientos (cuenta_id, tipo_movimiento, monto, saldo_anterior, saldo_posterior, referencia)
    VALUES (
        r_cuenta.cuenta_id,
        'DEPOSITO',
        p_monto,
        r_cuenta.saldo_contable,
        r_cuenta.saldo_contable + p_monto,
        FORMAT('Desembolso automático Crédito #%s (%s meses, cuota $%s)', v_credito_id, p_plazo_meses, v_cuota)
    );

    RAISE NOTICE 'Crédito #% desembolsado con éxito. Cuota mensual: $%. Nuevo saldo cuenta %: $%.',
        v_credito_id, v_cuota, r_cuenta.numero_cuenta, r_cuenta.saldo_contable + p_monto;
END;
$$;

-- Prueba de desembolso exitoso para Valeria Andrade:
CALL sp_desembolsar_credito('1710020031', '400-0001-99', 5000.00, 10.50, 24::SMALLINT);
```

</details>

---

### Ejercicio 6: Administración del Ciclo de Vida (Modificación y Eliminación de Funciones y Procedimientos)
**Requerimiento:**
1. Modifica (`CREATE OR REPLACE FUNCTION`) la función `fn_listar_cuentas_por_segmento` para que filtre únicamente cuentas con `estado = 'ACTIVA'`.
2. Crea una función temporal de prueba `fn_temporal_auditoria(INTEGER, VARCHAR)` y un procedimiento `sp_temporal_limpieza(DATE)`, y luego demuestra su eliminación segura usando `DROP FUNCTION IF EXISTS` y `DROP PROCEDURE IF EXISTS` especificando sus firmas de tipos.
3. Escribe una consulta al catálogo del sistema (`pg_proc` unido con `pg_namespace`) que liste todas las funciones y procedimientos creados hoy en el esquema `coop_yavirac`.

<details>
<summary>✅ Ver Solución Propuesta — Ejercicio 6</summary>

```sql
-- 1. Modificación de la lógica interna con CREATE OR REPLACE FUNCTION
CREATE OR REPLACE FUNCTION fn_listar_cuentas_por_segmento(
    p_segmento      VARCHAR DEFAULT 'VIP',
    p_saldo_minimo  NUMERIC DEFAULT 0.00
)
RETURNS TABLE (
    socio_cedula       VARCHAR,
    socio_nombre       VARCHAR,
    numero_cuenta      VARCHAR,
    tipo_cuenta        VARCHAR,
    saldo_disponible   NUMERIC(14,2)
)
LANGUAGE plpgsql
STABLE
AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.cedula,
        s.nombres_completos,
        c.numero_cuenta,
        c.tipo_cuenta,
        (c.saldo_contable - c.saldo_bloqueado)::NUMERIC(14,2) AS disp
    FROM socios s
    INNER JOIN cuentas c ON c.socio_id = s.socio_id
    WHERE s.segmento = UPPER(TRIM(p_segmento))
      AND (c.saldo_contable - c.saldo_bloqueado) >= p_saldo_minimo
      AND s.activo = TRUE
      AND c.estado = 'ACTIVA' -- Nuevo filtro agregado sin romper la firma
    ORDER BY disp DESC;
END;
$$;

-- 2. Creación y eliminación explícita con firma de argumentos
CREATE OR REPLACE FUNCTION fn_temporal_auditoria(p_id INTEGER, p_tag VARCHAR)
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
    RAISE NOTICE 'Auditoría temporal % - %', p_id, p_tag;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_temporal_limpieza(p_fecha_corte DATE)
LANGUAGE plpgsql AS $$
BEGIN
    RAISE NOTICE 'Limpieza hasta %', p_fecha_corte;
END;
$$;

-- Eliminación segura especificando los tipos de datos de la firma:
DROP FUNCTION IF EXISTS fn_temporal_auditoria(INTEGER, VARCHAR);
DROP PROCEDURE IF EXISTS sp_temporal_limpieza(DATE);

-- 3. Consulta al catálogo de PostgreSQL (pg_proc) para auditar nuestras rutinas:
SELECT
    n.nspname AS esquema,
    p.proname AS nombre_rutina,
    CASE p.prokind
        WHEN 'f' THEN 'FUNCTION'
        WHEN 'p' THEN 'PROCEDURE'
    END AS tipo_objeto,
    pg_get_function_arguments(p.oid) AS argumentos,
    COALESCE(pg_get_function_result(p.oid), 'N/A (PROCEDURE)') AS retorno
FROM pg_proc p
INNER JOIN pg_namespace n ON n.oid = p.pronamespace
WHERE n.nspname = 'coop_yavirac'
ORDER BY tipo_objeto, nombre_rutina;
```

</details>

---

## 🚀 7. Actividades de Refuerzo Autónomo

En cumplimiento de la habilidad blanda del PEA (*"Realiza ejercicios extras de Funciones y Triggers de forma autónoma"*), resuelve los siguientes retos fuera del aula:

1. **Reto Autónomo 1 — Función de Estado de Cuenta en `JSONB`:**
   - Crea la función `fn_exportar_estado_cuenta_json(p_numero_cuenta VARCHAR, p_ultimos_n INT DEFAULT 5) RETURNS JSONB` que utilice `SELECT ... INTO` y `jsonb_build_object` / `jsonb_agg` para devolver en un solo documento JSONB los datos del titular, los saldos de la cuenta y un arreglo con sus últimos `N` movimientos.
2. **Reto Autónomo 2 — Procedimiento de Reclasificación Masiva de Segmentos:**
   - Crea el procedimiento `sp_reclasificar_segmentos_socios()` que actualice automáticamente la columna `segmento` de todos los socios activos: si la suma de sus saldos supera `$15,000` y su score es `>= 800`, pasa a `'VIP'`; si supera `$3,000` y su score es `>= 650`, pasa a `'PREFERENTE'`; caso contrario `'ESTANDAR'`.

---

## 📊 8. Rúbrica de Evaluación y Preguntas de Autoevaluación

### 8.1 Rúbrica del Taller Práctico (APECD - Semana 05)

| Criterio | Excelente (10 pts) | Satisfactorio (7.5 pts) | En Proceso (5 pts) | Insuficiente (<2.5 pts) |
| :--- | :--- | :--- | :--- | :--- |
| **Uso de `FUNCTION` vs `PROCEDURE`** | Selecciona e invoca correctamente `SELECT` para funciones y `CALL` para procedimientos, respetando los tipos de retorno. | Crea ambos tipos de rutinas pero confunde la invocación de parámetros `OUT`/`INOUT` en `CALL`. | Implementa todo como `FUNCTION` ignorando `CREATE PROCEDURE`. | El código presenta errores de sintaxis en las cabeceras. |
| **Manejo de `RECORD`, `%ROWTYPE` y `SELECT INTO`** | Usa `RECORD` y `%ROWTYPE` apropiadamente, validando `NOT FOUND` o `STRICT` y previniendo ambigüedad de nombres. | Usa `SELECT INTO` pero omite validar qué sucede cuando una consulta devuelve 0 filas. | Declara múltiples variables sueltas innecesarias o sufre colisiones de nombres con columnas. | No utiliza `SELECT ... INTO` o deja consultas sin destino en `PL/pgSQL`. |
| **Control de Flujo y Excepciones (`RAISE`)** | Implementa bucles `FOR`, condicionales y bloques `EXCEPTION` informativos con `ERRCODE` y `FOR UPDATE` en transacciones financieras. | Usa `RAISE EXCEPTION` básico pero omite bloqueos `FOR UPDATE` o captura de errores. | Lógica condicional incompleta que permite saldos negativos o transferencias inválidas. | No valida datos de entrada ni maneja errores. |

---

### 8.2 Preguntas de Autoevaluación

1. **¿Qué sucede si dentro de una función `PL/pgSQL` ejecutas `SELECT saldo_contable INTO v_saldo FROM cuentas WHERE cuenta_id = 99999;` (sin la palabra `STRICT`) y el `cuenta_id` no existe?**
2. **¿Por qué no es posible cambiar el tipo de retorno de una función existente usando únicamente `CREATE OR REPLACE FUNCTION`?**
3. **¿Cuál es la diferencia práctica entre declarar una variable como `r_fila cuentas%ROWTYPE;` frente a `r_fila RECORD;`?**
4. **¿Cómo se invoca una función que retorna `TABLE(...)` para ver sus columnas separadas en lugar de una sola tupla empaquetada?**

<details>
<summary>✅ Ver Respuestas de Autoevaluación</summary>

1. **Sin `STRICT`:** PostgreSQL **no lanza ninguna excepción**; asigna `NULL` a la variable `v_saldo` y establece la variable interna `FOUND` en `FALSE`. Por ello es obligatorio verificar `IF NOT FOUND THEN ...` inmediatamente después, o bien usar `SELECT ... INTO STRICT`.
2. **Cambio de tipo de retorno:** Porque PostgreSQL almacena la firma de salida en el catálogo `pg_proc` y otras vistas o funciones pueden depender de ese tipo exacto. Para cambiar el `RETURNS`, primero debes ejecutar `DROP FUNCTION nombre(tipos_argumentos);` y luego `CREATE FUNCTION`.
3. **`%ROWTYPE` vs `RECORD`:** `cuentas%ROWTYPE` fija su estructura desde el momento de la declaración con todas las columnas exactas de la tabla `cuentas`. En cambio, `RECORD` es una estructura comodín cuya forma se define en tiempo de ejecución según las columnas que proyecte el `SELECT ... INTO` o el bucle `FOR` (ideal cuando hacemos `JOIN` entre varias tablas).
4. **Invocación de `RETURNS TABLE`:** Se debe colocar la llamada en la cláusula `FROM`: `SELECT * FROM fn_nombre_funcion(arg1, arg2);` (si se llama como `SELECT fn_nombre_funcion(...)`, PostgreSQL devuelve una sola columna de tipo compuesto `(col1,col2,...)`).

</details>

---

## 📖 9. Bibliografía y Recursos Recomendados

1. **PostgreSQL Global Development Group.** (2026). *PostgreSQL 16 Official Documentation — Chapter 43: PL/pgSQL — SQL Procedural Language*. Disponible en: `https://www.postgresql.org/docs/current/plpgsql.html`
2. **Riggs, S., & Ciolli, G.** (2022). *PostgreSQL 14 Administration Cookbook*. Packt Publishing.
3. **Schönig, H.-J.** (2023). *Mastering PostgreSQL 15: Advanced techniques to build and administer scalable and reliable PostgreSQL database applications* (5.ª ed.). Packt Publishing.
4. **Instituto Superior Tecnológico de Turismo y Patrimonio Yavirac.** (2026). *Programa de Estudio de la Asignatura (PEA) — Base de Datos Avanzada (DS4AC1-215)*. Quito, Ecuador.

---

<div align="center">

⬅️ [Semana 04: Repaso y Examen Parcial 1](./semana-04-repaso-examen-parcial-1.md) &nbsp;|&nbsp; 🏠 [Volver al Sílabo General (README)](../README.md) &nbsp;|&nbsp; [Semana 06: Fundamentos y Creación de Triggers](./semana-06-fundamentos-creacion-triggers.md) ➡️

</div>
