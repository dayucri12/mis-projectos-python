import json
import os
from datetime import datetime

ARCHIVO_TAREAS = "tareas.json"


class Tarea:
    def __init__(self, texto, id_tarea, completada=False, fecha=None):
        self.id = id_tarea
        self.texto = texto
        self.completada = completada
        if fecha is None:
            self.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        else:
            self.fecha = fecha

    def marcar_completada(self):
        self.completada = True

    def desmarcar(self):
        self.completada = False

    def editar_texto(self, nuevo_texto):
        self.texto = nuevo_texto

    def a_diccionario(self):
        return {
            "id": self.id,
            "texto": self.texto,
            "completada": self.completada,
            "fecha": self.fecha,
        }

    def __str__(self):
        estado = "✅" if self.completada else "⬜"
        return f"[{self.id:03d}] {estado} {self.fecha}  {self.texto}"


class GestorTareas:
    def __init__(self):
        self.tareas = []
        self.proximo_id = 1
        self.cargar_de_json()

    def guardar_en_json(self):
        lista_dicts = [t.a_diccionario() for t in self.tareas]
        datos = {"proximo_id": self.proximo_id, "tareas": lista_dicts}
        with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    def cargar_de_json(self):
        if not os.path.exists(ARCHIVO_TAREAS):
            return
        try:
            with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as f:
                datos = json.load(f)
            self.proximo_id = datos.get("proximo_id", 1)
            lista_dicts = datos.get("tareas", [])
            self.tareas = [
                Tarea(
                    texto=d["texto"],
                    id_tarea=d["id"],
                    completada=d["completada"],
                    fecha=d["fecha"]
                )
                for d in lista_dicts
            ]
        except (json.JSONDecodeError, IOError):
            self.tareas = []
            self.proximo_id = 1

    def añadir_tarea(self, texto):
        if not texto.strip():
            print("❌ El texto de la tarea no puede estar vacío.")
            return None
        nueva = Tarea(texto, self.proximo_id)
        self.tareas.append(nueva)
        self.proximo_id += 1
        self.guardar_en_json()
        print(f"✅ Añadida tarea [{nueva.id:03d}]")
        return nueva

    def listar_tareas(self, solo_pendientes=False):
        if not self.tareas:
            print("\n📭 No hay tareas.")
            return
        if solo_pendientes:
            lista = [t for t in self.tareas if not t.completada]
        else:
            lista = self.tareas
        print(f"\n📋 Lista de tareas ({len(lista)}):")
        print("-" * 70)
        for t in lista:
            print(t)
        print("-" * 70)
        completadas = sum(1 for t in self.tareas if t.completada)
        total = len(self.tareas)
        print(f"📊 Progreso: {completadas}/{total} completadas.")

    def _buscar_por_id(self, id_tarea):
        for tarea in self.tareas:
            if tarea.id == id_tarea:
                return tarea
        return None

    def marcar_completada(self, id_tarea):
        t = self._buscar_por_id(id_tarea)
        if t is None:
            print(f"❌ No existe tarea con id {id_tarea}.")
            return
        t.marcar_completada()
        self.guardar_en_json()
        print(f"✅ Tarea [{t.id:03d}] marcada como completada.")

    def desmarcar(self, id_tarea):
        t = self._buscar_por_id(id_tarea)
        if t is None:
            print(f"❌ No existe tarea con id {id_tarea}.")
            return
        t.desmarcar()
        self.guardar_en_json()
        print(f"⬜ Tarea [{t.id:03d}] desmarcada.")

    def borrar_tarea(self, id_tarea):
        t = self._buscar_por_id(id_tarea)
        if t is None:
            print(f"❌ No existe tarea con id {id_tarea}.")
            return
        self.tareas.remove(t)
        self.guardar_en_json()
        print(f"🗑️ Tarea [{id_tarea:03d}] borrada correctamente.")

    def editar_tarea(self, id_tarea):
        t = self._buscar_por_id(id_tarea)
        if t is None:
            print(f"❌ No existe tarea con id {id_tarea}.")
            return
        print(f"Editando: [{t.id:03d}] {t.texto}")
        nuevo_texto = input("Nuevo texto(INTRO para no cambiar): ").strip()
        if nuevo_texto:
            t.editar_texto(nuevo_texto)
            self.guardar_en_json()
            print(f"✅ Texto actualizado correctamente.")
        else:
            print("ℹ️ No se ha cambiado nada.")


def pedir_id_valido(mensaje="ID de la tarea: "):
    while True:
        texto = input(mensaje).strip()
        try:
            return int(texto)
        except ValueError:
            print("❌ Por favor, escribe un NÚMERO entero.")


def mostrar_menu():
    print("\n" + "=" * 70)
    print("                     ✅ GESTOR DE TAREAS ✅")
    print("=" * 70)
    print("  1. Añadir nueva tarea")
    print("  2. Ver TODAS las tareas")
    print("  3. Ver solo PENDIENTES")
    print("  4. Marcar tarea como COMPLETADA (por ID)")
    print("  5. Desmarcar tarea (por ID)")
    print("  6. Editar texto de una tarea (por ID)")
    print("  7. Borrar tarea (por ID)")
    print("  0. SALIR")
    print("=" * 70)


def main():
    gestor = GestorTareas()
    print(f"👋 Bienvenido. Cargadas {len(gestor.tareas)} tarea(s).")

    while True:
        mostrar_menu()
        opcion = input("Elige una opción (0-7): ").strip()

        if opcion == "1":
            texto = input("\n✏️  Texto de la nueva tarea: ").strip()
            gestor.añadir_tarea(texto)

        elif opcion == "2":
            gestor.listar_tareas()

        elif opcion == "3":
            gestor.listar_tareas(solo_pendientes=True)

        elif opcion == "4":
            id_n = pedir_id_valido()
            gestor.marcar_completada(id_n)

        elif opcion == "5":
            id_n = pedir_id_valido()
            gestor.desmarcar(id_n)

        elif opcion == "6":
            id_n = pedir_id_valido()
            gestor.editar_tarea(id_n)

        elif opcion == "7":
            id_n = pedir_id_valido()
            confirm = input(f"⚠️  ¿Seguro que borras tarea {id_n}? (s/N): ").strip().lower()
            if confirm == "s":
                gestor.borrar_tarea(id_n)
            else:
                print("✅ Operación cancelada.")

        elif opcion == "0":
            gestor.guardar_en_json()
            print("\n👋 ¡Hasta luego! Tareas guardadas en tareas.json 👍\n")
            break

        else:
            print("\n❌ Opción no válida. Escribe un número entre 0 y 7.")


if __name__ == "__main__":
    main()
