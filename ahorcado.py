import random
import sys

PALABRAS = [
    "python", "programar", "ordenador", "serpiente", "juego",
    "ahorcado", "teclado", "pantalla", "raton", "codigo",
    "variable", "funcion", "algoritmo", "internet", "software",
    "hardware", "consola", "archivo", "datos", "memoria",
    "perro", "gato", "elefante", "jirafa", "delfin",
    "manzana", "platano", "sandia", "naranja", "fresa",
    "casa", "coche", "bicicleta", "avion", "barco",
    "libro", "escuela", "profesor", "alumno", "lapiz",
    "sol", "luna", "estrella", "montana", "playa",
    "musica", "guitarra", "piano", "cancion", "pelicula"
]

HORCA = [
    """
  +---+
      |
      |
      |
     ===
    """,
    """
  +---+
  O   |
      |
      |
     ===
    """,
    """
  +---+
  O   |
  |   |
      |
     ===
    """,
    """
  +---+
  O   |
 /|   |
      |
     ===
    """,
    """
  +---+
  O   |
 /|\\  |
      |
     ===
    """,
    """
  +---+
  O   |
 /|\\  |
 /    |
     ===
    """,
    """
  +---+
  O   |
 /|\\  |
 / \\  |
     ===
    """
]

def obtener_letra_valida():
    while True:
        letra = input("\n 👉 Escriba una letra").strip().lower()
        if len(letra) == 1 and letra.isalpha():
            return letra
        print("❌ Entrada no valida. Escribe UNA sola letra.")
        
def mostrar_tablero(palabra, acertadas,fallos):
    print("\n" + "=" * 40)
    print(HORCA[fallos])
    
    progreso = []
    for letra in palabra:
      if letra in acertadas:
        progreso.append(letra + " ")
      else:
        progreso.append("_ ")
    print("Palabra: " + "".join(progreso))
    if fallos:
      print(f"Fallos: {fallos}/6")
    print("=" * 40)
def jugar_partida():
    palabra = random.choice(PALABRAS)
    acertadas = set()
    usadas = set()
    fallos = 0
    while True:
      mostrar_tablero(palabra, acertadas,fallos)
      if fallos >= 6:
        print(f"\n💀 ¡GAME OVER! El juego ha terminado. La palabra era: {palabra.upper()}")
        return False
      if all(letra in acertadas for letra in palabra):
        print(f"\n🏆 ¡ENHORABUENA! Has acertado: {palabra.upper()}")
        return True
      
      letra = obtener_letra_valida()
      if letra in usadas:
        print(f"⚠️ Ya dijiste '{letra}' Prueba otra.")
        continue
      usadas.add(letra)
      
      if letra in palabra:
        acertadas.add(letra)
        print(f"✅ ¡Bien! La '{letra}' esta en la palabra.")
      else:
        fallos += 1
        print(f"❌ ¡Fallo! La '{letra}' NO esta en la palabra.")
        
def main():
  print("\n🎮 ¡Bienvenido al juego del Ahorcado!")
  victorias = 0
  derrotas = 0
  
  while True:
    resultado = jugar_partida()
    if resultado:
       victorias += 1
    else:
       derrotas += 1
      
    print(f"\n📊 MARCADOR: 🏆 {victorias} - 😢 {derrotas}")
    respuesta = input("\n¿Quieres jugar de nuevo? (s/n)")
    if respuesta.lower() != "s":
      print("\n¡Gracias por jugar! 1Hasta pronto.")
      break
if __name__ == "__main__":
   main()
    
  
    