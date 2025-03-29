# API de Búsqueda y Resumen

Esta API permite buscar información en internet y generar resúmenes automáticos de los contenidos encontrados.

## Características

- Búsqueda de información en internet
- Extracción de contenido relevante de páginas web
- Generación de resúmenes utilizando técnicas de procesamiento de texto

## Requisitos

- Python 3.8 o superior

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/TuliEscobar/desarrollo-de-api.git
cd desarrollo-de-api
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env-example .env
```
Edita el archivo `.env` si necesitas configurar alguna clave de API.

## Uso

Iniciar el servidor:
```bash
uvicorn main:app --reload
```

La API estará disponible en http://localhost:8000

### Documentación

La documentación automática está disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints

- `GET /`: Información básica de la API
- `POST /search`: Busca información y genera un resumen

Ejemplo de petición a `/search`:
```json
{
  "query": "inteligencia artificial",
  "max_results": 3
}
```

## Desarrollo

Todo este proyecto se desarrolló automáticamente desde Cursor IDE utilizando conexiones MCP de GitHub. La integración continua y el despliegue fueron automatizados gracias a estas herramientas.

## Licencia

MIT 