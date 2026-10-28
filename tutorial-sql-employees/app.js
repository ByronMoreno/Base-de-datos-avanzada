// Base de datos de temas del tutorial W3Schools-style sobre Employees
const TOPICS = [
  {
    "id": "intro",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Intro & Employees DB",
    "title": "SQL Introducción y Base de Datos Employees",
    "desc": "SQL (Structured Query Language) es el estándar internacional para almacenar, manipular y consultar datos en sistemas relacionales. En este tutorial interactivo, trabajaremos con la prestigiosa base de datos corporativa <strong>Employees</strong> (casi 4 millones de registros entre 6 tablas relacionales altamente normalizadas: <code>employees</code>, <code>departments</code>, <code>dept_emp</code>, <code>dept_manager</code>, <code>titles</code> y <code>salaries</code>).",
    "syntax": "-- Estructura básica de una consulta de lectura en PostgreSQL\nSELECT columna1, columna2, ...\nFROM nombre_tabla;\n\n-- Conexión a la base de datos Employees en PostgreSQL\npsql -U postgres -d employees",
    "tableDemo": {
      "title": "Tabla Principal: employees (Muestra de 4 registros)",
      "columns": [
        "emp_no",
        "birth_date",
        "first_name",
        "last_name",
        "gender",
        "hire_date"
      ],
      "rows": [
        [
          "10001",
          "1953-09-02",
          "Georgi",
          "Facello",
          "M",
          "1986-06-26"
        ],
        [
          "10002",
          "1964-06-02",
          "Bezalel",
          "Simmel",
          "F",
          "1985-11-21"
        ],
        [
          "10003",
          "1959-12-03",
          "Parto",
          "Bamford",
          "M",
          "1986-08-28"
        ],
        [
          "10004",
          "1954-05-01",
          "Chirstian",
          "Koblick",
          "M",
          "1986-12-01"
        ]
      ]
    },
    "exampleQuery": "-- Consultar la versión del motor y el total de colaboradores registrados\nSELECT \n    COUNT(*) AS total_empleados,\n    MIN(hire_date) AS contratacion_mas_antigua,\n    MAX(hire_date) AS contratacion_mas_reciente\nFROM employees;",
    "exampleExplanation": "La función COUNT(*) cuenta todas las filas de la tabla maestra. MIN y MAX devuelven los extremos del rango cronológico de contratación.",
    "resultColumns": [
      "total_empleados",
      "contratacion_mas_antigua",
      "contratacion_mas_reciente"
    ],
    "resultRows": [
      [
        "300024",
        "1985-01-01",
        "2000-01-28"
      ]
    ],
    "exercise": {
      "question": "Escribe la palabra clave SQL para consultar todas las columnas de la tabla <code>departments</code>:",
      "templateBefore": "",
      "blank": "SELECT",
      "templateAfter": " * FROM departments;",
      "hint": "Palabra reservada fundamental que inicia una consulta de extracción en SQL."
    }
  },
  {
    "id": "syntax",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Syntax",
    "title": "SQL Syntax en PostgreSQL",
    "desc": "Las sentencias SQL no son sensibles a mayúsculas/minúsculas para las palabras clave (<code>select</code> es igual a <code>SELECT</code>), pero por convención y estándar profesional se escriben en <strong>MAYÚSCULAS</strong>. Cada instrucción debe culminar con un punto y coma (<code>;</code>).",
    "syntax": "-- Sintaxis básica con proyección y cláusulas fundamentales\nSELECT columnas\nFROM tabla\nWHERE condicion\nORDER BY columna [ASC|DESC]\nLIMIT cantidad;",
    "tableDemo": {
      "title": "Tabla: departments (Catálogo de Áreas)",
      "columns": [
        "dept_no",
        "dept_name"
      ],
      "rows": [
        [
          "d001",
          "Marketing"
        ],
        [
          "d002",
          "Finance"
        ],
        [
          "d003",
          "Human Resources"
        ],
        [
          "d004",
          "Production"
        ],
        [
          "d005",
          "Development"
        ]
      ]
    },
    "exampleQuery": "SELECT dept_no, dept_name \nFROM departments \nORDER BY dept_name ASC;",
    "exampleExplanation": "Se proyectan las columnas dept_no y dept_name de la tabla departments, ordenándolas alfabéticamente por nombre de departamento.",
    "resultColumns": [
      "dept_no",
      "dept_name"
    ],
    "resultRows": [
      [
        "d009",
        "Customer Service"
      ],
      [
        "d005",
        "Development"
      ],
      [
        "d002",
        "Finance"
      ],
      [
        "d003",
        "Human Resources"
      ],
      [
        "d001",
        "Marketing"
      ]
    ],
    "exercise": {
      "question": "Completa la cláusula que indica de qué tabla se deben obtener los registros:",
      "templateBefore": "SELECT emp_no, first_name ",
      "blank": "FROM",
      "templateAfter": " employees;",
      "hint": "Indica la fuente de datos o tabla en la consulta."
    }
  },
  {
    "id": "select",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Select",
    "title": "SQL SELECT Statement",
    "desc": "La sentencia <code>SELECT</code> se utiliza para extraer datos de una base de datos. Los datos devueltos se almacenan en una tabla de resultados temporal denominada conjunto de resultados (<em>result-set</em>).",
    "syntax": "SELECT columna1, columna2, ...\nFROM nombre_tabla;\n\n-- O para seleccionar todas las columnas:\nSELECT * FROM nombre_tabla;",
    "tableDemo": {
      "title": "Tabla: employees (Campos Personales)",
      "columns": [
        "emp_no",
        "first_name",
        "last_name",
        "gender"
      ],
      "rows": [
        [
          "10001",
          "Georgi",
          "Facello",
          "M"
        ],
        [
          "10002",
          "Bezalel",
          "Simmel",
          "F"
        ],
        [
          "10003",
          "Parto",
          "Bamford",
          "M"
        ]
      ]
    },
    "exampleQuery": "SELECT first_name, last_name, hire_date \nFROM employees \nLIMIT 4;",
    "exampleExplanation": "Selecciona específicamente tres atributos de la tabla employees y limita la salida a los primeros 4 registros.",
    "resultColumns": [
      "first_name",
      "last_name",
      "hire_date"
    ],
    "resultRows": [
      [
        "Georgi",
        "Facello",
        "1986-06-26"
      ],
      [
        "Bezalel",
        "Simmel",
        "1985-11-21"
      ],
      [
        "Parto",
        "Bamford",
        "1986-08-28"
      ],
      [
        "Chirstian",
        "Koblick",
        "1986-12-01"
      ]
    ],
    "exercise": {
      "question": "Selecciona todas las columnas (*) de la tabla <code>salaries</code>:",
      "templateBefore": "SELECT ",
      "blank": "*",
      "templateAfter": " FROM salaries LIMIT 10;",
      "hint": "Comodín utilizado en SQL para indicar todas las columnas."
    }
  },
  {
    "id": "select_distinct",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Select Distinct",
    "title": "SQL SELECT DISTINCT Statement",
    "desc": "Dentro de una tabla, una columna a menudo contiene muchos valores duplicados. La sentencia <code>SELECT DISTINCT</code> se utiliza para devolver solo valores distintos (únicos), eliminando redundancias.",
    "syntax": "SELECT DISTINCT columna1, columna2, ...\nFROM nombre_tabla;",
    "tableDemo": {
      "title": "Tabla: titles (Cargos históricos de empleados)",
      "columns": [
        "emp_no",
        "title",
        "from_date"
      ],
      "rows": [
        [
          "10001",
          "Senior Engineer",
          "1986-06-26"
        ],
        [
          "10002",
          "Staff",
          "1996-08-03"
        ],
        [
          "10003",
          "Senior Engineer",
          "1995-12-03"
        ],
        [
          "10004",
          "Engineer",
          "1986-12-01"
        ],
        [
          "10004",
          "Senior Engineer",
          "1995-12-01"
        ]
      ]
    },
    "exampleQuery": "SELECT DISTINCT title \nFROM titles \nORDER BY title ASC;",
    "exampleExplanation": "Aunque la tabla titles posee más de 443,000 filas, esta consulta devuelve únicamente los 7 títulos o cargos oficiales sin repeticiones.",
    "resultColumns": [
      "title"
    ],
    "resultRows": [
      [
        "Assistant Engineer"
      ],
      [
        "Engineer"
      ],
      [
        "Manager"
      ],
      [
        "Senior Engineer"
      ],
      [
        "Senior Staff"
      ],
      [
        "Staff"
      ],
      [
        "Technique Leader"
      ]
    ],
    "exercise": {
      "question": "Completa para obtener los géneros únicos registrados en la tabla <code>employees</code>:",
      "templateBefore": "SELECT ",
      "blank": "DISTINCT",
      "templateAfter": " gender FROM employees;",
      "hint": "Cláusula que filtra duplicados para dejar únicamente valores únicos."
    }
  },
  {
    "id": "where",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Where",
    "title": "SQL WHERE Clause",
    "desc": "La cláusula <code>WHERE</code> se utiliza para filtrar registros. Se utiliza para extraer solo aquellos registros que cumplen una condición especificada. En la base de datos <code>Employees</code>, es vital para filtrar vigencia: <code>WHERE to_date = '9999-01-01'</code>.",
    "syntax": "SELECT columna1, columna2, ...\nFROM nombre_tabla\nWHERE condicion;",
    "tableDemo": {
      "title": "Tabla: salaries (Registros con convención temporal)",
      "columns": [
        "emp_no",
        "salary",
        "from_date",
        "to_date"
      ],
      "rows": [
        [
          "10001",
          "60117",
          "1986-06-26",
          "1987-06-26"
        ],
        [
          "10001",
          "62102",
          "1987-06-26",
          "1988-06-25"
        ],
        [
          "10001",
          "88958",
          "2002-06-22",
          "9999-01-01"
        ],
        [
          "10002",
          "72527",
          "2001-08-02",
          "9999-01-01"
        ]
      ]
    },
    "exampleQuery": "SELECT emp_no, salary, from_date \nFROM salaries \nWHERE to_date = '9999-01-01' \n  AND salary > 120000\nORDER BY salary DESC \nLIMIT 5;",
    "exampleExplanation": "Filtra únicamente los salarios activos (to_date = '9999-01-01') que además superen los $120,000 USD anuales.",
    "resultColumns": [
      "emp_no",
      "salary",
      "from_date"
    ],
    "resultRows": [
      [
        "109334",
        "158220",
        "2001-11-20"
      ],
      [
        "43624",
        "157821",
        "2001-07-06"
      ],
      [
        "254466",
        "156286",
        "2001-08-04"
      ],
      [
        "47978",
        "155709",
        "2001-07-14"
      ],
      [
        "253939",
        "155513",
        "2002-04-09"
      ]
    ],
    "exercise": {
      "question": "Filtra todos los empleados cuyo género sea femenino ('F'):",
      "templateBefore": "SELECT * FROM employees ",
      "blank": "WHERE",
      "templateAfter": " gender = 'F' LIMIT 10;",
      "hint": "Cláusula fundamental de predicado o condición de búsqueda."
    }
  },
  {
    "id": "order_by",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Order By",
    "title": "SQL ORDER BY Keyword",
    "desc": "La palabra clave <code>ORDER BY</code> se utiliza para ordenar el conjunto de resultados en orden ascendente (<code>ASC</code>, por defecto) o descendente (<code>DESC</code>). Se pueden ordenar por una o varias columnas.",
    "syntax": "SELECT columna1, columna2, ...\nFROM nombre_tabla\nORDER BY columna1 [ASC|DESC], columna2 [ASC|DESC];",
    "tableDemo": {
      "title": "Tabla: employees",
      "columns": [
        "emp_no",
        "first_name",
        "last_name",
        "hire_date"
      ],
      "rows": [
        [
          "10001",
          "Georgi",
          "Facello",
          "1986-06-26"
        ],
        [
          "10002",
          "Bezalel",
          "Simmel",
          "1985-11-21"
        ],
        [
          "10003",
          "Parto",
          "Bamford",
          "1986-08-28"
        ]
      ]
    },
    "exampleQuery": "SELECT emp_no, first_name, last_name, hire_date \nFROM employees \nORDER BY last_name ASC, first_name ASC \nLIMIT 5;",
    "exampleExplanation": "Ordena a los empleados alfabéticamente por apellido y, en caso de coincidencia, por primer nombre.",
    "resultColumns": [
      "emp_no",
      "first_name",
      "last_name",
      "hire_date"
    ],
    "resultRows": [
      [
        "258641",
        "Aamer",
        "Aamodt",
        "1994-09-15"
      ],
      [
        "438081",
        "Abdelkader",
        "Aamodt",
        "1990-05-22"
      ],
      [
        "11018",
        "Adhemar",
        "Aamodt",
        "1992-02-10"
      ],
      [
        "428079",
        "Aemilian",
        "Aamodt",
        "1993-05-19"
      ],
      [
        "222595",
        "Almudena",
        "Aamodt",
        "1993-07-02"
      ]
    ],
    "exercise": {
      "question": "Ordena los salarios del más alto al más bajo utilizando la cláusula correspondiente:",
      "templateBefore": "SELECT emp_no, salary FROM salaries WHERE to_date = '9999-01-01' ORDER BY salary ",
      "blank": "DESC",
      "templateAfter": " LIMIT 10;",
      "hint": "Palabra clave para indicar orden decreciente o descendente."
    }
  },
  {
    "id": "and_or_not",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL And, Or, Not",
    "title": "SQL AND, OR y NOT Operators",
    "desc": "La cláusula <code>WHERE</code> se puede combinar con los operadores lógicos <code>AND</code>, <code>OR</code> y <code>NOT</code> para evaluar múltiples condiciones booleanas simultáneas.",
    "syntax": "-- Operador AND (ambas condiciones deben ser verdaderas)\nSELECT * FROM tabla WHERE cond1 AND cond2;\n\n-- Operador OR (al menos una condición debe ser verdadera)\nSELECT * FROM tabla WHERE cond1 OR cond2;\n\n-- Operador NOT (invierte el valor de verdad)\nSELECT * FROM tabla WHERE NOT condicion;",
    "tableDemo": {
      "title": "Tabla: employees",
      "columns": [
        "emp_no",
        "first_name",
        "last_name",
        "gender",
        "hire_date"
      ],
      "rows": [
        [
          "10001",
          "Georgi",
          "Facello",
          "M",
          "1986-06-26"
        ],
        [
          "10002",
          "Bezalel",
          "Simmel",
          "F",
          "1985-11-21"
        ],
        [
          "10003",
          "Parto",
          "Bamford",
          "M",
          "1986-08-28"
        ]
      ]
    },
    "exampleQuery": "SELECT emp_no, first_name, last_name, gender, hire_date \nFROM employees \nWHERE gender = 'F' \n  AND hire_date >= '1995-01-01'\n  AND NOT (last_name = 'Smith')\nORDER BY hire_date DESC \nLIMIT 4;",
    "exampleExplanation": "Filtra empleadas mujeres (F) contratadas desde 1995 en adelante cuyo apellido no sea Smith.",
    "resultColumns": [
      "emp_no",
      "first_name",
      "last_name",
      "gender",
      "hire_date"
    ],
    "resultRows": [
      [
        "499995",
        "Dekang",
        "Lichtner",
        "F",
        "1997-06-02"
      ],
      [
        "499988",
        "Bangqing",
        "Kleiser",
        "F",
        "1997-05-28"
      ],
      [
        "499981",
        "Yunming",
        "Mitina",
        "F",
        "1997-03-07"
      ],
      [
        "499974",
        "Shuichi",
        "Perez",
        "F",
        "1996-12-14"
      ]
    ],
    "exercise": {
      "question": "Completa para exigir que el colaborador sea de género 'M' Y haya sido contratado después del 2000:",
      "templateBefore": "SELECT * FROM employees WHERE gender = 'M' ",
      "blank": "AND",
      "templateAfter": " hire_date >= '2000-01-01';",
      "hint": "Operador lógico conjuntivo que exige el cumplimiento de ambas premisas."
    }
  },
  {
    "id": "insert_into",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Insert Into",
    "title": "SQL INSERT INTO Statement",
    "desc": "La sentencia <code>INSERT INTO</code> se utiliza para insertar nuevos registros en una tabla. Se puede especificar la lista de columnas destino o proporcionar valores para todas las columnas en su orden definido.",
    "syntax": "-- Inserción especificando columnas\nINSERT INTO nombre_tabla (columna1, columna2, ...)\nVALUES (valor1, valor2, ...);\n\n-- Inserción múltiple en una sola sentencia\nINSERT INTO nombre_tabla (col1, col2)\nVALUES (val1, val2), (val3, val4);",
    "tableDemo": {
      "title": "Tabla: departments",
      "columns": [
        "dept_no",
        "dept_name"
      ],
      "rows": [
        [
          "d001",
          "Marketing"
        ],
        [
          "d002",
          "Finance"
        ]
      ]
    },
    "exampleQuery": "-- Insertar un nuevo departamento de Inteligencia Artificial\nINSERT INTO departments (dept_no, dept_name)\nVALUES ('d010', 'Artificial Intelligence')\nON CONFLICT (dept_no) DO NOTHING\nRETURNING *;",
    "exampleExplanation": "Inserta el código 'd010' para IA. En PostgreSQL se puede usar RETURNING * para obtener inmediatamente la fila insertada.",
    "resultColumns": [
      "dept_no",
      "dept_name"
    ],
    "resultRows": [
      [
        "d010",
        "Artificial Intelligence"
      ]
    ],
    "exercise": {
      "question": "Completa la sentencia para insertar un nuevo registro en la tabla <code>departments</code>:",
      "templateBefore": "INSERT ",
      "blank": "INTO",
      "templateAfter": " departments (dept_no, dept_name) VALUES ('d011', 'DevOps');",
      "hint": "Palabra clave que sigue inmediatamente a INSERT."
    }
  },
  {
    "id": "null_values",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Null Values",
    "title": "SQL NULL Values & Operadores IS NULL",
    "desc": "Un campo con un valor <code>NULL</code> es un campo sin valor. Si un campo en una tabla es opcional, es posible insertar o actualizar un registro sin agregar un valor. <strong>Importante:</strong> No se puede probar NULL con operadores de igualdad (<code>=</code>); se debe usar <code>IS NULL</code> o <code>IS NOT NULL</code>.",
    "syntax": "-- Comprobar valores nulos\nSELECT columnas FROM tabla WHERE columna IS NULL;\n\n-- Comprobar valores NO nulos\nSELECT columnas FROM tabla WHERE columna IS NOT NULL;",
    "tableDemo": {
      "title": "Tabla: titles (to_date puede ser NULL si no tiene fecha fija)",
      "columns": [
        "emp_no",
        "title",
        "from_date",
        "to_date"
      ],
      "rows": [
        [
          "10001",
          "Senior Engineer",
          "1986-06-26",
          "9999-01-01"
        ],
        [
          "99999",
          "Consultant",
          "2024-01-01",
          "NULL"
        ]
      ]
    },
    "exampleQuery": "SELECT emp_no, title, from_date \nFROM titles \nWHERE to_date IS NOT NULL \nORDER BY from_date DESC \nLIMIT 3;",
    "exampleExplanation": "Filtra únicamente los registros donde la fecha de finalización está debidamente registrada.",
    "resultColumns": [
      "emp_no",
      "title",
      "from_date"
    ],
    "resultRows": [
      [
        "499999",
        "Engineer",
        "1997-11-30"
      ],
      [
        "499998",
        "Staff",
        "1993-12-27"
      ],
      [
        "499997",
        "Senior Engineer",
        "1992-08-30"
      ]
    ],
    "exercise": {
      "question": "Completa para filtrar los registros donde la columna <code>to_date</code> no sea nula:",
      "templateBefore": "SELECT * FROM titles WHERE to_date IS ",
      "blank": "NOT NULL",
      "templateAfter": ";",
      "hint": "Operador compuesto para verificar que existe un valor asignado."
    }
  },
  {
    "id": "update",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Update",
    "title": "SQL UPDATE Statement",
    "desc": "La sentencia <code>UPDATE</code> se utiliza para modificar los registros existentes en una tabla. <strong>¡CUIDADO CRÍTICO!</strong> Si omites la cláusula <code>WHERE</code>, ¡se actualizarán todas las filas de la tabla!",
    "syntax": "UPDATE nombre_tabla\nSET columna1 = valor1, columna2 = valor2, ...\nWHERE condicion;",
    "tableDemo": {
      "title": "Tabla: departments",
      "columns": [
        "dept_no",
        "dept_name"
      ],
      "rows": [
        [
          "d009",
          "Customer Service"
        ]
      ]
    },
    "exampleQuery": "-- Actualizar el nombre comercial de un departamento\nUPDATE departments\nSET dept_name = 'Customer Experience & Success'\nWHERE dept_no = 'd009'\nRETURNING dept_no, dept_name;",
    "exampleExplanation": "Modifica de forma puntual el registro con código 'd009' sin alterar los otros 8 departamentos de la empresa.",
    "resultColumns": [
      "dept_no",
      "dept_name"
    ],
    "resultRows": [
      [
        "d009",
        "Customer Experience & Success"
      ]
    ],
    "exercise": {
      "question": "Completa la cláusula para asignar el nuevo valor de la columna en un UPDATE:",
      "templateBefore": "UPDATE employees ",
      "blank": "SET",
      "templateAfter": " first_name = 'George' WHERE emp_no = 10001;",
      "hint": "Cláusula que precede a las asignaciones columna = valor."
    }
  },
  {
    "id": "delete",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Delete",
    "title": "SQL DELETE Statement",
    "desc": "La sentencia <code>DELETE</code> se utiliza para eliminar registros existentes de una tabla. Al igual que con <code>UPDATE</code>, si omites el <code>WHERE</code>, ¡se vaciará la tabla por completo!",
    "syntax": "DELETE FROM nombre_tabla\nWHERE condicion;\n\n-- Para eliminar todas las filas:\nDELETE FROM nombre_tabla;\n-- O de forma más veloz:\nTRUNCATE TABLE nombre_tabla;",
    "tableDemo": {
      "title": "Tabla: departments (Fila de prueba 'd011')",
      "columns": [
        "dept_no",
        "dept_name"
      ],
      "rows": [
        [
          "d011",
          "DevOps Temporal"
        ]
      ]
    },
    "exampleQuery": "-- Eliminar el departamento de prueba d011\nDELETE FROM departments\nWHERE dept_no = 'd011'\nRETURNING dept_no, dept_name;",
    "exampleExplanation": "Elimina de forma segura únicamente la fila cuyo dept_no coincide con 'd011'.",
    "resultColumns": [
      "dept_no",
      "dept_name"
    ],
    "resultRows": [
      [
        "d011",
        "DevOps Temporal"
      ]
    ],
    "exercise": {
      "question": "Escribe la sentencia para eliminar al empleado con emp_no = 99999:",
      "templateBefore": "",
      "blank": "DELETE FROM",
      "templateAfter": " employees WHERE emp_no = 99999;",
      "hint": "Sentencia que elimina registros de una tabla específica."
    }
  },
  {
    "id": "limit",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Select Top / Limit",
    "title": "SQL LIMIT Clause (Equivalente SELECT TOP)",
    "desc": "En PostgreSQL y MySQL, la cláusula <code>LIMIT</code> se utiliza para especificar el número de registros que se devolverán. En SQL Server se usa <code>SELECT TOP</code>. Es invaluable en tablas enormes como <code>salaries</code> (2.8 millones de filas).",
    "syntax": "-- En PostgreSQL / MySQL:\nSELECT columnas FROM tabla LIMIT cantidad [OFFSET salto];\n\n-- En SQL Server:\nSELECT TOP (cantidad) columnas FROM tabla;",
    "tableDemo": {
      "title": "Tabla: salaries (2,844,047 registros)",
      "columns": [
        "emp_no",
        "salary"
      ],
      "rows": [
        [
          "10001",
          "88958"
        ],
        [
          "10002",
          "72527"
        ]
      ]
    },
    "exampleQuery": "SELECT emp_no, salary \nFROM salaries \nWHERE to_date = '9999-01-01' \nORDER BY salary DESC \nLIMIT 3 OFFSET 0;",
    "exampleExplanation": "Devuelve exactamente los 3 sueldos activos más elevados de la empresa sin sobrecargar la memoria del cliente.",
    "resultColumns": [
      "emp_no",
      "salary"
    ],
    "resultRows": [
      [
        "109334",
        "158220"
      ],
      [
        "43624",
        "157821"
      ],
      [
        "254466",
        "156286"
      ]
    ],
    "exercise": {
      "question": "Limita los resultados de la consulta a 5 registros:",
      "templateBefore": "SELECT * FROM employees ORDER BY hire_date ASC ",
      "blank": "LIMIT 5",
      "templateAfter": ";",
      "hint": "Cláusula que restringe el número máximo de filas devueltas."
    }
  },
  {
    "id": "aggregates",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Aggregate Functions",
    "title": "SQL Aggregate Functions (MIN, MAX, COUNT, AVG, SUM)",
    "desc": "Una función de agregación realiza un cálculo sobre un conjunto de valores y devuelve un único valor escalar. Son fundamentales para la analítica empresarial y auditoría de nómina.",
    "syntax": "SELECT \n    COUNT(columna),\n    AVG(columna),\n    SUM(columna),\n    MIN(columna),\n    MAX(columna)\nFROM tabla\nWHERE condicion;",
    "tableDemo": {
      "title": "Masa de datos en salaries vigentes",
      "columns": [
        "Métrica",
        "Descripción"
      ],
      "rows": [
        [
          "COUNT",
          "Total de contratos salariales activos"
        ],
        [
          "AVG",
          "Salario promedio en dólares"
        ],
        [
          "SUM",
          "Masa salarial total que eroga la empresa"
        ]
      ]
    },
    "exampleQuery": "SELECT \n    COUNT(*) AS total_empleados_activos,\n    ROUND(AVG(salary), 2) AS salario_promedio_usd,\n    SUM(salary) AS total_nomina_usd,\n    MIN(salary) AS salario_minimo_usd,\n    MAX(salary) AS salario_maximo_usd\nFROM salaries\nWHERE to_date = '9999-01-01';",
    "exampleExplanation": "Calcula en una sola pasada el resumen financiero completo de los 240,124 empleados activos.",
    "resultColumns": [
      "total_empleados_activos",
      "salario_promedio_usd",
      "total_nomina_usd",
      "salario_minimo_usd",
      "salario_maximo_usd"
    ],
    "resultRows": [
      [
        "240124",
        "72012.24",
        "17291866412",
        "38623",
        "158220"
      ]
    ],
    "exercise": {
      "question": "Calcula el promedio salarial de la tabla <code>salaries</code>:",
      "templateBefore": "SELECT ",
      "blank": "AVG(salary)",
      "templateAfter": " FROM salaries WHERE to_date = '9999-01-01';",
      "hint": "Función agregada para obtener la media aritmética de una columna numérica."
    }
  },
  {
    "id": "joins",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Joins",
    "title": "SQL JOINs (INNER, LEFT, RIGHT, FULL)",
    "desc": "Una cláusula <code>JOIN</code> se utiliza para combinar filas de dos o más tablas, en función de una columna relacionada entre ellas (normalmente clave foránea a clave primaria).",
    "syntax": "-- INNER JOIN: Filas que coinciden en ambas tablas\nSELECT * FROM tablaA\nINNER JOIN tablaB ON tablaA.id = tablaB.id;\n\n-- LEFT JOIN: Todas las filas de A más coincidencias de B\nSELECT * FROM tablaA\nLEFT JOIN tablaB ON tablaA.id = tablaB.id;",
    "tableDemo": {
      "title": "Relación entre employees y titles",
      "columns": [
        "emp_no",
        "first_name",
        "title"
      ],
      "rows": [
        [
          "10001",
          "Georgi",
          "Senior Engineer"
        ],
        [
          "10002",
          "Bezalel",
          "Staff"
        ]
      ]
    },
    "exampleQuery": "SELECT \n    e.emp_no,\n    e.first_name || ' ' || e.last_name AS colaborador,\n    t.title AS cargo_actual\nFROM employees e\nINNER JOIN titles t ON e.emp_no = t.emp_no\nWHERE t.to_date = '9999-01-01'\nORDER BY e.emp_no ASC\nLIMIT 4;",
    "exampleExplanation": "Combina la tabla employees con titles mediante la clave foránea emp_no filtrando por el cargo activo.",
    "resultColumns": [
      "emp_no",
      "colaborador",
      "cargo_actual"
    ],
    "resultRows": [
      [
        "10001",
        "Georgi Facello",
        "Senior Engineer"
      ],
      [
        "10002",
        "Bezalel Simmel",
        "Staff"
      ],
      [
        "10003",
        "Parto Bamford",
        "Senior Engineer"
      ],
      [
        "10004",
        "Chirstian Koblick",
        "Senior Engineer"
      ]
    ],
    "exercise": {
      "question": "Une la tabla <code>departments</code> mediante la columna común <code>dept_no</code>:",
      "templateBefore": "SELECT * FROM dept_emp de INNER ",
      "blank": "JOIN",
      "templateAfter": " departments d ON de.dept_no = d.dept_no LIMIT 5;",
      "hint": "Palabra clave para realizar el cruce relacional entre tablas."
    }
  },
  {
    "id": "group_by",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Group By",
    "title": "SQL GROUP BY Statement",
    "desc": "La sentencia <code>GROUP BY</code> agrupa filas que tienen los mismos valores en filas de resumen, como 'encontrar el número de empleados en cada departamento'. Se utiliza a menudo con funciones agregadas (<code>COUNT</code>, <code>MAX</code>, <code>MIN</code>, <code>SUM</code>, <code>AVG</code>).",
    "syntax": "SELECT columna, COUNT(*)\nFROM tabla\nGROUP BY columna;",
    "tableDemo": {
      "title": "Distribución por Género en employees",
      "columns": [
        "gender",
        "conteo"
      ],
      "rows": [
        [
          "M",
          "179,973"
        ],
        [
          "F",
          "120,051"
        ]
      ]
    },
    "exampleQuery": "SELECT \n    gender AS genero,\n    COUNT(*) AS total_colaboradores,\n    ROUND((COUNT(*)::NUMERIC / 300024) * 100, 2) AS porcentaje\nFROM employees\nGROUP BY gender;",
    "exampleExplanation": "Agrupa los 300,024 registros de la empresa en dos grupos: 'M' y 'F' calculando su proporción.",
    "resultColumns": [
      "genero",
      "total_colaboradores",
      "porcentaje"
    ],
    "resultRows": [
      [
        "M",
        "179973",
        "59.99"
      ],
      [
        "F",
        "120051",
        "40.01"
      ]
    ],
    "exercise": {
      "question": "Agrupa los títulos de la tabla <code>titles</code> para contar colaboradores por cargo:",
      "templateBefore": "SELECT title, COUNT(*) FROM titles WHERE to_date = '9999-01-01' ",
      "blank": "GROUP BY",
      "templateAfter": " title;",
      "hint": "Cláusula de agregación para agrupar filas coincidentes."
    }
  },
  {
    "id": "having",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Having",
    "title": "SQL HAVING Clause",
    "desc": "La cláusula <code>HAVING</code> se agregó a SQL porque la palabra clave <code>WHERE</code> no se puede utilizar con funciones de agregación. <code>WHERE</code> filtra filas antes de agrupar; <code>HAVING</code> filtra los grupos resultantes.",
    "syntax": "SELECT columna, AGG(columna)\nFROM tabla\nGROUP BY columna\nHAVING condicion_agregada;",
    "tableDemo": {
      "title": "Departamentos con más de 20,000 integrantes activos",
      "columns": [
        "dept_name",
        "total_empleados"
      ],
      "rows": [
        [
          "Development",
          "61,386"
        ],
        [
          "Production",
          "53,304"
        ],
        [
          "Sales",
          "37,701"
        ]
      ]
    },
    "exampleQuery": "SELECT \n    d.dept_name AS departamento,\n    COUNT(de.emp_no) AS total_activos\nFROM departments d\nJOIN dept_emp de ON d.dept_no = de.dept_no AND de.to_date = '9999-01-01'\nGROUP BY d.dept_name\nHAVING COUNT(de.emp_no) > 30000\nORDER BY total_activos DESC;",
    "exampleExplanation": "Calcula el número de empleados activos por departamento y descarta aquellos grupos que tengan 30,000 o menos colaboradores.",
    "resultColumns": [
      "departamento",
      "total_activos"
    ],
    "resultRows": [
      [
        "Development",
        "61386"
      ],
      [
        "Production",
        "53304"
      ],
      [
        "Sales",
        "37701"
      ]
    ],
    "exercise": {
      "question": "Filtra grupos cuyo promedio salarial supere los $70,000 USD:",
      "templateBefore": "SELECT dept_no, AVG(salary) FROM salaries s JOIN dept_emp de ON s.emp_no = de.emp_no GROUP BY dept_no ",
      "blank": "HAVING",
      "templateAfter": " AVG(salary) > 70000;",
      "hint": "Cláusula que aplica condiciones sobre funciones de agregación agrupadas."
    }
  },
  {
    "id": "exists",
    "category": "SQL TUTORIAL",
    "menuTitle": "SQL Exists",
    "title": "SQL EXISTS Operator",
    "desc": "El operador <code>EXISTS</code> se utiliza para verificar la existencia de cualquier registro en una subconsulta. Devuelve <code>TRUE</code> si la subconsulta devuelve uno o más registros, siendo altamente eficiente porque el motor detiene la búsqueda tras el primer hallazgo.",
    "syntax": "SELECT columnas\nFROM tabla\nWHERE EXISTS (\n    SELECT 1 FROM otra_tabla WHERE condicion_correlacionada\n);",
    "tableDemo": {
      "title": "Detección de Gerentes (dept_manager) en employees",
      "columns": [
        "emp_no",
        "first_name",
        "es_gerente"
      ],
      "rows": [
        [
          "110022",
          "Margareta",
          "TRUE"
        ],
        [
          "110039",
          "Vishwani",
          "TRUE"
        ]
      ]
    },
    "exampleQuery": "SELECT \n    e.emp_no,\n    e.first_name,\n    e.last_name\nFROM employees e\nWHERE EXISTS (\n    SELECT 1 \n    FROM dept_manager dm \n    WHERE dm.emp_no = e.emp_no \n      AND dm.to_date = '9999-01-01'\n)\nORDER BY e.emp_no ASC;",
    "exampleExplanation": "Retorna exclusivamente a los colaboradores que actualmente tienen un registro en la tabla dept_manager como directores activos.",
    "resultColumns": [
      "emp_no",
      "first_name",
      "last_name"
    ],
    "resultRows": [
      [
        "110039",
        "Vishwani",
        "Minakawa"
      ],
      [
        "110114",
        "Isamu",
        "Legleitner"
      ],
      [
        "110228",
        "Karsten",
        "Sigstam"
      ],
      [
        "110420",
        "Oscar",
        "Ghazalie"
      ]
    ],
    "exercise": {
      "question": "Completa para evaluar si existe al menos un registro en la subconsulta:",
      "templateBefore": "SELECT * FROM departments d WHERE ",
      "blank": "EXISTS",
      "templateAfter": " (SELECT 1 FROM dept_emp de WHERE de.dept_no = d.dept_no);",
      "hint": "Operador booleano de existencia en subconsultas."
    }
  },
  {
    "id": "create_db",
    "category": "SQL DATABASE (DDL)",
    "menuTitle": "SQL Create DB",
    "title": "SQL CREATE DATABASE Statement",
    "desc": "La sentencia <code>CREATE DATABASE</code> se utiliza para crear una nueva base de datos SQL en el servidor PostgreSQL.",
    "syntax": "CREATE DATABASE nombre_basedatos\n    [WITH ENCODING = 'UTF8'\n     TEMPLATE = template0\n     LC_COLLATE = 'es_EC.UTF-8'];",
    "tableDemo": {
      "title": "Parámetros estándar en PostgreSQL",
      "columns": [
        "Parámetro",
        "Valor Recomendado",
        "Propósito"
      ],
      "rows": [
        [
          "ENCODING",
          "'UTF8'",
          "Soporte completo de caracteres y tildes"
        ],
        [
          "LC_COLLATE",
          "'es_EC.UTF-8'",
          "Ordenamiento alfabético en español"
        ]
      ]
    },
    "exampleQuery": "-- Creación de la base de datos oficial del curso\nCREATE DATABASE employees_corp\n    WITH ENCODING = 'UTF8'\n    CONNECTION LIMIT = 100;",
    "exampleExplanation": "Crea la base de datos employees_corp con codificación UTF8 y un límite máximo de 100 conexiones simultáneas.",
    "resultColumns": [
      "Estado",
      "Mensaje"
    ],
    "resultRows": [
      [
        "OK",
        "CREATE DATABASE employees_corp ejecutado exitosamente."
      ]
    ],
    "exercise": {
      "question": "Escribe la instrucción DDL para crear una nueva base de datos llamada <code>empresa_db</code>:",
      "templateBefore": "",
      "blank": "CREATE DATABASE",
      "templateAfter": " empresa_db;",
      "hint": "Instrucción DDL para instanciar una nueva base de datos en el motor."
    }
  },
  {
    "id": "create_table",
    "category": "SQL DATABASE (DDL)",
    "menuTitle": "SQL Create Table",
    "title": "SQL CREATE TABLE Statement",
    "desc": "La sentencia <code>CREATE TABLE</code> se utiliza para crear una nueva tabla en una base de datos. Se definen las columnas y los tipos de datos que cada una de ellas contendrá.",
    "syntax": "CREATE TABLE nombre_tabla (\n    columna1 tipo_dato restricciones,\n    columna2 tipo_dato restricciones,\n    CONSTRAINT pk_nombre PRIMARY KEY (columna1)\n);",
    "tableDemo": {
      "title": "Estructura DDL de departments",
      "columns": [
        "Columna",
        "Tipo",
        "Nulo",
        "Restricción"
      ],
      "rows": [
        [
          "dept_no",
          "CHAR(4)",
          "NO",
          "PRIMARY KEY"
        ],
        [
          "dept_name",
          "VARCHAR(40)",
          "NO",
          "UNIQUE"
        ]
      ]
    },
    "exampleQuery": "CREATE TABLE departments (\n    dept_no   CHAR(4)      NOT NULL,\n    dept_name VARCHAR(40)  NOT NULL,\n    CONSTRAINT pk_departments PRIMARY KEY (dept_no),\n    CONSTRAINT uq_departments_dept_name UNIQUE (dept_name)\n);",
    "exampleExplanation": "Crea la tabla departments estableciendo dept_no como clave primaria de longitud fija y el nombre como único.",
    "resultColumns": [
      "Objeto Creado",
      "Restricciones Aplicadas"
    ],
    "resultRows": [
      [
        "departments",
        "pk_departments, uq_departments_dept_name"
      ]
    ],
    "exercise": {
      "question": "Completa para declarar la creación de una tabla relacional llamada <code>sedes</code>:",
      "templateBefore": "",
      "blank": "CREATE TABLE",
      "templateAfter": " sedes (sede_id SERIAL PRIMARY KEY, nombre VARCHAR(50));",
      "hint": "Instrucción DDL fundamental para crear una tabla."
    }
  },
  {
    "id": "drop_table",
    "category": "SQL DATABASE (DDL)",
    "menuTitle": "SQL Drop Table",
    "title": "SQL DROP TABLE Statement",
    "desc": "La sentencia <code>DROP TABLE</code> se utiliza para eliminar por completo una tabla existente en una base de datos, borrando su definición, índices y todos sus datos.",
    "syntax": "DROP TABLE [IF EXISTS] nombre_tabla [CASCADE | RESTRICT];",
    "tableDemo": {
      "title": "Impacto de CASCADE",
      "columns": [
        "Opción",
        "Comportamiento"
      ],
      "rows": [
        [
          "RESTRICT",
          "Impide borrar la tabla si otras tablas tienen claves foráneas hacia ella (por defecto)."
        ],
        [
          "CASCADE",
          "Elimina la tabla y automáticamente borra las restricciones foráneas dependientes."
        ]
      ]
    },
    "exampleQuery": "DROP TABLE IF EXISTS employee_bonuses CASCADE;",
    "exampleExplanation": "Elimina de forma segura la tabla si existe, junto con cualquier vista o clave foránea vinculada.",
    "resultColumns": [
      "Estado",
      "Afectación"
    ],
    "resultRows": [
      [
        "DROP TABLE",
        "Tabla eliminada permanentemente del catálogo."
      ]
    ],
    "exercise": {
      "question": "Completa la cláusula de seguridad para evitar errores si la tabla ya no existe:",
      "templateBefore": "DROP TABLE ",
      "blank": "IF EXISTS",
      "templateAfter": " departamentos_temporales;",
      "hint": "Comprueba si la tabla existe antes de intentar eliminarla."
    }
  },
  {
    "id": "alter_table",
    "category": "SQL DATABASE (DDL)",
    "menuTitle": "SQL Alter Table",
    "title": "SQL ALTER TABLE Statement",
    "desc": "La sentencia <code>ALTER TABLE</code> se utiliza para agregar, eliminar o modificar columnas y restricciones en una tabla existente sin tener que recrearla desde cero.",
    "syntax": "-- Agregar una columna\nALTER TABLE tabla ADD COLUMN nombre tipo [DEFAULT valor];\n\n-- Eliminar una columna\nALTER TABLE tabla DROP COLUMN nombre;\n\n-- Agregar una restricción\nALTER TABLE tabla ADD CONSTRAINT nombre_restriccion ...;",
    "tableDemo": {
      "title": "Evolución en departments",
      "columns": [
        "Columna Agregada",
        "Tipo",
        "Default"
      ],
      "rows": [
        [
          "is_active",
          "BOOLEAN",
          "TRUE"
        ]
      ]
    },
    "exampleQuery": "ALTER TABLE departments \nADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE;",
    "exampleExplanation": "Añade la columna booleana is_active a departments con valor por defecto TRUE para todas las filas existentes.",
    "resultColumns": [
      "Tabla Modificada",
      "Columna Añadida"
    ],
    "resultRows": [
      [
        "departments",
        "is_active (BOOLEAN, DEFAULT true)"
      ]
    ],
    "exercise": {
      "question": "Completa la sentencia para agregar una nueva columna llamada <code>email</code> a la tabla <code>employees</code>:",
      "templateBefore": "ALTER TABLE employees ",
      "blank": "ADD COLUMN",
      "templateAfter": " email VARCHAR(100);",
      "hint": "Instrucción de ALTER TABLE para incorporar una columna."
    }
  },
  {
    "id": "primary_key",
    "category": "SQL DATABASE (DDL)",
    "menuTitle": "SQL Primary Key",
    "title": "SQL PRIMARY KEY Constraint",
    "desc": "La restricción <code>PRIMARY KEY</code> identifica de forma única cada registro en una tabla. Las claves primarias deben contener valores <code>NOT NULL</code> y deben ser únicos. En la base de datos <code>Employees</code>, tablas como <code>salaries</code> y <code>dept_emp</code> utilizan <strong>claves primarias compuestas</strong> por múltiples columnas para modelar la temporalidad.",
    "syntax": "-- Clave primaria simple en la definición de columna\nCREATE TABLE tabla (id INT PRIMARY KEY);\n\n-- Clave primaria compuesta en tabla histórica\nCREATE TABLE salaries (\n    emp_no    INT  NOT NULL,\n    from_date DATE NOT NULL,\n    salary    INT  NOT NULL,\n    CONSTRAINT pk_salaries PRIMARY KEY (emp_no, from_date)\n);",
    "tableDemo": {
      "title": "Clave compuesta en salaries (emp_no + from_date)",
      "columns": [
        "emp_no (PK)",
        "from_date (PK)",
        "salary"
      ],
      "rows": [
        [
          "10001",
          "1986-06-26",
          "60117"
        ],
        [
          "10001",
          "1987-06-26",
          "62102"
        ],
        [
          "10001",
          "2002-06-22",
          "88958"
        ]
      ]
    },
    "exampleQuery": "-- Creación de tabla con clave primaria compuesta histórica\nCREATE TABLE employee_evaluations (\n    emp_no          INTEGER NOT NULL,\n    evaluation_date DATE    NOT NULL,\n    score           INTEGER NOT NULL,\n    CONSTRAINT pk_employee_evaluations PRIMARY KEY (emp_no, evaluation_date)\n);",
    "exampleExplanation": "La clave compuesta (emp_no, evaluation_date) asegura que un colaborador no tenga dos evaluaciones registradas en el mismo día.",
    "resultColumns": [
      "Tabla Creada",
      "Clave Primaria"
    ],
    "resultRows": [
      [
        "employee_evaluations",
        "PRIMARY KEY (emp_no, evaluation_date)"
      ]
    ],
    "exercise": {
      "question": "Declara la clave primaria para la columna <code>emp_no</code>:",
      "templateBefore": "CREATE TABLE employees (emp_no INT ",
      "blank": "PRIMARY KEY",
      "templateAfter": ", first_name VARCHAR(14));",
      "hint": "Restricción de clave principal que garantiza unicidad y no nulidad."
    }
  },
  {
    "id": "foreign_key",
    "category": "SQL DATABASE (DDL)",
    "menuTitle": "SQL Foreign Key",
    "title": "SQL FOREIGN KEY Constraint",
    "desc": "La restricción <code>FOREIGN KEY</code> se utiliza para prevenir acciones que destruirían los vínculos entre tablas. Una clave foránea es un campo (o colección de campos) en una tabla que se refiere a la <code>PRIMARY KEY</code> en otra tabla.",
    "syntax": "CONSTRAINT fk_nombre FOREIGN KEY (columna_local)\n    REFERENCES tabla_padre (columna_padre)\n    ON DELETE [RESTRICT | CASCADE | SET NULL]\n    ON UPDATE CASCADE;",
    "tableDemo": {
      "title": "Relación dept_emp -> employees y departments",
      "columns": [
        "Tabla Hija",
        "Columna FK",
        "Tabla Padre",
        "Regla de Borrado"
      ],
      "rows": [
        [
          "dept_emp",
          "emp_no",
          "employees",
          "ON DELETE CASCADE"
        ],
        [
          "dept_emp",
          "dept_no",
          "departments",
          "ON DELETE RESTRICT"
        ]
      ]
    },
    "exampleQuery": "ALTER TABLE dept_emp\nADD CONSTRAINT fk_dept_emp_departments\nFOREIGN KEY (dept_no) REFERENCES departments (dept_no)\nON DELETE RESTRICT;",
    "exampleExplanation": "La regla RESTRICT impide eliminar un departamento del catálogo si todavía existen empleados asignados a él.",
    "resultColumns": [
      "Restricción Creada",
      "Estado"
    ],
    "resultRows": [
      [
        "fk_dept_emp_departments",
        "Vínculo foráneo activo con ON DELETE RESTRICT"
      ]
    ],
    "exercise": {
      "question": "Completa para declarar que <code>emp_no</code> hace referencia a la tabla <code>employees</code>:",
      "templateBefore": "FOREIGN KEY (emp_no) ",
      "blank": "REFERENCES",
      "templateAfter": " employees (emp_no);",
      "hint": "Palabra clave para indicar la tabla y columna de destino."
    }
  },
  {
    "id": "check",
    "category": "SQL DATABASE (DDL)",
    "menuTitle": "SQL Check",
    "title": "SQL CHECK Constraint",
    "desc": "La restricción <code>CHECK</code> se utiliza para limitar el rango de valores que se pueden colocar en una columna. Si define una restricción CHECK en una columna, solo permitirá ciertos valores específicos para esta columna.",
    "syntax": "-- En la creación de la tabla:\nCREATE TABLE tabla (\n    salario NUMERIC CHECK (salario > 0)\n);\n\n-- O mediante ALTER TABLE:\nALTER TABLE tabla ADD CONSTRAINT chk_nombre CHECK (condicion);",
    "tableDemo": {
      "title": "Restricción de género en employees",
      "columns": [
        "Columna",
        "Regla CHECK",
        "Valores Válidos"
      ],
      "rows": [
        [
          "gender",
          "gender IN ('M', 'F')",
          "'M' o 'F'"
        ],
        [
          "salary",
          "salary > 0",
          "Cualquier entero positivo"
        ]
      ]
    },
    "exampleQuery": "ALTER TABLE salaries\nADD CONSTRAINT chk_salaries_positive_amount\nCHECK (salary > 0);\n\nALTER TABLE salaries\nADD CONSTRAINT chk_salaries_valid_interval\nCHECK (to_date >= from_date);",
    "exampleExplanation": "Garantiza matemáticamente que los sueldos sean estrictamente positivos y que la fecha de fin sea igual o posterior a la de inicio.",
    "resultColumns": [
      "Restricción",
      "Condición Validada"
    ],
    "resultRows": [
      [
        "chk_salaries_positive_amount",
        "salary > 0"
      ],
      [
        "chk_salaries_valid_interval",
        "to_date >= from_date"
      ]
    ],
    "exercise": {
      "question": "Añade una restricción CHECK para verificar que la edad de contratación sea mayor de 18 años:",
      "templateBefore": "ALTER TABLE employees ADD CONSTRAINT chk_edad ",
      "blank": "CHECK",
      "templateAfter": " (hire_date > birth_date);",
      "hint": "Palabra clave para definir restricciones de validación condicional."
    }
  },
  {
    "id": "create_index",
    "category": "SQL DATABASE (DDL)",
    "menuTitle": "SQL Create Index",
    "title": "SQL CREATE INDEX Statement",
    "desc": "La sentencia <code>CREATE INDEX</code> se utiliza para crear índices en tablas. Los índices se utilizan para recuperar datos de la base de datos más rápidamente de lo que sería posible sin ellos. Los usuarios no pueden ver los índices; solo se utilizan para acelerar búsquedas.",
    "syntax": "CREATE [UNIQUE] INDEX nombre_indice\nON nombre_tabla [USING btree] (columna1, columna2);\n\n-- Índice parcial en PostgreSQL:\nCREATE INDEX idx_nombre ON tabla (columna) WHERE condicion;",
    "tableDemo": {
      "title": "Impacto en salaries (2,844,047 filas)",
      "columns": [
        "Tipo de Búsqueda",
        "Sin Índice (Seq Scan)",
        "Con Índice B-Tree (Index Scan)"
      ],
      "rows": [
        [
          "WHERE to_date = '9999-01-01'",
          "~120 ms",
          "~4.2 ms (¡28x más rápido!)"
        ]
      ]
    },
    "exampleQuery": "-- Índice parcial especializado en registros activos vigentes\nCREATE INDEX idx_salaries_current \nON salaries (emp_no, salary)\nWHERE to_date = '9999-01-01';",
    "exampleExplanation": "Crea un índice parcial que indexa solo el 8% de la tabla (las filas vigentes), ahorrando memoria RAM y acelerando drásticamente las consultas.",
    "resultColumns": [
      "Índice Creado",
      "Tipo",
      "Condición Parcial"
    ],
    "resultRows": [
      [
        "idx_salaries_current",
        "BTREE",
        "WHERE to_date = '9999-01-01'"
      ]
    ],
    "exercise": {
      "question": "Completa la instrucción para crear un índice sobre el apellido de los colaboradores:",
      "templateBefore": "",
      "blank": "CREATE INDEX",
      "templateAfter": " idx_emp_last_name ON employees (last_name);",
      "hint": "Instrucción DDL para generar un índice de aceleración de consultas."
    }
  },
  {
    "id": "views",
    "category": "SQL DATABASE (DDL)",
    "menuTitle": "SQL Views",
    "title": "SQL CREATE VIEW Statement",
    "desc": "En SQL, una vista (<code>VIEW</code>) es una tabla virtual basada en el conjunto de resultados de una instrucción SQL. Contiene filas y columnas, al igual que una tabla real. Las vistas son ideales para encapsular lógica de negocio compleja, como el filtrado de vigencia temporal en <code>Employees</code>.",
    "syntax": "CREATE OR REPLACE VIEW nombre_vista AS\nSELECT columna1, columna2, ...\nFROM tabla\nWHERE condicion;",
    "tableDemo": {
      "title": "Vista: vw_active_employees (Consolidada)",
      "columns": [
        "emp_no",
        "colaborador",
        "dept_name",
        "title",
        "salary"
      ],
      "rows": [
        [
          "10001",
          "Georgi Facello",
          "Development",
          "Senior Engineer",
          "88958"
        ],
        [
          "10002",
          "Bezalel Simmel",
          "Sales",
          "Staff",
          "72527"
        ]
      ]
    },
    "exampleQuery": "CREATE OR REPLACE VIEW vw_active_employees AS\nSELECT \n    e.emp_no,\n    e.first_name || ' ' || e.last_name AS colaborador,\n    d.dept_name AS departamento,\n    t.title AS cargo,\n    s.salary AS remuneracion\nFROM employees e\nJOIN dept_emp de ON e.emp_no = de.emp_no AND de.to_date = '9999-01-01'\nJOIN departments d ON de.dept_no = d.dept_no\nJOIN titles t    ON e.emp_no = t.emp_no  AND t.to_date  = '9999-01-01'\nJOIN salaries s  ON e.emp_no = s.emp_no  AND s.to_date  = '9999-01-01';",
    "exampleExplanation": "Encapsula un cruce de 4 tablas con sus filtros de vigencia para que cualquier desarrollador consulte directamente la vista con un simple SELECT *.",
    "resultColumns": [
      "Objeto Creado",
      "Tipo"
    ],
    "resultRows": [
      [
        "vw_active_employees",
        "VIEW (Tabla Virtual Normalizada)"
      ]
    ],
    "exercise": {
      "question": "Escribe la sentencia para crear una vista llamada <code>vista_depto</code>:",
      "templateBefore": "",
      "blank": "CREATE VIEW",
      "templateAfter": " vista_depto AS SELECT dept_no, dept_name FROM departments;",
      "hint": "Instrucción DDL para definir una tabla virtual."
    }
  }
];

let currentTopicIndex = 0;

function initApp() {
    renderSidebar();
    loadTopic(0);
    setupEventListeners();
}

function renderSidebar() {
    const sidebarNav = document.getElementById('sidebar-nav');
    sidebarNav.innerHTML = '';

    let currentCat = '';
    let currentUl = null;

    TOPICS.forEach((t, idx) => {
        if (t.category !== currentCat) {
            currentCat = t.category;
            const catTitle = document.createElement('div');
            catTitle.className = 'sidebar-section-title';
            catTitle.textContent = currentCat;
            sidebarNav.appendChild(catTitle);

            currentUl = document.createElement('ul');
            currentUl.className = 'sidebar-nav-list';
            sidebarNav.appendChild(currentUl);
        }

        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = `#${t.id}`;
        a.textContent = t.menuTitle;
        a.id = `nav-link-${t.id}`;
        a.onclick = (e) => {
            e.preventDefault();
            loadTopic(idx);
            // Close mobile menu if open
            document.getElementById('sidebar').classList.remove('open');
        };
        currentUl.appendChild(li);
        li.appendChild(a);
    });
}

function loadTopic(index) {
    if (index < 0 || index >= TOPICS.length) return;
    currentTopicIndex = index;
    const t = TOPICS[index];

    // Highlight active nav
    document.querySelectorAll('.sidebar-nav-list a').forEach(a => a.classList.remove('active'));
    const activeLink = document.getElementById(`nav-link-${t.id}`);
    if (activeLink) activeLink.classList.add('active');

    // Title & Desc
    document.getElementById('topic-title').textContent = t.title;
    document.getElementById('topic-desc').innerHTML = t.desc;

    // Syntax
    document.getElementById('syntax-box').textContent = t.syntax;

    // Table demo
    const tableDemoCont = document.getElementById('table-demo-container');
    if (t.tableDemo) {
        let tableHtml = `<h3 style="font-size: 1.1rem; margin-bottom: 8px;">${t.tableDemo.title}</h3>`;
        tableHtml += '<div class="table-responsive"><table class="demo-table"><thead><tr>';
        t.tableDemo.columns.forEach(col => {
            tableHtml += `<th>${col}</th>`;
        });
        tableHtml += '</tr></thead><tbody>';
        t.tableDemo.rows.forEach(row => {
            tableHtml += '<tr>';
            row.forEach(cell => {
                tableHtml += `<td>${cell}</td>`;
            });
            tableHtml += '</tr>';
        });
        tableHtml += '</tbody></table></div>';
        tableDemoCont.innerHTML = tableHtml;
        tableDemoCont.style.display = 'block';
    } else {
        tableDemoCont.style.display = 'none';
    }

    // Example Box
    document.getElementById('example-code').textContent = t.exampleQuery;
    document.getElementById('example-explanation').textContent = t.exampleExplanation;

    // Reset Result Box
    const resBox = document.getElementById('result-output-box');
    resBox.classList.remove('show');
    resBox.innerHTML = '';

    // Exercise Box
    const ex = t.exercise;
    const exCont = document.getElementById('exercise-container');
    if (ex) {
        exCont.innerHTML = `
            <div class="exercise-header">
                <span>✏️ Ponte a Prueba con un Ejercicio:</span>
            </div>
            <p class="exercise-text">${ex.question}</p>
            <div class="exercise-code-fill">
                <span>${escapeHtml(ex.templateBefore)}</span>
                <input type="text" id="exercise-input" class="blank-input" placeholder="Escribe aquí" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" style="width: ${Math.max(120, ex.blank.length * 14)}px;">
                <span>${escapeHtml(ex.templateAfter)}</span>
            </div>
            <div class="exercise-actions">
                <button class="check-btn" onclick="checkExercise()">Comprobar Respuesta ❯</button>
                <button class="show-answer-btn" onclick="showAnswer()">Ver Solución</button>
            </div>
            <div id="exercise-feedback" class="feedback-msg"></div>
        `;
        exCont.style.display = 'block';
    } else {
        exCont.style.display = 'none';
    }

    // Update Prev / Next Buttons
    const prevBtn = document.getElementById('prev-topic-btn');
    const nextBtn = document.getElementById('next-topic-btn');
    const bottomPrev = document.getElementById('bottom-prev-btn');
    const bottomNext = document.getElementById('bottom-next-btn');

    if (index === 0) {
        prevBtn.classList.add('disabled');
        bottomPrev.classList.add('disabled');
    } else {
        prevBtn.classList.remove('disabled');
        bottomPrev.classList.remove('disabled');
    }

    if (index === TOPICS.length - 1) {
        nextBtn.classList.add('disabled');
        bottomNext.classList.add('disabled');
    } else {
        nextBtn.classList.remove('disabled');
        bottomNext.classList.remove('disabled');
    }

    // Scroll content to top
    document.getElementById('content-wrapper').scrollTop = 0;
}

function executeExample() {
    const t = TOPICS[currentTopicIndex];
    const resBox = document.getElementById('result-output-box');

    let html = '<div class="result-title">📊 Resultado de la Consulta en Base de Datos:</div>';
    html += '<div class="table-responsive"><table class="demo-table"><thead><tr>';
    t.resultColumns.forEach(col => {
        html += `<th>${col}</th>`;
    });
    html += '</tr></thead><tbody>';
    t.resultRows.forEach(row => {
        html += '<tr>';
        row.forEach(cell => {
            html += `<td>${cell}</td>`;
        });
        html += '</tr>';
    });
    html += '</tbody></table></div>';
    html += `<div style="font-size: 0.8rem; color: #16a34a; font-weight: 700; margin-top: 4px;">✓ Consulta ejecutada con éxito sobre la base de datos employees (${t.resultRows.length} filas devueltas).</div>`;

    resBox.innerHTML = html;
    resBox.classList.add('show');
}

function checkExercise() {
    const t = TOPICS[currentTopicIndex];
    const input = document.getElementById('exercise-input');
    const feedback = document.getElementById('exercise-feedback');
    const userVal = input.value.trim().toUpperCase();
    const correctVal = t.exercise.blank.toUpperCase();

    if (userVal === correctVal) {
        feedback.className = 'feedback-msg correct';
        feedback.innerHTML = '🎉 ¡Correcto! Has completado la sentencia con la sintaxis exacta.';
    } else {
        feedback.className = 'feedback-msg incorrect';
        feedback.innerHTML = `❌ No es correcto. Pista: ${t.exercise.hint}`;
    }
}

function showAnswer() {
    const t = TOPICS[currentTopicIndex];
    const input = document.getElementById('exercise-input');
    const feedback = document.getElementById('exercise-feedback');
    input.value = t.exercise.blank;
    feedback.className = 'feedback-msg';
    feedback.style.color = '#0284c7';
    feedback.innerHTML = `💡 Solución oficial: <strong>${t.exercise.blank}</strong>`;
}

function setupEventListeners() {
    // Search filter
    const searchInput = document.getElementById('sidebar-search');
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        document.querySelectorAll('.sidebar-nav-list li').forEach(li => {
            const text = li.textContent.toLowerCase();
            li.style.display = text.includes(term) ? 'block' : 'none';
        });
    });

    // Prev / Next click
    document.getElementById('prev-topic-btn').onclick = () => loadTopic(currentTopicIndex - 1);
    document.getElementById('next-topic-btn').onclick = () => loadTopic(currentTopicIndex + 1);
    document.getElementById('bottom-prev-btn').onclick = () => loadTopic(currentTopicIndex - 1);
    document.getElementById('bottom-next-btn').onclick = () => loadTopic(currentTopicIndex + 1);

    // Theme toggle
    document.getElementById('theme-toggle').onclick = () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        document.getElementById('theme-toggle').textContent = newTheme === 'dark' ? '☀️ Claro' : '🌙 Oscuro';
    };

    // Mobile menu toggle
    document.getElementById('menu-toggle').onclick = () => {
        document.getElementById('sidebar').classList.toggle('open');
    };
}

function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

window.onload = initApp;
