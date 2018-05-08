import pygame
import pygame_textinput

VIOLET = (146, 144, 244)
PURPLE = (17, 22, 78)
GREEN = (137, 255, 223)

class TextBox():

    def __init__(self, screen, x, y, width, height, text="", size=30, hide=False):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.size = size
        self.activated = False
        self.textinput = pygame_textinput.TextInput(self.width, self.height, font_size=size, hide=hide)
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

    def is_in(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        return self.x <= x_mouse <= self.x+self.width and self.y <= y_mouse <= self.y+self.height

    def update_press(self):
        pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
        if pressed1:
            if self.is_in():
                self.activated = True
            else:
                self.activated = False

    def update(self, events):
        self.update_press()
        if self.activated:
            self.textinput.update(events)
            self.screen.blit(self.textinput.get_surface(), (self.x+4, self.y+11))
        else:
            if self.textinput.get_text() == "":
                text = self.textinput.font_object.render(self.text, True, (127, 127, 127))
                self.screen.blit(text, (self.x+4, self.y+11))
            else:
                self.screen.blit(self.textinput.get_text_surface(), (self.x+4, self.y+11))

    def get_text(self):
        return self.textinput.get_text()

    def clear(self):
        self.textinput.clear()


class Button():

    def __init__(self, x, y, width, height, description=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.description = description
        self.released = True

    def is_in(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        return self.x < x_mouse < int(self.x+self.width) and self.y < y_mouse < int(self.y+self.height)

    def is_pressed(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.is_in():
                self.released = False
                return False
            elif event.type == pygame.MOUSEBUTTONUP and not self.is_in() and not self.released:
                self.released = True
                return False
            if event.type == pygame.MOUSEBUTTONUP and self.is_in() and not self.released:
                self.released = True
                return True
        return False

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width


class ImageButton(Button):
    def __init__(self, screen, x, y, image, description=""):
        if type(image) is str:
            self.image = pygame.image.load(image)
        else:
            self.image = image
        Button.__init__(self, x, y, self.image.get_width(), self.image.get_height(), description)
        self.screen = screen

    def show(self):
        self.screen.blit(self.image, (self.x, self.y))


class DrawButton(Button):
    def __init__(self, screen,  x, y, width, height, color, text="", text_color=(255, 255, 255), stroke_color=None):
        Button.__init__(self, x, y, width, height, text)
        self.color = color
        self.screen = screen
        self.text_color = text_color
        self.stroke_color = stroke_color

    def show(self):
        if self.stroke_color is not None:
            pygame.draw.rect(self.screen, self.stroke_color, (self.x-1, self.y-1, self.width+2, self.height+2))
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('', 30)
        text = font.render(self.description, True, self.text_color)
        self.screen.blit(text, (self.x + (self.width - text.get_width()) / 2,
                                self.y + (self.height - text.get_height()) / 2))


class DialogBox():
    def __init__(self, screen, x, y, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.text = text
        self.box = pygame.image.load("images\dialog.png").convert_alpha()
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
            self.screen.blit(text, (int(self.x+self.box.get_width()/2-text.get_width()/2), self.y+40))
            if self.ok_button.is_pressed(events):
                break
            pygame.display.flip()


class PromptBox(DialogBox):
    def __init__(self, screen, x, y, box_height, text, box_text="Enter info"):
        DialogBox.__init__(self, screen, x, y, text)
        self.box_height = box_height
        self.box_text = box_text
        self.text_box = TextBox(screen, self.x + 20, self.y + 60, self.box.get_width() - 40, box_height, self.box_text)


    def activate(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            self.screen.blit(self.box, (self.x, self.y))
            font = pygame.font.SysFont('', 24)
            text = font.render(self.text, True, (120, 221, 213))
            self.screen.blit(text, (int(self.x+(self.box.get_width()/2-text.get_width()/2)), self.y+40))
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (self.text_box.x, self.text_box.y, self.text_box.width, self.text_box.height))
            self.text_box.update(events)
            if self.ok_button.is_pressed(events):
                break
            pygame.display.flip()

    def get_text(self):
        return self.text_box.get_text()


class ScrollBox():

    def __init__(self, screen, x, y, width, height, surfaces=[], margin=15):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surfaces = surfaces
        self.scroll_pos = 0
        self.margin = margin
        self.pressed = False
        self.scroll_bar_rect = (self.x+self.width - 25, self.y + 50, 5, self.height-100)
        self.thumb = ImageButton(self.screen, self.x+self.width - 47, self.y, "images/glow.png", "scroll position")

    def show(self, events):
        sur_x = self.x + self.margin
        sur_y = self.y + self.margin
        scroll_height = self.scroll_bar_rect[3]
        scroll_y = self.scroll_bar_rect[1]

        sur = pygame.Surface((abs(self.x+self.width), abs(self.y+self.height)), pygame.SRCALPHA, 32)
        self.thumb.screen = sur
        for surface in self.surfaces:
            if type(surface) is pygame.Surface:
                showed_y = int(sur_y - float(self.scroll_pos) / scroll_height * (self.get_dept()-self.height))
                sur.blit(surface, (sur_x, showed_y))
                sur_y += surface.get_height() + self.margin
            else:
                surface.set_position(sur_x, int(sur_y - float(self.scroll_pos) / scroll_height * (self.get_dept()-self.height)))
                surface.screen = sur
                surface.show()
                sur_y += surface.get_height() + self.margin

        # self.scroll_bar.show()
        pygame.draw.rect(sur, (255, 255, 255), self.scroll_bar_rect)
        dept = self.get_dept()
        # if dept > self.height:
        press_y = pygame.mouse.get_pos()[1]
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.thumb.is_in():
                self.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.pressed = False

        if self.pressed:
            press_y = max(press_y, scroll_y)
            press_y = min(press_y, scroll_y + scroll_height)
            self.scroll_pos = press_y - self.scroll_bar_rect[1]

        self.thumb.y = self.scroll_pos + self.y + 25
        self.thumb.show()

        self.screen.blit(sur, (self.x, self.y), (self.x, self.y, self.width, self.height))


    def get_dept(self):
        dept = 0
        for surface in self.surfaces:
            dept += surface.get_height()
        dept += self.margin * (len(self.surfaces)+1)
        return max(dept, self.height)


class Post():

    def __init__(self, screen, x, y, width, user, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.user = user
        self.text = text
        self.frame_color = VIOLET
        self.fill_color = PURPLE
        self.bright_color = GREEN
        self.font_size = 30
        self.font = pygame.font.SysFont('', self.font_size)
        self.padding = 20
        self.friend_button = DrawButton(self.screen, self.x+self.width - 155 - self.padding,
                                        self.y + self.padding, 155, 49, self.bright_color, text="add friend")

    def line_up(self):
        font = self.font
        line_width = self.width - self.friend_button.get_width() - self.padding * 3
        if self.text == "":
            return ""
        words = self.text.split(" ")
        words_width = [font.render(x, True, (0, 0, 0)).get_width() for x in words]
        letters_width = [[font.render(letter, True, (0, 0, 0)).get_width() for letter in word] for word in words]
        line_len = 0

        i = 0
        for lw in letters_width:
            temp_list = []
            temp_word = ""
            temp_len = []
            len_word = 0
            if words_width[i] >= line_width:
                for j in range(len(lw)):
                    if len_word + lw[j] >= line_width:
                        temp_list.append(temp_word)
                        temp_word = words[i][j]
                        temp_len.append(len_word)
                        len_word = lw[j]
                    else:
                        temp_word += words[i][j]
                        len_word = font.render(temp_word, True, (0, 0, 0)).get_width()
                temp_list.append(temp_word)
                temp_len.append(len_word)
                words = words[:i] + temp_list + words[i+1:]
                words_width = words_width[:i] + temp_len + words_width[i+1:]
                i += len(temp_list)-1
            i += 1

        show_text = ""
        line = ""
        for i in range(len(words)):
            if words[i] != "":
                if words[i][0] == "\n":
                    line_len = 0
            if line_len + words_width[i] >= line_width:
                show_text += "\n" + words[i] + " "
                line = words[i] + " "
                line_len = words_width[i] + 6
            else:
                show_text += words[i] + " "
                line += words[i] + " "
                line_len += words_width[i] + 6
        return show_text

    def show(self):
        lined_text = self.line_up().split("\n")
        pygame.draw.rect(self.screen, self.frame_color, (self.x, self.y, self.width, self.get_height()))
        pygame.draw.rect(self.screen, self.fill_color, (int(self.x+2), int(self.y+2), int(self.width-4), int(self.get_height())-4))
        text = self.font.render(self.user, True, self.bright_color)
        self.screen.blit(text, (self.x+self.padding, self.y + self.padding))
        for i in range(len(lined_text)):
            text = self.font.render(lined_text[i], True, (255, 255, 255))
            self.screen.blit(text, (self.x+self.padding, self.y + self.padding + (i+1) * self.font_size))
        self.friend_button.show()

    def get_height(self):
        lined_text = self.line_up().split("\n")
        return (len(lined_text) + 1) * self.font_size + self.padding * 2

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.friend_button.y = y + self.padding
        self.friend_button.x = self.x + self.width - self.friend_button.width - self.padding


class WritePostBar():
    def __init__(self, screen):
        self.screen = screen
        self.activated = False
        self.text_button = DrawButton(screen,  0, 480, 750, 58, (255,255,255), text="Write post...", text_color=(127, 127, 127))
        self.fake_post_button = DrawButton(screen,  625, 480, 125, 58, (17, 22, 78), text="Post", text_color=(137, 255, 223))
        self.text_box = TextBox(screen, 0, 300, 625, 238, "What's on your mind?")
        self.post_button = DrawButton(screen,  625, 300, 125, 238, (17, 22, 78), text="Post", text_color=(137, 255, 223))

    def update(self, events):
        while self.activated:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                elif self.post_button.is_pressed(events):
                    self.activated = False
                    text = self.text_box.get_text()
                    self.text_box.clear()
                    return text
                elif not self.text_box.is_in() and event.type == pygame.MOUSEBUTTONUP:
                    self.activated = False
            pygame.draw.rect(self.screen, (255, 255, 255), (0, 300, 625, 238))
            self.text_box.update(events)
            self.post_button.show()
            pygame.display.flip()
        else:
            self.text_button.show()
            self.fake_post_button.show()
            if self.text_button.is_pressed(events):
                self.activated = True
        return ""


class FriendsBar():

    def __init__(self, screen, x, y, friends=[]):
        self.x = x
        self.y = y
        self.screen = screen
        self.background = pygame.image.load("images\\friends.png")
        self.width = self.background.get_width()
        self.height = self.background.get_height()
        self.scroll_box = ScrollBox(screen, self.x, self.y+100, self.width, self.height-100)
        self.friends = friends
        self.clock = pygame.time.Clock()
        self.released = True

    def set_friends(self, friends_list):
        self.friends = friends_list
        self.scroll_box.surfaces = [DrawButton(self.scroll_box.screen, self.x, self.y, 210, 40, PURPLE, friend, GREEN, GREEN)
                                    for friend in friends_list]

    def is_in(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        return self.x < x_mouse < int(self.x+self.width) and self.y < y_mouse < int(self.y+self.height)

    def in_scroll_box(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        x = self.scroll_box.x
        y = self.scroll_box.y
        width = self.scroll_box.width
        height = self.scroll_box.height
        return x < x_mouse < int(x + width) and y < y_mouse < int(y + height)

    def is_pressed_out(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.is_in():
                self.released = False
                return False
            elif event.type == pygame.MOUSEBUTTONUP and self.is_in() and not self.released:
                self.released = True
                return False
            if event.type == pygame.MOUSEBUTTONUP and not self.is_in() and not self.released:
                self.released = True
                return True
        return False

    def activate(self):
        sprite_offset = -self.width
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                elif self.is_pressed_out(events):
                    return None

            for button in self.scroll_box.surfaces:
                if button.is_pressed(events) and self.in_scroll_box():
                    return button.description


            if sprite_offset < 0:
                sprite_offset += 10


            self.screen.blit(self.background, (self.x + sprite_offset, self.y))
            self.scroll_box.x = sprite_offset
            self.scroll_box.show(events)
            pygame.display.flip()
            self.clock.tick(100)









def screen_print(screen, x):
    font = pygame.font.SysFont('', 30)
    text = font.render(str(x), True, (0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (50, 50, 150, 50))
    screen.blit(text, (52, 52))

def line_up(string, width, font):
        line_width = width - 15
        if string == "":
            return ""
        words = string.split(" ")
        words_width = [font.render(x, True, (0, 0, 0)).get_width() for x in words]
        letters_width = [[font.render(letter, True, (0, 0, 0)).get_width() for letter in word] for word in words]
        line_len = 0

        i = 0
        for lw in letters_width:
            temp_list = []
            temp_word = ""
            temp_len = []
            len_word = 0
            if words_width[i] >= line_width:
                for j in range(len(lw)):
                    if len_word + lw[j] >= line_width:
                        temp_list.append(temp_word)
                        temp_word = words[i][j]
                        temp_len.append(len_word)
                        len_word = lw[j]
                    else:
                        temp_word += words[i][j]
                        len_word = font.render(temp_word, True, (0, 0, 0)).get_width()
                temp_list.append(temp_word)
                temp_len.append(len_word)
                words = words[:i] + temp_list + words[i+1:]
                words_width = words_width[:i] + temp_len + words_width[i+1:]
                i += len(temp_list)-1
            i += 1

        show_text = ""
        line = ""
        for i in range(len(words)):
            if words[i] != "":
                if words[i][0] == "\n":
                    line_len = 0
            if line_len + words_width[i] >= line_width:
                show_text += "\n" + words[i] + " "
                line = words[i] + " "
                line_len = words_width[i] + 6
            else:
                show_text += words[i] + " "
                line += words[i] + " "
                line_len += words_width[i] + 6
        return show_text

def main():
    pygame.init()
    screen = pygame.display.set_mode((750, 538))
    clock = pygame.time.Clock()

    bar = FriendsBar(screen, 80, 0)
    bar.set_friends(["elai", "maureen", "jesus", "momo", "shlomo", "yecheskerghoma", "fucker", "maureen is annoyinggg", "f", "f", "sf", "Sd"])

    while True:
        screen.fill((225, 225, 225))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        bar.activate()
        # s.show(events)
        #
        # background = pygame.image.load("authen.jpg")
        # screen.blit(background, (0, 0))
        #
        # pos = pygame.mouse.get_pos()
        # font = pygame.font.SysFont('arial', 30)
        # text = font.render(str(pos), True, (0, 0, 0))
        # pygame.draw.rect(screen, (255, 255, 255), (40, 50, 400, 300))
        # y.update(events)
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
