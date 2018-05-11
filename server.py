import socket
import threading
from SQL_ORM import ORM
import pickle
import subprocess


db = ORM()
srv_sock = socket.socket()
ip = "0.0.0.0" # means local
port = 59567
srv_sock.bind((ip, port))
srv_sock.listen(10)
threads = []
game_is_open = False

requests = []
messages = []
invites = []
accepts = []

#divide list to parts
def parts(message):
    return message.split("~")

#take care of login and signup
def get_authen(sock):
    data = sock.recv(1024)
    message = parts(data)
    if message[0] == "LOGIN":
        user = db.get_user(message[1])
        if user is None:
            sock.send("LOF")
            return None
        elif user.password != message[2]:
            sock.send("LOF")
            return None
        else:
            sock.send("LOS")
            return user
    else:
        if db.get_user(message[1]) is not None:
            sock.send("SUF")
            return None
        else:
            db.insert_new_user(message[1], message[2])
            sock.send("SUS")
            return None


#send whatever client needs for the games
def send_game_info(sock, game):
    sock.send("GINFO~" + str(game.name) + "~" + str(game.price))
    posts = db.get_game_posts(game.id)
    str_posts = pickle.dumps(posts)
    sock.send("GPOSTS~" + str_posts)

#checks if user bought a specific game
def game_bought(game_id, username):
    purchased_games_info = db.get_user(username).games
    purchased_games = [game_info[:2] for game_info in purchased_games_info]
    return game_id in purchased_games

#checks if user has game invites
def check_invites(name):
    print invites
    for invt in invites:
        if invt[0] == name:
            invites.remove(invt)
            return [invt[1], invt[2], invt[3], invt[4]]
    return None

#checks if user has messages
def check_messages(name):
    for msg in messages:
        if msg[0] == name:
            messages.remove(msg)
            return [msg[1], msg[2]]
    return None

#checks if user has messages
def check_accepts(name):
    for acpt in accepts:
        if acpt[0] == name:
            accepts.remove(acpt)
            return [acpt[1], acpt[2]]
    return None

#checks if user has messages
def check_requests(name):
    for req in requests:
        if req[0] == name:
            requests.remove(req)
            return req[1]
    return None

#checks if user has messages
def server(sock, address):
    try:
        while True:
            user = get_authen(sock)
            if user is not None:
                break
        while True:
                info = parts(sock.recv(1024))
                action = info[0]
                if action == "":
                    break

                elif action == "CHSGM":
                    game = db.get_game(info[1])
                    send_game_info(sock, game)

                elif action == "POST":
                    db.insert_new_post(int(info[1]), info[2], user.name, info[3])

                elif action == "PLAY":
                    if game_bought(info[1], user.name):
                        sock.send("approved")
                    else:
                        sock.send("BUYPLZ")

                elif action == "BUY":
                    if game_bought(info[1], user.name):
                        sock.send("ALBUY")
                    else:
                        db.buy_game(user.name, info[1])
                        sock.send("BUYSUC")

                elif action == "SNDMSG":
                    if info[2] == "=%#00#%=":
                        invitation = [info[1], user.name, "00", address[0], "61234"]
                        if invitation not in invites:
                            invites.append(invitation)
                    else:
                        messages.append([info[1], user.name, info[2]])

                elif action == "SNDACPT":
                        acception = [info[1], user.name, info[2]]
                        if acception not in accepts:
                            accepts.append(acception)

                elif action == "GETMSG":
                    found = check_messages(user.name)
                    if found:
                        sock.send("GOTMSG~%s~%s" % (found[0], found[1]))
                    else:
                        sock.send("NOMSG")

                elif action == "GETREQ":
                    found = check_requests(user.name)
                    if found:
                        sock.send("GOTREQ~%s" % (found[0]))
                    else:
                        sock.send("NOREQ")

                elif action == "ASKFRND":
                    req = (info[1], user.name)
                    if req not in requests:
                        requests.append(req)

                elif action == "GETINVT":
                    found = check_invites(user.name)
                    if found:
                        sock.send("GOTINVT~%s~%s~%s~%s" % (found[0], found[1], found[2], found[3]))
                    else:
                        sock.send("NOINVT")

                elif action == "GETACPT":
                    found = check_accepts(user.name)
                    if found:
                        sock.send("GOTACPT~%s~%s" % (found[0], found[1]))
                    else:
                        sock.send("NOACPT")

                elif action == "ADDFRND":
                    db.attach_friends(user.name, info[1])

                elif action == "GETFRNDS":
                    sock.send("~".join(["FRNDS"]+db.get_user(user.name).friends))
    except:
        print "client disconnected"
        # found = check_messages(user.name)
        # if found:
        #     sock.send("GOTMSG~%s~%s" % (found[0], found[1]))
        # else :
        #     sock.send("NOMSG")



# while True:
    #     data = sock.recv(1024)

# subprocess.Popen(["python", "shoot\\server.py"])
while True:
    cli_s, addr = srv_sock.accept()
    t = threading.Thread(target=server, args=(cli_s, addr,))
    t.start()
    threads.append(t)

