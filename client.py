import socket
import pygame
import graphics
import hashlib
import subprocess

pygame.init()
screen = pygame.display.set_mode((750, 538))
clock = pygame.time.Clock()


sock = socket.socket()
ip = "127.0.0.1"    # means local
port = 60000
sock.connect((ip, port))

#authentication screen
login_background = pygame.image.load("authen.jpg")
login_username_box = graphics.TextBox(screen, 200, 175, 350, 40, "username")
login_password_box = graphics.TextBox(screen, 200, 241, 350, 40, "password")
login_button = graphics.Button(195, 307, 360, 43, "sign in")
create_account_button = graphics.Button(394, 371, 151, 20, "create account")
login_error_box = graphics.DialogBox(screen, 195, 123, "wrong password or username")

#register screen
signup_background = pygame.image.load("signup.jpg")
signup_username_box = graphics.TextBox(screen, 200, 170, 350, 40, "username")
signup_password_box = graphics.TextBox(screen, 200, 236, 350, 40, "password")
signup_confirm_box = graphics.TextBox(screen, 200, 300, 350, 40, "confirm password")
sign_up_button = graphics.Button(196, 366, 360, 43, "sign up")


#menu screen
menu_background = pygame.image.load("games_menu.jpg")
game_buttons = [
    graphics.ImageButton(screen, 37, 117, "images\shoot.jpg", "0"),
    graphics.ImageButton(screen, 379, 117, "images\shoot.jpg", "1"),
    graphics.ImageButton(screen, 37, 322, "images\shoot.jpg", "2"),
    graphics.ImageButton(screen, 379, 322, "images\shoot.jpg", "3")
]



current_screen = "login"
while True:

    while current_screen == "login":
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        screen.blit(login_background, (0, 0))
        login_username_box.update(events)
        login_password_box.update(events)

        if create_account_button.is_pressed(events):
            current_screen = "signup"

        elif login_button.is_pressed(events):
            username = login_username_box.get_text()
            password = hashlib.md5(login_password_box.get_text()).hexdigest()
            sock.send("LOGIN~%s~%s" % (username, password))

            recv = sock.recv(3)
            if recv == "LOS":
                current_screen = "menu"
            else:
                print "FAILED LOGIN :("
                login_error_box.activate()

        pygame.display.flip()

    while current_screen == "signup":
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        screen.blit(signup_background, (0, 0))
        signup_username_box.update(events)
        signup_password_box.update(events)
        signup_confirm_box.update(events)

        if sign_up_button.is_pressed(events):
            username = signup_username_box.get_text()
            password = hashlib.md5(signup_password_box.get_text()).hexdigest()
            sock.send("SIGNUP~%s~%s" % (username, password))
            recv = sock.recv(3)
            if recv == "SUS":
                current_screen = "login"
            else:
                print "SIGN UP FAILED :("
        pygame.display.flip()

    while current_screen == "menu":
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        screen.blit(menu_background, (0, 0))
        for game in game_buttons:
            game.show()
            if game.is_pressed(events):
                # sock.send("CHSGM~" + game.description)
                # current_screen = "game_page"
                subprocess.Popen(["python", "shoot\\server.py"])
                subprocess.Popen(["python", "shoot\\client.py"])
                pass
        pygame.display.flip()

    while current_screen == "game_page":
        pass

