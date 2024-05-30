import zmq
import datetime
import time


def publicar_medicion(self):
    self.context = zmq.Context()

    # Proxy
    self.socket = self.context.socket(zmq.PUSH)
    self.socket.connect("tcp://10.43.100.158:5555")

    # Actuator
    self.actuator_socket = self.context.socket(zmq.PUSH)
    self.actuator_socket.connect("tcp://10.43.100.158:5556")

    # Quality system
    self.quality_socket = self.context.socket(zmq.PUSH)
    self.quality_socket.connect("tcp://10.43.100.158:5557")

    # Cloud
    self.cloud_socket = self.context.socket(zmq.PUSH)
    self.cloud_socket.connect("tcp://10.43.100.158:5558")

    while True:
        medicion = self.generar_medicion()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'=' * 40}\nMeasurement Report\n{'=' * 40}")
        print(f"Sensor Type   : {self.tipo_sensor}")
        print(f"Measurement   : {medicion}")
        print(f"Timestamp     : {timestamp}")
        print(f"{'=' * 40}\n")

        self.socket.send_string(f"{self.tipo_sensor} {medicion} at {timestamp}")
        if self.tipo_sensor == "Humo" and medicion == "True":
            self.actuator_socket.send_string("Activate")
            self.socket.send_string(f"Alert: {self.tipo_sensor} detected at {timestamp}")
            self.quality_socket.send_string(f"Quality System Alert: {self.tipo_sensor} detected at {timestamp}")
            self.cloud_socket.send_string(f"Cloud Storage: {self.tipo_sensor} {medicion} at {timestamp}")

        time.sleep(self.tiempo)
