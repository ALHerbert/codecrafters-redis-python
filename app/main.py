from _thread import start_new_thread

def parse_command(command):
    command = command.decode()

    if command[0] == '*':
        array_length = int(command[1])
        command = command[4:]

    items = []

    for i in range(array_length):
        if command[0] == '$':
            string_length = command[1]
            if command[2] != '\r':
                string_length += command[2]
                command = command[1:]
            command = command[4:]

            item = command[0:int(string_length)]
            items.append(item)

            command = command[int(string_length)+2:]
    return items 

def handle_client(c):
    #b'*1\r\n$4\r\nping\r\n' ping
    #b'*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n"
    with c:
        while True:
            data = c.recv(1024)
            print("data", data)

            if not data:
                break

            commands = parse_command(data)
            print(commands)
            if commands[0].upper() == "PING":
                c.send(b"+PONG\r\n")
            elif commands[0].upper() == "ECHO":
                print("echo:", commands[1])
                output = f"${len(commands[1])}\r\n{commands[1]}\r\n"
                c.send(output.encode())
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    import socket
    s = socket.create_server(("localhost", 6379), reuse_port=True)
    s.listen(5)

    while True:
        c, addr = s.accept() # wait for client

        print(f"Connected to : {addr}")
        
        start_new_thread(handle_client, (c,))

    s.close()



if __name__ == "__main__":
    main()
    #items = parse_command(b"*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n")
    #print(items)
    #items = parse_command(b'*2\r\n$4\r\necho\r\n$11\r\nwatermelons\r\n')
    #print(items)

