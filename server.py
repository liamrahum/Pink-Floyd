import socket
import data

LISTEN_PORT = 8086
IP = "127.0.0.1"
ACTIONS_BY_COMMAND = {"92": data.get_albums, "34": data.get_album_songs, "80": data.get_song_len,
                      "64": data.get_song_lyrics, "17": data.get_album_by_song,
                      "47": data.get_songs_by_word_in_name, "69": data.get_songs_by_lyrics, "100": "EXIT"}
EXIT_MESSAGE = "HAVE A GOOD DAY!"
ERROR = "ERROR"
HASHED_PASS = '3362443743'
SIZE_KB = 1024

def myHash(text: str):
    """
    Function copied from StackOverFlow for one hash between sessions, hashlib and other hash functions don't return static value
    :param text: string to hash
    :return: hashed string
    """
    hash = 0
    for ch in text:
        hash = (hash * 281 ^ ord(ch) * 997) & 0xFFFFFFFF
    return hash


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_sock:
        logged_in = False
        server_address = (IP, LISTEN_PORT)
        listening_sock.bind(server_address)  # Sets listen port 8096
        listening_sock.listen(1)
        client_soc, client_address = listening_sock.accept()  # client accept
        while not logged_in:
            if client_soc.recv(SIZE_KB).decode() == HASHED_PASS:
                try:
                    client_soc.sendall("Welcome to my Pink Floyd database!".encode())
                    logged_in = True
                except Exception as e:
                    print(f"Connection error: {e}")
            else:
                try:
                    client_soc.sendall("Incorrect pass, try again.".encode())
                except Exception as e:
                    print(f"Connection error: {e}")


        last_iteration = False
        while not last_iteration:
            client_msg = client_soc.recv(SIZE_KB)  # get client message
            client_msg = client_msg.decode()  # read client
            print(f"Client says: {client_msg}")
            if "EXIT" in client_msg:
                client_soc.sendall(EXIT_MESSAGE.encode())
                last_iteration = True
                break
            command = client_msg[:client_msg.find(':')]
            response = data.create_response(ACTIONS_BY_COMMAND[command](client_msg.split(':')[-1]))
            try:
                client_soc.sendall(response.encode())
                print(f"Sent response: {response}")
            except Exception as e:
                print("Error sending message")
        input()


if __name__ == '__main__':
    main()
