import pygame
import random
from math import *

BLACK = (0,0,0)
WHITE = (255,255,255)
colors = [(0,0,0),(255,0,0),(0,255,0),(0,0,255)]
SKY = (0, 0, 100)
GROUND = (200, 200, 100)
map = ''

walls = {
    "1": pygame.image.load("wall1.png"),
    "2": pygame.image.load("brks_1.png"),
    "3": pygame.image.load("brks_2.png"),
}

enemies = [
  {
    "x": 250,
    "y": 250,
    "texture": pygame.image.load('enemy.png')
  },
]


class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.blocksize = 50
        self.map = []
        self.player = {
            "x": int(self.blocksize + self.blocksize/2),
            "y": int(self.blocksize + self.blocksize/2),
            "fov": int(pi/3),
            "a": int(pi/3)

        }

        self.minimap = {
            "x": int(15), 
            "y": int(15)
        }
        self.temp = {
            "x": 0,
            "y": 0
        }


    def point(self, x,y,c = WHITE):
        self.screen.set_at((x,y),c)

    def block(self,x,y,c=WHITE):
        for i in range(0,10):
            for j in range(0,10):
                self.point(i+10*x,j+10*y,(100,100,100))
    def goal(self):
        for i in range(0,10):
            for j in range(0,10):
                if map == "map.txt":
                    self.point(i+80,j+80,(150,150,150))
                if map == "map2.txt":
                    self.point(i+10,j+80,(150,150,150))
                if map == "map3.txt":
                    self.point(i+80,j+10,(150,150,150))


    def load_map(self, filename):
        with open(filename, "r") as f:
            x = f.readlines()
            for line in x:
                self.map.append(list(line))

    def draw_map(self):
        for x in range(0,500,self.blocksize):
            for y in range(0,500,self.blocksize):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                if self.map[j][i] != ' ':

                    self.block(i,j, colors[int(self.map[j][i])])

    def draw_player(self):
        self.point(self.minimap["x"], self.minimap["y"])
        

    def draw_stake(self, x, h, tx, intensity=1):
        start_y = int(self.height/2 - h/2)
        end_y = int(self.height/2 + h/2)
        height = end_y - start_y

        for y in range(start_y, end_y):
            ty  = int((y-start_y)*128/height)
            c = walls["1"].get_at((tx,ty))
            if map == "map.txt" or map == "map2.txt":
                newcolor = (min(250,c[0]+intensity),min(c[1]+intensity,250),min(c[2]+intensity,250))
            else:
                newcolor = (min(250,c[0]+intensity),min(c[1]+intensity,50),min(c[2]+intensity,50))
            self.point(x,y,newcolor)
        

    def cast_ray(self,a):
        d = 0
        ox = self.player["x"]
        oy = self.player["y"]
        while True:
            x = int(ox + d*cos(a))
            y = int(oy + d*sin(a))

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x - i*self.blocksize
                hity = y - j*self.blocksize
                if 1 < hitx<self.blocksize-1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit*128/self.blocksize)
                return d, self.map[j][i], tx  
            
            d+=1
    def draw_sprite(self, sprite, intensity=1):
        sprite_a = atan2(sprite["y"]-self.player["y"],sprite["x"]-self.player["x"])
        
        d = ((self.player["x"] -sprite["x"])**2 + (self.player["y"]-sprite["y"])**2)**0.5        
        sprite_size = int(500/d + 500/10)
        sprite_x = int(250 + (sprite_a - self.player["a"]) * 500/self.player["fov"] + sprite_size/2)
        sprite_y = 250

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                    tx = int((x - sprite_x) * 128/sprite_size)
                    ty = int((y - sprite_y) * 128/sprite_size)
                    c = sprite["texture"].get_at((tx, ty))
                    if map == "map.txt" or map == "map.txt":
                        newcolor = (min(250,c[0]+intensity),min(c[1]+intensity,250),min(c[2]+intensity,250))
                    else:
                        newcolor = (min(250,c[0]+intensity),min(c[1]+intensity,50),min(c[2]+intensity,50))
                    self.point(x, y, newcolor)
    def render(self):



        for i in range(0, int(self.width)):
            a = self.player["a"] - self.player["fov"]/2 + self.player["fov"]*i/int(self.width)
            d, c, tx = self.cast_ray(a)
            if d == 0:
                self.player["x"] = self.temp["x"]
                self.player["y"] = self.temp["y"]

                d, c, tx = self.cast_ray(a)
                print(d)
                 
            x = i
            h = self.height/(d* cos(a -self.player["a"]))*self.height/10
            ty = 0
            c = walls[c].get_at((tx,ty))
            for j in range(0, int(self.height)):
                if map == "map.txt" or map == "map2.txt":
                    if j > 300:
                        self.point(i,j, (min(250,255-(j-350)),min(250,255-(j-350)),min(250,255-(j-350))))
                    else:
                        self.point(i,j, (min(250,0+j*2),min(250,0+j*2),min(250,100+j*2)))
                else:
                    if j > 300:
                        self.point(i,j, (min(250,255-(j-350)),min(50,255-(j-350)),min(50,255-(j-350))))
                    else:
                        self.point(i,j, (min(250,0+j*2),min(50,0+j*2),min(20,100+j*2)))
            
            self.draw_stake(x, h, tx, intensity= d if d < 100 else 9*d/8)

        screen.fill(BLACK, (0,0, r.width/5, r.height/5))
        self.draw_map()
        self.goal()
        self.draw_player()

            

                
            

pygame.init()
font_name = '8-BIT WONDER.TTF'
#font_name = pygame.font.get_default_font()
screen = pygame.display.set_mode((500,500))
r = Raycaster(screen)
walking = pygame.mixer.Sound("Walking.wav")
music = pygame.mixer.music.load("SummerSnow.mp3")

clock = pygame.time.Clock()
pygame.display.flip()


# white color 
color = (255,255,255) 
smallfont = pygame.font.SysFont('Corbel',35) 
bigfont = pygame.font.SysFont('Sylfaen',50) 
# rendering a text written in 
# this font 
text1 = smallfont.render('Level 1', True , color) 
text2 = smallfont.render('Level 2', True , color) 
text3 = smallfont.render('Level 3', True , color) 
text4 = bigfont.render("Escapa de la niebla...", True, color)
text5 = bigfont.render("¿Escapaste, pero ", True, color)
text6 = bigfont.render("puedes con los otros?", True, color)
def result():
    running = True
    while running:
        screen.fill((150,150,150), (0,0, r.width, r.height))
        

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False
        screen.blit(text5, (width/2-200,height/2-40))
        screen.blit(text6, (width/2-180,height/2))
        pygame.display.update() 

def main():
    running = True
    pygame.mixer.music.play(-1)
    while running:
        screen.fill(BLACK, (0,0, r.width/2, r.height))
        screen.fill(SKY, (r.width/2,0, r.width, r.height/2))
        screen.fill(GROUND, (r.width/2,r.height/2, r.width, r.height/2))
        r.render()
        pygame.display.flip()
        clock.tick(60)
        print("FPS:" + str(clock.get_fps()))
        

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False

            if(event.type == pygame.KEYDOWN):
                walking.play()
                if event.key == pygame.K_d:
                    r.player["a"] += pi/10
                if event.key == pygame.K_a:
                    r.player["a"] -= pi/10
                
                if event.key == pygame.K_RIGHT:
                    r.temp["x"] = r.player["x"]
                    r.player["x"] += 15
                    r.minimap["x"] += 3
                if event.key == pygame.K_LEFT:
                    r.temp["x"] = r.player["x"]
                    r.player["x"] -= 15
                    r.minimap["x"] -= 3
                if event.key == pygame.K_UP:
                    r.temp["y"] = r.player["y"]
                    
                    r.player["y"] -= 15
                    r.minimap["y"] -= 3
                if event.key == pygame.K_DOWN:
                    r.temp["y"] = r.player["y"]
                    r.player["y"] += 15
                    r.minimap["y"] += 3
        if (r.player["x"] >= 400 and r.player["x"] < 450) and (r.player["y"] >= 400 and r.player["y"] < 450) and map == "map.txt":
            screen.fill(BLACK, (0,0, r.width, r.height))
            running = False
            pygame.mixer.music.stop()
            result()
        if (r.player["x"] >= 50 and r.player["x"] < 100) and (r.player["y"] >= 400 and r.player["y"] < 450) and map == "map2.txt":
            screen.fill(BLACK, (0,0, r.width, r.height))
            running = False
            pygame.mixer.music.stop()
            result()
        if (r.player["x"] >= 400 and r.player["x"] < 450) and (r.player["y"] >= 50 and r.player["y"] < 100) and map == "map3.txt":
            screen.fill(BLACK, (0,0, r.width, r.height))
            running = False
            pygame.mixer.music.stop()
            result()
            

        mouse_position = pygame.mouse.get_pos()
        if mouse_position[0] < 167:
            r.player["a"] -= pi/20
        elif mouse_position[0] > (500-167):
            r.player["a"] += pi/20

res = (500,500) 
  
# opens up a window 
screen = pygame.display.set_mode(res) 
  

  
# light shade of the button 
color_light = (170,170,170) 
  
# dark shade of the button 
color_dark = (100,100,100) 
  
# stores the width of the 
# screen into a variable 
width = screen.get_width() 
  
# stores the height of the 
# screen into a variable 
height = screen.get_height() 
  
# defining a font 
m = True
print("\n\n\n")
print("Instrucciones: ")
print("Muevete hasta poder escapar la niebla que no te permite ver.")
print("Utiliza las flechas del teclado para poder moverte, y a y d para mover la cámara.")
print("También puedes utilizar el mouse para mover la cámara, solo gire hacia el borde de la ventana.")
while m: 
      
    for ev in pygame.event.get(): 
          
        if ev.type == pygame.QUIT: 
            pygame.quit() 
              
        #checks if a mouse is clicked 
        if ev.type == pygame.MOUSEBUTTONDOWN: 
              
            #if the mouse is clicked on the 
            # button the game is terminated 
            if width/2-70 <= mouse[0] <= width/2+70 and height/2 <= mouse[1] <= height/2+40:
                map = 'map.txt'
                r.load_map(map) 
                main()
                m = False
            elif width/2-70 <= mouse[0] <= width/2+70 and height/2+50 <= mouse[1] <= height/2+40+50:
                map = 'map2.txt'
                r.load_map(map) 
                main()
                m = False
            elif width/2-70 <= mouse[0] <= width/2+70 and height/2+100 <= mouse[1] <= height/2+40+100:
                map = 'map3.txt'
                r.load_map(map)  
                main()
                m = False
                  
    # fills the screen with a color 
    screen.fill((100,00,00)) 
      
    # stores the (x,y) coordinates into 
    # the variable as a tuple 
    mouse = pygame.mouse.get_pos() 
      
    # if mouse is hovered on a button it 
    # changes to lighter shade 
    if width/2-70 <= mouse[0] <= width/2-70+140 and height/2 <= mouse[1] <= height/2+40: 
        pygame.draw.rect(screen,color_light,[width/2-70,height/2,140,40])
        pygame.draw.rect(screen,color_dark,[width/2-70,height/2+50,140,40])
        pygame.draw.rect(screen,color_dark,[width/2-70,height/2+100,140,40])
    elif width/2-70 <= mouse[0] <= width/2-70+140 and height/2+50 <= mouse[1] <= height/2+40+50: 
        pygame.draw.rect(screen,color_dark,[width/2-70,height/2,140,40])
        pygame.draw.rect(screen,color_light,[width/2-70,height/2+50,140,40])
        pygame.draw.rect(screen,color_dark,[width/2-70,height/2+100,140,40])
    elif width/2-70 <= mouse[0] <= width/2-70+140 and height/2+100 <= mouse[1] <= height/2+40+100: 
        pygame.draw.rect(screen,color_dark,[width/2-70,height/2,140,40])
        pygame.draw.rect(screen,color_dark,[width/2-70,height/2+50,140,40])
        pygame.draw.rect(screen,color_light,[width/2-70,height/2+100,140,40])
    else: 
        pygame.draw.rect(screen,color_dark,[width/2-70,height/2,140,40])
        pygame.draw.rect(screen,color_dark,[width/2-70,height/2+50,140,40])
        pygame.draw.rect(screen,color_dark,[width/2-70,height/2+100,140,40])

      
    # superimposing the text onto our button 
    screen.blit(text1 , (width/2-45,height/2)) 
    screen.blit(text2 , (width/2-45,height/2+50)) 
    screen.blit(text3 , (width/2-45,height/2+100)) 
    screen.blit(text4 , (width/2-200,height/2-100)) 

      
    # updates the frames of the game 
    pygame.display.update() 



            

        
