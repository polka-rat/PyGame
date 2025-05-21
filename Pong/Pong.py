import pygame
import time

pygame.init() # Initialising the pygame environment

with open(r'C:\Users\shand\Personal Projects\Pong\HighScore.txt') as f:
    score = f.read()

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
fps=pygame.time.Clock()
pygame.display.set_caption('Pong')
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
live_ball=False
font1= pygame.font.SysFont('STHupo',30)
font2= pygame.font.SysFont('Comic Sans MS',30)

winner=0
winner2=0

def draw_board():
    screen.fill(bg)
    pygame.draw.line(screen,white,(0,margin),(SCREEN_WIDTH,margin))
    
def draw_text(text, font1, col, x,y):
    img = font1.render(text,True,col)
    screen.blit(img,(x,y))
    
class paddle():
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
        pygame.draw.rect(screen,grey,self.rect,border_radius=10)

class ball():
    def __init__(self,x,y):
        self.reset(x,y)
        
    def draw(self):
        pygame.draw.circle(screen,white,(self.rect.x+self.ball_rad,self.rect.y+self.ball_rad),self.ball_rad)
        
    def move(self,player2,player1,count):
        self.speed_x+=0.001*self.speed_x/abs(self.speed_x)
        self.speed_y+=0.001*self.speed_y/abs(self.speed_y)
        
        if self.rect.top<margin or self.rect.bottom>SCREEN_HEIGHT:
            self.speed_y*=-1
         
        if (self.rect.colliderect(player2_paddle) or self.rect.colliderect(player1_paddle) )and (time.time()-self.col_time)>0.5:
            self.speed_x*=-1
            self.col_time=time.time()
           
        self.rect.x+=self.speed_x
        self.rect.y+=self.speed_y
        
        if self.rect.left<0:
            self.winner=1
        if self.rect.right>SCREEN_WIDTH:
            self.winner=-1
        
        return self.winner
    
    def reset(self,x,y):
        self.col_time=0
        self.x=x
        self.y=y
        self.ball_rad=8
        self.rect=pygame.Rect((self.x,self.y,self.ball_rad*2,self.ball_rad*2))
        self.speed_x=-4
        self.speed_y=4
        self.winner=0
            
        

#create paddle
player2_paddle =paddle(SCREEN_WIDTH-40,SCREEN_HEIGHT//2)
player1_paddle =paddle(20,SCREEN_HEIGHT//2)

#create pong
pong=ball(0,SCREEN_HEIGHT//2+50)

player2=pygame.Rect((300,250,50,50))
run=True
count=0
while run: 
    fps.tick(60)
    draw_board() 
     
    draw_text('P1: '+str(player1_score),font1,white,20,15) 
    draw_text('P2: '+str(player2_score),font1,white,SCREEN_WIDTH-100,15)        
    draw_text('Ball Speed: '+str(abs(round(pong.speed_x,2))),font1,white,SCREEN_WIDTH//2-100,15)  
    # pygame.draw.rect(screen,(255,0,0),player2)
    
    # key=pygame.key.get_pressed()
    # if key[pygame.K_a]:
    #     player2.move_ip(-1,0)
    # if key[pygame.K_w]:
    #     player2.move_ip(0,-1)
    # if key[pygame.K_d]:
    #     player2.move_ip(1,0)
    # if key[pygame.K_s]:
    #     player2.move_ip(0,1)
    
    #draw paddles
    player2_paddle.draw()
    player1_paddle.draw()
    
    if live_ball==True:
        winner =pong.move((player2_paddle.rect.top,player2_paddle.rect.bottom,player2_paddle.x),(player1_paddle.rect.top,player1_paddle.rect.bottom,player1_paddle.x),count)
        if winner==0:
            player2_paddle.move(pygame.K_UP,pygame.K_DOWN)
            player1_paddle.move(pygame.K_w,pygame.K_s)
            pong.draw()
        else:
            live_ball=False
            if winner==1:
                player2_score+=1
            else:
                player1_score+=1
                
    if live_ball==False:
        if winner==0:
            draw_text('CLICK ANYWHERE TO START',font2,white,180,SCREEN_HEIGHT//2-100)
        elif winner==1:
            draw_text('PLAYER 2 SKILL BONUS',font2,white,230,SCREEN_HEIGHT//2-100)
            draw_text('CLICK ANYWHERE AGAIN TO RESTART',font2,white,100,SCREEN_HEIGHT//2-50)
        else:
            draw_text('PLAYER 1 SKILL BONUS',font2,white,230,SCREEN_HEIGHT//2-100)
            draw_text('CLICK ANYWHERE AGAIN TO RESTART',font2,white,100,SCREEN_HEIGHT//2-50)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball==False:
            live_ball=True
            pong.reset(SCREEN_WIDTH -60,SCREEN_HEIGHT//2+50)
    
    count+=1
    pygame.display.update()
    
    

pygame.quit()