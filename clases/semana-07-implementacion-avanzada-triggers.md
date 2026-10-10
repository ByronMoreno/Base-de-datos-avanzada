# ⚡ Semana 7: Implementación Avanzada de Triggers en Producción

---

## 📋 1. Portada y Ficha Técnica de la Sesión

| Campo | Detalle Oficial (PEA) |
| :--- | :--- |
| **Institución** | Instituto Superior Tecnológico de Turismo y Patrimonio Yavirac |
| **Carrera** | Tecnología Superior en Desarrollo de Software |
| **Asignatura** | Base de Datos Avanzada |
| **Código de Asignatura** | `DS4AC1-215` |
| **Semestre / Periodo** | Segundo Semestre — Periodo Académico `2026-II` |
| **Modalidad** | Dual |
| **Unidad Curricular** | **Unidad 2:** Generación de procedimientos, funciones y triggers (Cierre de Unidad) |
| **Semana** | Semana 7 de 9 |
| **Carga Horaria Semanal** | **5 Horas Totales** — Aprendizaje en Contacto con el Docente (**ACD**): `2h` \| Aprendizaje Práctico-Experimental en Contacto con el Docente (**APECD**): `3h` |
| **Contenidos del PEA** | Implementación de Trigger |
| **Software y Herramientas** | PostgreSQL 16+, pgAdmin 4 / DBeaver / DataGrip, Terminal `psql`, Git |

---

## 🎯 2. Objetivos, Resultados de Aprendizaje y Competencias

### Objetivo General de la Sesión
Diseñar, implementar y optimizar arquitecturas empresariales de **Triggers en PostgreSQL (PL/pgSQL)** aplicadas a sistemas transaccionales en producción, abarcando control de inventario en tiempo real, auditoría forense diferencial con `JSONB`, sincronización de campos calculados desnormalizados, borrado lógico (*Soft Delete*), vistas actualizables con `INSTEAD OF` y control de recursividad.

### Alineación con el Programa de Estudio de la Asignatura (PEA)

| Componente Curricular | Descripción Oficial según el PEA |
| :--- | :--- |
| **Resultado de Aprendizaje (RdA 2)** | Desarrollo de procedimientos almacenados, funciones o triggers. |
| **Resultado de Aprendizaje (RdA 3)** | Brinda asistencia técnica en el diseño de bases de datos mediante procesos de control y seguimiento de las operaciones para el manejo adecuado de la información. |
| **Competencia Específica** | Administrar y controlar las operaciones de bases de datos mediante mecanismos de seguimiento, integridad y gestión de transacciones que garanticen la confiabilidad de la información. |
| **Actividad ACD (2h)** | Implementar un trigger (Patrones avanzados de arquitectura con Triggers en sistemas en producción). |
| **Actividad APECD (3h)** | Crear e invocar trigger (Taller práctico integrador de cierre de la Unidad 2). |
| **Evidencia de Aprendizaje** | Scripts SQL/PLpgSQL funcionales con motores de reglas de negocio, auditoría `JSONB` y pruebas de validación ante casos borde. |
| **Habilidades Blandas** | Pensamiento sistémico, atención al detalle en integridad financiera, responsabilidad ética en el rastro de auditoría y resolución colaborativa de problemas. |

---

## ⏱️ 3. Agenda Detallada de la Sesión (5 Horas)

| Bloque | Duración | Componente | Tema / Actividad |
| :---: | :---: | :---: | :--- |
| **1** | 30 min | **ACD** | Arquitectura de ejecución de Triggers en producción, orden de disparo y matrices de eventos (`INSERT`, `UPDATE`, `DELETE`). |
| **2** | 35 min | **ACD** | **Patrones 1, 2 y 3:** Control de stock en tiempo real con `RAISE EXCEPTION`, Auditoría forense diferencial con `JSONB` y Mantenimiento de tablas resumen / campos desnormalizados. |
| **3** | 35 min | **ACD** | **Patrones 4 y 5:** Borrado lógico (*Soft Delete*), Triggers `INSTEAD OF` sobre vistas complejas, prevención de recursividad (`pg_trigger_depth()`) y optimización con tablas de transición. |
| **4** | 20 min | **ACD** | Demostración en vivo: Ejecución guiada de los 5 patrones en PostgreSQL y análisis de planes de ejecución. |
| **5** | 150 min | **APECD** | **Taller Práctico Integrador de Unidad 2:** Construcción del motor de reglas de negocio y auditoría forense para la distribuidora *TechAndes S.A.* (5 retos progresivos). |
| **6** | 30 min | **APECD** | Revisión cruzada de código, validación de casos borde, rúbrica de evaluación y cierre de la Unidad 2. |

---

## 📚 4. Desarrollo Teórico-Conceptual Profundo (ACD - 2 Horas)

En la Semana 6 estudiamos la anatomía sintáctica de un *trigger* (`CREATE FUNCTION ... RETURNS TRIGGER` + `CREATE TRIGGER`), las pseudovariables `NEW` y `OLD`, y la diferencia básica entre `BEFORE` y `AFTER`. En esta **Semana 7**, damos el salto de la sintaxis básica a la **ingeniería de software en producción**: ¿cómo se diseñan triggers robustos que soportan miles de operaciones por minuto sin corromper saldos contables ni generar bucles infinitos?

### 4.1. Tubería Completa de Ejecución de Triggers en PostgreSQL

Cuando una aplicación envía una sentencia DML (`INSERT`, `UPDATE` o `DELETE`) a PostgreSQL, el motor ejecuta una secuencia determinista de pasos. Comprender esta tubería es vital para decidir dónde colocar cada regla de negocio:

```mermaid
flowchart TD
    A["Sentencia DML entrante (INSERT / UPDATE / DELETE)"] --> B["1. Triggers BEFORE EACH STATEMENT"]
    B --> C{"¿Objetivo es Tabla o Vista?"}
    C -- "Vista" --> D["2. Triggers INSTEAD OF EACH ROW"]
    D --> H["5. Triggers AFTER EACH STATEMENT"]
    C -- "Tabla Base" --> E["2. Triggers BEFORE EACH ROW (Validar / Mutar NEW)"]
    E --> F{"¿Retorna NULL o lanza RAISE EXCEPTION?"}
    F -- "RAISE EXCEPTION" --> X["ABORTA TODA LA TRANSACCIÓN (Rollback automático de la sentencia)"]
    F -- "Retorna NULL" --> Y["Cancela silenciosamente la operación sobre la fila actual"]
    F -- "Retorna NEW / OLD" --> G["3. Escritura Física de la Fila y Verificación de Constraints (PK, FK, CHECK)"]
    G --> I["4. Triggers AFTER EACH ROW (Auditoría, Tablas Resumen, Stock)"]
    I --> H
    H --> Z["Operación Completada Exitosamente"]
```

> [!IMPORTANT]
> **Regla de Oro en Producción:**
> - Usa **`BEFORE EACH ROW`** para **validar datos** (`RAISE EXCEPTION` si una regla falla) o **normalizar/modificar la propia fila** que se está guardando (`NEW.updated_at := NOW()`).
> - Usa **`AFTER EACH ROW`** cuando necesites **propagar efectos a otras tablas** (descontar inventario en `productos`, recalcular `facturas.total`, o insertar un registro en `auditoria_forense`), porque en el momento `AFTER` ya tienes la certeza de que la fila superó todas las restricciones `NOT NULL`, `UNIQUE`, `CHECK` y `FOREIGN KEY`.

---

### 4.2. Patrón 1: Control de Stock e Inventario en Tiempo Real con Bloqueo de Saldos Negativos

Uno de los errores más frecuentes en desarrolladores junior es programar el trigger de inventario pensando únicamente en el evento `INSERT` de una venta. En un sistema real en producción, un ítem de factura o pedido puede sufrir **tres operaciones distintas**, y el trigger debe manejar la matemática exacta de cada una:

| Operación en `detalle_venta` | Efecto Matemático sobre `productos.stock_actual` | Validación Crítica |
| :--- | :--- | :--- |
| **`INSERT`** | `stock_actual = stock_actual - NEW.cantidad` | Verificar que `stock_actual >= NEW.cantidad` antes de descontar. |
| **`DELETE`** | `stock_actual = stock_actual + OLD.cantidad` | Devolver las unidades al inventario cuando se elimina una línea. |
| **`UPDATE`** (Mismo producto) | `stock_actual = stock_actual + OLD.cantidad - NEW.cantidad` | Si `NEW.cantidad > OLD.cantidad`, verificar disponibilidad de la diferencia `(NEW.cantidad - OLD.cantidad)`. |
| **`UPDATE`** (Cambio de `producto_id`) | Sumar `OLD.cantidad` al producto `OLD.producto_id` y restar `NEW.cantidad` al producto `NEW.producto_id`. | Verificar stock suficiente en el nuevo producto `NEW.producto_id`. |

#### Bloqueo de Filas y `RAISE EXCEPTION` con `SQLSTATE`
Para evitar que dos cajeros vendan simultáneamente la última unidad disponible (*condición de carrera*), dentro de la función trigger realizamos un `SELECT stock_actual INTO v_stock FROM productos WHERE id = NEW.producto_id FOR UPDATE;`. Si el stock resultante sería negativo, abortamos inmediatamente con:

```sql
RAISE EXCEPTION 'Stock insuficiente para el producto ID %. Disponible: %, Solicitado: %',
    NEW.producto_id, v_stock, v_requerido
    USING ERRCODE = 'P0001',
          HINT = 'Solicite reabastecimiento a bodega o reduzca la cantidad del ítem.';
```

---

### 4.3. Patrón 2: Auditoría Forense Avanzada con `JSONB` y Cálculo de Diferencias

En la Semana 6 creamos tablas de auditoría guardando todo el registro antiguo y nuevo. En producción, cuando una tabla tiene 40 columnas y un usuario solo modifica el campo `precio_unitario`, queremos saber **exactamente qué columnas cambiaron**, además del estado completo en formato `JSONB` indexable y los metadatos de red de la conexión.

PostgreSQL provee la función nativa `to_jsonb(record)` que convierte cualquier fila `OLD` o `NEW` en un documento binario `JSONB` sin importar la estructura de la tabla. Esto nos permite crear **una única función de auditoría universal** que sirve para auditar 5, 20 o 100 tablas distintas sin reescribir código.

```mermaid
sequenceDiagram
    autonumber
    participant App as "Aplicación / Usuario"
    participant Tabla as "Tabla de Negocio (ej. productos)"
    participant Trg as "fn_auditoria_forense_jsonb()"
    participant Aud as "Tabla seguridad.bitacora_forense"

    App->>Tabla: UPDATE productos SET precio = 125.00 WHERE id = 10
    Tabla->>Trg: Dispara AFTER UPDATE (pasa OLD y NEW)
    Note over Trg: Convierte to_jsonb(OLD) y to_jsonb(NEW)
    Note over Trg: Calcula jsonb_diff (solo claves modificadas)
    Note over Trg: Captura current_user, inet_client_addr(), txid_current()
    Trg->>Aud: INSERT INTO seguridad.bitacora_forense (...)
    Aud-->>Trg: Confirmación de registro inmutable
    Trg-->>App: Retorna NEW (Transacción continúa)
```

#### Metadatos Forenses Clave en PostgreSQL
- `TG_TABLE_SCHEMA` y `TG_TABLE_NAME`: Esquema y nombre de la tabla afectada.
- `TG_OP`: Operación ejecutada (`'INSERT'`, `'UPDATE'`, `'DELETE'`, `'TRUNCATE'`).
- `session_user` vs `current_user`: Usuario autenticado originalmente vs rol efectivo actual.
- `inet_client_addr()` y `inet_client_port()`: Dirección IP y puerto desde donde se conectó el cliente.
- `current_setting('application_name', true)`: Nombre de la aplicación o microservicio que ejecutó el cambio.
- `txid_current()` / `pg_current_xact_id()`: Identificador único de la transacción (permite agrupar todos los cambios ocurridos dentro de un mismo `BEGIN ... COMMIT`).

---

### 4.4. Patrón 3: Mantenimiento Automático de Tablas Resumen y Campos Calculados Desnormalizados

Aunque la Tercera Forma Normal (3FN) sugiere no almacenar campos calculados como `total_factura` en la tabla `facturas` (pues se pueden obtener con `SUM(subtotal)` desde `detalle_factura`), en sistemas de alto tráfico **consultar sumatorias sobre millones de líneas en cada listado de facturas degrada el rendimiento**.

La solución de ingeniería consiste en aplicar **desnormalización controlada por triggers**:
1. La tabla cabecera `facturas` almacena físicamente las columnas `subtotal`, `iva` y `total`.
2. La tabla `clientes` almacena físicamente la columna `saldo_pendiente`.
3. Un trigger `AFTER INSERT OR UPDATE OR DELETE` en `detalle_factura` calcula el delta exacto (`v_delta := COALESCE(NEW.subtotal_linea, 0) - COALESCE(OLD.subtotal_linea, 0)`) y actualiza de forma atómica tanto la factura como el saldo del cliente.

> [!TIP]
> **¿Actualizar con `SUM()` completo o aplicar el Delta (`NEW - OLD`)?**
> - **Recálculo completo (`SELECT COALESCE(SUM(...), 0)`)**: Es inmune a desincronizaciones previas y muy seguro cuando una factura tiene entre 1 y 100 líneas.
> - **Actualización incremental por Delta (`total = total + v_delta`)**: Es $O(1)$ y no requiere escanear las demás filas del detalle, ideal para tablas resumen mensuales o saldos acumulados con millones de movimientos.

---

### 4.5. Patrón 4: Borrado Lógico (*Soft Delete*) y Triggers `INSTEAD OF` sobre Vistas

En sistemas empresariales, médicos o financieros, **está prohibido eliminar físicamente registros maestros o históricos** (`DELETE FROM clientes`). Sin embargo, a menudo el software heredado (*legacy*) o ciertos ORMs siguen enviando sentencias `DELETE`. Existen dos estrategias profesionales con triggers para resolverlo:

#### Estrategia A: Interceptar `BEFORE DELETE` en la Tabla Base
En un trigger `BEFORE DELETE FOR EACH ROW`, si la función ejecuta un `UPDATE` marcando `activo = FALSE, eliminado_en = NOW()` y luego **retorna `NULL`**, PostgreSQL cancela silenciosamente el borrado físico de la fila pero conserva el `UPDATE` realizado dentro de la función:

```sql
CREATE OR REPLACE FUNCTION fn_soft_delete_tabla()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    UPDATE clientes
       SET activo = FALSE,
           fecha_baja = NOW(),
           usuario_baja = current_user
     WHERE id = OLD.id;

    -- Al retornar NULL en un trigger BEFORE DELETE, el borrado físico se cancela
    RETURN NULL;
END;
$$;
```

#### Estrategia B: Vistas de Negocio con Triggers `INSTEAD OF`
Las vistas que combinan múltiples tablas con `JOIN` o agregaciones no son actualizables directamente por PostgreSQL. Los triggers **`INSTEAD OF`** ("en lugar de") solo pueden definirse sobre **Vistas (`VIEW`)** a nivel `FOR EACH ROW` y le indican al motor exactamente qué hacer en las tablas subyacentes cuando alguien ejecuta `INSERT`, `UPDATE` o `DELETE` contra la vista.

| Característica | Trigger `BEFORE` / `AFTER` | Trigger `INSTEAD OF` |
| :--- | :--- | :--- |
| **Objetos soportados** | Tablas (y vistas extranjeras) | **Exclusivamente Vistas (`VIEW`)** |
| **Granularidad** | `FOR EACH ROW` o `FOR EACH STATEMENT` | **Exclusivamente `FOR EACH ROW`** |
| **Propósito principal** | Validar, transformar o auditar datos | Hacer que vistas complejas (`JOIN`) sean editables y aplicar *Soft Delete* transparente |

---

### 4.6. Patrón 5: Prevención de Recursividad Infinita, Orden de Ejecución y Rendimiento

#### 1. El Peligro de la Recursividad Infinita y `pg_trigger_depth()`
Imagina que un trigger `AFTER UPDATE` sobre la tabla `empleados` ejecuta un `UPDATE empleados SET fecha_modificacion = NOW() WHERE id = NEW.id;`. Ese segundo `UPDATE` volverá a disparar el mismo trigger, el cual hará otro `UPDATE`, provocando un desbordamiento de pila (`stack depth limit exceeded`).
- **Regla 1:** Si necesitas modificar la misma fila que se está actualizando, hazlo en un trigger **`BEFORE UPDATE`** asignando `NEW.fecha_modificacion := NOW();` sin ejecutar otra sentencia `UPDATE`.
- **Regla 2:** Cuando sea estrictamente necesario que un trigger ejecute DML sobre su propia tabla (por ejemplo, recalcular jerarquías o ajustar otra fila de la misma tabla) o exista recursividad mutua entre Tabla A y Tabla B, utiliza la función **`pg_trigger_depth()`**, que devuelve el nivel de anidamiento actual (`0` fuera de triggers, `1` en el primer disparo, `2` en un disparo provocado por otro trigger):

```sql
IF pg_trigger_depth() > 1 THEN
    RETURN NEW; -- Corta la recursividad en el segundo nivel
END IF;
```
También puedes limitar el disparo desde la propia definición DDL del trigger usando la cláusula **`WHEN`**:
```sql
CREATE TRIGGER trg_evitar_recursividad
AFTER UPDATE ON cuentas
FOR EACH ROW
WHEN (pg_trigger_depth() < 1 AND OLD.saldo IS DISTINCT FROM NEW.saldo)
EXECUTE FUNCTION fn_sincronizar_cuentas();
```

#### 2. Orden de Ejecución cuando existen Múltiples Triggers
¿Qué ocurre si una tabla tiene tres triggers `BEFORE UPDATE`?
En PostgreSQL (siguiendo el estándar SQL moderno), los triggers del **mismo momento (`BEFORE`/`AFTER`) y mismo nivel (`STATEMENT`/`ROW`) se ejecutan en estricto ORDEN ALFABÉTICO por su nombre**.
- Por convención profesional, cuando el orden importa se prefijan los nombres con números:
  - `trg_01_normalizar_datos` (se ejecuta primero)
  - `trg_02_validar_reglas_negocio` (recibe el `NEW` ya modificado por `trg_01`)
  - `trg_99_auditoria_forense` (se ejecuta al final)

#### 3. Impacto en el Rendimiento y Tablas de Transición (`REFERENCING`)
Si ejecutas `UPDATE productos SET precio = precio * 1.05;` sobre 50,000 productos:
- Un trigger `FOR EACH ROW` invocará la función PL/pgSQL **50,000 veces**.
- Un trigger `AFTER UPDATE ... REFERENCING OLD TABLE AS tabla_old NEW TABLE AS tabla_new FOR EACH STATEMENT` invocará la función **una sola vez**, entregándole dos tablas temporales en memoria (`tabla_old` y `tabla_new`) para insertar las 50,000 filas de auditoría en una única operación masiva (`INSERT INTO auditoria SELECT ... FROM tabla_new`).

---

## 💻 5. Ejemplos Guiados Paso a Paso en PostgreSQL

A continuación, construimos un laboratorio completo y 100% ejecutable que demuestra en acción los **5 patrones de arquitectura en producción**.

### 5.1. Preparación del Esquema y Tablas del Laboratorio Guiado

```sql
-- ============================================================================
-- LABORATORIO GUIADO SEMANA 7: ARQUITECTURA DE TRIGGERS EN PRODUCCIÓN
-- ============================================================================
DROP SCHEMA IF EXISTS lab_s7 CASCADE;
CREATE SCHEMA lab_s7;
SET search_path TO lab_s7, public;

-- 1. Tabla de Clientes (Con saldo desnormalizado y soporte Soft Delete)
CREATE TABLE clientes (
    cliente_id       SERIAL PRIMARY KEY,
    ruc_cedula       VARCHAR(13) UNIQUE NOT NULL,
    razon_social     VARCHAR(120) NOT NULL,
    cupo_credito     NUMERIC(12,2) NOT NULL DEFAULT 1000.00 CHECK (cupo_credito >= 0),
    saldo_pendiente  NUMERIC(12,2) NOT NULL DEFAULT 0.00 CHECK (saldo_pendiente >= 0),
    activo           BOOLEAN NOT NULL DEFAULT TRUE,
    eliminado_en     TIMESTAMPTZ,
    eliminado_por    VARCHAR(60)
);

-- 2. Tabla de Productos (Control estricto de inventario)
CREATE TABLE productos (
    producto_id      SERIAL PRIMARY KEY,
    sku              VARCHAR(20) UNIQUE NOT NULL,
    nombre           VARCHAR(120) NOT NULL,
    precio_unitario  NUMERIC(12,2) NOT NULL CHECK (precio_unitario > 0),
    stock_actual     INTEGER NOT NULL DEFAULT 0,
    stock_minimo     INTEGER NOT NULL DEFAULT 5,
    alerta_reposicion BOOLEAN NOT NULL DEFAULT FALSE,
    actualizado_en   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Tabla Cabecera de Facturas (Con totales desnormalizados)
CREATE TABLE facturas (
    factura_id       SERIAL PRIMARY KEY,
    cliente_id       INTEGER NOT NULL REFERENCES clientes(cliente_id),
    fecha_emision    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    estado           VARCHAR(20) NOT NULL DEFAULT 'EMITIDA'
                     CHECK (estado IN ('EMITIDA', 'PAGADA', 'ANULADA')),
    subtotal         NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    iva_15           NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    total            NUMERIC(12,2) NOT NULL DEFAULT 0.00
);

-- 4. Tabla Detalle de Facturas
CREATE TABLE detalle_factura (
    detalle_id       SERIAL PRIMARY KEY,
    factura_id       INTEGER NOT NULL REFERENCES facturas(factura_id) ON DELETE CASCADE,
    producto_id      INTEGER NOT NULL REFERENCES productos(producto_id),
    cantidad         INTEGER NOT NULL CHECK (cantidad > 0),
    precio_venta     NUMERIC(12,2) NOT NULL CHECK (precio_venta > 0),
    subtotal_linea   NUMERIC(12,2) NOT NULL DEFAULT 0.00
);

-- 5. Tabla Universal de Auditoría Forense JSONB
CREATE TABLE auditoria_forense (
    auditoria_id     BIGSERIAL PRIMARY KEY,
    fecha_evento     TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    txid             BIGINT NOT NULL DEFAULT txid_current(),
    esquema_tabla    TEXT NOT NULL,
    operacion        VARCHAR(10) NOT NULL,
    usuario_bd       TEXT NOT NULL DEFAULT current_user,
    ip_cliente       INET DEFAULT inet_client_addr(),
    aplicacion       TEXT DEFAULT current_setting('application_name', true),
    datos_anteriores JSONB,
    datos_nuevos     JSONB,
    diferencias      JSONB
);

-- Datos semilla iniciales
INSERT INTO clientes (ruc_cedula, razon_social, cupo_credito) VALUES
('1790011223001', 'Comercializadora Pichincha S.A.', 5000.00),
('1712345678001', 'Inversiones Quiteñas Cía. Ltda.', 800.00);

INSERT INTO productos (sku, nombre, precio_unitario, stock_actual, stock_minimo) VALUES
('LAP-PRO-16', 'Laptop Workstation 16GB RAM', 1200.00, 10, 3),
('MON-4K-27',  'Monitor UltraHD 27 Pulgadas',  350.00,  4, 2),
('TEC-MEC-RGB','Teclado Mecánico Industrial',   80.00, 25, 5);
```

---

### 5.2. Implementación del Patrón 1 y 3: Control de Stock + Cálculo de Línea y Totales de Factura

Observa cómo separamos responsabilidades usando el orden de disparo:
1. Un trigger `BEFORE INSERT OR UPDATE` en `detalle_factura` calcula automáticamente `NEW.subtotal_linea := ROUND(NEW.cantidad * NEW.precio_venta, 2)` y valida/actualiza el stock del producto.
2. Un trigger `AFTER INSERT OR UPDATE OR DELETE` en `detalle_factura` recalcula los totales (`subtotal`, `iva_15`, `total`) en la tabla `facturas` y ajusta el `saldo_pendiente` del cliente verificando que no supere su `cupo_credito`.

```sql
-- ============================================================================
-- PATRÓN 1: CONTROL DE STOCK EN TIEMPO REAL Y CÁLCULO DE SUBTOTAL DE LÍNEA
-- ============================================================================
CREATE OR REPLACE FUNCTION fn_trg_01_control_stock_detalle()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_stock_actual INTEGER;
    v_diferencia   INTEGER;
BEGIN
    -- Caso 1: INSERT (Nueva línea de factura)
    IF TG_OP = 'INSERT' THEN
        -- Bloqueamos la fila del producto para evitar condiciones de carrera
        SELECT stock_actual INTO v_stock_actual
          FROM productos
         WHERE producto_id = NEW.producto_id
           FOR UPDATE;

        IF v_stock_actual < NEW.cantidad THEN
            RAISE EXCEPTION 'STOCK INSUFICIENTE: Producto ID % tiene % unidades disponibles y se intentan facturar %.',
                NEW.producto_id, v_stock_actual, NEW.cantidad
                USING ERRCODE = 'P0001';
        END IF;

        -- Descontamos el stock
        UPDATE productos
           SET stock_actual = stock_actual - NEW.cantidad
         WHERE producto_id = NEW.producto_id;

        -- Calculamos el subtotal de la línea antes de guardar
        NEW.subtotal_linea := ROUND(NEW.cantidad * NEW.precio_venta, 2);
        RETURN NEW;

    -- Caso 2: UPDATE (Modificación de cantidad, precio o cambio de producto)
    ELSIF TG_OP = 'UPDATE' THEN
        -- Si cambió de producto_id, devolvemos stock al producto anterior y descontamos del nuevo
        IF OLD.producto_id <> NEW.producto_id THEN
            UPDATE productos
               SET stock_actual = stock_actual + OLD.cantidad
             WHERE producto_id = OLD.producto_id;

            SELECT stock_actual INTO v_stock_actual
              FROM productos
             WHERE producto_id = NEW.producto_id
               FOR UPDATE;

            IF v_stock_actual < NEW.cantidad THEN
                RAISE EXCEPTION 'STOCK INSUFICIENTE al cambiar al Producto ID %: Disponible %, Solicitado %.',
                    NEW.producto_id, v_stock_actual, NEW.cantidad
                    USING ERRCODE = 'P0001';
            END IF;

            UPDATE productos
               SET stock_actual = stock_actual - NEW.cantidad
             WHERE producto_id = NEW.producto_id;
        ELSE
            -- Es el mismo producto: calculamos la diferencia neta solicitada
            v_diferencia := NEW.cantidad - OLD.cantidad;

            IF v_diferencia > 0 THEN
                SELECT stock_actual INTO v_stock_actual
                  FROM productos
                 WHERE producto_id = NEW.producto_id
                   FOR UPDATE;

                IF v_stock_actual < v_diferencia THEN
                    RAISE EXCEPTION 'STOCK INSUFICIENTE para ampliar cantidad del Producto ID %: Stock adicional disponible %, adicional solicitado %.',
                        NEW.producto_id, v_stock_actual, v_diferencia
                        USING ERRCODE = 'P0001';
                END IF;
            END IF;

            UPDATE productos
               SET stock_actual = stock_actual - v_diferencia
             WHERE producto_id = NEW.producto_id;
        END IF;

        NEW.subtotal_linea := ROUND(NEW.cantidad * NEW.precio_venta, 2);
        RETURN NEW;

    -- Caso 3: DELETE (Eliminación de línea de factura -> devolver stock)
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE productos
           SET stock_actual = stock_actual + OLD.cantidad
         WHERE producto_id = OLD.producto_id;
        RETURN OLD;
    END IF;
END;
$$;

CREATE TRIGGER trg_01_control_stock_detalle
BEFORE INSERT OR UPDATE OR DELETE ON detalle_factura
FOR EACH ROW
EXECUTE FUNCTION fn_trg_01_control_stock_detalle();
```

Ahora implementamos el **Patrón 3 (Sincronización de Totales y Saldo del Cliente)**:

```sql
-- ============================================================================
-- PATRÓN 3: MANTENIMIENTO AUTOMÁTICO DE TOTALES Y CUPO DE CRÉDITO DEL CLIENTE
-- ============================================================================
CREATE OR REPLACE FUNCTION fn_trg_02_sincronizar_totales_factura()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_factura_id     INTEGER;
    v_cliente_id     INTEGER;
    v_total_anterior NUMERIC(12,2);
    v_nuevo_subtotal NUMERIC(12,2);
    v_nuevo_iva      NUMERIC(12,2);
    v_nuevo_total    NUMERIC(12,2);
    v_delta_total    NUMERIC(12,2);
    v_saldo_nuevo    NUMERIC(12,2);
    v_cupo_credito   NUMERIC(12,2);
BEGIN
    -- Determinar qué factura fue afectada
    v_factura_id := COALESCE(NEW.factura_id, OLD.factura_id);

    -- Obtener datos actuales de la cabecera de factura
    SELECT cliente_id, total
      INTO v_cliente_id, v_total_anterior
      FROM facturas
     WHERE factura_id = v_factura_id
       FOR UPDATE;

    -- Recalcular sumatoria exacta desde el detalle
    SELECT COALESCE(SUM(subtotal_linea), 0.00)
      INTO v_nuevo_subtotal
      FROM detalle_factura
     WHERE factura_id = v_factura_id;

    v_nuevo_iva   := ROUND(v_nuevo_subtotal * 0.15, 2);
    v_nuevo_total := v_nuevo_subtotal + v_nuevo_iva;
    v_delta_total := v_nuevo_total - v_total_anterior;

    -- Actualizar cabecera de factura
    UPDATE facturas
       SET subtotal = v_nuevo_subtotal,
           iva_15   = v_nuevo_iva,
           total    = v_nuevo_total
     WHERE factura_id = v_factura_id;

    -- Actualizar saldo pendiente del cliente y validar cupo de crédito
    UPDATE clientes
       SET saldo_pendiente = saldo_pendiente + v_delta_total
     WHERE cliente_id = v_cliente_id
    RETURNING saldo_pendiente, cupo_credito INTO v_saldo_nuevo, v_cupo_credito;

    IF v_saldo_nuevo > v_cupo_credito THEN
        RAISE EXCEPTION 'CUPO DE CRÉDITO EXCEDIDO: El cliente ID % tiene un cupo de $% y su nuevo saldo sería $%.',
            v_cliente_id, v_cupo_credito, v_saldo_nuevo
            USING ERRCODE = 'P0002';
    END IF;

    RETURN NULL; -- En triggers AFTER el valor de retorno se ignora
END;
$$;

CREATE TRIGGER trg_02_sincronizar_totales_factura
AFTER INSERT OR UPDATE OR DELETE ON detalle_factura
FOR EACH ROW
EXECUTE FUNCTION fn_trg_02_sincronizar_totales_factura();
```

---

### 5.3. Implementación del Patrón 2 y 5: Auditoría Forense `JSONB` y Prevención de Recursividad

Creamos primero la función universal de auditoría que extrae únicamente los campos que cambiaron en un `UPDATE`, y luego un trigger en `productos` que demuestra el uso de `pg_trigger_depth()` para evitar recursividad cuando actualiza la bandera `alerta_reposicion`.

```sql
-- ============================================================================
-- PATRÓN 2: AUDITORÍA FORENSE UNIVERSAL CON DIFERENCIAS JSONB
-- ============================================================================
CREATE OR REPLACE FUNCTION fn_auditoria_forense_jsonb()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_old_jsonb JSONB := NULL;
    v_new_jsonb JSONB := NULL;
    v_diff      JSONB := '{}'::JSONB;
    v_key       TEXT;
    v_val       JSONB;
BEGIN
    IF TG_OP IN ('UPDATE', 'DELETE') THEN
        v_old_jsonb := to_jsonb(OLD);
    END IF;

    IF TG_OP IN ('INSERT', 'UPDATE') THEN
        v_new_jsonb := to_jsonb(NEW);
    END IF;

    -- Si es UPDATE, calculamos exactamente qué claves cambiaron (antes vs después)
    IF TG_OP = 'UPDATE' THEN
        FOR v_key, v_val IN SELECT * FROM jsonb_each(v_new_jsonb)
        LOOP
            IF v_old_jsonb -> v_key IS DISTINCT FROM v_val THEN
                v_diff := v_diff || jsonb_build_object(
                    v_key, jsonb_build_object(
                        'antes',   v_old_jsonb -> v_key,
                        'despues', v_val
                    )
                );
            END IF;
        END LOOP;
    END IF;

    INSERT INTO auditoria_forense (
        esquema_tabla, operacion, datos_anteriores, datos_nuevos, diferencias
    ) VALUES (
        TG_TABLE_SCHEMA || '.' || TG_TABLE_NAME,
        TG_OP,
        v_old_jsonb,
        v_new_jsonb,
        CASE WHEN TG_OP = 'UPDATE' THEN v_diff ELSE NULL END
    );

    RETURN COALESCE(NEW, OLD);
END;
$$;

-- Conectamos la misma función de auditoría a múltiples tablas críticas
CREATE TRIGGER trg_99_auditoria_productos
AFTER INSERT OR UPDATE OR DELETE ON productos
FOR EACH ROW EXECUTE FUNCTION fn_auditoria_forense_jsonb();

CREATE TRIGGER trg_99_auditoria_facturas
AFTER INSERT OR UPDATE OR DELETE ON facturas
FOR EACH ROW EXECUTE FUNCTION fn_auditoria_forense_jsonb();

-- ============================================================================
-- PATRÓN 5: PREVENCIÓN DE RECURSIVIDAD CON pg_trigger_depth()
-- ============================================================================
CREATE OR REPLACE FUNCTION fn_verificar_alerta_reposicion()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Si este trigger fue disparado por el propio UPDATE interno, salimos de inmediato
    IF pg_trigger_depth() > 1 THEN
        RETURN NEW;
    END IF;

    UPDATE productos
       SET alerta_reposicion = (NEW.stock_actual <= NEW.stock_minimo),
           actualizado_en    = NOW()
     WHERE producto_id = NEW.producto_id;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_50_alerta_reposicion
AFTER UPDATE OF stock_actual ON productos
FOR EACH ROW
EXECUTE FUNCTION fn_verificar_alerta_reposicion();
```

---

### 5.4. Implementación del Patrón 4: *Soft Delete* y Vista Editable con `INSTEAD OF`

```sql
-- ============================================================================
-- PATRÓN 4: BORRADO LÓGICO (SOFT DELETE) E INSTEAD OF TRIGGER SOBRE VISTA
-- ============================================================================
-- 4A. Impedir borrado físico en tabla clientes y convertirlo en Soft Delete
CREATE OR REPLACE FUNCTION fn_soft_delete_clientes()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE clientes
       SET activo        = FALSE,
           eliminado_en  = NOW(),
           eliminado_por = current_user
     WHERE cliente_id = OLD.cliente_id;

    RAISE NOTICE 'BORRADO LÓGICO APLICADO: El cliente "%" (ID %) fue desactivado sin eliminar su historial.',
        OLD.razon_social, OLD.cliente_id;

    RETURN NULL; -- Cancela el DELETE físico
END;
$$;

CREATE TRIGGER trg_01_soft_delete_clientes
BEFORE DELETE ON clientes
FOR EACH ROW
EXECUTE FUNCTION fn_soft_delete_clientes();

-- 4B. Vista de clientes activos con resumen financiero editable vía INSTEAD OF
CREATE OR REPLACE VIEW vw_clientes_activos AS
SELECT cliente_id,
       ruc_cedula,
       razon_social,
       cupo_credito,
       saldo_pendiente,
       (cupo_credito - saldo_pendiente) AS cupo_disponible
  FROM clientes
 WHERE activo = TRUE;

CREATE OR REPLACE FUNCTION fn_instead_of_vw_clientes_activos()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO clientes (ruc_cedula, razon_social, cupo_credito)
        VALUES (NEW.ruc_cedula, UPPER(TRIM(NEW.razon_social)), COALESCE(NEW.cupo_credito, 1000.00))
        RETURNING cliente_id, ruc_cedula, razon_social, cupo_credito, saldo_pendiente,
                  (cupo_credito - saldo_pendiente)
             INTO NEW;
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE clientes
           SET razon_social = UPPER(TRIM(NEW.razon_social)),
               cupo_credito = NEW.cupo_credito
         WHERE cliente_id = OLD.cliente_id;
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        -- Delegamos al DELETE de la tabla base (que a su vez ejecuta el Soft Delete)
        DELETE FROM clientes WHERE cliente_id = OLD.cliente_id;
        RETURN OLD;
    END IF;
END;
$$;

CREATE TRIGGER trg_instead_of_clientes_activos
INSTEAD OF INSERT OR UPDATE OR DELETE ON vw_clientes_activos
FOR EACH ROW
EXECUTE FUNCTION fn_instead_of_vw_clientes_activos();
```

---

### 5.5. Script de Prueba y Verificación de los 5 Patrones

```sql
-- 1. Crear una factura para Comercializadora Pichincha S.A. (cliente_id = 1, cupo = $5000)
INSERT INTO facturas (cliente_id) VALUES (1); -- Genera factura_id = 1

-- 2. Insertar 2 monitores ($350 c/u) y 1 laptop ($1200)
INSERT INTO detalle_factura (factura_id, producto_id, cantidad, precio_venta)
VALUES (1, 2, 2, 350.00),
       (1, 1, 1, 1200.00);

-- 3. Verificar totales calculados automáticamente en la factura y saldo del cliente
SELECT factura_id, subtotal, iva_15, total FROM facturas WHERE factura_id = 1;
-- Resultado esperado: subtotal = 1900.00 | iva_15 = 285.00 | total = 2185.00

SELECT cliente_id, razon_social, cupo_credito, saldo_pendiente, cupo_disponible
  FROM vw_clientes_activos WHERE cliente_id = 1;
-- Resultado esperado: saldo_pendiente = 2185.00 | cupo_disponible = 2815.00

-- 4. Verificar que el Monitor (tenía stock 4, vendimos 2, mínimo es 2) activó alerta_reposicion = TRUE
SELECT sku, nombre, stock_actual, stock_minimo, alerta_reposicion FROM productos;

-- 5. Probar el Soft Delete desde la vista
DELETE FROM vw_clientes_activos WHERE cliente_id = 2;
SELECT cliente_id, razon_social, activo, eliminado_en, eliminado_por FROM clientes;

-- 6. Consultar las diferencias JSONB registradas en la bitácora forense
SELECT auditoria_id, esquema_tabla, operacion, diferencias
  FROM auditoria_forense
 WHERE operacion = 'UPDATE'
 ORDER BY auditoria_id;
```

---

## 🛠️ 6. Taller Práctico-Experimental en Contacto con el Docente (APECD - 3 Horas)

### Caso de Estudio Integrador de Cierre de Unidad 2: *Distribuidora Mayorista TechAndes S.A.*

La empresa **TechAndes S.A.** requiere blindar su base de datos en PostgreSQL para evitar pérdidas por errores de aplicación. El equipo de arquitectura ha decidido implementar todas las reglas críticas directamente en el motor de base de datos mediante **Triggers y Funciones PL/pgSQL**.

```mermaid
erDiagram
    BODEGAS ||--o{ INVENTARIO_BODEGA : "almacena"
    ARTICULOS ||--o{ INVENTARIO_BODEGA : "tiene stock en"
    CLIENTES_MAYORISTAS ||--o{ ORDENES_PEDIDO : "solicita"
    BODEGAS ||--o{ ORDENES_PEDIDO : "despacha desde"
    ORDENES_PEDIDO ||--|{ DETALLE_ORDEN : "contiene"
    ARTICULOS ||--o{ DETALLE_ORDEN : "incluye"

    BODEGAS {
        int bodega_id PK
        varchar codigo_bodega UK
        varchar ciudad
        boolean activa
    }
    ARTICULOS {
        int articulo_id PK
        varchar codigo_barra UK
        varchar descripcion
        numeric costo_promedio
        numeric precio_mayorista
        boolean activo
    }
    INVENTARIO_BODEGA {
        int bodega_id PK, FK
        int articulo_id PK, FK
        int existencia_actual
        int punto_reorden
        timestamptz ultima_salida
    }
    CLIENTES_MAYORISTAS {
        int mayorista_id PK
        varchar ruc UK
        varchar nombre_comercial
        numeric limite_credito
        numeric deuda_acumulada
        boolean activo
        timestamptz fecha_inactivacion
    }
    ORDENES_PEDIDO {
        int orden_id PK
        int mayorista_id FK
        int bodega_id FK
        varchar estado_orden
        numeric subtotal_bruto
        numeric monto_descuento
        numeric monto_iva
        numeric total_neto
        timestamptz creado_en
    }
    DETALLE_ORDEN {
        int item_id PK
        int orden_id FK
        int articulo_id FK
        int cantidad
        numeric precio_unitario
        numeric porcentaje_descuento
        numeric total_linea
    }
```

### 6.1. Script Base del Taller (Ejecutar antes de iniciar los retos)

```sql
-- ============================================================================
-- TALLER APECD SEMANA 7: MOTOR DE REGLAS Y AUDITORÍA TECHANDES S.A.
-- ============================================================================
DROP SCHEMA IF EXISTS techandes CASCADE;
CREATE SCHEMA techandes;
SET search_path TO techandes, public;

CREATE TABLE bodegas (
    bodega_id     SERIAL PRIMARY KEY,
    codigo_bodega VARCHAR(15) UNIQUE NOT NULL,
    ciudad        VARCHAR(60) NOT NULL,
    activa        BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE articulos (
    articulo_id      SERIAL PRIMARY KEY,
    codigo_barra     VARCHAR(25) UNIQUE NOT NULL,
    descripcion      VARCHAR(150) NOT NULL,
    costo_promedio   NUMERIC(12,2) NOT NULL CHECK (costo_promedio > 0),
    precio_mayorista NUMERIC(12,2) NOT NULL CHECK (precio_mayorista > 0),
    activo           BOOLEAN NOT NULL DEFAULT TRUE,
     fecha_baja       TIMESTAMPTZ
);

CREATE TABLE inventario_bodega (
    bodega_id         INTEGER NOT NULL REFERENCES bodegas(bodega_id),
    articulo_id       INTEGER NOT NULL REFERENCES articulos(articulo_id),
    existencia_actual INTEGER NOT NULL DEFAULT 0,
    punto_reorden     INTEGER NOT NULL DEFAULT 10,
    ultima_salida     TIMESTAMPTZ,
    PRIMARY KEY (bodega_id, articulo_id)
);

CREATE TABLE clientes_mayoristas (
    mayorista_id       SERIAL PRIMARY KEY,
    ruc                VARCHAR(13) UNIQUE NOT NULL,
    nombre_comercial   VARCHAR(120) NOT NULL,
    limite_credito     NUMERIC(12,2) NOT NULL DEFAULT 3000.00,
    deuda_acumulada    NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    activo             BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_inactivacion TIMESTAMPTZ
);

CREATE TABLE ordenes_pedido (
    orden_id        SERIAL PRIMARY KEY,
    mayorista_id    INTEGER NOT NULL REFERENCES clientes_mayoristas(mayorista_id),
    bodega_id       INTEGER NOT NULL REFERENCES bodegas(bodega_id),
    estado_orden    VARCHAR(20) NOT NULL DEFAULT 'ABIERTA'
                    CHECK (estado_orden IN ('ABIERTA', 'CONFIRMADA', 'ANULADA')),
    subtotal_bruto  NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    monto_descuento NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    monto_iva       NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    total_neto      NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    creado_en       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE detalle_orden (
    item_id              SERIAL PRIMARY KEY,
    orden_id             INTEGER NOT NULL REFERENCES ordenes_pedido(orden_id) ON DELETE CASCADE,
    articulo_id          INTEGER NOT NULL REFERENCES articulos(articulo_id),
    cantidad             INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario      NUMERIC(12,2) NOT NULL CHECK (precio_unitario > 0),
    porcentaje_descuento NUMERIC(5,2) NOT NULL DEFAULT 0.00
                         CHECK (porcentaje_descuento BETWEEN 0 AND 30),
    total_linea          NUMERIC(12,2) NOT NULL DEFAULT 0.00
);

CREATE TABLE bitacora_cambios_jsonb (
    log_id         BIGSERIAL PRIMARY KEY,
    momento        TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    txid           BIGINT NOT NULL DEFAULT txid_current(),
    tabla          VARCHAR(60) NOT NULL,
    operacion      VARCHAR(10) NOT NULL,
    usuario        VARCHAR(60) NOT NULL DEFAULT current_user,
    estado_previo  JSONB,
    estado_actual  JSONB,
    campos_mutados JSONB
);

-- Datos semilla
INSERT INTO bodegas (codigo_bodega, ciudad) VALUES
('BOD-UIO-01', 'Quito'),
('BOD-GYE-01', 'Guayaquil');

INSERT INTO articulos (codigo_barra, descripcion, costo_promedio, precio_mayorista) VALUES
('78610001', 'Router Empresarial Wi-Fi 6E Dual WAN', 140.00, 210.00),
('78610002', 'Switch Administrable PoE+ 24 Puertos', 260.00, 390.00),
('78610003', 'Bobina Cable UTP Cat 6A 305m Blindado', 110.00, 165.00);

INSERT INTO inventario_bodega (bodega_id, articulo_id, existencia_actual, punto_reorden) VALUES
(1, 1, 15, 5),
(1, 2,  8, 3),
(1, 3, 30, 10),
(2, 1,  6, 4),
(2, 2,  4, 2);

INSERT INTO clientes_mayoristas (ruc, nombre_comercial, limite_credito) VALUES
('1792345678001', 'Redes & Telecomunicaciones del Ecuador S.A.', 4500.00),
('0991122334001', 'Soluciones Digitales del Pacífico Cía. Ltda.', 1500.00);
```

---

### 6.2. Enunciados de los Retos del Taller

#### Reto 1: Trigger de Validación de Precio Mínimo y Control de Inventario por Bodega (`BEFORE INSERT OR UPDATE OR DELETE` en `detalle_orden`)
Crea la función `fn_trg_detalle_orden_inventario()` y su trigger `trg_01_detalle_orden_inventario`:
1. En `INSERT` o `UPDATE`, verifica que la orden padre (`ordenes_pedido`) esté en estado `'ABIERTA'`. Si está `'CONFIRMADA'` o `'ANULADA'`, lanza `RAISE EXCEPTION` impidiendo modificar sus ítems.
2. Verifica que el precio neto unitario después del descuento (`precio_unitario * (1 - porcentaje_descuento / 100.0)`) **nunca sea inferior al `costo_promedio` del artículo** (prohibido vender a pérdida).
3. Calcula automáticamente `NEW.total_linea := ROUND(NEW.cantidad * NEW.precio_unitario * (1 - NEW.porcentaje_descuento / 100.0), 2)`.
4. Descuenta o revierte `existencia_actual` en la tabla `inventario_bodega` correspondiente a la `bodega_id` de la orden padre, bloqueando saldos negativos con `RAISE EXCEPTION` y actualizando `ultima_salida = NOW()`.

<details>
<summary>✅ Ver Solución Propuesta — Reto 1</summary>

```sql
CREATE OR REPLACE FUNCTION fn_trg_detalle_orden_inventario()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_bodega_id   INTEGER;
    v_estado      VARCHAR(20);
    v_costo_prom  NUMERIC(12,2);
    v_precio_neto NUMERIC(12,2);
    v_stock_bod   INTEGER;
    v_delta_cant  INTEGER;
BEGIN
    -- Obtener bodega y estado de la orden padre
    SELECT bodega_id, estado_orden
      INTO v_bodega_id, v_estado
      FROM ordenes_pedido
     WHERE orden_id = COALESCE(NEW.orden_id, OLD.orden_id);

    IF v_estado <> 'ABIERTA' THEN
        RAISE EXCEPTION 'ORDEN BLOQUEADA: No se permiten cambios en la orden % porque su estado es %.',
            COALESCE(NEW.orden_id, OLD.orden_id), v_estado
            USING ERRCODE = 'P0010';
    END IF;

    -- Validaciones para INSERT y UPDATE
    IF TG_OP IN ('INSERT', 'UPDATE') THEN
        SELECT costo_promedio INTO v_costo_prom
          FROM articulos
         WHERE articulo_id = NEW.articulo_id;

        v_precio_neto := ROUND(NEW.precio_unitario * (1.0 - (NEW.porcentaje_descuento / 100.0)), 2);

        IF v_precio_neto < v_costo_prom THEN
            RAISE EXCEPTION 'VENTA BAJO COSTO PROHIBIDA: Artículo ID % tiene costo promedio $% y el precio neto con descuento es $%.',
                NEW.articulo_id, v_costo_prom, v_precio_neto
                USING ERRCODE = 'P0011';
        END IF;

        NEW.total_linea := ROUND(NEW.cantidad * v_precio_neto, 2);
    END IF;

    -- Gestión de Inventario en la Bodega asignada a la orden
    IF TG_OP = 'INSERT' THEN
        SELECT existencia_actual INTO v_stock_bod
          FROM inventario_bodega
         WHERE bodega_id = v_bodega_id AND articulo_id = NEW.articulo_id
           FOR UPDATE;

        IF v_stock_bod IS NULL OR v_stock_bod < NEW.cantidad THEN
            RAISE EXCEPTION 'STOCK INSUFICIENTE en Bodega ID % para Artículo ID %: Disponible %, Solicitado %.',
                v_bodega_id, NEW.articulo_id, COALESCE(v_stock_bod, 0), NEW.cantidad
                USING ERRCODE = 'P0012';
        END IF;

        UPDATE inventario_bodega
           SET existencia_actual = existencia_actual - NEW.cantidad,
               ultima_salida     = NOW()
         WHERE bodega_id = v_bodega_id AND articulo_id = NEW.articulo_id;

        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        v_delta_cant := NEW.cantidad - OLD.cantidad;

        IF v_delta_cant > 0 THEN
            SELECT existencia_actual INTO v_stock_bod
              FROM inventario_bodega
             WHERE bodega_id = v_bodega_id AND articulo_id = NEW.articulo_id
               FOR UPDATE;

            IF v_stock_bod < v_delta_cant THEN
                RAISE EXCEPTION 'STOCK INSUFICIENTE en Bodega ID % para incrementar cantidad: Disponible %, Adicional solicitado %.',
                    v_bodega_id, v_stock_bod, v_delta_cant
                    USING ERRCODE = 'P0012';
            END IF;
        END IF;

        UPDATE inventario_bodega
           SET existencia_actual = existencia_actual - v_delta_cant,
               ultima_salida     = NOW()
         WHERE bodega_id = v_bodega_id AND articulo_id = NEW.articulo_id;

        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        UPDATE inventario_bodega
           SET existencia_actual = existencia_actual + OLD.cantidad
         WHERE bodega_id = v_bodega_id AND articulo_id = OLD.articulo_id;

        RETURN OLD;
    END IF;
END;
$$;

CREATE TRIGGER trg_01_detalle_orden_inventario
BEFORE INSERT OR UPDATE OR DELETE ON detalle_orden
FOR EACH ROW
EXECUTE FUNCTION fn_trg_detalle_orden_inventario();
```
</details>

---

#### Reto 2: Trigger de Recálculo de Cabecera de Orden y Control de Límite de Crédito (`AFTER INSERT OR UPDATE OR DELETE` en `detalle_orden`)
Crea la función `fn_trg_recalcular_orden_y_credito()` y el trigger `trg_02_recalcular_orden_y_credito`:
1. Recalcula en `ordenes_pedido` los campos:
   - `subtotal_bruto = SUM(cantidad * precio_unitario)`
   - `monto_descuento = SUM(cantidad * precio_unitario) - SUM(total_linea)`
   - `monto_iva = ROUND(SUM(total_linea) * 0.15, 2)`
   - `total_neto = SUM(total_linea) + monto_iva`
2. Ajusta la columna `deuda_acumulada` en `clientes_mayoristas` sumando la diferencia entre el nuevo `total_neto` y el `total_neto` anterior.
3. Si `deuda_acumulada > limite_credito`, lanza `RAISE EXCEPTION` abortando la operación.

<details>
<summary>✅ Ver Solución Propuesta — Reto 2</summary>

```sql
CREATE OR REPLACE FUNCTION fn_trg_recalcular_orden_y_credito()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_orden_id       INTEGER;
    v_mayorista_id   INTEGER;
    v_total_previo   NUMERIC(12,2);
    v_bruto          NUMERIC(12,2);
    v_neto_lineas    NUMERIC(12,2);
    v_descuento      NUMERIC(12,2);
    v_iva            NUMERIC(12,2);
    v_total_nuevo    NUMERIC(12,2);
    v_delta_deuda    NUMERIC(12,2);
    v_deuda_actual   NUMERIC(12,2);
    v_limite_credito NUMERIC(12,2);
BEGIN
    v_orden_id := COALESCE(NEW.orden_id, OLD.orden_id);

    SELECT mayorista_id, total_neto
      INTO v_mayorista_id, v_total_previo
      FROM ordenes_pedido
     WHERE orden_id = v_orden_id
       FOR UPDATE;

    SELECT COALESCE(SUM(ROUND(cantidad * precio_unitario, 2)), 0.00),
           COALESCE(SUM(total_linea), 0.00)
      INTO v_bruto, v_neto_lineas
      FROM detalle_orden
     WHERE orden_id = v_orden_id;

    v_descuento   := v_bruto - v_neto_lineas;
    v_iva         := ROUND(v_neto_lineas * 0.15, 2);
    v_total_nuevo := v_neto_lineas + v_iva;
    v_delta_deuda := v_total_nuevo - v_total_previo;

    UPDATE ordenes_pedido
       SET subtotal_bruto  = v_bruto,
           monto_descuento = v_descuento,
           monto_iva       = v_iva,
           total_neto      = v_total_nuevo
     WHERE orden_id = v_orden_id;

    UPDATE clientes_mayoristas
       SET deuda_acumulada = deuda_acumulada + v_delta_deuda
     WHERE mayorista_id = v_mayorista_id
    RETURNING deuda_acumulada, limite_credito INTO v_deuda_actual, v_limite_credito;

    IF v_deuda_actual > v_limite_credito THEN
        RAISE EXCEPTION 'LÍMITE DE CRÉDITO SUPERADO: Mayorista ID % tiene límite $% y su deuda subiría a $%.',
            v_mayorista_id, v_limite_credito, v_deuda_actual
            USING ERRCODE = 'P0013';
    END IF;

    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_02_recalcular_orden_y_credito
AFTER INSERT OR UPDATE OR DELETE ON detalle_orden
FOR EACH ROW
EXECUTE FUNCTION fn_trg_recalcular_orden_y_credito();
```
</details>

---

#### Reto 3: Trigger de Anulación Automática de Orden con Devolución de Stock y Liberación de Cupo (`AFTER UPDATE OF estado_orden` en `ordenes_pedido`)
Cuando una orden pasa de `'ABIERTA'` o `'CONFIRMADA'` al estado `'ANULADA'`, el sistema debe devolver automáticamente todas las unidades de esa orden a `inventario_bodega` y restar el `total_neto` de la `deuda_acumulada` del cliente mayorista. Además, usa `pg_trigger_depth()` o cláusula `WHEN` para evitar ciclos innecesarios.

<details>
<summary>✅ Ver Solución Propuesta — Reto 3</summary>

```sql
CREATE OR REPLACE FUNCTION fn_trg_anular_orden_reversion()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF OLD.estado_orden <> 'ANULADA' AND NEW.estado_orden = 'ANULADA' THEN
        -- 1. Devolver el stock de todos los ítems de la orden a la bodega respectiva
        UPDATE inventario_bodega ib
           SET existencia_actual = ib.existencia_actual + d.cantidad
          FROM detalle_orden d
         WHERE d.orden_id    = NEW.orden_id
           AND ib.bodega_id  = NEW.bodega_id
           AND ib.articulo_id = d.articulo_id;

        -- 2. Liberar la deuda acumulada del cliente mayorista
        UPDATE clientes_mayoristas
           SET deuda_acumulada = GREATEST(0.00, deuda_acumulada - NEW.total_neto)
         WHERE mayorista_id = NEW.mayorista_id;

        RAISE NOTICE 'Orden ID % ANULADA: Stock reintegrado a bodega % y deuda de $% liberada al cliente %.',
            NEW.orden_id, NEW.bodega_id, NEW.total_neto, NEW.mayorista_id;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_03_anular_orden_reversion
AFTER UPDATE OF estado_orden ON ordenes_pedido
FOR EACH ROW
WHEN (OLD.estado_orden IS DISTINCT FROM NEW.estado_orden)
EXECUTE FUNCTION fn_trg_anular_orden_reversion();
```
</details>

---

#### Reto 4: Trigger de Auditoría Forense Diferencial `JSONB` (`AFTER INSERT OR UPDATE OR DELETE`)
Implementa la función `fn_trg_bitacora_jsonb()` que registre en `bitacora_cambios_jsonb` todos los cambios sobre `articulos`, `inventario_bodega` y `ordenes_pedido`, almacenando en `campos_mutados` únicamente los atributos que cambiaron de valor durante un `UPDATE`.

<details>
<summary>✅ Ver Solución Propuesta — Reto 4</summary>

```sql
CREATE OR REPLACE FUNCTION fn_trg_bitacora_jsonb()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_prev JSONB := NULL;
    v_curr JSONB := NULL;
    v_diff JSONB := '{}'::JSONB;
    v_k    TEXT;
    v_v    JSONB;
BEGIN
    IF TG_OP IN ('UPDATE', 'DELETE') THEN
        v_prev := to_jsonb(OLD);
    END IF;

    IF TG_OP IN ('INSERT', 'UPDATE') THEN
        v_curr := to_jsonb(NEW);
    END IF;

    IF TG_OP = 'UPDATE' THEN
        FOR v_k, v_v IN SELECT * FROM jsonb_each(v_curr)
        LOOP
            IF v_prev -> v_k IS DISTINCT FROM v_v THEN
                v_diff := v_diff || jsonb_build_object(
                    v_k, jsonb_build_object('antes', v_prev -> v_k, 'despues', v_v)
                );
            END IF;
        END LOOP;
    END IF;

    INSERT INTO bitacora_cambios_jsonb (
        tabla, operacion, estado_previo, estado_actual, campos_mutados
    ) VALUES (
        TG_TABLE_NAME, TG_OP, v_prev, v_curr,
        CASE WHEN TG_OP = 'UPDATE' THEN v_diff ELSE NULL END
    );

    RETURN COALESCE(NEW, OLD);
END;
$$;

CREATE TRIGGER trg_99_audit_articulos
AFTER INSERT OR UPDATE OR DELETE ON articulos
FOR EACH ROW EXECUTE FUNCTION fn_trg_bitacora_jsonb();

CREATE TRIGGER trg_99_audit_inventario
AFTER INSERT OR UPDATE OR DELETE ON inventario_bodega
FOR EACH ROW EXECUTE FUNCTION fn_trg_bitacora_jsonb();

CREATE TRIGGER trg_99_audit_ordenes
AFTER INSERT OR UPDATE OR DELETE ON ordenes_pedido
FOR EACH ROW EXECUTE FUNCTION fn_trg_bitacora_jsonb();
```
</details>

---

#### Reto 5: Vista de Catálogo por Bodega con `INSTEAD OF` Trigger y *Soft Delete* de Artículos
1. Crea un trigger `BEFORE DELETE` en `articulos` que impida el borrado físico y en su lugar marque `activo = FALSE, fecha_baja = NOW()`.
2. Crea la vista `vw_stock_bodega_quito` que muestre `articulo_id`, `codigo_barra`, `descripcion`, `precio_mayorista` y `existencia_actual` para la bodega `'BOD-UIO-01'` solo de artículos activos.
3. Crea un trigger `INSTEAD OF UPDATE OR DELETE` sobre `vw_stock_bodega_quito` que permita actualizar directamente el `precio_mayorista` (en `articulos`) y la `existencia_actual` (en `inventario_bodega`), o desactivar el artículo cuando se ejecute `DELETE` sobre la vista.

<details>
<summary>✅ Ver Solución Propuesta — Reto 5</summary>

```sql
-- 1. Soft Delete en articulos
CREATE OR REPLACE FUNCTION fn_soft_delete_articulos()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE articulos
       SET activo     = FALSE,
           fecha_baja = NOW()
     WHERE articulo_id = OLD.articulo_id;
    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_01_soft_delete_articulos
BEFORE DELETE ON articulos
FOR EACH ROW
EXECUTE FUNCTION fn_soft_delete_articulos();

-- 2. Vista de stock en Bodega Quito
CREATE OR REPLACE VIEW vw_stock_bodega_quito AS
SELECT a.articulo_id,
       a.codigo_barra,
       a.descripcion,
       a.precio_mayorista,
       ib.existencia_actual
  FROM articulos a
  JOIN inventario_bodega ib ON ib.articulo_id = a.articulo_id
  JOIN bodegas b            ON b.bodega_id = ib.bodega_id
 WHERE b.codigo_bodega = 'BOD-UIO-01'
   AND a.activo = TRUE;

-- 3. Trigger INSTEAD OF sobre la vista
CREATE OR REPLACE FUNCTION fn_instead_of_vw_stock_quito()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        UPDATE articulos
           SET descripcion      = NEW.descripcion,
               precio_mayorista = NEW.precio_mayorista
         WHERE articulo_id = OLD.articulo_id;

        UPDATE inventario_bodega ib
           SET existencia_actual = NEW.existencia_actual
          FROM bodegas b
         WHERE ib.bodega_id   = b.bodega_id
           AND b.codigo_bodega = 'BOD-UIO-01'
           AND ib.articulo_id = OLD.articulo_id;

        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        DELETE FROM articulos WHERE articulo_id = OLD.articulo_id;
        RETURN OLD;
    END IF;
END;
$$;

CREATE TRIGGER trg_instead_of_vw_stock_quito
INSTEAD OF UPDATE OR DELETE ON vw_stock_bodega_quito
FOR EACH ROW
EXECUTE FUNCTION fn_instead_of_vw_stock_quito();
```
</details>

---

## 🚀 7. Actividades de Refuerzo Autónomo

1. **Tablas de Transición (`REFERENCING NEW TABLE AS ...`):** Investiga e implementa una versión `FOR EACH STATEMENT` del trigger de auditoría forense de `productos` empleando tablas de transición, y compara con `EXPLAIN ANALYZE` el tiempo de ejecución al actualizar 10,000 registros de golpe frente al trigger `FOR EACH ROW`.
2. **Triggers Condicionales con Cláusula `WHEN`:** Refactoriza los triggers del taller para que el trigger de auditoría de `articulos` solo se dispare cuando cambie `costo_promedio`, `precio_mayorista` o `activo`, ignorando actualizaciones cosméticas en `descripcion`.

---

## 📊 8. Rúbrica de Evaluación y Autoevaluación

### 8.1. Rúbrica Oficial del Taller Práctico (APECD — 10 Puntos)

| Criterio de Evaluación | Excelente (100%) | Satisfactorio (75%) | En Proceso (50%) | Insuficiente (0-25%) | Puntaje |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **1. Control de Stock y Validación de Costos (Reto 1)** | Gestiona `INSERT`, `UPDATE` y `DELETE` con bloqueo `FOR UPDATE`, valida venta bajo costo y bloquea saldos negativos con `RAISE EXCEPTION`. | Gestiona `INSERT` y `DELETE` correctamente pero omite el diferencial en `UPDATE` o el bloqueo de fila. | Solo descuenta stock en `INSERT` sin validar saldos negativos. | El trigger presenta errores de sintaxis o no compila. | **3.0 pts** |
| **2. Sincronización Desnormalizada y Crédito (Retos 2 y 3)** | Recalcula subtotal, descuento, IVA y total en cabecera, controla cupo del cliente y revierte stock/deuda al anular la orden. | Recalcula cabecera de orden pero no sincroniza o valida el límite de crédito del cliente. | Calcula totales con errores aritméticos o sin considerar eliminaciones. | No logra mantener sincronizada la tabla cabecera. | **3.0 pts** |
| **3. Auditoría Forense `JSONB` Diferencial (Reto 4)** | Registra `to_jsonb(OLD)`, `to_jsonb(NEW)` y construye el objeto `campos_mutados` únicamente con las llaves modificadas. | Registra `OLD` y `NEW` en `JSONB` pero no calcula el diferencial de claves modificadas. | Guarda texto plano o audita solo una operación DML. | No implementa el trigger de auditoría. | **2.0 pts** |
| **4. *Soft Delete* y `INSTEAD OF` sobre Vistas (Reto 5)** | Implementa borrado lógico retornando `NULL` en `BEFORE DELETE` y hace editable la vista `JOIN` mediante `INSTEAD OF`. | Implementa el *Soft Delete* en tabla pero falla en la propagación del `INSTEAD OF` en la vista. | Solo crea la vista sin el trigger `INSTEAD OF`. | No comprende la diferencia entre `BEFORE` e `INSTEAD OF`. | **2.0 pts** |
| **TOTAL** | | | | | **10.0 pts** |

---

### 8.2. Preguntas de Autoevaluación

1. **¿Qué ocurre exactamente cuando una función de trigger `BEFORE DELETE FOR EACH ROW` ejecuta un `UPDATE` sobre la misma tabla y finaliza con `RETURN NULL;`?**
   <details>
   <summary>Ver respuesta</summary>
   PostgreSQL cancela silenciosamente la eliminación física de la fila (`DELETE`), pero conserva los cambios realizados por la sentencia `UPDATE` previa dentro de la misma transacción. Este es el mecanismo estándar para implementar *Soft Delete* transparente a nivel de tabla.
   </details>

2. **Si una tabla tiene definidos los triggers `trg_validar_stock`, `trg_auditar_operacion` y `trg_ajustar_descuento`, todos configurados como `BEFORE INSERT FOR EACH ROW`, ¿en qué orden exacto los ejecuta PostgreSQL?**
   <details>
   <summary>Ver respuesta</summary>
   Los ejecuta en **orden alfabético estricto**: primero `trg_ajustar_descuento`, segundo `trg_auditar_operacion` y tercero `trg_validar_stock`. Por ello se recomienda usar prefijos numéricos (`trg_01_...`, `trg_02_...`, `trg_99_...`).
   </details>

3. **¿Por qué no es posible crear un trigger `BEFORE UPDATE` sobre una vista compleja con `JOIN`, y qué tipo de trigger debe utilizarse en su lugar?**
   <details>
   <summary>Ver respuesta</summary>
   Porque una vista no almacena tuplas físicas; es una consulta virtual. Para interceptar operaciones `INSERT`, `UPDATE` o `DELETE` sobre vistas con `JOIN` o agregaciones se debe utilizar un trigger **`INSTEAD OF ... FOR EACH ROW`**, el cual reemplaza la operación sobre la vista por las sentencias DML correspondientes sobre las tablas base.
   </details>

4. **¿Para qué sirve la función `pg_trigger_depth()` y qué valor devuelve cuando un usuario ejecuta directamente un `UPDATE` desde su aplicación?**
   <details>
   <summary>Ver respuesta</summary>
   Devuelve el nivel actual de anidamiento de triggers. Cuando la sentencia proviene directamente del usuario o aplicación, fuera del trigger vale `0` y dentro del primer trigger disparado vale `1`. Si ese trigger ejecuta otro `UPDATE` que vuelve a disparar un trigger, en el segundo nivel `pg_trigger_depth()` vale `2`. Es fundamental para cortar la recursividad infinita (`IF pg_trigger_depth() > 1 THEN RETURN NEW; END IF;`).
   </details>

5. **En una función trigger de control de inventario, ¿por qué ocurre una inconsistencia grave si solo programamos `stock = stock - NEW.cantidad` sin distinguir entre `INSERT` y `UPDATE`?**
   <details>
   <summary>Ver respuesta</summary>
   Porque si un ítem tenía originalmente `cantidad = 5` (ya descontadas en el `INSERT`) y luego se actualiza a `cantidad = 7` mediante un `UPDATE`, restar `NEW.cantidad` volvería a descontar 7 unidades adicionales (12 en total en vez de 7). En un `UPDATE` sobre el mismo producto solo debe descontarse la diferencia neta: `NEW.cantidad - OLD.cantidad`.
   </details>

---

## 📖 9. Bibliografía y Recursos Recomendados

- **Silberschatz, A., Korth, H. F., & Sudarshan, S. (2014).** *Fundamentos de bases de datos* (6.ª ed.). McGraw-Hill. (Capítulo 5: SQL Avanzado — Disparadores y Reglas Activas).
- **Date, C. J. (2001).** *Introducción a los sistemas de bases de datos* (7.ª ed.). Pearson Educación.
- **Kroenke, D. M. (2003).** *Procesamiento de bases de datos: Fundamentos, diseño e implementación* (8.ª ed.). Pearson Educación.
- **PostgreSQL Global Development Group. (2026).** *PostgreSQL 16 Official Documentation — Chapter 38: Triggers & Chapter 43: PL/pgSQL Trigger Functions*. Disponible en: `https://www.postgresql.org/docs/current/triggers.html`

---

<div align="center">

⬅️ [Semana 6: Fundamentos y Creación de Triggers](./semana-06-fundamentos-creacion-triggers.md) &nbsp;&nbsp;|&nbsp;&nbsp; 🏠 [Volver al Sílabo Principal](../README.md) &nbsp;&nbsp;|&nbsp;&nbsp; ➡️ [Semana 8: Transacciones, Concurrencia y Seguridad (Roles y Usuarios)](./semana-08-transacciones-concurrencia-seguridad-roles.md)

</div>
