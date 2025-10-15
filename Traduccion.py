import requests
import sys

# Configura tu token de GraphHopper
GRAPHOPPER_KEY = "71d1227a-b33c-45a9-8a45-53b326814c9e"
BASE_URL = "https://graphhopper.com/api/1/route"

def formatea_distancia(metros: float) -> str:
    # Convertir a kilómetros y limitar a 2 decimales
    km = metros / 1000.0
    return f"{km:.2f} km"

def formatea_tiempo(ms: float) -> str:
    # Convertir a minutos y limitar a 2 decimales
    minutos = ms / 1000.0 / 60.0
    return f"{minutos:.2f} min"

def solicitar(texto: str) -> str:
    return input(texto).strip()

def es_salida(valor: str) -> bool:
    return valor.lower() in {"s", "salir"}

def geocodifica(direccion: str):
    """
    Usa el servicio de geocodificación de GraphHopper para obtener (lat, lon)
    a partir de una dirección o lugar.
    """
    geocode_url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": direccion,
        "key": GRAPHOPPER_KEY,
        "locale": "es",
        "limit": 1
    }
    resp = requests.get(geocode_url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    hits = data.get("hits", [])
    if not hits:
        return None
    punto = hits[0]
    return punto["point"]["lat"], punto["point"]["lng"], punto.get("name", direccion)

def ruta(origen_lat, origen_lon, destino_lat, destino_lon, profile="car"):
    """
    Solicita una ruta a GraphHopper, con instrucciones en español.
    """
    params = {
        "key": GRAPHOPPER_KEY,
        "point": [f"{origen_lat},{origen_lon}", f"{destino_lat},{destino_lon}"],
        "profile": profile,          # car | foot | bike
        "locale": "es",              # instrucciones en español
        "instructions": "true",
        "points_encoded": "false",   # útil para depuración
        "calc_points": "true"
    }
    resp = requests.get(BASE_URL, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()

def imprime_resumen(path):
    distancia = path.get("distance", 0.0)  # en metros
    tiempo = path.get("time", 0.0)         # en milisegundos
    print(f"- Distancia total: {formatea_distancia(distancia)}")
    print(f"- Tiempo estimado: {formatea_tiempo(tiempo)}")

def imprime_narrativa(instructions):
    """
    Imprime las instrucciones paso a paso en español.
    """
    print("\nInstrucciones del viaje:")
    for i, step in enumerate(instructions, start=1):
        texto = step.get("text", "")
        distancia = step.get("distance", 0.0)
        tiempo = step.get("time", 0.0)
        print(f"{i}. {texto}  |  {formatea_distancia(distancia)}, {formatea_tiempo(tiempo)}")

def main():
    print("=== Planificador de rutas (GraphHopper) ===")
    print('Escribe "s" o "salir" en cualquier momento para terminar.')

    while True:
        try:
            origen = solicitar("Ingresa dirección de origen: ")
            if es_salida(origen):
                print("Saliendo del programa. ¡Hasta luego!")
                sys.exit(0)

            destino = solicitar("Ingresa dirección de destino: ")
            if es_salida(destino):
                print("Saliendo del programa. ¡Hasta luego!")
                sys.exit(0)

            print("\nBuscando coordenadas...")
            origen_pt = geocodifica(origen)
            destino_pt = geocodifica(destino)

            if origen_pt is None:
                print("No se encontró el origen. Intenta con una dirección más precisa.")
                continue
            if destino_pt is None:
                print("No se encontró el destino. Intenta con una dirección más precisa.")
                continue

            o_lat, o_lon, o_name = origen_pt
            d_lat, d_lon, d_name = destino_pt
            print(f"Origen: {o_name} ({o_lat:.6f}, {o_lon:.6f})")
            print(f"Destino: {d_name} ({d_lat:.6f}, {d_lon:.6f})")

            print("\nCalculando ruta...")
            data = ruta(o_lat, o_lon, d_lat, d_lon, profile="car")

            paths = data.get("paths", [])
            if not paths:
                print("No se pudo calcular una ruta entre los puntos indicados.")
                continue

            path = paths[0]
            print("\n=== Resumen del viaje ===")
            imprime_resumen(path)

            instructions = path.get("instructions", [])
            if instructions:
                imprime_narrativa(instructions)
            else:
                print("No se recibieron instrucciones detalladas para este viaje.")

            print("\nRuta calculada correctamente.\n")

        except requests.HTTPError as e:
            # Errores HTTP (p.ej., token inválido, límites, etc.)
            try:
                detalle = e.response.json()
            except Exception:
                detalle = e.response.text if hasattr(e, "response") and e.response is not None else str(e)
            print(f"Error HTTP: {detalle}")
        except requests.RequestException as e:
            print(f"Error de conexión: {e}")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

        # Preguntar si desea otra ruta o salir
        continuar = solicitar('\n¿Deseas calcular otra ruta? (s/salir para terminar, cualquier otra tecla para continuar): ')
        if es_salida(continuar):
            print("Saliendo del programa. ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
