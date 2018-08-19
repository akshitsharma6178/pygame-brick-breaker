
import sys
import pygame
import os
SCREEN_SIZE = 1040, 768

BRICK_WIDTH = 60
BRICK_HEIGHT = 15
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 12
BALL_DIAMETER = 20
BALL_RADIUS = int(BALL_DIAMETER / 2)
MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
MAX_BALL_X = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y = SCREEN_SIZE[1] - BALL_DIAMETER

PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10


BACKGROUND= (0, 0, 0)
TEXT_FILL = (255, 255, 255)
BALL_COLOR = (0, 0, 255)
BRICK_COLOR = (200, 200, 0)
red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
brightgreen = (0,255,0)

global flag
global flag2
flag2=1
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3
LEVEL=2

class Library:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Bounce Breaker")

        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = None
        #if flag2==1:
        #self.game_intro()
        self.init_game()



    def init_game(self):
        self.lives = 3
        self.score = 0
        self.state = STATE_BALL_IN_PADDLE

        self.paddle = pygame.Rect(300, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(300, PADDLE_Y - BALL_DIAMETER, BALL_DIAMETER, BALL_DIAMETER)

        self.ball_vel = [12, -12]

        self.create_bricks()

    def create_bricks(self):
        global flag
        if LEVEL == 1 :
            flag=0
            y_ofs = 35
            self.bricks = []
            for i in range(6):
                x_ofs = 35
                for j in range(14):
                    self.bricks.append(pygame.Rect(x_ofs, y_ofs, BRICK_WIDTH, BRICK_HEIGHT))
                    x_ofs += BRICK_WIDTH + 10
                y_ofs += BRICK_HEIGHT + 5
        elif LEVEL == 2 :
            flag =0
            y_ofs = 35
            self.bricks = []
            for i in range(6):
                x_ofs = 35
                for j in range(14):
                    if j%2==0 :
                        self.bricks.append(pygame.Rect(x_ofs, y_ofs, BRICK_WIDTH, BRICK_HEIGHT))
                        x_ofs += BRICK_WIDTH + 90
                y_ofs += BRICK_HEIGHT + 5
        elif LEVEL == 3 :
            flag =0
            y_ofs = 35
            self.bricks = []
            for i in range(6):
                x_ofs = 35
                for j in range(4):
                    if j%2==0:
                        self.bricks.append(pygame.Rect(x_ofs, y_ofs, BRICK_WIDTH, BRICK_HEIGHT))
                        if i%2==0:
                            if j == 0:
                                x_ofs+=BRICK_WIDTH +180
                            x_ofs += BRICK_WIDTH + 90
                        elif i%2!=0 and j==0:
                            x_ofs += BRICK_WIDTH + 180
                y_ofs += BRICK_HEIGHT + 5

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, BRICK_COLOR, brick)



    def check_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.paddle.left -= 15
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            self.paddle.left += 15
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:
            self.ball_vel = [6, -6]
            self.state = STATE_PLAYING
        elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER or self.state == STATE_WON):
            self.init_game()

    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top += self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]

        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= MAX_BALL_Y:
            self.ball.top = MAX_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 3
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                if(self.ball[0]<=20):
                    self.ball_vel[0]+=1
                    self.ball_vel[1]=-self.ball_vel[0]

                break

        if len(self.bricks) == 0:
            self.state = STATE_WON

        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER

    def show_stats(self):
        if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives) + " LEVEL: " + str(LEVEL), False, TEXT_FILL)
            self.screen.blit(font_surface, (400, 5))

    def show_message(self, message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message, False, TEXT_FILL)
            x = (SCREEN_SIZE[0] - size[0]) / 2
            y = (SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x, y))

    def run(self):
        global LEVEL
        global flag
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.clock.tick(50)
            self.screen.fill(BACKGROUND)

            self.check_input()

            if self.state == STATE_PLAYING:
                self.move_ball()
                self.handle_collisions()
            elif self.state == STATE_BALL_IN_PADDLE:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top = self.paddle.top - self.ball.height
                self.show_message("PRESS SPACE TO LAUNCH THE BALL")
            elif self.state == STATE_GAME_OVER:
                self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
            elif self.state == STATE_WON:
                self.show_message("YOU WON! PRESS ENTER TO CONTINUE")
                if (flag == 0):
                    LEVEL += 1
                    print(LEVEL)
                    flag = 2

            self.draw_bricks()

            pygame.draw.rect(self.screen, BALL_COLOR, self.paddle)

            pygame.draw.circle(self.screen, TEXT_FILL, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS),
                               BALL_RADIUS)

            self.show_stats()

            pygame.display.flip()

  #  def button(msg, x, y, w, h, ic, ac, action=None):
   #     gamedisplay=pygame.display.set_mode(SCREEN_SIZE)
    #    mouse = pygame.mouse.get_pos()
     #   click = pygame.mouse.get_pressed()
      #  print(click)
       # if x+w > int(mouse[0]) > x and y + h > int(mouse[1]) > y:
        #    pygame.draw.rect(gamedisplay, ac, (x, y, w, h))

         #   if click[0] == 1 and action != None:
          #      if action==1:
          #          Library().run()
        #3else:
           # pygame.draw.rect(gamedisplay, ic, (x, y, w, h))

        #Library().show_message("Hello")
        #textRect.center = ((x + (w / 2)), (y + (h / 2)))
        #gamedisplay.blit(textSurf, textRect)

    #def game_intro(self):
    #    pygame.init()
     #   intro = True

      #  while intro:
         #   for event in pygame.event.get():
       #         # print(event)
        #        if event.type == pygame.QUIT:
                    #pygame.quit()
                    #quit()

          #  self.screen.fill(BACKGROUND)
            #self.show_message("A bit Racey")
            #TextRect.center = ((display_width / 2), (display_height / 2))
            #gameDisplay.blit(TextSurf, TextRect)
           # Library().button("PLay",150,450,100,50,green,brightgreen,)
 #          Library().button(550, 450, 100, 50, red, bright_red, 2)
#
  #          pygame.display.update()

if __name__ == "__main__":
    Library().run()

