import socket
import json

HOST = 'localhost'
PORT = 1234

isReady = False

def networkStuff(sock, json_data):
    # Remove the socket creation, binding, and listening from here

    cs, addr = sock.accept()

    # Send the JSON data to the client side
    cs.sendall(json.dumps(json_data).encode("utf-8"))
    received_data = cs.recv(1024)
    decoded_data = received_data.decode("utf-8")
    response = json.loads(decoded_data)
    if response["payload"]:
        isReady = True
        print("Is the user ready? ", isReady)

    if isReady:
        with open('gameInfo.json', 'r') as file:
            time_Data = json.load(file)
        cs.sendall(json.dumps(time_Data).encode("utf-8"))
        
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
    # Create the socket here
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and port
    server_address = (HOST, PORT)

    # Bind and listen here
    sock.bind(server_address)
    sock.listen(5)

    # Read the initial JSON data from info.json
    with open('ready.json', 'r') as file:
        initial_data = json.load(file)

    # Pass the initial JSON data to networkStuff()
    networkStuff(sock, initial_data)

    # when done, close the socket
    sock.close()

if __name__ == "__main__":
    main()
