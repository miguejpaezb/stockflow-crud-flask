# StockFlow — Sistema de Inventario

Aplicación web ligera para gestión de inventario con **Flask** (backend), **MySQL** (base de datos) y **HTML/CSS/JS** (frontend vanilla). Permite listar, crear, editar, eliminar productos y agregar stock mediante una interfaz de una sola página (SPA).

---

## Stack tecnológico

| Capa          | Tecnología                                          |
| ------------- | --------------------------------------------------- |
| Backend       | Python 3, Flask 3.x (POO: MVC con dataclasses)      |
| Base de datos | MySQL 8+                                            |
| Frontend      | HTML5, CSS3 (custom properties), JavaScript vanilla |
| Comunicación  | REST API JSON (`fetch`)                             |
| Conector DB   | `mysql-connector-python`                            |
| Paradigma     | Orientado a objetos + MethodView + Repository       |

---

## Estructura del proyecto

```
ADSO-StockFlow/
├── main.py                          # Punto de entrada: create_app().run()
├── app/                             # Paquete Flask (POO)
│   ├── __init__.py                  # Fábrica create_app() — inyecta dependencias
│   ├── config.py                    # @dataclass Config — lee .env
│   ├── database.py                  # Clase Database — conexiones MySQL
│   ├── json_provider.py             # Serializador JSON para Decimal
│   ├── .env                         # Variables de entorno (credenciales DB)
│   ├── env.example                  # Plantilla de .env
│   ├── models/
│   │   └── product.py               # @dataclass Product — entidad de dominio
│   ├── repositories/
│   │   └── product_repository.py    # ProductRepository — capa de acceso a datos
│   ├── controllers/
│   │   ├── product_list_controller.py   # GET / POST /api/products
│   │   ├── product_item_controller.py   # GET / PUT / DELETE /api/products/<id>
│   │   └── stock_controller.py          # PUT /api/products/<id>/stock
│   ├── static/                      # Frontend estático (CSS, JS, íconos)
│   │   ├── css/main.css
│   │   ├── js/
│   │   │   ├── app.js
│   │   │   ├── modal.js             # [Legacy]
│   │   │   └── services/api.js
│   │   └── assets/icons/
│   └── templates/
│       └── index.html               # Página SPA (renderizada por Flask)
├── sql/
│   └── database.sql                 # Esquema BD + datos de prueba
├── .gitignore
└── README.md
```

---

## Requisitos previos

- **Python 3.10+** instalado
- **MySQL 8+** corriendo en `localhost`
- **pip** para instalar dependencias

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/miguejpaezb/stockflow-crud-flask.git
cd ADSO-StockFlow
```

### 2. Crear entorno virtual e instalar dependencias

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install flask==3.1.0 flask-cors==5.0.0 mysql-connector-python==9.3.0 python-dotenv==1.1.0
```

### 3. Configurar variables de entorno

```powershell
copy app\env.example app\.env
```

Editar `app/.env` con las credenciales de tu MySQL:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=stockflow_db
```

### 4. Crear la base de datos

```powershell
# Desde el monitor de MySQL o línea de comandos
mysql -u root -p < sql\database.sql
```

El script crea la base de datos `stockflow_db`, la tabla `products` y 6 productos de prueba.

### 5. Ejecutar la aplicación

```powershell
python main.py
```

Abrir el navegador en **http://localhost:5000**

---

## API REST — Endpoints

| Método   | Ruta                       | Descripción                         |
| -------- | -------------------------- | ----------------------------------- |
| `GET`    | `/api/products`            | Listar todos los productos          |
| `GET`    | `/api/products/<id>`       | Obtener producto por ID             |
| `POST`   | `/api/products`            | Crear un nuevo producto             |
| `PUT`    | `/api/products/<id>`       | Actualizar producto (merge parcial) |
| `PUT`    | `/api/products/<id>/stock` | Agregar unidades al stock           |
| `DELETE` | `/api/products/<id>`       | Eliminar producto                   |

### Ejemplo de petición

```bash
# Crear producto
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Cable USB","category":"Cables","stock":20,"minimum_stock":5,"price":12000}'

# Respuesta
# {"message": "Producto creado exitosamente", "id": 7}
```

---

## Características principales

- **CRUD completo** de productos con API REST
- **Búsqueda en tiempo real** (filtrado client-side sin recargar)
- **Agregar stock** con modal dedicado e incremento atómico en BD
- **Edición parcial** (PATCH-style merge) — envía solo los campos modificados
- **Diseño responsive** con CSS custom properties y flexbox
- **Prevención de SQL injection** con placeholders parametrizados
- **Sanitización XSS** en el frontend al renderizar nombres de producto
- **Datos de prueba** incluidos para empezar a usar inmediatamente

---

## Licencia

Uso educativo — ADSO 3134556
