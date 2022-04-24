from _thread import start_new_thread

def handle_client(c):
    with c:
        while True:
            data = c.recv(1024)
            print("data", data)
            if not data:
                break
            c.send(b"+PONG\r\n")
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
