import zmq

class EdgeQualitySystem:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind("tcp://10.43.100.158:5557")

    def procesar_alarma(self, mensaje):
        print(f"Alarma recibida en Edge: {mensaje}")
        # Implementar el procesamiento de alarmas en la capa Edge

    def run(self):
        while True:
            mensaje = self.socket.recv_string()
            self.procesar_alarma(mensaje)

if __name__ == "__main__":
    edge_quality_system = EdgeQualitySystem()
    edge_quality_system.run()
