# Evaluacion2

Este repositorio corresponde a la Evaluación Parcial N°2 de la asignatura Telepresencia y Entornos Innovadores de Colaboración Humana 

El repositorio incluye dos scripts en Python:

- traduccion.py  
  Al ejecutarlo solicita dos direcciones (origen y destino) y, utilizando la API de GraphHopper, muestra:  
  - La distancia total del trayecto.  
  - El tiempo estimado de viaje (en minutos).  
  - Las instrucciones paso a paso en español.  
  Además, permite salir del programa escribiendo `s` o `salir`.

- import_requests.py  
  Genera 50 libros aleatorios (título, autor e ISBN) y los añade a la biblioteca de la máquina virtual DEVASC mediante la API correspondiente.  
  Finalmente, lista todos los libros creados, ordenados por autor e incluyendo el ISBN.


## Requisitos

- Python 3.x  
- Librería `requests` instalada:
  ```bash
  pip install requests
