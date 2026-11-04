# 📝 Semana 2 — Guía de 30 Ejercicios Prácticos de SQL (Base de Datos Real Employees de Neon)

> **Instituto Superior Tecnológico de Turismo y Patrimonio Yavirac**  
> **Carrera:** Tecnología Superior en Desarrollo de Software  
> **Asignatura:** Base de Datos Avanzada (`DS4AC1-215`) | **Paralelo:** D  
> **Docente:** Ing. Byron Moreno  
> **Periodo Académico:** 2026-II | **Modalidad:** Dual  
> **Banco de Datos:** 🐘 Base de datos real `Employees` de Neon (~3.9 millones de filas / 6 tablas normalizadas)  
> **Documento:** Guía de Práctica y Enunciados de Estudio Autónomo y Laboratorio

---

## 🎯 Objetivos de Aprendizaje
Al resolver estos 30 ejercicios, el estudiante:
1. Domina el filtrado preciso de registros mediante `WHERE` con operadores relacionales, lógicos y de fecha.
2. Aplica búsquedas por patrones de texto utilizando comodines con `LIKE` (prefijos, sufijos y caracteres individuales).
3. Evalúa pertenencia y exclusión en rangos continuos con `BETWEEN` y conjuntos discretos con `IN` / `NOT IN`.
4. Organiza y presenta la información de forma profesional mediante `ORDER BY` y límites con `LIMIT`.
5. Ejecuta resúmenes estadísticos corporativos mediante funciones de agregación (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`).
6. Agrupa información con `GROUP BY` y aplica condiciones sobre grupos agregados utilizando `HAVING`.

---

## 🧭 Resumen Rápido de Sintaxis SQL Clave

| Cláusula / Operador | Propósito | Ejemplo en Employees |
| :--- | :--- | :--- |
| `WHERE` | Filtra filas según condiciones lógicas | `WHERE gender = 'F'` |
| `ORDER BY` | Ordena los resultados (`ASC` o `DESC`) | `ORDER BY salary DESC` |
| `LIMIT` | Restringe el número máximo de filas devueltas | `LIMIT 10` |
| `LIKE 'A%'` | Coincide con cadenas que inician con 'A' | `WHERE first_name LIKE 'Mar%'` |
| `LIKE '%son'` | Coincide con cadenas que terminan en 'son' | `WHERE last_name LIKE '%son'` |
| `LIKE '_am'` | El guion bajo `_` coincide con 1 carácter exacto | `WHERE first_name LIKE 'A_am'` |
| `BETWEEN a AND b` | Evalúa rangos continuos inclusivos | `WHERE salary BETWEEN 50000 AND 70000` |
| `IN (v1, v2, ...)` | Comprueba si el valor pertenece a la lista | `WHERE dept_no IN ('d001', 'd005')` |
| `NOT IN (...)` | Excluye registros que coincidan con la lista | `WHERE title NOT IN ('Staff')` |
| `COUNT(*)` | Cuenta el número de filas | `SELECT COUNT(*) FROM employees` |
| `AVG(col)` / `SUM(col)` | Media aritmética y suma acumulada | `SELECT ROUND(AVG(salary), 2) ...` |
| `MIN(col)` / `MAX(col)` | Valor mínimo y máximo de una columna | `SELECT MIN(salary), MAX(salary) ...` |
| `GROUP BY` | Agrupa filas con valores idénticos | `GROUP BY gender` |
| `HAVING` | Filtra grupos resultantes del `GROUP BY` | `HAVING COUNT(*) > 20000` |

---

## 📋 Lista de los 30 Ejercicios Prácticos

### 📌 Ejercicio 01 — Filtro con WHERE (Igualdad de texto)
- **Nivel:** Básico 1
- **Enunciado:** La Dirección de Talento Humano necesita listar a todas las colaboradoras de género femenino ('F') registradas en la compañía. Muestra su número de empleado (emp_no), nombre (first_name), apellido (last_name) y género (gender). Limita la consulta a las primeras 10 filas.
- **💡 Pista metodológica:** Utiliza la cláusula WHERE con el operador de igualdad = comparando contra el literal 'F'. Añade LIMIT 10 al final.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 02 — Filtro con WHERE (Comparación numérica)
- **Nivel:** Básico 1
- **Enunciado:** El departamento de Auditoría Financiera solicita una lista de los colaboradores que actualmente perciben un sueldo estrictamente superior a $90,000 USD anuales. Consulta las columnas emp_no, salary, from_date y to_date en la tabla salaries, filtrando solo salarios vigentes (to_date = '9999-01-01'). Limita la salida a 10 filas.
- **💡 Pista metodológica:** Combina dos condiciones en WHERE usando el operador lógico AND: una para el salario (> 90000) y otra para la vigencia (to_date = '9999-01-01').

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 03 — Filtro con WHERE (Fechas)
- **Nivel:** Básico 1
- **Enunciado:** Se requiere consultar a los empleados más recientes contratados a partir del 1 de enero de 1998 en adelante. Muestra emp_no, first_name, last_name y hire_date, limitando el resultado a 10 filas.
- **💡 Pista metodológica:** Las fechas en SQL se escriben entre comillas simples con formato ISO 'YYYY-MM-DD'. Utiliza el operador >= sobre la columna hire_date.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 04 — Ordenamiento con ORDER BY (Ascendente)
- **Nivel:** Básico 1
- **Enunciado:** Consulta todos los departamentos corporativos de la tabla departments (dept_no, dept_name) ordenados alfabéticamente de la A a la Z por el nombre del departamento.
- **💡 Pista metodológica:** La cláusula ORDER BY se coloca al final de la consulta. La dirección ASC (ascendente) es la predeterminada.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 05 — Ordenamiento con ORDER BY (Descendente y LIMIT)
- **Nivel:** Básico 1
- **Enunciado:** La Gerencia General desea identificar los 5 salarios activos más altos pagados en toda la corporación. Muestra el número de empleado (emp_no) y el sueldo (salary) de la tabla salaries, considerando únicamente los salarios vigentes (to_date = '9999-01-01').
- **💡 Pista metodológica:** Usa ORDER BY salary DESC para ubicar los mayores sueldos al inicio y añade LIMIT 5 para restringir la salida.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 06 — WHERE con ORDER BY Múltiple
- **Nivel:** Básico 1
- **Enunciado:** Consulta a los empleados de género masculino ('M') contratados en el año 1990. Muestra emp_no, first_name, last_name, gender y hire_date, ordenados cronológicamente por hire_date (del más antiguo al más reciente) y, en caso de empates en fecha, alfabéticamente por last_name. Limita a 10 filas.
- **💡 Pista metodológica:** Puedes separar múltiples columnas en ORDER BY con comas: ORDER BY hire_date ASC, last_name ASC.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 07 — LIKE con Prefijo (%)
- **Nivel:** Básico 2
- **Enunciado:** Busca a todos los empleados cuyo primer nombre comience exactamente con las letras 'Mar' (por ejemplo: Mario, Mary, Mark, Martin). Proyecta emp_no, first_name y last_name. Limita el resultado a 10 registros ordenados alfabéticamente por first_name.
- **💡 Pista metodológica:** El símbolo % representa cero o más caracteres. La expresión 'Mar%' busca cualquier cadena que inicie con 'Mar'.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 08 — LIKE con Sufijo (%)
- **Nivel:** Básico 2
- **Enunciado:** Recursos Humanos está realizando un estudio genealógico de apellidos anglosajones y necesita listar a los colaboradores cuyo apellido termine en 'son' (por ejemplo: Johnson, Peterson, Anderson). Muestra emp_no, first_name y last_name, limitando a 10 filas.
- **💡 Pista metodológica:** Coloca el comodín % al principio de la cadena: LIKE '%son'.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 09 — LIKE con Subcadena en cualquier posición (%...%)
- **Nivel:** Básico 2
- **Enunciado:** Consulta a los empleados cuyo apellido contenga en alguna parte la sílaba 'an'. Proyecta emp_no, first_name y last_name, ordenados por last_name y limitados a 10 filas.
- **💡 Pista metodológica:** Rodea la subcadena buscada con el comodín porcentual en ambos lados: LIKE '%an%'.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 10 — LIKE con Carácter Individual (_)
- **Nivel:** Básico 2
- **Enunciado:** El comodín guion bajo (_) representa exactamente un único carácter cualquiera. Encuentra a los empleados cuyo primer nombre tenga exactamente 4 letras, comience con 'A' y termine en 'am' (ejemplo: 'Adam'). Proyecta emp_no, first_name y last_name limitando a 10 filas.
- **💡 Pista metodológica:** Usa 'A_am' en la cláusula LIKE para indicar un carácter desconocido entre la 'A' y la 'a'.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 11 — NOT LIKE (Exclusión de patrones)
- **Nivel:** Básico 2
- **Enunciado:** La empresa desea listar los títulos de la tabla titles que no comiencen con la palabra 'Senior'. Muestra de forma única (DISTINCT) la columna title.
- **💡 Pista metodológica:** Combina DISTINCT en el SELECT con la condición WHERE title NOT LIKE 'Senior%'.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 12 — Rango de Fechas con BETWEEN
- **Nivel:** Básico 3
- **Enunciado:** El departamento de Recursos Humanos prepara un reconocimiento de antigüedad para los colaboradores contratados en el bienio comprendido entre el 1 de enero de 1991 y el 31 de diciembre de 1992 (ambas fechas inclusive). Muestra emp_no, first_name, last_name y hire_date ordenados por fecha de contratación. Limita a 10 registros.
- **💡 Pista metodológica:** La sintaxis es: WHERE columna BETWEEN valor_inicial AND valor_final.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 13 — Rango Numérico con BETWEEN
- **Nivel:** Básico 3
- **Enunciado:** Filtra de la tabla salaries todos los salarios vigentes (to_date = '9999-01-01') que se encuentren en el rango de remuneración media entre $60,000 y $65,000 USD anuales. Muestra emp_no y salary, ordenados por salario de menor a mayor. Limita a 10 filas.
- **💡 Pista metodológica:** Aplica: WHERE to_date = '9999-01-01' AND salary BETWEEN 60000 AND 65000.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 14 — Rango con Fechas de Nacimiento (BETWEEN)
- **Nivel:** Básico 3
- **Enunciado:** El plan de salud ocupacional necesita identificar a los colaboradores nacidos entre el 1 de enero de 1960 y el 31 de diciembre de 1962. Muestra emp_no, first_name, last_name y birth_date ordenados por birth_date. Limita a 10 filas.
- **💡 Pista metodológica:** Aplica BETWEEN sobre la columna birth_date.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 15 — Exclusión de Rangos con NOT BETWEEN
- **Nivel:** Básico 3
- **Enunciado:** Identifica los salarios activos (to_date = '9999-01-01') que están en los extremos: que NO estén comprendidos entre $45,000 y $110,000 USD. Muestra emp_no y salary, ordenados por salary. Limita a 10 filas.
- **💡 Pista metodológica:** Usa la sintaxis: WHERE to_date = '9999-01-01' AND salary NOT BETWEEN 45000 AND 110000.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 16 — Pertenencia a Lista con IN (Texto)
- **Nivel:** Básico 4
- **Enunciado:** Consulta a los colaboradores cuyo primer nombre sea exactamente 'Elvis', 'Pradeep' o 'Kyoichi'. Muestra emp_no, first_name, last_name y gender ordenados por first_name. Limita a 10 registros.
- **💡 Pista metodológica:** El operador IN permite especificar una lista de valores separados por comas entre paréntesis: WHERE first_name IN ('Elvis', 'Pradeep', 'Kyoichi').

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 17 — Pertenencia a Lista con IN (Claves de Catálogo)
- **Nivel:** Básico 4
- **Enunciado:** Consulta los registros de la tabla dept_emp para los departamentos 'd001' (Marketing), 'd003' (Human Resources) y 'd005' (Development) que se encuentren vigentes (to_date = '9999-01-01'). Muestra emp_no, dept_no y from_date, limitando a 10 filas.
- **💡 Pista metodológica:** Aplica: WHERE to_date = '9999-01-01' AND dept_no IN ('d001', 'd003', 'd005').

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 18 — Exclusión de Lista con NOT IN (Texto)
- **Nivel:** Básico 4
- **Enunciado:** La Dirección Técnica busca empleados con cargos técnicos y operativos, por lo que necesita consultar los títulos vigentes (to_date = '9999-01-01') de la tabla titles excluyendo a los cargos administrativos 'Staff' y 'Senior Staff'. Muestra emp_no, title y from_date, limitando a 10 filas.
- **💡 Pista metodológica:** Utiliza: WHERE to_date = '9999-01-01' AND title NOT IN ('Staff', 'Senior Staff').

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 19 — Pertenencia a Lista con IN (Valores Numéricos)
- **Nivel:** Básico 4
- **Enunciado:** El comité de bienvenida desea revisar la información salarial vigente (to_date = '9999-01-01') de un grupo puntual de 5 empleados cuyos identificadores (emp_no) son: 10001, 10005, 10010, 10020 y 10050. Muestra emp_no, salary y from_date ordenados por emp_no.
- **💡 Pista metodológica:** Para números no se usan comillas simples: IN (10001, 10005, 10010, 10020, 10050).

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 20 — Exclusión de Departamentos con NOT IN
- **Nivel:** Básico 4
- **Enunciado:** Consulta los códigos y nombres de la tabla departments excluyendo a los departamentos de Finanzas ('Finance') y Mercadeo ('Marketing'). Muestra dept_no y dept_name ordenados por dept_name.
- **💡 Pista metodológica:** WHERE dept_name NOT IN ('Finance', 'Marketing').

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 21 — Función de Agregación: COUNT(*)
- **Nivel:** Básico 5
- **Enunciado:** Calcula el número total de colaboradores registrados en la base de datos dentro de la tabla maestra employees. Asigna el alias total_empleados a la columna resultante.
- **💡 Pista metodológica:** La función COUNT(*) cuenta todas las filas devueltas por la consulta.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 22 — COUNT con Condición en WHERE
- **Nivel:** Básico 5
- **Enunciado:** La Comisión de Equidad necesita saber cuántas colaboradoras de género femenino ('F') fueron contratadas en la compañía a partir del año 1995 en adelante. Nombra a la columna mujeres_contratadas_post_1995.
- **💡 Pista metodológica:** Aplica COUNT(*) combinándolo con WHERE gender = 'F' AND hire_date >= '1995-01-01'.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 23 — Funciones MIN() y MAX()
- **Nivel:** Básico 5
- **Enunciado:** Calcula de forma simultánea el salario mínimo histórico y el salario máximo histórico registrado en toda la tabla salaries. Asigna los alias salario_minimo y salario_maximo.
- **💡 Pista metodológica:** Usa SELECT MIN(salary) AS ..., MAX(salary) AS ... FROM salaries.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 24 — Función AVG() con Redondeo (ROUND)
- **Nivel:** Básico 5
- **Enunciado:** Calcula el salario promedio actual de la compañía considerando únicamente las remuneraciones vigentes (to_date = '9999-01-01'). Redondea el resultado a 2 decimales y asigna el alias salario_promedio_usd.
- **💡 Pista metodológica:** Utiliza ROUND(AVG(salary), 2) y no olvides filtrar con to_date = '9999-01-01'.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 25 — Función SUM() y Masa Salarial Total
- **Nivel:** Básico 5
- **Enunciado:** El Directorio solicita conocer el presupuesto total erogado anualmente por la compañía para el pago de salarios vigentes (to_date = '9999-01-01'). Además, muestra el total de empleados activos que componen esa nómina.
- **💡 Pista metodológica:** Combina SUM(salary) AS total_nomina_usd y COUNT(*) AS empleados_activos en un mismo SELECT.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 26 — GROUP BY Básico
- **Nivel:** Básico 6
- **Enunciado:** Calcula la cantidad total de colaboradores registrados por cada género ('M' y 'F') en la tabla employees. Muestra las columnas gender y total_colaboradores, ordenados por total de mayor a menor.
- **💡 Pista metodológica:** Coloca gender en el SELECT y en el GROUP BY, usando COUNT(*) para el conteo.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 27 — GROUP BY con Títulos y Salarios Vigentes
- **Nivel:** Básico 6
- **Enunciado:** Para cada título o cargo formal vigente en la tabla titles (to_date = '9999-01-01'), cuenta cuántos colaboradores ostentan dicho cargo en la actualidad. Muestra title y cantidad_colaboradores ordenados de mayor a menor.
- **💡 Pista metodológica:** Aplica WHERE to_date = '9999-01-01' antes del GROUP BY title.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 28 — GROUP BY con Condición Agregada (HAVING)
- **Nivel:** Básico 6
- **Enunciado:** En la tabla dept_emp, calcula cuántos colaboradores activos (to_date = '9999-01-01') pertenecen a cada departamento (dept_no). Muestra únicamente aquellos departamentos masivos que tengan más de 20,000 colaboradores activos. Ordena de mayor a menor dotación.
- **💡 Pista metodológica:** Usa WHERE to_date = '9999-01-01' para las filas individuales y HAVING COUNT(*) > 20000 para filtrar los grupos resultantes.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 29 — WHERE + GROUP BY + HAVING con Promedios
- **Nivel:** Básico 6
- **Enunciado:** Consulta los departamentos en dept_emp (dept_no) que tengan más de 15,000 empleados contratados originalmente entre los años 1985 y 1990 (filtra hire_date o fechas en from_date). Para este ejercicio pedagógico, cuenta los emp_no en dept_emp donde from_date >= '1985-01-01', agrupados por dept_no, que superen los 15,000 registros.
- **💡 Pista metodológica:** Aplica WHERE from_date >= '1985-01-01', agrupa por dept_no y usa HAVING COUNT(emp_no) > 15000.

```sql
-- Escribe tu consulta SQL aquí:

```

---

### 📌 Ejercicio 30 — Combinación Integral (IN, BETWEEN, GROUP BY, HAVING, ORDER BY)
- **Nivel:** Básico 6
- **Enunciado:** Genera un reporte analítico de dotación por departamento en dept_emp que combine todo lo aprendido: filtra los departamentos clave 'd001', 'd002', 'd004', 'd005' y 'd007' mediante IN, cuyas asignaciones hayan iniciado en el rango de años 1990 a 1998 (BETWEEN '1990-01-01' AND '1998-12-31'). Agrupa por departamento y muestra únicamente aquellos que acumulen más de 8,000 colaboradores en ese periodo. Ordena el resultado descendentemente por cantidad.
- **💡 Pista metodológica:** Combina: WHERE dept_no IN (...) AND from_date BETWEEN ... GROUP BY dept_no HAVING COUNT(*) > 8000 ORDER BY cantidad DESC.

```sql
-- Escribe tu consulta SQL aquí:

```

---

## 🚀 ¿Necesitas validar tus resultados?
Consulta el documento hermano con todas las consultas oficiales explicadas y sus tablas de resultados:  
👉 **[`ejercicios-sql-employees-solucionario.md`](./ejercicios-sql-employees-solucionario.md)**
