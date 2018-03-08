
"""
Copyright 2017, Silas Gyger, silasgyger@gmail.com, All rights reserved.
"""

import pygame
import pygame.locals as pl
import os.path
pygame.font.init()


class TextInput:
    """
    This class lets the user input a piece of text, e.g. a name or a message.

    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, home and end work as well.
    """
    def __init__(self, width, height,
                        font_family = "",
                        font_size = 35,
                        antialias=True,
                        text_color=(0, 0, 0),
                        cursor_color=(0, 0, 1),
                        repeat_keys_initial_ms=400,
                        repeat_keys_interval_ms=35):
        """
        Args:
            font_family: Name or path of the font that should be used. Default is pygame-font
            font_size: Size of the font in pixels
            antialias: (bool) Determines if antialias is used on fonts or not
            text_color: Color of the text
            repeat_keys_initial_ms: ms until the keydowns get repeated when a key is not released
            repeat_keys_interval_ms: ms between to keydown-repeats if key is not released
        """

        self.width = width
        self.height = height
        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.input_string = "" # Inputted text
        if not os.path.isfile(font_family): font_family = pygame.font.match_font(font_family)
        self.font_object = pygame.font.Font(font_family, font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((self.width ,self.height), pygame.SRCALPHA, 32).convert_alpha()
        # self.surface.fill((255,255,255))

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {} # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size/20+1), font_size*3/4))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = 0 # Inside text
        self.cursor_visible = True # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500 # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, events):

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True # So the user sees where he writes

                # If none exist, create counter for that key:
                if not event.key in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pl.K_BACKSPACE:  # FIXME: Delete at beginning of line?
                    self.input_string = self.input_string[:max(self.cursor_position - 1, 0)] + \
                                        self.input_string[self.cursor_position:]

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pl.K_DELETE:
                    self.input_string = self.input_string[:self.cursor_position] + \
                                        self.input_string[self.cursor_position + 1:]

                elif event.key == pl.K_RETURN:
                    lines = self.line_up(self.input_string, self.width).split("\n")
                    if len(lines) < (self.height - 22) / self.font_size:
                        self.input_string = self.input_string[:self.cursor_position] + \
                                            " \n" + \
                                            self.input_string[self.cursor_position:]
                        self.cursor_position += len(event.unicode) +1
                        return True

                elif event.key == pl.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == pl.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pl.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pl.K_HOME:
                    self.cursor_position = 0


                else:
                    lines = self.line_up(self.input_string + event.unicode, self.width).split("\n")
                    if len(lines) <= (self.height) / self.font_size:
                            self.input_string = self.input_string[:self.cursor_position] + \
                                                event.unicode + \
                                                self.input_string[self.cursor_position:]
                            self.cursor_position += len(event.unicode) # Some are empty, e.g. K_UP


            elif event.type == pl.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time() # Update clock
            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = self.keyrepeat_intial_interval_ms - \
                                                    self.keyrepeat_interval_ms

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(pl.KEYDOWN, key=event_key, unicode=event_unicode))

        # Rerender text surface:
        lines = self.line_up(self.input_string, self.width).split("\n")
        # print lines
        self.surface = pygame.Surface((self.width, len(lines) * self.font_size), pygame.SRCALPHA, 32).convert_alpha()
        # self.surface.fill((255,255,255))
        for i in range(len(lines)):
            line_surface = self.font_object.render(lines[i], self.antialias, self.text_color)
            self.surface.blit(line_surface, (0, i * self.font_size))

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        s = 0
        if len(lines) > 1:
            for i in range(len(lines) - 1):
                s += len(lines[i]) - 1

        if self.cursor_visible:
            cursor_y_pos = self.font_object.size(lines[-1][:self.cursor_position - s])[0]
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0:
                cursor_y_pos -= self.cursor_surface.get_width()
            self.surface.blit(self.cursor_surface, (cursor_y_pos, self.font_size*(len(lines)-1)))

        self.clock.tick()
        return False

    def clear(self):
        self.input_string = ""
        self.cursor_position = 0

    def get_surface(self):
        return self.surface

    def get_text_surface(self):
        lines = self.line_up(self.input_string, self.width).split("\n")
        # print lines
        sur = pygame.Surface((self.width, len(lines) * self.font_size), pygame.SRCALPHA, 32).convert_alpha()
        # self.surface.fill((255,255,255))
        for i in range(len(lines)):
            line_surface = self.font_object.render(lines[i], self.antialias, self.text_color)
            sur.blit(line_surface, (0, i * self.font_size))
        return sur

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def line_up(self, string, width):
        font = self.font_object
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
