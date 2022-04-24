def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    import socket
    s = socket.create_server(("localhost", 6379), reuse_port=True)
    c, addr = s.accept() # wait for client

    '''
    while True:
        data = s.recv(1024)
        print("data", data)
        if not data:
            break
        s.sendall("+PONG\r\n")
    '''
    c.send("+PONG\r\n")

if __name__ == "__main__":
    main()
