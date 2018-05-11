import socket
import json
import thread
from shooter import Shooter

print "NOOOOOOOOOOOOOOOOO"
srv_sock = socket.socket()
ip = "0.0.0.0" # means local
port = 61234
srv_sock.bind((ip, port))
srv_sock.listen(10)


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

X_BOUND = SCREEN_WIDTH*2
Y_BOUND = SCREEN_HEIGHT*2

shooters = []


def get_approval(shtr):
        """
         check if shooter's color available.
        """
        for shooter in shooters:
            if shooter.color == shtr.color:
                return False
        return True


def update_shooters(shtr):
    """
    updates newest shooter in shooters list. if shooter does not exist create a new one.
    """
    for i in range(len(shooters)):
        if shooters[i].color == shtr.color:
            shooters[i] = shtr   #updating existing shooter
            return
    shooters.append(shtr)   #creating a new shooter



def control_player(presses, me):
    """
    if mouse was clicked, shoot a bullet
    if a,s,d,w keys were pressed, move shooter in a direction corrected speed.
    """
    if "shoot" in presses:
        me.shoot(me.angle)
        presses.remove("shoot")
    movement = 3
    if len(presses) == 2:
        movement = 2.121 # movement^2 + movement^2 =  new_movement^2
    for press in presses:
        if press == "up" and me.y > 0 + me.RADIUS:
            me.y -= movement
        if press == "down" and me.y < Y_BOUND - me.RADIUS:
            me.y += movement
        if press == "left" and me.x > 0 + me.RADIUS:
            me.x -= movement
        if press == "right" and me.x < X_BOUND - me.RADIUS:
            me.x += movement

def shooters_to_send(me):
    """
    return a list to send to the client - [me, other players]
    """
    enemy_shooters = shooters[:]
    enemy_shooters.remove(me)
    for i in range(len(enemy_shooters)):
        enemy_shooters[i] = enemy_shooters[i].to_list()

    return [me.to_list()] + enemy_shooters


def check_hits(me):
    """
    for each shooter:
    if a bullet in its stack hit the player:
    -remove bullet
    -decrease players life
    -increase shooter score
    """
    for i in range(len(shooters)):
        hits = me.check_hit(shooters[i].stack)
        shooters[i].score += len(hits)*100
        for hit in hits:
            shooters[i].stack.remove(hit)



def do_client(new_sock):
    """
    ~main server's loop~
    for each client -
    send his shooter and all shooters in arena after some update, and checks
    """
    me = Shooter(None, 500, 30)
    me.set_new_color()
    while not get_approval(me):
        me.set_new_color()

    me.set_random_position(X_BOUND, Y_BOUND)
    shooters.append(me)

    Done = False
    while not Done:
        try:
            to_send = shooters_to_send(me)

            if me.life <= 0:
                Done = True
                to_send = "LOS"
            elif me.life < 100:
                me.life += 0.01

            to_send = json.dumps(to_send)
            new_sock.send(to_send)

            recv = new_sock.recv(1024)

            if recv == "CLD": #stands for - CLient Disconnected
                print "Client Disconnected"
                Done = True
            else:
                recv = json.loads(recv)
                me.angle = recv[0]
                presses = recv[1::]
                control_player(presses, me)
                me.move_shot()
                update_shooters(me)
                check_hits(me)

        except:
            print "closing current socket because of technical issues"
            Done = True
    shooters.remove(me)
    new_sock.close()



while True:
    (new_sock, address) = srv_sock.accept()
    t = thread.start_new_thread(do_client, (new_sock,))



