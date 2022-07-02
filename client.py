import socket
from time import sleep
import psutil
import json

host = '127.0.0.1'
port = 8080
FORMAT = 'UTF-8'


def main():
    CONNECTED = True
    while CONNECTED:
        sleep(2)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            print(f'Connected to Server {host}:{port}')
            counter = 1
            CONNECTED = True
            while CONNECTED:
                information = {
                    'RAM: ': psutil.virtual_memory()[2],
                    'CPU: ': psutil.cpu_percent(interval=4),
                    'disk: ': psutil.disk_usage('.').free,
                    'CPU counts: ': psutil.cpu_count()}
                message = json.dumps(information)
                s.send(message.encode(FORMAT))
                print(f"Message Number {counter} Sent to Server")
                counter = counter + 1
                sleep(4)
        except Exception as err:
            print(err)
            inp = input("We Lost the Connection to Server, Try again? N/Y")
            if inp == "Y":
                continue
            else:
                break


if __name__ == "__main__":
    main()
