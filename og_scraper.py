import urllib.request
import urllib.error
import html.parser
import ssl
import re

class OGParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.resultados = {}
        self._dentro_title = False
        self.title_fallback = ""
        
    def handle_starttag(self, tag, attrs: list[tuple]):
        d = dict(attrs)
        if tag == "meta":
            atributos = dict(attrs)
            if "property"  in atributos: 
               if atributos["property"].startswith("og:"):
                self.resultados[atributos["property"]] = atributos.get("content", "")
                
        if tag == "title":
            self._dentro_title = True
            pass
        
    def handle_data(self, data: str):
        if self._dentro_title == True:
            self.title_fallback += data.strip()
            pass
        
    def handle_endtag(self, tag: str):
        if tag == "title":
            self._dentro_title = False
            pass
        
#-----------------------------------------------------------------------------------------------------

def extraer_og(url: str) -> dict:
    if not(url.startswith("http://") or url.startswith("https://")):
        return{"error": "URL invalida, debe empezar por https o http"}
    
    cabeceras = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    peticion = urllib.request.Request(url, headers=cabeceras)
    
    try:
        respuesta = urllib.request.urlopen(peticion, timeout=10, context=ssl._create_unverified_context())
        html_crudo = respuesta.read().decode("utf-8", errors="ignore")
        
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}"}
        
    except urllib.error.URLError as e:
        return {"error": f"URL mala: {e.reason}"}
    
    OG = OGParser()
    OG.feed(html_crudo)
    
    if "og:title" not in OG.resultados or not OG.resultados["og:title"].strip():
        OG.resultados["og:title"] = OG.title_fallback
    return OG.resultados


    
    
def imprimir_tarjeta(datos: dict):
    if "error" in datos:
        print("❌ Error:", datos["error"])
        return
    print("="* 50)
    print("🪪 TITULO:     " + (datos.get("og:title") or "(No disponible)" ))
    print("📝 DESCRIPCION:" + (datos.get("og:description") or "(No disponible)"))
    print("🖼️ IMAGEN:     " + (datos.get("og:image") or "(No disponible)"))
    print("🏷️ TIPO:       " + (datos.get("og:type") or "website"))
    print("🔗 URL OG:     " + (datos.get("og:url") or "(No disponible)"))
        
def main():
    print("🔍 OPENGRAPH INTEL OSINT SCRAPER")
    print("="*50)
    url = input("👉 Introduce la URL a analizar (https//...): ").strip()
    if url == "":
        print("ℹ️ Saliendo")
        return
    datos = extraer_og(url)
    imprimir_tarjeta(datos)
    
if __name__ == "__main__":
        main()
        
        
        
        
            
    
    
    
        
       
    
                    
