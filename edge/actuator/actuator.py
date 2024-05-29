import zmq

class Actuator:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind("tcp://10.43.100.158:5556")

    def run(self):
        while True:
            message = self.socket.recv_string()
            if message == "Activate":
                print("Sprinkler activated due to smoke detection!")

if __name__ == "__main__":
    actuator = Actuator()
    actuator.run()
