
import csv 
import os 
from datetime import datetime

class Libro:
    def __init__(self,id_libro, titulo, autor,genero,paginas,leido=False,puntuacion=0,fecha_lectura=None ):
        self.id_libro = id_libro
        self.titulo = titulo.title().strip()
        self.autor = autor.lower().strip()
        self.genero = genero.lower().strip()
        self.paginas = int(paginas)
        self.leido = leido
        self.puntuacion = puntuacion
        self.fecha_lectura = fecha_lectura
        
    def marcar_leido(self,puntuacion):
        
        if 0 <= puntuacion <= 5:
             self.puntuacion = puntuacion
            
        else:
            print("❌ La puntuacion debe ser un numero entre 0 y 5")
        self.leido = True    
        if self.fecha_lectura is None: 
            self.fecha_lectura = datetime.now().strftime("%Y-%m-%d")
        
    def a_fila_csv(self) -> dict:
        """Convierte este objeto Libro a un DICCIONARIO PYTHON con las 8 keys exactas
        (id, titulo, autor, genero, paginas, leido, puntuacion, fecha_lectura).
        Nota: el booleano leido lo convertimos a STRING porque CSV solo guarda texto.
        """
        return {
            "id":self.id_libro,
            "titulo":self.titulo,
            "autor":self.autor,
            "genero":self.genero,
            "paginas":self.paginas,
            "leido":str(self.leido),# Para leído: str(self.leido) para que sea "True"/"False" string.
            "puntuacion":self.puntuacion,
            "fecha_lectura":self.fecha_lectura or ""# Para fecha: self.fecha_lectura or "" (si es None, pon cadena vacía para CSV).
        }

    @classmethod
    def desde_fila_csv(cls, fila: dict):  # cls = Libro (la propia clase)
        """✨ Método MÁGICO de CLASE (no de objeto). Recibe una fila del CSV (diccionario)
        y DEVUELVE UN NUEVO OBJETO Libro() con los datos ya CONVERTIDOS a sus tipos reales.
        """
        return cls(
            # RELLENA TÚ LOS 8 PARÁMETROS del constructor Libro, con las CONVERSIONES.
            id_libro=int(fila.get("id")),
            titulo=fila.get("titulo"),
            autor=fila.get("autor"),
            genero=fila.get("genero"),
            paginas=int(fila.get("paginas")),
            leido=True if fila.get("leido")=="True" else False,
            puntuacion=int(fila.get("puntuacion",0)),
            fecha_lectura=fila.get("fecha_lectura")or None 
       
        )
            
    
    def __str__(self):     
        estado =  "✅ leido"if self.leido  else "◻️ pendiente"
        return f"📚 {self.titulo} |  {estado} | {'⭐️' * self.puntuacion}  { '✫' * (5 - self.puntuacion)}" 
    
ARCHIVO_CSV = "biblioteca.csv" 

class GestorBiblioteca:
    def __init__(self):
        self.libros = []
        self.proximo_id = 1
        self.cargar_csv()
    
    def guardar_csv(self):
        with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f,fieldnames=["id","titulo","autor","genero","paginas","leido","puntuacion","fecha_lectura"])
            escritor.writeheader()
            escritor.writerows([libro.a_fila_csv() for libro in self.libros])
            
            
    def cargar_csv(self):
        if os.path.exists(ARCHIVO_CSV) is False:
            return
        with open(ARCHIVO_CSV, "r", encoding="utf-8")as f:
            reader = csv.DictReader(f)
            self.libros = [Libro.desde_fila_csv(fila)for fila in reader]
            if self.libros:
                self.proximo_id = max(libro.id_libro for libro in self.libros)
                self.proximo_id += 1
            else:
                self.proximo_id = 1
            

    def _buscar_por_id(self,id_libro:int):
        for libro in self.libros:
            if libro.id_libro == id_libro:
                return libro
        return None
    
    def añadir_libro(self,titulo: str, autor:str,genero:str,paginas:int) -> Libro | None:
        if titulo.strip() == "":
            print("❌ Error titulo vacio")
            return None
        nuevo_libro = Libro(self.proximo_id, titulo, autor, genero, paginas)
        self.libros.append(nuevo_libro)
        self.proximo_id+=1
        self.guardar_csv()
        print(f"✅ Libro {nuevo_libro} añadido correctamente")
        return nuevo_libro
    
    def ver_todos(self, solo_pendientes=False):
        if not self.libros:
            print("📭 No hay libros en la biblioteca")
            return
        if solo_pendientes:
            mostrados = [l for l in self.libros if not l.leido]
        else:
            mostrados = self.libros[:]
        titulo = "📚 LIBROS PENDIENTES DE LEER"if solo_pendientes else "📚 Todos los libro"
        print(f"\n{titulo} ({len(mostrados)}) ")
        print("-" * 100)
        for l in mostrados:
            print(l)
        
        if not solo_pendientes:
            leidos = sum(1 for l in self.libros if l.leido)
            total = len(self.libros)
            print("-" * 100)
            print(f"📊 Progreso lectura: {leidos} / {total} leidos ({round(leidos*100/total, 1)}%)")
            
    def buscar_libro(self, busqueda: str):
        texto_busqueda = busqueda.lower().strip()
        resultados = [l for l in self.libros if (texto_busqueda in l.titulo.lower()) 
                     or (texto_busqueda in l.autor.lower())
                     ]
        if not resultados:
            print(f"❌ Libro no encontrado libros con '{texto_busqueda}'.")
            return []
        
        print(f"\n🔎 Encontrados {len(resultados)} libro(s) con '{texto_busqueda}':")
        print("-" * 100)
        for l in resultados:
            print(l)
        print("-" * 100)
        return resultados
       
        
    def marcar_leido(self,id_libro:int, puntuacion: int):
        libro = self._buscar_por_id(id_libro)
        if libro is None:
            print("❌ Libro no encontrado")
            return
        else:
            libro.marcar_leido(puntuacion)
            self.guardar_csv()
            print(f"✅ Libro {id_libro} marcado leido con puntuacion {puntuacion}")
            
    def editar_libro(self, id_libro: int):
            libro = self._buscar_por_id(id_libro)
            if libro is None:      # <-- ESTE es el correcto
                print("❌ Libro no encontrado")
                return
            
            print(f"\n✏️ Editando el libro [{libro.id_libro:03d}] → {libro.titulo}")
            print("(pulsa INTRO directamente para NO CAMBIAR ese campo)\n")
            
            nuevo_titulo = input(f"Nuevo titulo (actual='{libro.titulo}'): ").strip()
            if nuevo_titulo:
                libro.titulo = nuevo_titulo.title().strip()
            
            nuevo_autor = input(f"Nuevo autor (actual= '{libro.autor}'): ").strip()
            if nuevo_autor:
                libro.autor = nuevo_autor.lower().strip()
                
            nuevo_genero = input(f"Nuevo genero (actual='{libro.genero}'): ").strip()
            if nuevo_genero:
                libro.genero = nuevo_genero.lower().strip()
                
            paginas_texto = input(f"Nº de paginas (actual={libro.paginas}): ").strip()
            if paginas_texto:
                try:
                    libro.paginas = int(paginas_texto)
                except ValueError:
                    print("ℹ️ Paginas no cambiadas (no escribiste un numero).")
            
            self.guardar_csv()
            print(f"\n✅ Libro [{libro.id_libro:03d}] actualizado correctamente.")
        
   
    def borrar_libro(self, id_libro: int, confirmar: bool = True):
        libro = self._buscar_por_id(id_libro)
        if libro is None:
            print(f"❌ Libro no encontrado.")
            return
        if confirmar:
            confirm = input(f"⚠️ ¿Seguro que quieres borrar el libro [{libro.id_libro:03d}] {libro.titulo}? (s/n)").strip().lower()
            if confirm not in ("s", "si", "sí"):
                print("ℹ️ Operacion cancelada")
                return
        
        self.libros.remove(libro)
        self.guardar_csv()
        print(f"🗑️ Libro [{libro.id_libro:03d}] borrado correctamente.")
        
def mostrar_menu():
     
        print("╔═════════════════════════════════════════════════════════╗")
        print("║               📚GESTOR DE BIBLIOTECA                    ║")
        print("║ 1. Añadir nuevo                                         ║")
        print("║ 2. Ver todos los libros                                 ║")
        print("║ 3. 📚 Ver solo los pendientes de leer                   ║")
        print("║ 4. 🔎 Buscar libro                                      ║")
        print("║ 5. ✅ Marcar libro como leido                           ║")
        print("║ 6. ✏️ Editar informacion de un libro                    ║")
        print("║ 7. 🗑️ Borrar libro                                      ║")
        print("║                                                         ║")
        print("║ 0. 🚪 Salir                                             ║")
        print("╚═════════════════════════════════════════════════════════╝")
        
        opcion = input("Ingrese su opcion: ").strip()
        return opcion
    
def pedir_id_valido(gestor):
    while True:
        texto_id = input("\n📌 Escribe el ID del libro (o 'salir' para cncelar): ").strip().lower()
        
        if texto_id == "" or texto_id  == "salir":
            print("ℹ️ Operacion cacelada.")
            return None
        
        try:
            id_numero = int(texto_id)
        except ValueError:
            print("❌ Tienes que escribir un NUMERO entero. Intentalo de nuevo.")
            continue
        
        libro_encontrado = gestor._buscar_por_id(id_numero)
        if libro_encontrado is None:
            print(f"❌ No existe ningun libro con ID {id_numero}. Prueba otro.")
            continue
        
        return id_numero
    
def main():
    gestor = GestorBiblioteca()
    while True:
        print("\n" * 20)
        
        opcion = mostrar_menu()
        
        if opcion == "1":
            print("\n AÑADIR NUEVO LIBRO")
            print("-" * 50)
            titulo = input("Titulo: ").strip()
            autor = input("Autor: ").strip()
            genero = input("Genero: ").strip()
            try:
                paginas = int(input("Nº de paginas: "))
            except ValueError:
                print("❌ Error: las paginas tienen que ser un numero entero. Libro NO añadido")
                input("\nPulsa INTRO para continuar...")
                continue
            
            gestor.añadir_libro(titulo, autor, genero, paginas)
            input("\nPulsa INTRO para continuar...")
            
        elif opcion == "2":
            gestor.ver_todos()
            input("\nPulsa INTRO para continuar...")
            
        elif opcion == "3":
            gestor.ver_todos(solo_pendientes=True)
            input("\nPulsa INTRO para continuar...")
            
        elif opcion == "4":
            texto = input(" Texto a buscar en titulo / autor: ").strip()
            gestor.buscar_libro(texto)
            input("\nPulsa INTRO para continuar...")
            
        elif opcion == "5":
            print("\n✅ MARCAR LIBRO COMO LEIDO")
            id_libro = pedir_id_valido(gestor)
            if id_libro is None:
                input("\nPulsa INTRO para continuar...")
                continue
            
            try:
                puntuacion = int(input("Puntuacion (0 a 5): ").strip())
            except ValueError:
                print("❌ La puntuacion debe ser un numero entero. ")
                input("\nPulsa INTRO para continuar...")
                continue
            
            if not (0 <= puntuacion <= 5):
                print("❌ Puntuacion fuera de rango (0-5).")
                input("\nPulsa INTRO para continuar...")
                continue
            
            gestor.marcar_leido(id_libro,puntuacion)
            input("\nPulsa INTRO para continuar...")
            
        elif opcion == "6":
            print("\n✏️ Editar informacion de un libro")
            id_libro = pedir_id_valido(gestor)
            if id_libro is None:
                input("\nPulsa INTRO para continuar...")
                continue
            gestor.editar_libro(id_libro)
            input("\nPulsa INTRO para continuar...")
            
        elif opcion == "7":
            print("\n 🗑️ Borrar libro")
            id_libro = pedir_id_valido(gestor)
            if id_libro is None:
                input("\nPulsa INTRO para continuar...")
                continue
            gestor.borrar_libro(id_libro)
            input("\nPulsa INTRO para continuar...")
            
        elif opcion == "0":
            print("\n👋 ¡Hasta la proxima lector!📚")
            break
        
        else:
            print("❌ Opcion no valida. Escribe un numero del 0 al 7.")
            input("\nPulsa INTRO para continuar...")
            
if __name__ == "__main__":
    main()
    
        



       
        
                 
            
        
            
            
       

