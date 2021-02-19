import pygame
import random
pygame.init()
width=800
height=600
speed=4

scores=0
max_scores=0
max_above=0
above_cactus=False
display=pygame.display.set_mode ((width,height))
pygame.display.set_caption (('DINO'))

pygame.mixer.music.load ("Sounds/background.mp3")

pygame.mixer.music.set_volume (0.3)

jump_sound=pygame.mixer.Sound('Sounds/Rrr.wav')
music=pygame.mixer.Sound('Sounds/point.ogg')
music.set_volume (0.5)
fall_sound=pygame.mixer.Sound('Sounds/Bdish.wav')
loss_sound=pygame.mixer.Sound ('Sounds/loss.wav')
heart_plus_sound=pygame.mixer.Sound ('Sounds/hp+.wav')
button_sound=pygame.mixer.Sound ('Sounds/button.wav')

icon=pygame.image.load ("Backgrounds/icon.png")
cactus_img=[pygame.image.load ('Objects/Cactus0.png'),pygame.image.load ('Objects/Cactus1.png'),pygame.image.load ('Objects/Cactus2.png')]
cactus_options=[69,449,37,410,40,420]
pygame.display.set_icon(icon)

cloud_img=[pygame.image.load ('Objects/cloud0.png'),pygame.image.load ('Objects/Cloud1.png')]
dino_img=[pygame.image.load ('Dino/Dino0.png'),pygame.image.load ('Dino/Dino1.png'),pygame.image.load ('Dino/Dino2.png')]
health_img=pygame.image.load ('Effects/Ruby.png')
health_img=pygame.transform.scale(health_img,(30,30))
health=2

img_count=0
class Object:
    def __init__ (self,x,y,width,image,speed):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.image=image
        self.speed=speed
    def move (self):
        if self.x>=-cactus_width:
            display.blit (self.image,(self.x,self.y))
            #pygame.draw.rect(display,(224,121,31),(self.x,self.y,self.width,self.height))
            self.x-=self.speed
            return True
        else:
            self.x=900+100+random.randrange(-80,60)
            return False
    def return_self (self,radius,y,width,image):
        self.x=radius
        self.y=y
        self.width=width
        self.image=image
        display.blit (self.image,(self.x,self.y))
class Button:
    def __init__(self,width,height,font_size=30):
        self.width=width
        self.height=height
        self.inactive_clr=(13,162,58)
        self.active_clr=(23,204,58)
    def draw(self,x,y,message,action=None,font_size=30):
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        if x<mouse[0]<x+self.width and y<mouse[1]<y+self.height:
            pygame.draw.rect(display,self.active_clr,(x,y,self.width,self.height))
            if click[0]==1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action==quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
        else:
            pygame.draw.rect(display,self.inactive_clr,(x,y,self.width,self.height))
        print_text(message=message,x=x+10,y=y+10,font_size=font_size)

        
usr_width=60
usr_height=100
usr_x=100
usr_y=405

cactus_width=20
cactus_height=70
cactus_x=300
cactus_y=479
clock=pygame.time.Clock()
make_jump=False
jump_count=22
def show_menu():
    menu_bckgr=pygame.image.load('Backgrounds/Menu.png')
    start_btn=Button(288,70)
    quit_btn=Button(120,70)
    show=True
    while show:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit ()
                quit ()
                
        display.blit (menu_bckgr,(0,0))
        start_btn.draw(270,200,"Start Game",start_game,50)
        
        quit_btn.draw(350,300,"quit",quit,50)
        pygame.display.set_icon(icon)
        pygame.display.update()
        clock.tick(60)
def start_game():
    global scores,make_jump,jump_count,usr_y,health
    while game_cycle():
        scores=0
        make_jump=False
        jump_count=22
        usr_y=600-100-95
        health=2
    pygame.display.update()
def game_cycle ():
    pygame.mixer.music.play(-1)
    global make_jump
    run=True
    cactus_arr=[]
    anim_x=4
    creat_cactus_arr(cactus_arr)
    land=pygame.image.load ('Backgrounds/Land.jpg')
    anim=pygame.image.load ('Backgrounds/anim.png')
    
    cloud=open_random()
    heart=Object(width,280,30,health_img,4)
    button=Button(100,50)
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit ()
                quit ()
        
        display.blit (land,(0,0))
        display.blit (anim,(anim_x,500))
        display.blit (anim,(anim_x+800,500))
        anim_x-=8
        if anim_x<=-800:
            anim_x=0
        
        print_text ('scores: '+str(scores),580,10,((0,0,100)))
        draw_arr (cactus_arr)
        move_objects(cloud)
        count_scores(cactus_arr)
        draw_dino()
        key=pygame.key.get_pressed()
        if key [pygame.K_SPACE]:
            make_jump=True
        if key [pygame.K_ESCAPE]:
            pause()
        heart.move()
        hearts_plus(heart)
        if make_jump:
            jump()
            
        if check_collision (cactus_arr):
            pygame.mixer.music.stop()
            run=False
        
        show_health()


        
        pygame.display.update ()
        clock.tick (80)

    return game_over()
def jump():
    global usr_y,jump_count,make_jump
    if jump_count>=-22:
        if jump_count==22:
            pygame.mixer.Sound.play (jump_sound)
        if jump_count==-22:      
            pygame.mixer.Sound.play(fall_sound)
        usr_y-=jump_count
        jump_count-=1
    else:
        jump_count=22
        make_jump=False
def creat_cactus_arr (array):
    choise=random.randrange (0,3)
    img=cactus_img [choise]
    width=cactus_options [choise*2]
    height=cactus_options [choise*2+1]
    array.append (Object(width+600,height,width,img,8))
    
    choise=random.randrange (0,3)
    img=cactus_img [choise]
    width=cactus_options [choise*2]
    height=cactus_options [choise*2+1]
    array.append (Object(width+900,height,width,img,8))

    choise=random.randrange (0,3)
    img=cactus_img [choise]
    width=cactus_options [choise*2]
    height=cactus_options [choise*2+1]
    array.append (Object(width+1400,height,width,img,8))
    
def find_radius (array):
    maximum=max (array[0].x,array [1].x,array [2].x)
    if maximum<width:
        radius=width
        if radius-maximum<50:
            radius+=280
    else:
        radius=maximum
    choise=random.randrange (0,5)
    if choise ==0:
        radius+=random.randrange (10,15)
    else:
        radius +=random.randrange (250,400)
    return radius
def draw_arr (array):
    for cactus in array:
        check=cactus.move ()
        if not check:
            object_return(array,cactus)
def object_return(objects,obj):
    radius=find_radius (objects)
    
    choise=random.randrange(0,3)
    img=cactus_img [choise]
    width=cactus_options [choise*2]
    height=cactus_options [choise*2+1]
    
    obj.return_self(radius,height,width,img)



    
def open_random ():
    choise=random.randrange (0,2)
    img_of_cloud=cloud_img [choise]
    cloud=Object(width,80,70,img_of_cloud,2)
    return cloud
def move_objects (cloud):
    check=cloud.move()
    if not check:
        choise=random.randrange (0,2)
        img_of_cloud=cloud_img[choise]
        cloud.return_self (width,random.randrange(10,200),cloud.width ,img_of_cloud)
def draw_dino():
    global img_count
    if img_count==25:
        img_count=0
    display.blit(dino_img[img_count//9],(usr_x,usr_y))
    img_count+=1
def print_text (message,x,y,font_color=(0,0,0),font_type='PingPong.ttf',font_size=30):
    font_type=pygame.font.Font (font_type,font_size)
    text=font_type.render(message,True,font_color)
    display.blit (text,(x,y))
def pause():
    paussed=True
    pygame.mixer.music.pause()
    while paussed:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit ()
                quit ()
        print_text("PAUSED!",320,300,((0,0,100)))
        print_text ("Press enter to continue",200,350,((0,0,100)))
        key=pygame.key.get_pressed ()
        if key [pygame.K_RETURN]:
            paussed=False
        pygame.display.update()
        clock.tick (15)
    pygame.mixer.music.unpause()



def check_collision (barriers):
    for barrier in barriers:
        if barrier.y==449:#tegelek kaktus
            if not make_jump:
                if barrier.x<=usr_x+usr_width-35<=barrier.x+barrier.width:
                    if check_health():
                        object_return(barriers,barrier)
                        return False
                    else:
                        return True
                elif jump_count>=0:
                    if usr_y+usr_height-5>=barrier.y:
                        if barrier.x<=usr_x+usr_width-40<=barrier.x+barrier.width:
                            if check_health():
                                object_return(barriers,barrier)
                                return False
                            else:
                                return True
                else:
                    if usr_y+usr_height-10>=barrier.y:
                        if barrier.x<=usr_x<=barrier.x+barrier.width:
                            if check_health():
                                object_return(barriers,barrier)
                            return False
                        else:
                            return True
        else:
            if not make_jump:
                if barrier.x<=usr_x+usr_width-5<=barrier.x+barrier.width:
                    if check_health():
                        object_return(barriers,barrier)
                        return False
                    else:
                        return True
            elif jump_count==10:
                if usr_y+usr_height-5>=barrier.y:
                    if barrier.x<=usr_x+usr_width-5<=barrier.x+barrier.width:
                        if check_health():
                            object_return(barriers,barrier)
                            return False
                        else:
                            return True
            elif jump_count>=-1:
                if usr_y+usr_height-5>=barrier.y:
                    if barrier.x<=usr_x+5<=barrier.x+barrier.width:
                        if check_health():
                            object_return(barriers,barrier)
                            return False
                        else:
                            return True
                else:
                    if usr_y+usr_height-10>=barrier.y:
                        if barrier.x<=usr_x+5<=barrier.x+barrier.width:
                            if check_health():
                                object_return(barriers,barrier)
                            return False
                        else:
                            return True
    return False


def count_scores(barriers):
    global scores,max_above
    above_cactus=0
    if -20<=jump_count<25:
        for barrier in barriers:
            if usr_y+usr_height-5<=barrier.y:
                if barrier.x<=usr_x<=barrier.x+barrier.width:
                    above_cactus+=1
                elif barrier.x<=usr_x+usr_width<=barrier.x+barrier.width:
                    above_cactus+=1
        max_above=max(max_above,above_cactus)
    else:
        if jump_count==-22:
            scores+=max_above
            max_above=0
    
def game_over():
    global scores,max_scores
    if scores>max_scores:
        max_scores=scores
        
    stopped=True
    while stopped:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        print_text("Game over!",320,300,((255,0,0)))
        print_text ("Press Enter to play again, Esc to exit",120,350,((0,0,100)))
        print_text("Max scores: "+str(max_scores),300,400,((0,0,100)))
        keys=pygame.key.get_pressed()
        if keys [pygame.K_RETURN]:
            return True
        if keys [pygame.K_ESCAPE]:
            return False
        pygame.display.update()
        clock.tick (15)
def show_health():
    global health
    show=0
    x=20
    while show!=health:
        display.blit(health_img,(x,20))
        x+=40
        show+=1
def check_health():
    global health
    health-=1
    if health==0:
        pygame.mixer.Sound.play(loss_sound)
        return False
    else:
        pygame.mixer.Sound.play(fall_sound)
        return True
def hearts_plus(heart):
    global health,usr_x,usr_y,usr_width,usr_height
    if heart.x<=-heart.width:
        radius=width+random.randrange(580,1780)
        heart.return_self(radius,heart.y,heart.width,heart.image)
    if usr_x<=heart.x<=usr_x+usr_width:
        if usr_y<=heart.y<=usr_y+usr_height:
            pygame.mixer.Sound.play(heart_plus_sound)
            if health<5:
                health+=1
            radius=width+random.randrange(580,1780)
            heart.return_self(radius,heart.y,heart.width,heart.image)
            
show_menu()
pygame.quit()
quit()

