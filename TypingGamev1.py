# required imports
import pygame
from pygame.locals import *
import sys
import time
import random


class Game:

    def __init__(self):
        # constants
        self.WIDTH = 750
        self.HEIGHT = 500

        # colour constants
        self.HEAD_C = (255, 255, 255)
        self.TEXT_C = (195, 205, 255)
        self.RESULT_C = (255, 70, 70)

        # game settings
        self.reset = True
        self.active = False
        self.end = False

        # gave variables
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Accuracy:0 % Wpm:0 Cpm:0'
        self.wpm = 0
        self.cpm = 0

        self.char_count = -1
        self.movement_val = 0
        self.sentence_length = 0

        # importing images
        self.running_img = pygame.image.load('guyrunning.png')
        self.running_img = pygame.transform.scale(self.running_img, (75, 85))
        self.finish_img = pygame.image.load('finishline.jpg')
        self.finish_img = pygame.transform.scale(self.finish_img, (90, 90))

        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Type Speed test')

    def draw_text(self, screen, msg, y, fsize, colour):
        # create a new font of certain size
        font = pygame.font.Font(None, fsize)
        # render the font with message and different colour
        text = font.render(msg, 1, colour)
        # place text in the middle of the screen
        text_rect = text.get_rect(center=(self.WIDTH/2, y))
        # place onto the screen
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):
        # open up texts file
        f = open('sentences.txt').read()
        word = f.split('\n')
        x = True
        while x == True:
            # fucks up on capital letters
            sentence = ('{} {} {} {} {} {} {} {} {} {}'.format(random.choice(word), random.choice(word), random.choice(word), random.choice(word), random.choice(
                word), random.choice(word), random.choice(word), random.choice(word), random.choice(word), random.choice(word)))
            if len(sentence) < 50:
                self.sentence_length = len(sentence)
                x = False
        return sentence

    def show_results(self, screen):
        if(not self.end):
            # calculate time
            self.total_time = time.time() - self.time_start

            # calculate accuracy
            correct = 0
            for i, c in enumerate(self.word):
                try:
                    # if the letter input matches that of the text - correctness count increases by 1
                    if self.input_text[i] == c:
                        correct += 1
                except:
                    pass
            # calculation
            self.accuracy = correct/len(self.word)*100

            # calculate words per minute
            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.cpm = self.wpm*5
            self.end = True
            print(self.total_time)

            self.results = "Accuracy:" + str(
                round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm)) + '   Cpm: ' + str(round(self.cpm))

            # reset button
            self.time_img = pygame.image.load('restart.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))
            # screen.blit(self.time_img, (80,320))
            screen.blit(self.time_img, (self.WIDTH/2-75, self.HEIGHT-140))
            self.draw_text(screen, "Click to Restart", self.HEIGHT -
                           70, 26, (255, 30, 30))

            print(self.results)
            pygame.display.update()

    def run(self):
        self.reset_game()
        self.running = True

        while(self.running):
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (0, 40, 700, 135))
            self.screen.blit(self.running_img, (self.movement_val, 60))
            self.screen.blit(self.finish_img, (650, 60))
            pygame.display.update()
            # initialise clock
            clock = pygame.time.Clock()

            # experiment with what these ones do?
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, 650, 50), 2)

            # update the text of user input
            self.draw_text(self.screen, self.input_text,
                           274, 26, (250, 250, 250))

            pygame.display.update()

            # taking in inputs per event
            for event in pygame.event.get():
                # quitting out of game
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                # mouse input
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # clicking the input box starts the game
                    if(x >= 50 and x <= 650 and y >= 250 and y <= 300):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                     # position of reset box
                    if(x >= 310 and x <= 510 and y >= 390 and self.end):
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()

                # pressing down on keyboard
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        # space for a check that happens after everything
                        if event.key == pygame.K_SPACE:
                            # increase the count by one for every keystroke
                            self.char_count += 1
                            # end game if last word is reached on keyboard
                            if self.char_count == len(self.word):
                                print(self.input_text)
                                self.show_results(self.screen)
                                print(self.results)
                                # show the results on the screen
                                self.draw_text(
                                    self.screen, self.results, 350, 28, self.RESULT_C)
                                self.end = True
                            else:
                                try:
                                    self.input_text += event.unicode
                                    if self.input_text[self.char_count] == self.word[self.char_count]:
                                        print("CORRECT")
                                        self.movement_val += (675 /
                                                              self.sentence_length)
                                    else:
                                        print("WRONG")
                                except:
                                    pass

                        # backspace to remove text
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                            self.char_count -= 1
                        # all other keyboard inputs go into the input
                        else:
                            self.char_count += 1
                            # first input is always going to be correct
                            if self.char_count == 0:
                                self.word[self.char_count]
                                self.input_text += event.unicode
                            else:
                                try:
                                    self.input_text += event.unicode
                                    if self.input_text[self.char_count] == self.word[self.char_count]:
                                        print("CORRECT")
                                        self.movement_val += (675 /
                                                              self.sentence_length)
                                    else:
                                        print("WRONG")
                                except:
                                    pass

# next step is to change the text so that it fits into a specific category - consider placing the checker into its own individual function

            pygame.display.update()
        # check what this is
        clock.tick(60)

    def reset_game(self):
        self.reset = False
        self.end = False

        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0
        self.cpm = 0

        self.char_count = -1

        self.movement_val = 0
        self.sentence_length = 0

        # Get random sentence
        self.word = self.get_sentence()
        if (not self.word):
            self.reset_game()

        # drawing heading
        self.screen.fill((0, 0, 0))
        msg = "Type Racing Game"
        self.draw_text(self.screen, msg, 20, 60, self.HEAD_C)
        # draw the rectangle for input box
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)

        # draw the sentence string
        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)

        pygame.display.update()


Game().run()
