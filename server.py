import socket
import threading

sock = socket.socket()
ip = "0.0.0.0" # means local
port = 60000
sock.bind((ip, port))
sock.listen(10)
threads = []

def server(new_sock):
    # get_authen()
    # send_menu()
    # game = get_choice()
    # send_game_info(game)
    # send_posts(game)
    while True:
        data = new_sock.recv(1024)

while True:
    cli_s, addr = sock.accept()
    t = threading.Thread(target=server, args=(cli_s,))
    print "hi"
    t.start()
    threads.append(t)
