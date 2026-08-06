import socket
import requests
import json
import os
from datetime import datetime

# ============================================================
# 🔢 CONTADOR DE BÚSQUEDAS (Reto 3)
# ============================================================
ARCHIVO_CONTADOR = "contador_busquedas.txt"   # archivo donde guardamos el número (ej: "47")


def leer_contador() -> int:
    """Lee el archivo txt y DEVUELVE un ENTERO con el número total de búsquedas.
    Si el archivo no existe o está roto → devuelve 0 y NO ROMPE NADA.
    """
    try:
        with open(ARCHIVO_CONTADOR, "r", encoding="utf-8") as f:
            texto = f.read().strip()   # leemos todo el archivo (que es solo un número)
            return int(texto)
    except (FileNotFoundError, ValueError, IOError):
        return 0


def guardar_contador(numero: int) -> None:
    """Recibe un ENTERO (ej: 48) y LO GUARDA en el archivo txt (como texto plano).
    No devuelve nada.
    """
    try:
        with open(ARCHIVO_CONTADOR, "w", encoding="utf-8") as f:
            f.write(str(numero))   # convertimos ENTERO a TEXTO antes de escribir en disco
    except IOError as e:
        print(f"❌ No se pudo guardar el contador: {str(e)}")

class Dominio:
    def __init__(self, nombre):
        self.nombre = nombre.lower().strip()
        self.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        self.ip = None
        self.pais = None
        self.ciudad = None
        self.isp = None
        self.servidor_http = None
        self.estado_http = None
        
        self.errores = []
    
    def a_diccionario(self):
        return {
            "nombre" : self.nombre,
            "fecha" : self.fecha,
            "ip" : self.ip,
            "pais" : self.pais,
            "ciudad" : self.ciudad,
            "isp" : self.isp,
            "servidor_http": self.servidor_http,
            "estado_http" : self.estado_http,
            "errores": self.errores,
        }

    def __str__(self):
        lineas = [
            "=" * 60,
            f"🕵️ Informe OSINT de: {self.nombre}",
            f"📅 Fecha investigación: {self.fecha}",
            "-" * 60,
            f"📞 [DNS] IP        : {self.ip or '❌ No encontrado'}",
            f"🗺️  [GEO] País      : {self.pais or '❌ No encontrado'}",
            f"🗺️  [GEO] Ciudad    : {self.ciudad or '❌ No encontrado'}",
            f"🗺️  [GEO] ISP       : {self.isp or '❌ No encontrado'}",
            f"🏠 [HTTP] Servidor  : {self.servidor_http or '❌ No encontrado'}",
            f"🏠 [HTTP] Estado    : {self.estado_http or '❌ No encontrado'}",
            "-" * 60,
        ]
        if self.errores:
            lineas.append("⚠️  Errores:")
            for err in self.errores:
                lineas.append(f"   - {err}")
            lineas.append("-" * 60)
        return "\n".join(lineas)
    
# ============================================================
# 🔌 SISTEMA DE TRANSFORMS (AYUDANTES DETECTIVES)
# ============================================================

class Transform:
    """Clase BASE (plantilla). Todos los Transform reales heredarán de ella.
    Es como la clase Tarea, pero NUNCA crearemos un objeto Transform() directamente.
    Solo usaremos sus HIJOS: TransformDNS, TransformGeolocalizacion, TransformHTTP
    """
    nombre = "Transform Genérico"  # cada hijo lo sobrescribirá con su nombre

    def ejecutar(self, dominio: Dominio):
        """Método principal que todos los hijos deben reescribir.
        Recibe un Dominio, trabaja sobre él y lo modifica.
        Devuelve None (no devuelve nada, modifica el objeto directamente)
        """
        raise NotImplementedError("Los transforms de verdad deben hacer override de ejecutar()")


# -------- PRIMER TRANSFORM REAL: DNS ----------------
class TransformDNS(Transform):
    """📞 Ayudante 1: Busca la IP de un dominio usando socket.
    (Es como la guía telefónica de Internet)
    """
    nombre = "DNS (buscar IP)"

    def ejecutar(self, dominio):
        print(f"  📞 [{self.nombre}] Buscando IP de {dominio.nombre} ...")

        # 🔴 Cuidado: esta línea puede fallar si el dominio no existe!
        # por eso usamos try / except
        try:
            # socket.gethostbyname("google.com") → "142.250.184.14"
            ip = socket.gethostbyname(dominio.nombre)

            # Si todo fue bien, guardamos la IP en el dominio
            dominio.ip = ip
            print(f"  ✅ [{self.nombre}] IP encontrada: {ip}")

        except socket.gaierror as e:
            # Error típico: dominio NO EXISTE (NXDOMAIN) o no hay internet
            mensaje_error = f"No se pudo resolver DNS: {str(e)}"
            print(f"  ❌ [{self.nombre}] {mensaje_error}")
            dominio.errores.append(mensaje_error)
            
# -------- SEGUNDO TRANSFORM REAL: GEOLOCALIZACIÓN IP ----------------
class TransformGeolocalizacion(Transform):
    """🗺️ Ayudante 2: Dada una IP, pregunta a ip-api.com dónde está alojado.
    Si el TransformDNS falló y no hay IP, este ayudante no hace nada (se salta).
    """
    nombre = "Geolocalización IP"

    def ejecutar(self, dominio):
        # PRIMERA COMPROBACIÓN IMPORTANTE: ¿tengo ya la IP?
        # si el TransformDNS anterior falló → no podemos hacer nada → return
        if dominio.ip is None:
            print(f"  ⏭️  [{self.nombre}] Sin IP disponible, me salto este paso.")
            return  # salgo de la función sin hacer nada

        print(f"  🗺️  [{self.nombre}] Geolocalizando IP {dominio.ip} ...")

        try:
            # 📞 LLAMADA HTTP REAL a internet! (igual que cuando navegas)
            # requests.get("URL") → devuelve un objeto Response
            url = f"http://ip-api.com/json/{dominio.ip}?fields=status,country,city,isp,message"
            respuesta = requests.get(url, timeout=5)   # ← ¡RELLENA! método GET (método requests que usas para pedir datos a una web)

            # .json() convierte la respuesta HTTP (texto en formato JSON) a diccionario Python!
            datos = respuesta.json()                     # ← ¡RELLENA! método del objeto respuesta que convierte JSON a dict (tiene un .json...)

            if datos.get("status") == "success":
                # Todo OK, rellenamos los campos de Dominio
                dominio.pais = datos.get("country")
                dominio.ciudad = datos.get("city")       # ← ¡RELLENA! método de diccionario para obtener valor de una clave de forma segura
                dominio.isp = datos.get("isp")
                print(f"  ✅ [{self.nombre}] {dominio.ciudad}, {dominio.pais} — ISP: {dominio.isp}")
            else:
                # La API respondió pero con error (ej: IP reservada/privada)
                mensaje_error = f"API devolvió error: {datos.get('message', 'desconocido')}"
                print(f"  ❌ [{self.nombre}] {mensaje_error}")
                dominio.errores.append(mensaje_error)

        except requests.exceptions.RequestException as e:
            # Cualquier error de red: sin internet, timeout, etc.
            mensaje_error = f"Fallo de conexión HTTP: {str(e)}"
            print(f"  ❌ [{self.nombre}] {mensaje_error}")
            dominio.errores.append(mensaje_error)
            
# -------- TERCER TRANSFORM REAL: CABECERAS HTTP ----------------
class TransformHTTP(Transform):
    """🏠 Ayudante 3: Se conecta a http://dominio y pregunta sus cabeceras.
    Sirve para ver qué servidor tienen (nginx, Apache, cloudflare...)
    """
    nombre = "Cabeceras HTTP"

    def ejecutar(self, dominio):
        print(f"  🏠 [{self.nombre}] Consultando cabeceras HTTP de {dominio.nombre} ...")

        try:
            # .head() = pide SOLO cabeceras, no el contenido. Muy rápido.
            # allow_redirects=True → si el dominio manda a www. lo sigue.
            # timeout=5 → si tarda más de 5s, cancela.
            url = f"https://{dominio.nombre}"
            respuesta = requests.head(url, timeout=5, allow_redirects=True)  # ← ¡RELLENA! método para pedir SOLO cabeceras (empieza por h, acaba por d)

            # 1) Código de estado HTTP: 200 = OK, 404 = no encontrada, 301 = movida
            dominio.estado_http = f"{respuesta.status_code} {respuesta.reason}"
            print(f"  ✅ [{self.nombre}] Estado HTTP: {dominio.estado_http}")

            # 2) Cabecera 'Server' → nos dice qué software usan (nginx/Apache/etc.)
            #    .headers es un diccionario-like con todas las cabeceras.
            servidor = respuesta.headers.get("Server")   # ← ¡RELLENA! atributo del objeto respuesta con las cabeceras (empieza por h, acaba by rs)
            if servidor:
                dominio.servidor_http = servidor            # ← ¡RELLENA! atributo de Dominio para guardar el servidor (linea 16 de __init__: self.???????_http)
                print(f"  ✅ [{self.nombre}] Servidor detectado: {servidor}")
            else:
                print(f"  ℹ️  [{self.nombre}] El servidor no envía la cabecera 'Server' (es normal, por seguridad).")

        except requests.exceptions.RequestException as e:
            mensaje_error = f"No se pudo conectar por HTTPS: {str(e)}"
            print(f"  ❌ [{self.nombre}] {mensaje_error}")
            dominio.errores.append(mensaje_error)        # ← ¡RELLENA! atributo de Dominio donde guardamos la lista de fallos (linea 19 del __init__)
            
# ============================================================
# 🧠 CLASE CEREBRO: GESTIONA TODA LA INVESTIGACIÓN
# ============================================================

class InvestigacionOSINT:
    """🧠 El Jefe de detectives. Agrupa todos los transforms y los ejecuta en orden."""

    def __init__(self):
        # 📋 Lista de nuestros ayudantes (3 transforms)
        # Aquí es donde FÁCILMENTE podrías añadir MÁS transforms en el futuro
        # (igual que el Transform Hub de OGI, pero sin web)
        self.transforms = [
            TransformDNS(),
            TransformGeolocalizacion(),
            TransformHTTP(),
        ]

    def investigar(self, nombre_dominio: str) -> Dominio:
        """Método principal: dado un dominio (string), ejecuta TODOS los transforms
        en orden y devuelve el objeto Dominio completamente rellenado.
        """
        # 1) Creamos el expediente (Dominio vacío con sus campos None / listas vacías)
        dominio = Dominio(nombre_dominio)   # ← ¡RELLENA! Qué clase molde es el expediente? Empieza por D...
        print(f"\n🔍 Iniciando investigación OSINT de: {dominio.nombre}")
        print(f"👥 Equipo de detectives: {len(self.transforms)} transforms listos\n")

        # 2) Ejecutamos CADA transform en orden (lista self.transforms)
        for transform in self.transforms:      # ← ¡RELLENA! atributo de esta clase donde guardamos la lista de transforms (línea arriba)
            transform.ejecutar(dominio)       # ← ¡RELLENA! método principal que TODO transform tiene en común (empieza por eje, acaba por tar)
            # (no devuelve nada, modifica el propio objeto dominio)

        print(f"\n✅ Investigación finalizada para {dominio.nombre}")

        # RETO 3: actualizar contador de búsquedas TOTALES
        total = leer_contador()
        total_nuevo = total + 1
        guardar_contador(total_nuevo)
        print(f"\n📊 Total de búsquedas históricas: {total_nuevo}")

        return dominio

    def guardar_informe(self, dominio: Dominio, carpeta: str = "informes_osint"):
        """Guarda el objeto Dominio como archivo JSON dentro de la carpeta indicada.
        Si la carpeta no existe, la crea automáticamente (os.makedirs).
        Nombre archivo: nombre_dominio.json
        Devuelve la ruta del archivo si todo OK, o None si falla.
        """
        # Creamos carpeta si no existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok=True)

        # Nombre del archivo: reemplazamos / por _ por si acaso
        nombre_archivo = f"{dominio.nombre.replace('/', '_')}.json"
        ruta_completa = os.path.join(carpeta, nombre_archivo)

        try:
            with open(ruta_completa, "w", encoding="utf-8") as f:
                # ¡usamos a_diccionario()! Lo definimos en Dominio ;)
                json.dump(dominio.a_diccionario(), f, indent=2, ensure_ascii=False)   # ← ¡RELLENA! función de json para guardar (dump/dumps)
            print(f"\n💾 Informe guardado correctamente en: {ruta_completa}")
            return ruta_completa
        except IOError as e:
            print(f"\n❌ Error al guardar el informe: {str(e)}")
            return None
        
# ============================================================
# 🖥️ FUNCIÓN PRINCIPAL: INTERFAZ DE USUARIO (MENÚ CONSOLA)
# ============================================================

def mostrar_menu():
    """Imprime el menú principal por pantalla."""
    print("\n" + "=" * 60)
    print("           🕵️  MINI-OSINT DE DANIEL  🕵️")
    print("        (Inspirado en khashashin/ogi - versión tú)")
    print("=" * 60)
    print("  1. Investigar un dominio 🔍")
    print("  0. SALIR 👋")
    print("=" * 60)


def main():
    total_historico = leer_contador()
    print(f"👋 ¡Bienvenido al Mini-OSINT! Versión POO + HTTP APIs + JSON  |  📊 Llevas {total_historico} búsqueda(s) en total.")

    # Creamos AL PRINCIPIO el "jefe de detectives" (el cerebro)
    investigador = InvestigacionOSINT()   # ← ¡RELLENA! Clase cerebro que creamos en el paso 5, empieza por In...

    while True:
        mostrar_menu()
        opcion = input("Elige opción (1 o 0): ").strip()

        if opcion == "1":
            print("\n--- Nueva investigación ---")
            dominio_texto = input("Escribe el dominio a investigar (ej: google.com): ").strip()
            if not dominio_texto:
                print("⚠️  Dominio vacío. Inténtalo otra vez.")
                continue

            # 1) EJECUTAR LOS 3 TRANSFORMS (investigar)
            resultado: Dominio = investigador.investigar(dominio_texto)   # ← ¡RELLENA! método principal de InvestigacionOSINT que recibe un dominio string

            # 2) MOSTRAR RESULTADO POR PANTALLA (usa el __str__ de Dominio!)
            print()
            print(resultado)   # ← ¡llama automáticamente a __str__! Mágico Python.

            # 3) PREGUNTAR SI QUIERE GUARDAR EN JSON
            guardar = input("\n¿Guardar informe en JSON? (S/n): ").strip().lower()
            if guardar in ("s", "si", "sí", ""):
                investigador.guardar_informe(resultado)   # ← ¡RELLENA! método de InvestigacionOSINT que guarda el informe en fichero (recibe objeto Dominio)

        elif opcion == "0":
            print("\n👋 ¡Gracias por usar Mini-OSINT de Daniel!")
            print("Versión inspirada en khashashin/ogi")
            print("Siguiente paso: aprender FastAPI y montar una web visual como OGI 💪\n")
            break

        else:
            print("\n❌ Opción no válida. Escribe 1 o 0.")


# ============================================================
# 🚀 PUNTO DE ENTRADA (cuando ejecutas python3 mini_osint.py)
# ============================================================
if __name__ == "__main__":
    main()