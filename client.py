import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8086
COMMANDS_BY_CHOICE = {1: "92:GET ALBUMS", 2: "34:GET ALBUM SONGS:", 3: "80:GET SONG LENGTH:", 4: "64:GET SONG LYRICS:",
                      5: "17:GET ALBUMS BY SONG:", 6: "47:GET SONGS BY WORD IN NAME:", 7: "69:GET SONGS BY LYRICS:",
                      8: "100:EXIT:"}
WRONG_PASS_MESSAGE = "Incorrect pass, try again."
EXIT_MESSAGE = "HAVE A GOOD DAY!"
SIZE_KB = 1024

def menu():
    print("1 - Pink Floyd albums")
    print("2 - Songs in given album")
    print("3 - Song length (you choose song)")
    print("4 - Song lyrics (you choose song")
    print("5 - Album by song (you choose song)")
    print("6 - Songs containing a word in their title (you choose word)")
    print("7 - Song by lyrics (you choose lyrics)")
    print("8 - Exit")
    choice = input("Your choice: ")
    while choice == '' or not choice.isnumeric() or int(choice) < 1 or int(choice) > 8:
        choice = input("Wrong input. What information do you need? ")
    return int(choice)


ADDONS = {1: "", 2: "Enter album name: ", 3: "Enter song name: ", 4: "Enter song name: ",
          5: "Enter song name: ", 6: "Enter word(s): ", 7: "Enter word(s): ", 8: ""}


def message():
    choice = menu()  # Gets pass
    command = COMMANDS_BY_CHOICE[choice]
    # if there's no need for secondary input
    if ADDONS[choice] == "":
        return command
    return f"{command}:{input(ADDONS[choice])}"


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


def print_response(server_response):
    # if EXIT
    if EXIT_MESSAGE in server_response:
        print(f"Server says: {EXIT_MESSAGE}")
    elif "ERROR" in server_response:
        print(f"Server says: {server_response[server_response.find('ERROR'):]}")
    else:
        print(f"Server says: {server_response[server_response.find('['):]}")


def main():
    with socket.socket() as sock:
        # connect to server
        server_address = (SERVER_IP, SERVER_PORT)
        logged_in = False
        try:
            sock.connect(server_address)
            while not logged_in:
                sock.sendall(str(myHash(input("Enter pass: "))).encode())
                response = sock.recv(SIZE_KB).decode()
                print(response)
                if WRONG_PASS_MESSAGE not in response:
                    logged_in = True
        except Exception as e:
            print(f"Server connection error: {e}")
            exit()

        # start conversation (IN CLIENT SIDE, MESSAGES ARE SHOWN BEFORE CONVERTED/AFTER EXTRACTED FROM PROTOCOL)
        last_iteration = False
        while not last_iteration:
            client_query = message()
            # exit after finish
            if "EXIT" in client_query:
                last_iteration = True
            try:
                sock.sendall(client_query.encode())
                server_response = sock.recv(SIZE_KB).decode()
                print_response(server_response)
            except Exception as e:
                print("Server Error, please try again later")
    input()  # input for confirmation before leaving


if __name__ == '__main__':
    main()
