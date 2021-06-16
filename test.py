import pygame
from pygame.locals import *
import sys
import time
import random

class Game:
    # Constructor to define all the variables:
    def __init__(self):
        self.width=750
        self.height=500
        self.reset=True
        self.active = False
        self.input_text=''
        self.word = ''
        self.start_time = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.result = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.Header_color = (255,255,255)
        self.Text_color = (200,200,200)
        self.Result_Color = (250,250,0)

        pygame.init()
        self.main_img = pygame.image.load('type-speed-open.png')
        self.main_img = pygame.transform.scale(self.main_img, (self.width,self.height))

        self.background = pygame.image.load('bg1.png')
        self.background = pygame.transform.scale(self.background,(750,500))

        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption('Typing Speed test')

    def draw_text(self, screen, msg, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)            #1 is an antialias argument for smooth edges of the characters.
        text_rect = text.get_rect(center=(self.width/2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def random(self):
        f = open('Sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def show_results(self, screen):
        if(not self.end):
            #Calculate time
            self.total_time = time.time() - self.start_time

            #Calculate accuracy
            count = 0
            for i,c in enumerate(self.word):
#enumerate() method adds a counter to an iterable and returns it in a form of enumerate object which can be used directly in
#for loops or be converted into a list of tuples using list() method.
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.word)*100

            #Calculate words per minute
            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)

            self.results = 'Time: '+str(round(self.total_time)) +"sec; Accuracy: "+ str(round(self.accuracy)) + "%;" + ' Wpm: ' + str(round(self.wpm))

            # draw icon image
            self.reset_img = pygame.image.load('RESET2.png')
            self.reset_img = pygame.transform.scale(self.reset_img, (75,75))
            #screen.blit(self.reset_img, (80,320))
            screen.blit(self.reset_img, (self.width/2-30,self.height-100))
          #  self.draw_text(screen,"Reset", self.h - 70, 26, (0,0,0))

            print(self.results)
            pygame.display.update()

    def run(self):
        self.count = 0
        self.reset_game()
        self.running=True
        while(self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0,0,0), (50,250,650,50))
            pygame.draw.rect(self.screen,self.Header_color, (50,250,650,50),2)
            # update the text of user input
            self.draw_text(self.screen, self.input_text, 274, 26,(250,250,250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    # position of input box
                    if(x>=50 and x<=650 and y>=250 and y<=300):
                        self.active = True
                        self.input_text = ''
                        self.start_time = time.time()
                     # position of reset box
                    if(x>=345 and x<=420 and y>=400 and y<=475):
                        self.reset_game()
                        x,y = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results,350, 28, self.Result_Color)
                            self.end = True

                        elif event.key == pygame.K_BACKSPACE:
                            self.count+=1
                            if self.count==4:
                                print("Please try again...")
                                self.draw_text(self.screen,"You can't use backspace key more than 3 times." , 350, 28, (255,255,255))
                                self.draw_text(self.screen,"Please try again with the new sentence." , 375, 28, (255,255,255))
                                self.show_results(self.screen)
                            else:
                                self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass

            pygame.display.update()
        clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.main_img, (0,0))

        pygame.display.update()
        time.sleep(1)

        self.reset=False
        self.end = False

        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0
        self.count=0

        # Get random sentence
        self.word = self.random()
        if (not self.word): self.reset_game()
        #drawing heading
        self.screen.fill((0,0,0))
        self.screen.blit(self.background,(0,0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen,msg,80, 80,self.Header_color)
        # draw the rectangle for input box
        pygame.draw.rect(self.screen,(255,192,25), (50,250,650,50), 2)
        # draw the sentence string
        self.draw_text(self.screen, self.word,200, 28,self.Text_color)

        pygame.display.update()

Game().run()