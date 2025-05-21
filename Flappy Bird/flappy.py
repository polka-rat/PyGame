import pygame
import random
import time

with open(r'C:\Users\shand\Personal Projects\Flappy Bird\HighScore_flap.txt') as f: #To get the highscore
    high_score = f.read()
    
pygame.init()
SCREEN_WIDTH=550
SCREEN_HEIGHT=660
fps=pygame.time.Clock()
pygame.display.set_caption('Flappy Bird')
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

font1= pygame.font.SysFont('STHupo',30)
font2= pygame.font.SysFont('Bauhaus',80)
font3= pygame.font.SysFont('Comic Sans MS',30)

#define colours
bg=(102,178,255)
white=(255,255,255)
black=(0,0,0)
grey=(180,180,180)
brown=(255,204,153)

#define game variables
bg_img=pygame.image.load(r"C:\Users\shand\Personal Projects\Flappy Bird\sky.png")
grnd_img=pygame.image.load(r"C:\Users\shand\Personal Projects\Flappy Bird\ground.png")
pipe_img=pygame.image.load(r"C:\Users\shand\Personal Projects\Flappy Bird\pipe.png")
res_img=pygame.image.load(r"C:\Users\shand\Personal Projects\Flappy Bird\restart.png")
grnd_scroll=0
scroll_speed=4

def draw_board():   #To draw the board
    screen.blit(bg_img,(0,-100))
    screen.blit(grnd_img,(grnd_scroll,SCREEN_HEIGHT-100))
    
    if not game_over:
        grnd_scroll-=scroll_speed
    # rec=pygame.Rect((0,SCREEN_HEIGHT-100,SCREEN_WIDTH,100))
    # pygame.draw.rect(screen,brown,rec)
    # pygame.draw.line(screen,white,(0,margin),(SCREEN_WIDTH,margin))
    
def draw_text(text, fon, col, x,y):   #To draw text on the screen
    img = fon.render(text,True,col)
    screen.blit(img,(x,y))
    
class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.time_ini=time.time()
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for i in range(1,4):
            self.images.append(rf"C:\Users\shand\Personal Projects\Flappy Bird\bird{i}.png")
        self.image=pygame.image.load(self.images[self.index])
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=0
        self.clicked=False
        self.flag=0
        self.ti=0
        
    def update(self):
        self.counter+=1
        flapCooldown=10
        if self.counter==flapCooldown:
            self.index+=1
            self.counter=0
            if self.index==3:
                self.index=0
        self.image=pygame.image.load(self.images[self.index])
        
        if not game_over:
            if flying:
                if self.vel>8:
                    self.vel=8
                if self.rect.bottom < SCREEN_HEIGHT-100 :
                    self.vel+=0.3
                    self.rect.y+=int(self.vel)
                    self.image=pygame.transform.rotate(self.image,self.vel*-5)
                elif self.vel<0:
                    self.rect.y+=int(self.vel)
                
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    self.vel = -7
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
                
                # print(self.vel)
                
                
            else:
                self.time_ini=time.time()
        
        else:
            self.image=pygame.transform.rotate(self.image,-90)
            if self.rect.y<SCREEN_HEIGHT-130:
                if self.flag==0:
                    di=pygame.sprite.groupcollide(bird_group,pipe_group,False,False)
                    try:
                        pipe=list(di.items())[0][1][0]
                        bird=list(di.items())[0][0]
                        
                        if(abs(pipe.rect.bottomleft[0]-bird.rect.topright[0])<10):
                            if(pipe.rect.topright[1]<0):
                                self.flag=1
                            else:
                                self.flag=2
                        else:
                            if(pipe.rect.topright[1]<0):
                                self.flag=3
                                self.ti=time.time()
                            else:
                                self.flag=4
                    except IndexError:
                        pass
                elif self.flag==3:
                    if time.time()-self.ti<0.1 or not pygame.sprite.groupcollide(bird_group,pipe_group,False,False):
                        self.rect.y+=4
                if self.flag!=3 and self.flag!=4:
                    self.rect.y+=4
                
                
        
            

bird_group=pygame.sprite.Group()
flap=Bird(100,SCREEN_HEIGHT//2)
bird_group.add(flap)

pipe_group=pygame.sprite.Group()
pipe_gap=150
pipe_frequency=1500
last_pipe = pygame.time.get_ticks() - pipe_frequency

score=0
di={}

class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
    
    def draw(self):
        action=False
        pos=pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                action=True
        
        screen.blit(self.image,(self.rect.x,self.rect.y))
        
        return action
    
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pipe_img
        self.rect=self.image.get_rect()
        
        self.passed=False
        #position 1 -> top -1 -> bottom
        if position==1:
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft =[x,y-int(pipe_gap/2)]
        
        else:
            self.rect.topleft=[x,y+int(pipe_gap/2)]
            
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right<0:
            self.kill()

def reset_game():
    global score
    pipe_group.empty()
    bird_group.empty()
    flap=Bird(100,SCREEN_HEIGHT//2)
    bird_group.add(flap)
    # flying=False
    game_over=False
    score=0       

button=Button(SCREEN_WIDTH//2-50,500,res_img)

write_action=True
      
run=True
game_over=False
flying = False
while run: 
    
    fps.tick(55)
    # print(game_over,flying)
    screen.fill(bg)
    pipe_group.draw(screen)
     
    screen.blit(grnd_img,(grnd_scroll,SCREEN_HEIGHT-100))
    if not game_over:
        grnd_scroll-=scroll_speed
        if abs(grnd_scroll)>35:
            grnd_scroll=0
        
    bird_group.draw(screen)
    bird_group.update()
    
    #check score
    for i in pipe_group.sprites():
        if i.rect.left<100 and i.passed==False:
            score+=0.5
            i.passed=True
    #collision
    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) :
        game_over=True
        flying=False
        
    # pipe1 = pipe_img.get_rect()
    # screen.blit(pygame.transform.flip(pipe_img, False, True), pipe1)
    if game_over==False and flying ==True:
        time_now=pygame.time.get_ticks()        
        if time_now-last_pipe>pipe_frequency:
            pipe_height=random.randint(-120,120)
            btm_pipe=Pipe(SCREEN_WIDTH,int(SCREEN_HEIGHT//2)+pipe_height,-1) 
            top_pipe=Pipe(SCREEN_WIDTH,int(SCREEN_HEIGHT//2)+pipe_height,1)  
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe=time_now
            
        bird_group.update()
        pipe_group.update()
        
    if game_over:
        if score>int(high_score) and write_action:
            f=open(r'C:\Users\shand\Personal Projects\Flappy Bird\HighScore_flap.txt','w')
            f.write(f"{str(int(score))}")
            f.close()
            write_action=False
            high_score=score
        act=button.draw()
        if act:
            reset_game()
            game_over=False
        
    for event in pygame.event.get():
        keys = pygame.key.get_pressed() 
        if event.type == pygame.QUIT or keys[pygame.K_q]:
            run = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN and not flying and game_over == False:
            flying = True

        # Checking for 'Q' key to quit
        
    draw_text(f"{int(score)}",font2,white,SCREEN_WIDTH//2,50)
    draw_text(f"HS: { int(high_score)}",font1,black,20,20)
    pygame.display.update()
    
pygame.event.clear()
pygame.quit()
