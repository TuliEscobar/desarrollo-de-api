from fastapi import FastAPI
from pyngrok import ngrok
import uvicorn
import nest_asyncio
from dotenv import load_dotenv
import os

load_dotenv()

Ngrok_token = os.getenv("Ngrok_token")

# Permitir múltiples loops en Colab
nest_asyncio.apply()

# Crear una instancia de FastAPI
app = FastAPI()

# Definir una ruta de prueba
@app.get("/")
def read_root():
    return {"message": "¡Hola desde FastAPI en Colab!"}

# Definir una ruta con parámetros
@app.get("/saludar/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"Hola, {nombre}!"}

# Iniciar el servidor y exponerlo con ngrok
def run():
    public_url = ngrok.connect(8000).public_url
    print(f"🔥 FastAPI está corriendo en {public_url}")
    uvicorn.run(app, host="0.0.0.0", port=8000)

run()
