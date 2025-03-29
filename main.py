from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="API de Búsqueda y Resumen",
    description="API que busca información en internet y genera resúmenes",
    version="1.0.0"
)

class SearchRequest(BaseModel):
    query: str = Field(..., description="Término de búsqueda")
    max_results: int = Field(3, description="Número máximo de resultados")

class Source(BaseModel):
    title: str
    url: str

class SummaryResponse(BaseModel):
    query: str
    summary: str
    sources: List[Source]

@app.get("/")
def read_root():
    return {"message": "API de búsqueda y resumen. Usa /docs para ver la documentación."}

@app.post("/search", response_model=SummaryResponse)
async def search_and_summarize(request: SearchRequest):
    try:
        # Buscar información en internet
        search_results = search_web(request.query, request.max_results)
        
        if not search_results:
            raise HTTPException(status_code=404, detail="No se encontraron resultados para esta búsqueda")
        
        # Extraer contenido de las páginas
        contents = []
        sources = []
        
        for result in search_results:
            try:
                content = extract_content(result['url'])
                if content:
                    contents.append(content)
                    sources.append(Source(
                        title=result['title'],
                        url=result['url']
                    ))
            except Exception as e:
                print(f"Error extrayendo contenido de {result['url']}: {str(e)}")
        
        if not contents:
            raise HTTPException(status_code=404, detail="No se pudo extraer contenido de los resultados")
        
        # Generar resumen
        combined_content = "\n\n".join(contents)
        summary = generate_summary(request.query, combined_content)
        
        return SummaryResponse(
            query=request.query,
            summary=summary,
            sources=sources
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def search_web(query, max_results=3):
    """
    Función simple para simular búsqueda web.
    En una implementación real, usarías una API como Google Search, Bing, DuckDuckGo, etc.
    """
    # Aquí usamos una búsqueda básica de Google (nota: esto es para demostración)
    search_url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    for g in soup.find_all('div', class_='g')[:max_results]:
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            if link.startswith('/url?q='):
                link = link.split('/url?q=')[1].split('&')[0]
            
            title_element = g.find('h3')
            if title_element:
                title = title_element.text
                results.append({
                    'title': title,
                    'url': link
                })
    
    return results

def extract_content(url):
    """Extrae el contenido principal de una página web"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Eliminar elementos no deseados
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Extraer párrafos
        paragraphs = [p.text.strip() for p in soup.find_all('p') if p.text.strip()]
        
        # Limitar a un tamaño razonable
        max_chars = 5000
        combined = " ".join(paragraphs)
        if len(combined) > max_chars:
            combined = combined[:max_chars] + "..."
            
        return combined
    except Exception as e:
        print(f"Error extrayendo contenido de {url}: {str(e)}")
        return ""

def generate_summary(query, content):
    """
    Genera un resumen del contenido.
    En una implementación real, usarías una API como OpenAI.
    """
    # Implementación simple para demostración:
    words = content.split()
    max_words = 150
    if len(words) > max_words:
        summary = " ".join(words[:max_words]) + "..."
    else:
        summary = content
        
    return f"Resumen sobre '{query}': {summary}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
