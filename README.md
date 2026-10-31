# Práctica 1 – Hilos con Python

Hice un programa donde 4 trabajadores (hilos) se reparten 24 documentos. Cada documento tiene un id y un tamaño al azar entre 1 y 5

- Puse los 24 documentos en una queue.Queue.
- Cada trabajador saca documentos con get_nowait() hasta que sale queue.Empty, y ahi termina
- Para simular el trabajo uso time.sleep(tamaño * 0.1)
- Cuando termina un documento, suma 1 en el diccionario resultados dentro de with lock:
- Al final hago join() a los 4 hilos y muestro el total y el resumen

## Interpretación de cada ejecución

En las 4 ejecuciones el total fue 24 de 24, ningún documento se repitió y los 4 hilos terminaron sin quedarse trabados. Lo que cambia es cuántos documentos le tocan a cada trabajador

**Ejecución 1:** Trabajador-1 y Trabajador-2 hicieron 7 documentos cada uno, y Trabajador-3 y Trabajador-4 hicieron 5. Trabajador-2 hizo 7 pero su tamaño total fue solo 17, osea le tocaron documentos chicos y por eso se liberaba rápido y agarraba otro

**Ejecución 2:** Esta fue la mas desigual: Trabajador-3 hizo 9 documentos y Trabajador-1 solo 4. Pero si veo el tamaño total, todos están entre 16 y 19, entonces en realidad trabajaron casi lo mismo, solo que a Trabajador-3 le tocaron los documentos más livianos

**Ejecución 3:** Trabajador-1 y Trabajador-3 hicieron 7, Trabajador-4 hizo 6 y Trabajador-2 solo 4. A Trabajador-2 le tocaron documentos grandes (tamaño total 17 con solo 4 documentos), por eso estuvo más tiempo ocupado con cada uno

**Ejecución 4:** Ahora fue Trabajador-4 el que hizo más (8), Trabajador-1 hizo 6 y Trabajador-2 y Trabajador-3 hicieron 5 cada uno

**Lo que entendí:** no hay un trabajador "ganador" fijo, l que termina antes su documento es el que saca el siguiente de la cola, y eso depende del tamaño que le tocó y de cómo el sistema operativo reparte el tiempo entre los hilos, es por eso cada vez que lo corro sale distinto, pero la suma siempre da 24

## Reto adicional

Inclui los retos por que se encontraban en su presentación en power point:

- Tiempo total: lo medí con time.time() antes y después de los hilos
- Tamaño acumulado: agregué el diccionario tamanos que también se actualiza dentro del lock
- Comparación con versión secuencial: hice la función version_secuencial() que procesa los mismos 24 documentos uno tras otro

Con hilos fue entre 3.5 y 3.8 veces más rápido. Aquí la diferencia se nota porque time.sleep() es solo esperar, y mientras un hilo espera los otros pueden avanzar.

## Respuestas a las preguntas

**1. ¿Por qué queue.Queue es apropiada para compartir trabajos?**
Porque ya viene preparada para usarse con varios hilos, por dentro tiene su propio candado, así que cuando dos trabajadores hacen get_nowait() al mismo tiempo, a cada uno le da un documento distinto. Así ningún documento se procesa dos veces ni se pierde, y yo no tengo que programar esa parte.

**2. ¿Qué protege Lock y qué pasaría si se actualizara el resumen sin él?**
El lock protege los diccionarios resultados y tamanos. La línea resultados[nombre] = resultados.get(nombre, 0) + 1 en realidad hace tres cosas: leer, sumar y escribir. Si dos hilos lo hacen al mismo tiempo puede pasar una condición de carrera y que se pierda una suma, y al final el total podría salir menos de 24 aunque se procesaron todos

**3. ¿Qué cambiarías si cada documento tuviera que guardarse en un archivo real?**
Cambiaría el time.sleep() por abrir y escribir el archivo con with open(...) a cada documento le daría un nombre de archivo distinto (por ejemplo doc_5.txt) para que dos hilos no escriban en el mismo archivo. Si todos tuvieran que escribir en un solo archivo, como un registro, esa escritura también la pondría dentro del lock. Y pondría un try/except por si falla al guardar, para que el hilo no se cierre de golpe
