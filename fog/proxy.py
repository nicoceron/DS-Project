import zmq
import argparse

def main():
    # Configuración inicial y procesamiento de argumentos si es necesario

    context = zmq.Context()
    # Crear un socket PULL
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5555")  # Bind al puerto 5555 para escuchar a los sensores

    print("Proxy iniciado y escuchando a los sensores...")

    try:
        while True:
            # Espera por mensajes de cualquier sensor
            message = socket.recv_string()
            print(f"Mensaje recibido: {message}")
            # Procesar el mensaje recibido
    except KeyboardInterrupt:
        print("Cerrando proxy...")
    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    main()

# COmando para ejecutar el proxy
# python Proxy.py
