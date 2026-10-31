import threading
import queue
import time
import random

trabajos = queue.Queue()
resultados = {}
tamanos = {}
lock = threading.Lock()
documentos = []
for doc_id in range(1, 25):
    tam = random.randint(1, 5)
    documentos.append((doc_id, tam))
    trabajos.put((doc_id, tam))


def trabajador(nombre):
    while True:
        try:
            doc_id, tam = trabajos.get_nowait()
        except queue.Empty:
            break

        time.sleep(tam * 0.1)
        with lock:
            print(nombre, "proceso el documento", doc_id, "(tamano", tam, ")")
            resultados[nombre] = resultados.get(nombre, 0) + 1
            tamanos[nombre] = tamanos.get(nombre, 0) + tam


def version_secuencial():
    for doc_id, tam in documentos:
        time.sleep(tam * 0.1)

inicio = time.time()

hilos = []
for i in range(1, 5):
    h = threading.Thread(target=trabajador, args=("Trabajador-" + str(i),))
    hilos.append(h)
    h.start()

for h in hilos:
    h.join()

tiempo_hilos = time.time() - inicio
inicio = time.time()
version_secuencial()
tiempo_secuencial = time.time() - inicio
print()
print("===== RESUMEN =====")
total = 0
for i in range(1, 5):
    nombre = "Trabajador-" + str(i)
    cant = resultados.get(nombre, 0)
    print(nombre, "->", cant, "documentos, tamano total:", tamanos.get(nombre, 0))
    total = total + cant

print("Total procesado:", total, "de 24")
print("Tiempo con 4 hilos:", round(tiempo_hilos, 2), "segundos")
print("Tiempo secuencial:", round(tiempo_secuencial, 2), "segundos")
