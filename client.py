import socket
import pygame
import graphics
import threading


pygame.init()
screen = pygame.display.set_mode((750, 538))
clock = pygame.time.Clock()


# sock = socket.socket()
# ip = "127.0.0.1"    # means local
# port = 60000
# sock.connect((ip, port))

#authentication screen
login_background = pygame.image.load("authen.jpg")
login_username_box = graphics.text_box(screen, 200, 175, 350, 40, "username")
login_password_box = graphics.text_box(screen, 200, 241, 350, 40, "password")
Login_button = graphics.button(195, 307, 360, 43, "sign in")
create_account_button = graphics.button(394, 371, 151, 20, "create account")

#register screen
signup_background = pygame.image.load("signup.jpg")
signup_username_box = graphics.text_box(screen, 200, 170, 350, 40, "username")
signup_password_box = graphics.text_box(screen, 200, 236, 350, 40, "password")
signup_confirm_box = graphics.text_box(screen, 200, 300, 350, 40, "confirm password")
sign_up_button = graphics.button(196, 366, 360, 43, "sign up")


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

        font = pygame.font.SysFont('arial', 30)
        text = font.render(str(login_username_box.textinput.get_surface().get_width()), True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 150, 50))
        screen.blit(text, (2, 2))

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
            current_screen = "login"

        pygame.display.flip()


