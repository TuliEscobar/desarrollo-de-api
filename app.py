from fastapi import FastAPI

# Crear la aplicación FastAPI
app = FastAPI(title="API de Cálculos Geométricos")

def calcular_area_circulo(radio: float):
    return 3.14159 * radio ** 2

# Ahora lo expones como un endpoint en FastAPI
@app.get("/area_circulo/{radio}")
def area_circulo(radio: float):
    area = calcular_area_circulo(radio)
    return {"radio": radio, "area": area}

# Ruta principal
@app.get("/")
def read_root():
    return {"mensaje": "API de cálculos geométricos. Accede a /area_circulo/{radio} para calcular el área de un círculo."}

# Para ejecutar: uvicorn app:app --host 127.0.0.1 --port 8000 