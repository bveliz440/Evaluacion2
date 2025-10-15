import requests
from faker import Faker
import random

# Inicializar Faker en español
fake = Faker('es_ES')

# URL base de la API
BASE_URL = "http://library.demo.local/api/v1/books"

# API Key (reemplaza con la tuya si cambia)
headers = {
    "x-api-key": "cisco|a9RU5YYYT7oN5ELQP23q4cUeV5JbMnDJIEdGrGjV6L4"
}

# Crear 50 libros aleatorios
for i in range(50):
    book = {
        "id": random.randint(1000, 9999),  # ID aleatorio
        "title": fake.sentence(nb_words=4),  # título ficticio
        "author": fake.name(),              # autor ficticio
        "isbn": fake.isbn13()               # ISBN válido
    }
    
    response = requests.post(BASE_URL, json=book, headers=headers)
    if response.status_code in [200, 201]:
        print(f"Libro agregado: {book['title']} ({book['isbn']})")
    else:
        print(f"Error al agregar libro {book['id']}: {response.text}")

# Finalmente, listar todos los libros
resp = requests.get(BASE_URL, params={"includeISBN": "true", "sortBy": "author"}, headers=headers)
if resp.status_code == 200:
    libros = resp.json()
    print("\nCatálogo completo ordenado por autor:")
    for libro in libros:
        print(f"{libro['author']} - {libro['title']} (ISBN: {libro['isbn']})")
else:
    print("Error al listar libros:", resp.text)
