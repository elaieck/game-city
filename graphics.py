import pygame
import pygame_textinput


class TextBox():

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
        return self.x <= x_mouse <= self.x+self.width and self.y <= y_mouse <= self.y+self.height

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
            print self.textinput.get_text()
            print font.metrics(self.textinput.get_text())
            if self.textinput.get_text() == "":
                text = font.render(self.text, True, (127, 127, 127))
            else:
                text = font.render(self.textinput.get_text(), True, (0, 0, 0))
            self.screen.blit(text, (self.x+4, self.y+11))

    def get_text(self):
        return self.textinput.get_text()


class Button():

    def __init__(self, x, y, width, height, description=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.description = description

    def is_in(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        return self.x<x_mouse<int(self.x+self.width) and self.y<y_mouse<int(self.y+self.height)

    def is_pressed(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.is_in():
                return True
        return False


class ImageButton(Button):
    def __init__(self, screen, x, y, image, description):
        self.image = pygame.image.load(image)
        Button.__init__(self, x, y, self.image.get_width(), self.image.get_height(), description)
        self.screen = screen

    def show(self):
        self.screen.blit(self.image, (self.x, self.y))


class DrawButton(Button):
    def __init__(self, screen,  x, y, width, height, color, text="", text_color=(255, 255, 255)):
        Button.__init__(self, x, y, width, height, text)
        self.color = color
        self.screen = screen
        self.text_color = text_color

    def show(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('', 30)
        text = font.render(self.description, True, self.text_color)
        self.screen.blit(text, (self.x, self.y))


class DialogBox():
    def __init__(self, screen, x, y, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.text = text
        self.box = pygame.image.load("images\dialog.jpg")
        self.ok_button = Button(x+99, y+200, 120, 36)
        self.activated = False


    def activate(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            self.screen.blit(self.box, (self.x, self.y))
            font = pygame.font.SysFont('', 24)
            text = font.render(self.text, True, (120, 221, 213))
            self.screen.blit(text, (self.x+35, self.y+40))
            if self.ok_button.is_pressed(events):
                break
            pygame.display.flip()


class ScrollBox():

    def __init__(self, screen, x, y, width, height, surfaces=[]):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surfaces = surfaces
        self.scroll_pos = 0
        self.space = 15
        self.scroller = DrawButton(self.screen, self.x+self.width, self.y, 50, self.height, (255,255,255))

    def show(self, events):
        pygame.draw.rect(self.screen, (255, 255, 0), (self.x, self.y, self.width, self.height))
        sur_x = self.x + self.space
        sur_y = self.y + self.space
        for surface in self.surfaces:
            self.screen.blit(surface, (sur_x, sur_y - self.scroll_pos))
            sur_y += surface.get_height() + self.space

        self.scroller.show()
        if self.scroller.is_in() and pygame.mouse.get_pressed()[0]:
            self.scroll_pos = pygame.mouse.get_pos()[1] - self.y


# class ScrollBox():
#
#     def __init__(self, screen, x, y, width, height, surfaces=[]):
#         self.screen = screen
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.surfaces = surfaces
#         self.scroll_pos = 0
#         self.space = 15
#         self.scroller = DrawButton(self.screen, self.x+self.width, self.y, 50, self.height, (255,255,255))
#
#     def show(self, events):
#         pygame.draw.rect(self.screen, (255, 255, 0), (self.x, self.y, self.width, self.height))
#         sur_x = self.x + self.space
#         sur_y = self.y + self.space
#         for surface in self.surfaces:
#             self.screen.blit(surface, (sur_x, sur_y - self.scroll_pos))
#             sur_y += surface.get_height() + self.space
#
#         self.scroller.show()
#         if self.scroller.is_in() and pygame.mouse.get_pressed()[0]:
#             self.scroll_pos = pygame.mouse.get_pos()[1] - self.y


"""
game page:
colors: light purple: (146,144,244)
        black purple: (17,22,78)
        glowy greenish: (137,255,223)
"""


class Post():

    def __init__(self, screen, x, y, width, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.text = text
        self.frame_color = (146, 144, 244)
        self.color = (17, 22, 78)
        self.friend_button = DrawButton(self.screen, self.x+self.width-30-155, self.y+25, 155, 49,(17,22,78))

    def get_lined_string(self):
        font = pygame.font.SysFont('', 30)
        for index in range(len(self.text)):
            widths = [x[4] for x in font.metrics(self.text)]
            if sum(widths[:index]) / self.width > 0:
                new_text = self.text[:index]+"\n"+self.text[index:]
                break
        self.text = new_text

    def r(self,string, limit, p):
        font = pygame.font.SysFont('', 30)
        widths = [x[4] for x in font.metrics(string)]
        length = sum(widths)
        if length - p < limit:
            return string
        else:
            return self.r(string[1])










def screen_print(screen, x):
    font = pygame.font.SysFont('arial', 30)
    text = font.render(str(x), True, (0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 150, 50))
    screen.blit(text, (2, 2))





def main():
    pygame.init()
    screen = pygame.display.set_mode((750, 538))
    clock = pygame.time.Clock()

    # username_box = TextBox(screen, 200, 175, 350, 40, "username")
    # password_box = TextBox(screen, 200, 241, 350, 40, "password")
    # s = ScrollBox(screen, 20, 200, 600, 300, [pygame.image.load("images\\shoot.jpg"),pygame.image.load("images\\shoot.jpg")])
    p = Post(screen, 20, 100, 200, "dfsdsldjknlkjvlkjnjkjaal;skdf;asklsdghjkgjhkghkgjkl")
    print p.text
    p.get_lined_string()
    print p.text
    while True:
        screen.fill((225, 225, 225))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # s.show(events)
        #
        # background = pygame.image.load("authen.jpg")
        # screen.blit(background, (0, 0))
        #
        # pos = pygame.mouse.get_pos()
        # font = pygame.font.SysFont('arial', 30)
        # text = font.render(str(pos), True, (0, 0, 0))
        # pygame.draw.rect(screen, (255, 255, 255), (0, 0, 150, 50))
        # screen.blit(text, (2, 2))
        #
        # h = DialogBox(screen, 200, 175, "dfsgf")
        #
        # username_box.update(events)
        # password_box.update(events)

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
