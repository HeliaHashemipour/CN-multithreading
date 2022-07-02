import socket
import threading
import json
from prometheus_client import Gauge, start_http_server

host = '127.0.0.1'
port_num = 8080
FORMAT = 'UTF-8'
metric_1 = Gauge('memory_usage', 'Usage of RAM', ['client_number'])
metric_2 = Gauge('cpu_usage', 'Usage of CPU', ['client_number'])
metric_3 = Gauge('disk_usage', 'usage of disk', ['client_number'])
metric_4 = Gauge('cpu_counts', 'usage of cpu count', ['client_number'])


def received_data(connection, addr, client_number):
    print(f"Client Number {client_number} Connected, {addr}")
    try:
        CONNECTED = True
        while CONNECTED:
            msg = connection.recv(1024).decode(FORMAT)
            datas = json.loads(msg)
            print(f"[{addr}] {msg}")
            metric_1.labels(f'client_{client_number}').set(datas['RAM: '])
            metric_2.labels(f'client_{client_number}').set(datas['CPU: '])
            metric_3.labels(f'client_{client_number}').set(datas['disk: '])
            metric_4.labels(f'client_{client_number}').set(datas['CPU counts: '])
    except Exception as err:
        print(err)
        print(f'Client{client_number} disconnected!!!!')


def main():
    print("Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port_num))
    server.listen()
    print(f"Server {host}:{port_num} is connected...")
    client_number = 1
    start_http_server(8001)
    CONNECTED = True
    while CONNECTED:
        conncetion, addr = server.accept()
        thread = threading.Thread(target=received_data, args=(conncetion, addr, client_number))
        thread.start()
        print(f"[Active Clients] {client_number}")
        client_number = client_number + 1


if __name__ == "__main__":
    main()
