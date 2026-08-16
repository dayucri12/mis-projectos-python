from __future__ import annotations
import sqlite3
import os
from datetime import datetime

class Gasto:
    def __init__(self,id_gasto,concepto,categoria,importe,fecha=None,pagado=False):
        self.id_gasto = id_gasto
        self.concepto = concepto.strip().capitalize()
        self.categoria = categoria.lower().strip()
        self.importe = float(importe)
        if fecha is None:
            self.fecha = datetime.now().strftime("%Y-%m-%d")
        else:
            self.fecha = fecha
            self.pagado = pagado
    def __str__(self):
        estado = "👍 pagado" if self.pagado else "⏳ pendiente"
        emojis = {"comida": "🍔","transporte":"🚗","ocio":"🎮","alquiler":"🏠",
                  "facturas":"🏠","otros": "📦"}
        emoji = emojis.get(self.categoria, "💰")
        return f"[{self.id_gasto:03d}] {emoji} {self.fecha} | {self.categoria:<10} | {self.concepto:<30} | {self.importe:>8.2f} € | {estado}"
    
ARCHIVO_DB = "gastos.db"        
class GestorGastos:
    def __init__(self):
        self.conn = sqlite3.connect(ARCHIVO_DB, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._crear_tabla_si_no_existe()
        
    def _crear_tabla_si_no_existe(self):
        sql = """
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concepto TEXT NOT NULL,
            categoria TEXT NOT NULL,
            importe REAL NOT NULL,
            fecha TEXT NOT NULL,
            pagado INTEGER DEFAULT 0 
            )
        """
        self.cursor.execute(sql)
        self.conn.commit()
        
    def cerrar(self):
        self.conn.close()
        
    def _fila_a_gasto(self, fila: tuple) -> Gasto:
        return Gasto(
            id_gasto=fila[0],
            concepto=fila[1],
            categoria=fila[2],
            importe=fila[3],
            pagado=fila[5] == 1,
            fecha=fila[4],
            
        )
    
       
    
    def _buscar_por_id(self,id_gasto: int) -> Gasto | None:
        sql = "SELECT id, concepto, categoria, importe, fecha, pagado FROM gastos WHERE id = ?"
        self.cursor.execute(sql, (id_gasto,))
        fila = self.cursor.fetchone()
        if fila is None:
            return None
        return self._fila_a_gasto(fila)
        
# =================================================================
# 🚀 MÉTODOS CRUD  (7 métodos - TÚ RELLENAS LOS # TODO:)
# =================================================================

    def añadir_gasto(self, concepto: str, categoria: str, importe: float, fecha=None, pagado=False) -> Gasto | None:
        if concepto.strip() == "" or categoria.strip() == "": # ✅ PASO 1 (TU): Validar entrada. Si concepto.strip() == "" o categoria.strip() == "":
            print("❌ Error: concepto y categorias son obligatorios")#   print("❌ Error: concepto y categoría son obligatorios")
            return None
        
    

        # ✅ PASO 2 (YA HECHO): Normalizamos datos (igual que Gasto.__init__)
        concepto = concepto.strip().capitalize()
        categoria = categoria.lower().strip()
        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d")
        pagado_int = 1 if pagado else 0
        try:
            importe = float(importe)
            if importe <= 0:
                print("❌ Error: el importe debe ser MAYOR que 0")
                return None
        except ValueError:
            print("❌ Error: el importe tiene que ser un número (ej: 12.50)")
            return None

        # ✅ PASO 3 (YA HECHO): Sentencia SQL INSERT
        sql = "INSERT INTO gastos (concepto, categoria, importe, fecha, pagado) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(sql, (concepto, categoria, importe, fecha, pagado_int))
        self.conn.commit()

        # ✅ PASO 4 (TU): Recupera el ID que SQLite asignó automaticamente → self.cursor.lastrowid
        #   Luego crea OBJETO Gasto nuevo con ese ID y TODOS los datos (igual que desde_fila)
        #   print(f"✅ Gasto añadido correctamente: {objeto_gasto}")
        #   return objeto_gasto
        # TODO: aquí tu código
        nuevo_id = self.cursor.lastrowid
        gasto_nuevo = Gasto(nuevo_id, concepto, categoria, importe, fecha, pagado)
        print(f"✅ Gasto añadido correctamente: {gasto_nuevo}")
        return gasto_nuevo
    # -----------------------------------------------------------------

    def ver_todos(self, solo_pendientes: bool = False) -> list[Gasto]:
        # ✅ PASO 1 (YA HECHO): SQL SELECT
        if solo_pendientes:
            sql = "SELECT id, concepto, categoria, importe, fecha, pagado FROM gastos WHERE pagado = 0 ORDER BY fecha DESC"
        else:
            sql = "SELECT id, concepto, categoria, importe, fecha, pagado FROM gastos ORDER BY fecha DESC"
        self.cursor.execute(sql)
        filas = self.cursor.fetchall()  # ← lista de TUPLAS

        # ✅ PASO 2 (TU): Si no hay filas (len(filas) == 0) → print 📭 No hay gastos... return []
        # TODO: aquí tu código
        if not filas:
            print("⚠️ No hay gastos...")
            return []
        # ✅ PASO 3 (TU): Convierte CADA fila en OBJETO Gasto con list comprehension →
        gastos = [self._fila_a_gasto(fila) for fila in filas]
        # TODO: aquí tu código

        # ✅ PASO 4 (TU): Print cabecera. Si solo_pendientes → "📋 GASTOS PENDIENTES DE PAGAR"Si no → "📋 TODOS LOS GASTOS"
        print("📋 GASTOS PENDIENTES DE PAGAR" if solo_pendientes else "📋 TODOS LOS GASTOS")                
        print("-" * 110) # Luego print("-" * 110)
        for g in gastos: print(g)# Luego for g in gastos: print(g)
        print("-" * 110) # Luego print("-" * 110)
        total = sum(g.importe for g in gastos);print(f"💸 TOTAL: {total:.2f} €") # Luego Suma TOTAL: total = sum(g.importe for g in gastos) → print(f"💸 TOTAL: {total:.2f} €")
        if not solo_pendientes:
            total_pend = sum(g.importe for g in gastos if not g.pagado)# Si NO es solo_pendientes: suma también los pendientes: total_pend = sum(g.importe for g in gastos if not g.pagado)
            print(f"⏳ PENDIENTE DE PAGAR: {total_pend:.2f} €") #   → print(f"⏳ PENDIENTE DE PAGAR: {total_pend:.2f} €")
        return gastos # return gastos
        # TODO: aquí tu código

    # -----------------------------------------------------------------

    def ver_por_mes(self, anio:int, mes:int) -> list[Gasto]:
        sql = f"""
                SELECT id, concepto, categoria, importe, fecha, pagado
                FROM gastos
                WHERE strftime('%y', fecha) = ?
                AND strftime('%m', fecha) = ?
                ORDER BY fecha ASC
                """
        self.cursor.execute(sql, (str(anio), f"{mes:02d}"))
        filas = self.cursor.fetchall()
        
        
        meses= {1: "Enero",      2: "Febrero",
                3: "Marzo",      4: "Abril",
                5: "Mayo",       6: "Junio",
                7: "Julio",      8: "Agosto",
                9: "Septiembre",10: "Octubre",
                11: "Noviembre",12: "Diciembre"
                }
        nombre_mes = meses[mes]
        
        if len(filas) == 0:
            print(f"No hay gastos en {nombre_mes} de {anio}")
            return []
        
        gastos = [self._fila_a_gasto(fila) for fila in filas]
    
        print(f"💸 TOTAL {nombre_mes} de {anio}: {total:.2f} €")
        
        divisor = ("-" * 110)
        for g in gastos:
            print(g)
        print(divisor)
        total = sum(g.importe for g in gastos if g.pagado)
        print(f"✅ Gastos pagados: {total:.2f} €")
        return gastos
        
    

    
    
    
    
    
    # -----------------------------------------------------------------

    def buscar_por_categoria(self, categoria: str) -> list[Gasto]:
        # ✅ PASO 1 (TU): Normaliza categoria.lower().strip()
        # TODO: aquí tu código
        categoria = categoria.lower().strip()
        # ✅ PASO 2 (YA HECHO): SQL WHERE categoria = ?
        sql = "SELECT id, concepto, categoria, importe, fecha, pagado FROM gastos WHERE categoria = ? ORDER BY fecha DESC"
        self.cursor.execute(sql, (categoria,))   # ← ¡¡NO TE OLVIDES LA COMA FINAL!! es tupla 1 elemento
        filas = self.cursor.fetchall()

        # ✅ PASO 3 (TU): Si len(filas) == 0 → print "❌ No hay gastos en categoría X" return []
        # TODO: aquí tu código
        if len(filas) == 0:
            print(f"No hay gastos en categoria {categoria}")
            return []
        # ✅ PASO 4 (TU): Convertir a objetos, print cabecera "🔎 GASTOS EN CATEGORÍA: comida",
        # print cada uno, suma total, return.
        # TODO: aquí tu código
        print(f"🔎 GASTOS EN CATEGORIA: {categoria}")
        gastos = [self._fila_a_gasto(f) for f in filas]
        total_cat = sum(g.importe for g in gastos)
        print(f"💸 TOTAL {categoria.upper()}: {total_cat:.2f} €")
        for g in gastos: print(g)
        return gastos
    # -----------------------------------------------------------------

    def marcar_pagado(self, id_gasto: int, pagado: bool = True) -> bool:
        # ✅ PASO 1 (YA HECHO): SQL UPDATE
        sql = "UPDATE gastos SET pagado = ? WHERE id = ?"
        self.cursor.execute(sql, (1 if pagado else 0, id_gasto))
        self.conn.commit()

        # ✅ PASO 2 (TU): Si self.cursor.rowcount == 0 → no existe, print "❌ Gasto no encontrado" return False
        if self.cursor.rowcount == 0:
            print(f"|❌ Gasto  no encontrado|")
            return False
        # Sino: print(f"✅ Gasto [{id_gasto:03d}] marcado como PAGADO/PENDIENTE")
        else:
            print(f"|✅ Gasto [{id_gasto:03d}] | {'PAGADO' if pagado else 'PENDIENTE'}|")
            return True
        # TODO: aquí tu código
        

    # -----------------------------------------------------------------

    def editar_importe(self, id_gasto: int, nuevo_importe: float) -> bool:
        # ✅ PASO 1 (TU): Valida que nuevo_importe > 0. Si no → error return False
        # TODO: aquí tu código
       

        # ✅ PASO 2 (YA HECHO): SQL UPDATE
        sql = "UPDATE gastos SET importe = ? WHERE id = ?"
        self.cursor.execute(sql, (float(nuevo_importe), id_gasto))
        self.conn.commit()

        # ✅ PASO 3 (TU): rowcount para saber si existe. Print resultado, return True/False
        # TODO: aquí tu código
        if self.cursor.rowcount == 0:
            print(f"❌ Gasto no encontrado")
            return False
        else:
            print(f"|✅ Importe actualizado a {nuevo_importe:.2f} €|")
            return True

    # -----------------------------------------------------------------

    def borrar_gasto(self, id_gasto: int, confirmar: bool = True) -> bool:
        # ✅ PASO 1 (TU): Si confirmar == True → input usuario ¿seguro borrar? s/N.
        #   Si responde NO está en ("s","si","sí") → print "ℹ️ Operación cancelada", return False
        # TODO: aquí tu código
        if confirmar == True:
            confirmacion = input(f"⚠️  ¿Seguro que quieres borrar el gasto ID {id_gasto:03d}? (s/N): ").strip().lower()
            if confirmacion not in ("s","si","sí"):
                print("ℹ️ Operacion cancelada")
                return False
             # ✅ PASO 2 (YA HECHO): SQL DELETE
        sql = "DELETE FROM gastos WHERE id = ?"
        self.cursor.execute(sql, (id_gasto,))   # ← ¡¡NO TE OLVIDES LA COMA!!
        self.conn.commit()

        # ✅ PASO 3 (TU): rowcount para saber si borró. Print "🗑️ Gasto borrado" o "no encontrado"
        # return True/False
        # TODO: aquí tu código  
        if self.cursor.rowcount == 0:
            print(f"Gasto no encontrado")
            return False
        else:
            print(f"🗑️ Gasto borrado")
            return True
    def _buscar_por_id(self, id_gasto: int) -> Gasto | None:
        sql = "SELECT id, concepto, categoria, importe,fecha, pagado FROM gastos WHERE id = ?"
        self.cursor.execute(sql, (id_gasto,))
        fila = self.cursor.fetchone()
        if fila is None:
            return None
        return self._fila_a_gasto(fila)
    
def mostrar_menu() -> str:
    
    
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                💰 GESTOR DE GASTOS PERSONALES            ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print("║ 1. ✚ Añadir nuevo gasto                                  ║")
    print("║ 2. 📋 Ver todos los gastos                               ║")
    print("║ 3. ⏳ Ver solo pendientes de pagar                       ║")
    print("║ 4. 📆 Ver gastos de un mes/año                           ║")
    print("║ 5. 🔎 Filtrar gastos POR CATEGORIA                       ║")
    print("║ 6. ✅ Marcar gasto como pagado / pendiente               ║")
    print("║ 7. ✏️ Editar importe de un gasto                         ║")
    print("║ 8. 🗑️ Borrar gasto                                       ║")
    print("║ 0. 🚪 Salir                                              ║")
    print("╚══════════════════════════════════════════════════════════╝")  
    
    opcion = input("👉 Introduce tu opcion: ")
    return opcion
    
def pedir_id_valido(gestor) -> int | None:
        while True:
            texto_id = input("👉 Introduce el ID del gasto: ")
            
            if texto_id == "" or texto_id == "salir":
                print("ℹ️ Operacion cancelada")
                return None
                
            try:
                id_numero = int(texto_id)
            except ValueError:
                print("❌ El ID debe ser un numero entero")
                continue
            
            if gestor._buscar_por_id(id_numero) is None:
                print(f"❌ No existe gasto con ID {id_numero}")
                continue
            
            return id_numero
        
def main():
    gestor = GestorGastos()
    while True:   # ← BUCLE QUE REPITE EL MENÚ (NO TE LO OLVIDES!!)
        print("\n" * 20)
        opcion = mostrar_menu()

        if opcion == "1":
            # AQUÍ PRIMERO pides concepto/categoria/importe/fecha/pagado con inputs
            concepto = input("👉 Introduce el concepto del gasto: ")
            categoria = input("👉 Introduce la categoria: ")
            # LUEGO llamas a gestor.añadir_gasto(...)
            try:
                importe = float(input("👉 Introduce el importe: ").strip())      
            except ValueError:    
                print("❌ El importe debe ser un numero(ej: 12.50)")
                input("\nPulsa INTRO para continuar...")
                continue
                
            if importe <= 0:
                print("❌ El importe debe ser mayor que 0")
                input("\nPulsa INTRO para continuar...")
                continue
            
            fecha = input("👉 Introduce la fecha (yyyy-mm-dd, Intro hoy): ").strip()
            if fecha == "":
                fecha = None
            
            
            pagado_texto = input("👉 ¿Es pagado? (s/N): ").strip().lower()
            pagado = True if pagado_texto in ("s", "si", "sí") else False
        
            gestor.añadir_gasto(concepto, categoria, importe, fecha, pagado) 
            input("\nPulsa INTRO para continuar...")
            
        elif opcion == "2":
            gestor.ver_todos()
            input("\nPulsa INTRO para continuar...")
            
        elif opcion == "3":
            gestor.ver_todos(solo_pendientes=True)
            input("\nPulsa INTRO para continuar...")
        elif opcion == "4":
            # pide anio, mes con try/except, valida mes 1-12
            # luego: gestor.ver_por_mes(anio, mes)
            
            try:
                mes = int(input("👉 Introduce el mes: ")) 
                
            except ValueError:
                print("❌ Mes invalido")
                continue
            try:
                anio = int(input("👉 Introduce el año: "))
            except ValueError:
                print("❌ Año no valido (Escribe el numero )")
                continue
            
            if not (1 <= mes <= 12):
                print("❌ Mes fuera de rango (1-12)")
                continue
            
            gestor.ver_por_mes(anio, mes)
            input("\nPulsa INTRO para continuar...")
            
        elif opcion == "5":
            texto = input("👉 Introduce la categoria a buscar: ")
            gestor.buscar_por_categoria(texto)
            input("\nPulsa INTRO para continuar...")
            
        elif opcion == "6":
            id_gasto = pedir_id_valido(gestor)
            if id_gasto is None:
                continue
                
            pregunta = input("👉 ¿Marcar como pagado o pendiente? (p/a): ").strip().lower()
            if pregunta == "p":
                 gestor.marcar_pagado(id_gasto, pagado=True)
            else:
                gestor.marcar_pagado(id_gasto, pagado=False)
            input("\nPulsa INTRO para continuar...")
            
        elif opcion == "7":
            id_gasto = pedir_id_valido(gestor)
            if id_gasto is None:
                continue
                
            try:
                nuevo_imp = float(input("👉 Introduce el nuevo importe: ").strip())
            except ValueError:
                print("❌ Importe invalido, debe ser un numero positivo")
                input("\nPulsa INTRO para continuar...")
                continue
            if nuevo_imp <= 0:    
                print("❌ El importe debe ser mayor que 0")
                input("\nPulsa INTRO para continuar...")
                continue
            gestor.editar_importe(id_gasto, nuevo_imp)
            input("\nPulsa INTRO para continuar...")
            
        elif opcion == "8":
            id_gasto = pedir_id_valido(gestor)
            if id_gasto is None:
                continue
            gestor.borrar_gasto(id_gasto)
            print("\nPulsa INTRO para continuar...")
            
        elif opcion == "0":
            gestor.cerrar()   # IMPRESCINDIBLE
            print("👋 ¡Adiós!")
            break
        else:
            print("❌ Opción inválida (0-8)")
            input("\nPulsa INTRO para continuar...")

if __name__ == "__main__":
    main()
        
    
            
            

    
    

    
       
        

