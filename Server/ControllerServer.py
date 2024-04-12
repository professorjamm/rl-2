import socket
import json

HOST = 'localhost'
PORT = 2234

def networkStuff(json_data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and port
    server_address = (HOST, PORT)

    sock.bind((server_address))
    sock.listen(5)

    cs, addr = sock.accept()

    # Send the JSON data to the client side
    cs.sendall(json.dumps(json_data).encode("utf-8"))

    while True:
        received_data = cs.recv(1024)
        decoded_data = received_data.decode("utf-8")
        try:
            response = json.loads(decoded_data)
        except json.decoder.JSONDecodeError:
            print("Game Finished (no more info to decode)")
            break
        print(decoded_data)

def main():
    # Read the initial JSON data from info.json
    with open('movementInfo.json', 'r') as file:
        initial_data = json.load(file)

    # Pass the initial JSON data to networkStuff()
    networkStuff(initial_data)

if __name__ == "__main__":
    main()