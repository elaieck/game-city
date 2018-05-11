import pygame
import socket
import json
from shooter import Shooter
from Bullet import Bullet
import sys

pygame.init()

ip = sys.argv[1]
port = 61234


#_____________________________________________________________________functions____________________________________________________________________


def set_background(x_screen_delta, y_screen_delta):
    """
    sets arena background in a shape of a web
    """
    screen.fill((255,255,255))
    pygame.draw.lines(screen, (0,255,255), True, [(0-x_screen_delta, 0-y_screen_delta), (0-x_screen_delta, Y_BOUND-y_screen_delta), (X_BOUND - x_screen_delta, Y_BOUND - y_screen_delta), (X_BOUND - x_screen_delta, 0-y_screen_delta)], 4)
    j = 0
    while j < X_BOUND:
        pygame.draw.line(screen, (177,177,177), (j-x_screen_delta,0-y_screen_delta),(j-x_screen_delta, Y_BOUND-y_screen_delta))
        j +=100

    i = 0
    while i < Y_BOUND:
        pygame.draw.line(screen, (177,177,177), (0-x_screen_delta,i-y_screen_delta),(X_BOUND-x_screen_delta, i-y_screen_delta))
        i+=100


def show_score():
    """
    shows player's score in the bottom of the screen
    """
    score_font = pygame.font.SysFont("monospace", 40)
    label = score_font.render(str(me.score), 1, (0,0,0))
    screen.blit(label, (SCREEN_WIDTH/2-10, SCREEN_HEIGHT - 80))


def show_defeat_screen():
    """
    at defeat, show lost screen with a retry button
    """
    pic = pygame.image.load("shoot\\end.png").convert_alpha()
    screen.blit(pic, (0,0))

    score_font = pygame.font.SysFont("comicsansms", 55)
    label = score_font.render(str(me.score), 1, (44,137,109))
    screen.blit(label, (640, 353))

    Done = False
    while not Done:
        (Mx, My) = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if Mx > 423 and Mx < 666 and My > 450 and My < 575 and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] :
                Done = True

        pygame.display.flip()


def show_start_screen():
    """
     show screen when entering the game with a play button
    """
    pic = pygame.image.load("shoot\\start.png").convert_alpha()
    screen.blit(pic, (0,0))

    finish_start_screen = False
    while not finish_start_screen:
        (Mx, My) = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if Mx > 79 and Mx < 423 and My > 420 and My < 545 and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] :
            finish_start_screen = True

        pygame.display.flip()

def recv_info():
    """
    receive info from server and check if you lose
    """
    global me
    global defeat
    global done
    global shooters

    recv = sock.recv(3000)
    recv = json.loads(recv)
    if recv == "LOS":
        defeat = True
        done = True
    else:
        me = to_shooter(recv[0])
        shooters = recv[1:]
        for i in range(len(shooters)):
            shooters[i] = to_shooter(shooters[i])


def get_events():
    """
    return list of event that are important to the game - w,a,s,d, mouse click
    also check if the X button was pressed and exits the game
    """
    global done
    press = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            press.append("shoot")

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        press.append("up")
    if pressed[pygame.K_s]:
        press.append("down")
    if pressed[pygame.K_a]:
        press.append("left")
    if pressed[pygame.K_d]:
        press.append("right")

    return press


def to_shooter(list):
    """
    creates a shooter with a list of a shooter information
    """
    s = Shooter(screen, list[0], list[1])
    for tup in list[2]:
        s.stack.append(Bullet(screen, tup[0], tup[1], tup[2], tup[3],tup[4]))
    s.color = list[3]
    s.angle = list[4]
    s.life = list[5]
    s.score = list[6]
    s.X_BOUND = X_BOUND
    s.Y_BOUND = Y_BOUND
    return s



#____________________________________________________________________MAIN___________________________________________________________________
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

X_BOUND = SCREEN_WIDTH*2
Y_BOUND = SCREEN_HEIGHT*2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

#____________________________________________________________game_loop_____
quit = False
while not quit:
    show_start_screen()

    sock = socket.socket()
    sock.connect((ip, port))

    me = Shooter(screen, 500, 30)
    shooters = []

    x_screen_delta = me.x - SCREEN_WIDTH / 2
    y_screen_delta = me.y - SCREEN_HEIGHT / 2

    defeat = False
    done = False

    while not done:         #acctual game play loop
        try:
            set_background(x_screen_delta, y_screen_delta)

            recv_info()

            press = get_events()

            angle = me.get_angle(x_screen_delta, y_screen_delta)
            sock.send(json.dumps([angle] + press))


            x_screen_delta = int(me.x - SCREEN_WIDTH / 2)
            y_screen_delta = int(me.y - SCREEN_HEIGHT / 2)

            me.show_shot(x_screen_delta, y_screen_delta)
            me.show(x_screen_delta, y_screen_delta)

            for shtr in shooters:
                shtr.show_shot(x_screen_delta, y_screen_delta)
                shtr.show(x_screen_delta, y_screen_delta)


            show_score()

            pygame.display.flip()
            clock.tick(90)
        except:
            sock.send("CLD") #stands for - CLient Disconnected
            print "CLD"
            sock.close()
            sys.exit()

    sock.send("CLD") #stands for - CLient Disconnected
    print "CLD"
    sock.close()
    if defeat:
        show_defeat_screen()
    else:
        quit = True









