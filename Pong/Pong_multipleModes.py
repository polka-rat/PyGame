import pygame
import time
import random

pygame.init() #Initialising the Pygame environment

with open(r'C:\Users\shand\Personal Projects\Pong\HighScore.txt') as f: #To get the highscore
    high_score = f.read()

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
fps=pygame.time.Clock()
pygame.display.set_caption('Ping')
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#define colours
bg=(127,0,255)
white=(255,255,255)
black=(0,0,0)
grey=(180,180,180)

#define board variables
margin=50
player1_score=0
player2_score=0
player_score=0
live_ball=False
mode_choice=False
mode=0
font1= pygame.font.SysFont('STHupo',30)
font2= pygame.font.SysFont('Comic Sans MS',30)
winner=0
winner2=0

def draw_board():   #To draw the board
    screen.fill(bg)
    pygame.draw.line(screen,white,(0,margin),(SCREEN_WIDTH,margin))
    
def draw_text(text, font1, col, x,y):   #To draw text on the screen
    img = font1.render(text,True,col)
    screen.blit(img,(x,y))
    
class paddle():     #Crating a class for the paddle
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.rect=pygame.Rect((self.x,self.y,20,100))
        self.speed=8
        
    def move(self,up_key,down_key):
        key=pygame.key.get_pressed()
        if key[up_key] and self.rect.top>margin+2 :
            self.rect.move_ip(0,-1*self.speed)
        elif key[down_key] and self.rect.bottom<SCREEN_HEIGHT:
            self.rect.move_ip(0,self.speed)
    
    def draw(self):
        pygame.draw.rect(screen,black,self.rect,border_radius=10)

class ball():       #Creating a class for the ball
    def __init__(self,x,sign,name):
        self.name=name
        self.reset(x,sign)
        
        
    def draw(self):
        pygame.draw.circle(screen,white,(self.rect.x+self.ball_rad,self.rect.y+self.ball_rad),self.ball_rad)
        
    def move(self):
        self.speed_x+=0.001*self.speed_x/abs(self.speed_x)  #Ball slowly gets faster
        self.speed_y+=0.001*self.speed_y/abs(self.speed_y)
        
        state=False #To check if ball bounced
        if self.rect.top<margin or self.rect.bottom>SCREEN_HEIGHT:
            self.speed_y*=-1
         
        if (self.rect.colliderect(player2_paddle) or self.rect.colliderect(player1_paddle) )and (time.time()-self.col_time)>0.5:
            self.speed_x*=-1
            state=True
            self.col_time=time.time()
            
        # if self.name!='pong' and self.rect.colliderect(pong) and (time.time()-self.col_time)>0.5:     #Tried incorporating collision among the two balls 
        #     self.speed_y*=-1                                                                          # Didnt really work out well so dropped it
        #     self.speed_x*=-1
        #     self.col_time=time.time()            

        # if self.name!='pong2' and self.rect.colliderect(pong2) and (time.time()-self.col_time)>0.5:
        #     self.speed_y*=-1
        #     self.speed_x*=-1
        #     self.col_time=time.time()
                               
        self.rect.x+=self.speed_x
        self.rect.y+=self.speed_y
        
        if self.rect.left<0:    #Ball went out the screen
            self.winner=1
        if self.rect.right>SCREEN_WIDTH:
            self.winner=-1
        
        return self.winner,state
    
    def reset(self,x,sign):     #resetting the ball (after it went out)
        self.col_time=0
        self.x=x
        self.y=random.randint(margin,SCREEN_HEIGHT)
        self.ball_rad=8
        self.rect=pygame.Rect((self.x,self.y,self.ball_rad*2,self.ball_rad*2))
        
        if sign==1:     # Making sure that In the Two Balls game mode, the balls go in different directions
            self.speed_x=4*random.choice([-1,1])
            self.speed_y=4*random.choice([-1,1])
        else:
            self.speed_x=2*sign
            self.speed_y=2*sign        
        self.winner=0
            
        

#create paddle
player2_paddle =paddle(SCREEN_WIDTH-40,SCREEN_HEIGHT//2)
player1_paddle =paddle(20,SCREEN_HEIGHT//2)

#create pong
pong=ball(SCREEN_WIDTH//2,1,'pong')
pong2=ball(SCREEN_WIDTH//2,-2*pong.speed_y/abs(pong.speed_y),'pong2')

run=True
while run: 
    fps.tick(60)
    draw_board() 

    #draw paddles
    player2_paddle.draw()
    player1_paddle.draw()
     
    if mode_choice==False:  #Choosing the game mode
        draw_text('PRESS 1 FOR SINGLEPLAYER',font2,white,180,SCREEN_HEIGHT//2-100)
        draw_text('PRESS 2 FOR MULTIPLAYER',font2,white,180,SCREEN_HEIGHT//2-40)
        draw_text('PRESS 3 FOR TWO BALLS',font2,white,180,SCREEN_HEIGHT//2+20)
        
    if mode==2:    #Multiplayer Mode
        draw_text('P1: '+str(player1_score),font1,white,20,15) 
        draw_text('P2: '+str(player2_score),font1,white,SCREEN_WIDTH-100,15)        
        draw_text('Ball Speed: '+str(abs(round(pong.speed_x,2))),font1,white,SCREEN_WIDTH//2-100,15)          
        
        if live_ball==True:
            winner,_ =pong.move()
            
            if winner==0:
                player2_paddle.move(pygame.K_UP,pygame.K_DOWN)
                player1_paddle.move(pygame.K_w,pygame.K_s)
                pong.draw()
            else:
                live_ball=False
                if winner==1:
                    player2_score+=1    #Player 2 got the point
                else:
                    player1_score+=1     #Player 1 got the point
                    
        if live_ball==False:
            if winner==0 and mode_choice:
                draw_text('CLICK ANYWHERE TO START',font2,white,180,SCREEN_HEIGHT//2-100)

            elif winner==1:
                draw_text('PLAYER 2 SKILL BONUS',font2,white,230,SCREEN_HEIGHT//2-100)
                draw_text('CLICK ANYWHERE AGAIN TO RESTART',font2,white,100,SCREEN_HEIGHT//2-50)  #Restarting same game mode
                draw_text('PRESS X FOR MODE SELECT',font2,white,180,SCREEN_HEIGHT//2)    #Going back to mode select
            elif winner==-1:
                draw_text('PLAYER 1 SKILL BONUS',font2,white,230,SCREEN_HEIGHT//2-100)
                draw_text('CLICK ANYWHERE AGAIN TO RESTART',font2,white,100,SCREEN_HEIGHT//2-50) #Restarting same game mode
                draw_text('PRESS X FOR MODE SELECT',font2,white,180,SCREEN_HEIGHT//2)    #Going back to mode select
                
    elif mode==1:  #Single Player Mode
        with open(r'C:\Users\shand\Personal Projects\Pong\HighScore.txt') as f:
            high_score = f.read()  
        draw_text('Current Score: '+str(player_score),font1,white,5,15) 
        draw_text('HighScore: '+str(high_score),font1,white,SCREEN_WIDTH-200,15)        
        draw_text('Ball Speed: '+str(abs(round(pong.speed_x,2))),font1,white,SCREEN_WIDTH//2-100,15)  
        
        if live_ball==True:
            winner,bounce = pong.move()
            if bounce:
                player_score+=1
            if winner==0:
                player2_paddle.move(pygame.K_UP,pygame.K_DOWN)
                player1_paddle.move(pygame.K_w,pygame.K_s)
                pong.draw()
            else:
                live_ball=False
                  
        if live_ball==False:    #Game over
            if winner==0 and mode_choice:
                draw_text('CLICK ANYWHERE TO START',font2,white,180,SCREEN_HEIGHT//2-100)   #Restarting same game mode
                draw_text('PRESS X FOR MODE SELECT',font2,white,180,SCREEN_HEIGHT//2-40)    #Going back to mode select

            else:
                if player_score>int(high_score):
                    f=open(r'C:\Users\shand\Personal Projects\Pong\HighScore.txt','w')
                    f.write(f"{str(player_score)}")
                    f.close()
                    
                draw_text('F OGAYA',font2,white,340,SCREEN_HEIGHT//2-100)
                draw_text(f'YOUR SCORE: {player_score}',font2,white,290,SCREEN_HEIGHT//2-50)
                draw_text(f'HIGH SCORE: {high_score}',font2,white,290,SCREEN_HEIGHT//2)
                draw_text('CLICK ANYWHERE AGAIN TO RESTART',font2,white,100,SCREEN_HEIGHT//2+80)
                draw_text('PRESS X FOR MODE SELECT',font2,white,100,SCREEN_HEIGHT//2+130)
        
    elif mode==3:
        with open(r'C:\Users\shand\Personal Projects\Pong\HighScore_TwoBalls.txt') as f:
            high_score = f.read()  
        draw_text('Current Score: '+str(player_score),font1,white,5,15) 
        draw_text('HighScore: '+str(high_score),font1,white,SCREEN_WIDTH-200,15)        
        draw_text('Ball Speed: '+str(abs(round(pong.speed_x,2))),font1,white,SCREEN_WIDTH//2-100,15)  
        
        if live_ball==True:
            winner,bounce1 = pong.move()
            winner2,bounce2 = pong2.move()
            
            if bounce1:
                player_score+=1
            if bounce2:
                player_score+=1
            if winner==0 and winner2==0:
                player2_paddle.move(pygame.K_UP,pygame.K_DOWN)
                player1_paddle.move(pygame.K_w,pygame.K_s)
                pong.draw()
                pong2.draw()
            else:
                live_ball=False

                    
        if live_ball==False:
            if winner==0 and winner2 ==0 and mode_choice:
                draw_text('CLICK ANYWHERE TO START',font2,white,180,SCREEN_HEIGHT//2-100)
                draw_text('PRESS X FOR MODE SELECT',font2,white,180,SCREEN_HEIGHT//2-40)

            else:
                if player_score>int(high_score):
                    f=open(r'C:\Users\shand\Personal Projects\Pong\HighScore_TwoBalls.txt','w')
                    f.write(f"{str(player_score)}")
                    f.close()
                    
                draw_text('F OGAYA',font2,white,340,SCREEN_HEIGHT//2-100)
                draw_text(f'YOUR SCORE: {player_score}',font2,white,290,SCREEN_HEIGHT//2-50)
                draw_text(f'HIGH SCORE: {high_score}',font2,white,290,SCREEN_HEIGHT//2)
                draw_text('CLICK ANYWHERE AGAIN TO RESTART',font2,white,100,SCREEN_HEIGHT//2+80)
                draw_text('PRESS X FOR MODE SELECT',font2,white,100,SCREEN_HEIGHT//2+130)

    
    
    for event in pygame.event.get():
        key=pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.MOUSEBUTTONDOWN and mode_choice and live_ball==False:
            live_ball=True
            player_score=0
            pong.reset(SCREEN_WIDTH//2,1)
            pong2.reset(SCREEN_WIDTH//2,-2*pong.speed_x/abs(pong.speed_y))
            
        if key[pygame.K_x] and not live_ball:#Going back to mode select
            mode_choice=False
            winner=0
            mode=0
            
        if not mode_choice:
            if key[pygame.K_1]:
                mode_choice=True
                mode=1
            elif key[pygame.K_2]:
                mode_choice=True
                mode=2
            elif key[pygame.K_3]:
                mode_choice=True
                mode=3
            
    
    pygame.display.update()
    
    

pygame.quit()