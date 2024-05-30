import zmq

class Actuator:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind("tcp://localhost:5556")

    def run(self):
        print("Entro a la funcion run del actuador")
        mensaje = self.socket.recv_string()
        print(f"\nMensaje recibido, antes del while: {mensaje}")
        while True:
            print("Esperando mensaje...")
            message = self.socket.recv_string()
            print(f"\nMensaje recibido, despues del while: {message}")
            if message == "Activate":
                print("Sprinkler activated due to smoke detection!")
            else:
                print("Esta marcando otra cosa que no sea Activate")


if __name__ == "__main__":
    actuator = Actuator()
    actuator.run()
