import zmq
import time
from datetime import datetime

class Cloud:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind("tcp://localhost:5558")  # Conectar a una nueva dirección para Cloud
        self.almacenamiento = []

    def almacenar_medicion(self, medicion):
        self.almacenamiento.append(medicion)
        print(f"Medición almacenada: {medicion}")

    def procesar_datos(self):
        # Procesa los datos almacenados y genera alertas si es necesario
        for medicion in self.almacenamiento:
            tipo_sensor, valor, timestamp = medicion.split()
            if tipo_sensor == "humedad":
                self.calcular_humedad_mensual()
            # Agregar procesamiento para otros tipos de datos si es necesario

    def calcular_humedad_mensual(self):
        # Implementar el cálculo de humedad mensual según la fórmula HRmij
        print("Calculando humedad mensual...")

    def run(self):
        while True:
            mensaje = self.socket.recv_string()
            self.almacenar_medicion(mensaje)
            self.procesar_datos()
            time.sleep(20)  # Simular el procesamiento cada 20 segundos

if __name__ == "__main__":
    cloud = Cloud()
    cloud.run()
