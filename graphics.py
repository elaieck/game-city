import pygame
import pygame_textinput

class text_box():

    def __init__(self, screen, x , y, width, height, text="", size=30):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.size = size
        self.activated = False
        self.textinput = pygame_textinput.TextInput(font_size=size)
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

    def _is_in(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        return self.x < x_mouse < self.x+self.width and self.y < y_mouse < self.y+self.height


    def update_press(self):
        pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
        if pressed1:
            if self._is_in():
                self.activated = True
            else:
                self.activated = False

    def update(self, events, hide=False):
        self.update_press()

        if self.activated:
            if self.textinput.get_surface().get_width() >= self.width - 15:
                self.textinput.update(events, True)
            else:
                self.textinput.update(events)
            self.screen.blit(self.textinput.get_surface(), (self.x+4, self.y+11))
        else:
            font = pygame.font.SysFont('', self.size)
            if self.textinput.get_text() == "":
                text = font.render(self.text, True, (127, 127, 127))
            else:
                text = font.render(self.textinput.get_text(), True, (0, 0, 0))
            self.screen.blit(text, (self.x+4, self.y+11))

class button():

    def __init__(self, x , y, width, height, text=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

    def _is_in(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        return self.x<x_mouse<self.x+self.width and self.y<y_mouse<self.y+self.height


    def is_pressed(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self._is_in():
                return True
        return False

class image_button(button):
    def __init__(self,screen, x, y, image):
        self.image = pygame.image.load(image)
        button.__init__(self, x, y, self.image.get_width, self.image.get_height)
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)
        self.screen = screen

    def show(self):
        self.screen.blit(self.image, (self.x, self.y))













def main():
    pygame.init()
    screen = pygame.display.set_mode((750, 538))
    clock = pygame.time.Clock()

    username_box = text_box(screen, 200, 175, 350, 40, "username")
    password_box = text_box(screen, 200, 241, 350, 40, "password")

    while True:
        screen.fill((225, 225, 225))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        background = pygame.image.load("authen.jpg")
        screen.blit(background, (0, 0))

        pos = pygame.mouse.get_pos()
        font = pygame.font.SysFont('arial', 30)
        text = font.render(str(pos), True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 150, 50))
        screen.blit(text, (2, 2))

        username_box.update(events)
        password_box.update(events)

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
