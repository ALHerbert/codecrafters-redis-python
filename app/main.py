from _thread import start_new_thread
from datetime import datetime, timedelta


data_store = {} # k: str, v: MyObject

class MyObject:
    def __init__(self, value, expiry=None):
        self.value = value
        self.expiry = expiry

# update to not mutate in incoming command?
def parse_command(command: bytes): -> list
    # invalid inputs
    # something that is not bytes
    # something that doesn't start with the correct cahracers
    # something that doesnt have the right formatting like /r/n
    # something where the length doesn't match teh caracetrs
    command = command.decode() # i shouldnt modify an argument

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


# create output builder function
def create_output(input_datatype): -> str # or bytes
   # simple strings, errors, integers, bulk strings, arrays 

# create function that takes in data. returns binary string to respond with

def handle_client(c): # put the dispatch code into its own function.
    with c:
        while True:
            # data = c.recv(1024)
            #if not data:
            #    break
            # commands = parse_command(data)
            # output = handle_command(commands)
            # c.send(output.encode())
            data = c.recv(1024)
            print("data", data)

            if not data:
                break

            commands = parse_command(data)
            if commands[0].upper() == "PING":
                c.send(b"+PONG\r\n")
            elif commands[0].upper() == "ECHO":
                output = f"${len(commands[1])}\r\n{commands[1]}\r\n"
                c.send(output.encode())
            elif commands[0].upper() == "SET":
                expiry = None
                if len(commands) > 3 and commands[3].upper() == "PX":
                    expiry = datetime.now() + timedelta(milliseconds=int(commands[4]))

                data_store[commands[1]] = {'value': commands[2], 'expiry': expiry}
                c.send(b"+OK\r\n")
            elif commands[0].upper() == "GET":
                value = data_store[commands[1]]
                if value["expiry"] is None:
                    output = f"${len(value['value'])}\r\n{value['value']}\r\n"
                elif value["expiry"] > datetime.now(): 
                    output = f"${len(value['value'])}\r\n{value['value']}\r\n"
                else:
                    data_store.pop(commands[1])
                    output = "$-1\r\n"
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

