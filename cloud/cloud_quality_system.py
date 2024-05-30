import zmq

class QualitySystem:
    def __init__(self):
        self.context = zmq.Context()
        self.sockets = {
            "edge": self.context.socket(zmq.PULL),
            "fog": self.context.socket(zmq.PULL),
            "cloud": self.context.socket(zmq.PULL),
        }
        self.sockets["edge"].bind("tcp://10.43.100.158:5557")
        self.sockets["fog"].bind("tcp://10.43.100.158:5559")
        self.sockets["cloud"].bind("tcp://10.43.100.158:5560")

    def procesar_alarma(self, mensaje, origen):
        print(f"Alarma recibida de {origen}: {mensaje}")
        # Implementar el procesamiento de alarmas según el origen

    def run(self):
        while True:
            for origen, socket in self.sockets.items():
                try:
                    mensaje = socket.recv_string(zmq.NOBLOCK)
                    self.procesar_alarma(mensaje, origen)
                except zmq.Again:
                    continue

if __name__ == "__main__":
    quality_system = QualitySystem()
    quality_system.run()
