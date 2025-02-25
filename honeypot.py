from socket import *

def main():
    ip_add="10.10.32.252"
    port=80
    print("[+] Honeypot start.....")
    try:
        get_socket_con=socket(AF_INET, SOCK_STREAM)
        get_socket_con.bind((ip_add, port))
        get_socket_con.listen(10)
        while 1:
            client_con,client_addr=get_socket_con.accept()
            print("Visitor found! - [{}]".format(client_addr[0]))
            client_con.send(b"<h1> You have been hacked!</h1>")
            data=client_con.recv(2048)
            print(data.decode('utf-8'))
    except error as identifier:
        print("[+] Unspecified error occurred: [{}]".format(identifier))
    except KeyboardInterrupt as ky:
        print("[-] Process Stoped!")
    finally:
        get_socket_con.close()
    get_socket_con.close()
if __name__ == "__main__":
    main()


