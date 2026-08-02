import json
import os

ARCHIVO = "contactos.json"


def cargar_contactos():
    if not os.path.exists(ARCHIVO):
        return {}
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, IOError):
        return {}


def guardar_contactos(contactos):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(contactos, archivo, indent=2, ensure_ascii=False)


def añadir_contacto(contactos):
    nombre = input("\nNombre del contacto: ").strip().lower()
    if not nombre:
        print("❌ El nombre no puede estar vacío.")
        return
    if nombre in contactos:
        print(f"⚠️  Ya existe un contacto llamado '{nombre}'.")
        return
    telefono = input("Teléfono: ").strip()
    email = input("Email: ").strip()
    contactos[nombre] = {"telefono": telefono, "email": email}
    guardar_contactos(contactos)
    print(f"✅ Contacto '{nombre}' añadido correctamente.")


def ver_contactos(contactos):
    if not contactos:
        print("\n📭 La agenda está vacía.")
        return
    print(f"\n📇 Agenda ({len(contactos)} contactos):")
    print("=" * 50)
    for nombre, datos in sorted(contactos.items()):
        print(f"👤 {nombre.capitalize()}")
        print(f"   📞 Teléfono: {datos['telefono'] or '(no registrado)'}")
        print(f"   📧 Email:    {datos['email'] or '(no registrado)'}")
        print("-" * 50)


def buscar_contacto(contactos):
    busqueda = input("\nNombre a buscar: ").strip().lower()
    if not busqueda:
        print("❌ Debes escribir algo para buscar.")
        return
    encontrados = {
        nombre: datos
        for nombre, datos in contactos.items()
        if busqueda in nombre
    }
    if not encontrados:
        print(f"🔍 No se encontró ningún contacto con '{busqueda}'.")
        return
    print(f"\n✅ Encontrado(s) {len(encontrados)} contacto(s):")
    print("=" * 50)
    for nombre, datos in sorted(encontrados.items()):
        print(f"👤 {nombre.capitalize()}")
        print(f"   📞 Teléfono: {datos['telefono'] or '(no registrado)'}")
        print(f"   📧 Email:    {datos['email'] or '(no registrado)'}")
        print("-" * 50)


def borrar_contacto(contactos):
    nombre = input("\nNombre del contacto a borrar: ").strip().lower()
    if nombre not in contactos:
        print(f"❌ No existe el contacto '{nombre}'.")
        return
    confirmacion = input(f"⚠️  ¿Seguro que quieres borrar a '{nombre}'? (s/N): ").strip().lower()
    if confirmacion == "s":
        del contactos[nombre]
        guardar_contactos(contactos)
        print(f"🗑️  Contacto '{nombre}' borrado.")
    else:
        print("✅ Operación cancelada.")

def editar_contacto(contactos):
    nombre = input("\nNombre de contacto a editar:").strip().lower()
    if nombre not in contactos:
        print(f"❌ No existe el contacto '{nombre}'. ")
        return
    print(f"👤 Editando contacto '{nombre.capitalize()}'")
    print("   (Pulsa INTRO sin escribir nada para NO cambiarlo)")
    telefono_actual = contactos[nombre]["telefono"]
    email_actual = contactos[nombre]["email"]
    
    nuevo_tel = input(f"📞 Nuevo telefono[{telefono_actual}]: ").strip()
    nuevo_email = input(f"📲 Nuevo email[{email_actual}]: ").strip()
    
    if nuevo_tel:
        contactos[nombre]["telefono"] = nuevo_tel
    if nuevo_email:
        contactos[nombre]["email"] = nuevo_email
        
    guardar_contactos(contactos)
    print(f"✅ Contacto '{nombre}' actualizado correctamente.")
    
def mostrar_menu():
    print("\n" + "=" * 50)
    print("          📇 AGENDA DE CONTACTOS")
    print("=" * 50)
    print("  1. Añadir contacto")
    print("  2. Ver todos los contactos")
    print("  3. Buscar contacto")
    print("  4. Borrar contacto")
    print("  6. Editar contacto")
    print("  5. Salir")
    print("=" * 50)


def main():
    contactos = cargar_contactos()
    print(f"\n👋 Bienvenido. Se han cargado {len(contactos)} contacto(s).")

    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-6): ").strip()

        if opcion == "1":
            añadir_contacto(contactos)
        elif opcion == "2":
            ver_contactos(contactos)
        elif opcion == "3":
            buscar_contacto(contactos)
        elif opcion == "4":
            borrar_contacto(contactos)
        elif opcion == "6":
            editar_contacto(contactos)
        elif opcion == "5":
            guardar_contactos(contactos)
            print("\n👋 ¡Hasta pronto! Contactos guardados.\n")
            break
        else:
            print("\n❌ Opción no válida. Introduce un número del 1 al 6.")


if __name__ == "__main__":
    main()
