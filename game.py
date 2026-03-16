import pygame
import sys
import math

pygame.init()

# -------------------------
# WINDOW SETTINGS
# -------------------------

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Why Am I Angry Today?")

icon = pygame.image.load("Game Images/icon.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

# -------------------------
# COLORS / FONTS
# -------------------------

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (70,100,220)
HOVER_BLUE = (110,140,255)

font = pygame.font.SysFont("arial",28,bold=True)
small_font = pygame.font.SysFont("arial",22)
title_font = pygame.font.SysFont("arial",64,bold=True)

TEXT_BOX_BG = (0,0,0,180)

# -------------------------
# ASSETS
# -------------------------

asset_map = {

    "bg_livingroom":{"file":"Game Images/backgroundLight.png"},
    "bg_couch":{"file":"Game Images/backgroundDark.png"},
    "bg_bedroom":{"file":"Game Images/bedroom.png"},

    "char_neutral":{"file":"Game Images/charNeutral.png"},
    "char_angry":{"file":"Game Images/charAngry.png"},
    "char_furious":{"file":"Game Images/charAngry.png"},
    "char_happy":{"file":"Game Images/charHappy.png"},

    "none":None
}

loaded_assets = {}

def load_assets():

    for name,data in asset_map.items():

        if data is None:
            continue

        try:

            img = pygame.image.load(data["file"]).convert_alpha()

            if name.startswith("bg"):
                img = pygame.transform.scale(img,(WIDTH,HEIGHT))

            else:

                max_height = 420
                scale = max_height / img.get_height()

                new_w = int(img.get_width()*scale)
                new_h = int(img.get_height()*scale)

                img = pygame.transform.smoothscale(img,(new_w,new_h))

            loaded_assets[name] = img

        except:

            surf = pygame.Surface((WIDTH,HEIGHT) if name.startswith("bg") else (300,400))
            surf.fill((200,200,200))

            txt = small_font.render(name,True,BLACK)
            surf.blit(txt,(20,20))

            loaded_assets[name] = surf

load_assets()

# -------------------------
# BUTTON CLASS
# -------------------------

class Button:

    def __init__(self,text,x,y,w,h,target):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text
        self.target = target

    def draw(self,surface,mouse):

        color = HOVER_BLUE if self.rect.collidepoint(mouse) else BLUE
        pygame.draw.rect(surface,color,self.rect,border_radius=8)

        label = small_font.render(self.text,True,WHITE)
        rect = label.get_rect(center=self.rect.center)

        surface.blit(label,rect)

    def clicked(self,mouse,event):
        return event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and self.rect.collidepoint(mouse)

# -------------------------
# STORY DATA
# -------------------------

scenes = {

"title":{

    "texts":[""],
    "type":"menu",
    "bg":"bg_livingroom",
    "char":"none"
},

"intro":{

    "texts":[
        "You come home after a long day...",
        "Your girlfriend looks angry.",
        "(Click to continue)"
    ],

    "type":"story",
    "next":"ask",
    "bg":"bg_livingroom",
    "char":"char_angry"
},

"ask":{

    "texts":[
        "You: Hey... why are you angry?",
        "(Click)"
    ],

    "type":"story",
    "next":"nothing",
    "bg":"bg_livingroom",
    "char":"char_angry"
},

"nothing":{

    "texts":[
        "Her: Nothing.",
        "(She is clearly lying)",
        "(Click to guess)"
    ],

    "type":"story",
    "next":"guess",
    "bg":"bg_livingroom",
    "char":"char_angry"
},

"guess":{

    "texts":[
        "You try to guess the reason..."
    ],

    "type":"choice",

    "choices":[
        {"text":"Forgot anniversary","next":"anniversary"},
        {"text":"Liked another girl's post","next":"post"},
        {"text":"Because I exist","next":"exist"}
    ],

    "bg":"bg_livingroom",
    "char":"char_neutral"
},

"anniversary":{

    "texts":[
        "Her: IT'S IN MARCH!",
        "YOU DON'T EVEN KNOW?!",
        "She is furious."
    ],

    "type":"story",
    "next":"game_over",
    "bg":"bg_livingroom",
    "char":"char_furious"
},

"post":{

    "texts":[
        "Her: WOW.",
        "JUST WOW.",
        "She starts crying."
    ],

    "type":"story",
    "next":"game_over",
    "bg":"bg_livingroom",
    "char":"char_furious"
},

"exist":{

    "texts":[
        "Her: ...",
        "She tries not to laugh.",
        "She smirks."
    ],

    "type":"story",
    "next":"good",
    "bg":"bg_livingroom",
    "char":"char_happy"
},

"game_over":{

    "texts":[
        "Tonight's sleeping arrangement:",
        "THE COUCH",
        "GAME OVER"
    ],

    "type":"story",
    "next":"intro",
    "bg":"bg_couch",
    "char":"none"
},

"good":{

    "texts":[
        "Crisis Averted.",
        "You get to sleep in the bed!"
    ],

    "type":"story",
    "next":"intro",
    "bg":"bg_bedroom",
    "char":"char_happy"
}

}

# -------------------------
# TEXT ANIMATION
# -------------------------

anim = {
"line":0,
"char":0,
"display":[],
"finished":False,
"last":0,
"speed":30
}

def reset_anim(scene):

    anim["line"]=0
    anim["char"]=0
    anim["display"]=[""]*len(scene["texts"])
    anim["finished"]=False
    anim["last"]=pygame.time.get_ticks()

def complete_anim(scene):

    anim["display"]=scene["texts"].copy()
    anim["finished"]=True

# -------------------------
# GAME STATE
# -------------------------

current_scene="title"
active_buttons=[]

reset_anim(scenes[current_scene])

# -------------------------
# MAIN LOOP
# -------------------------

running=True

while running:

    scene = scenes[current_scene]
    time = pygame.time.get_ticks()

    mouse = pygame.mouse.get_pos()

    # ---------------------
    # CHARACTER ANIMATION
    # ---------------------

    bob = math.sin(time*0.005)*5 if scene["char"]!="none" else 0

    # ---------------------
    # TYPEWRITER
    # ---------------------

    if not anim["finished"]:

        if time - anim["last"] > anim["speed"]:

            target = scene["texts"][anim["line"]]

            if anim["char"] < len(target):

                anim["display"][anim["line"]] += target[anim["char"]]
                anim["char"]+=1
                anim["last"]=time

            else:

                if anim["line"] < len(scene["texts"])-1:

                    anim["line"]+=1
                    anim["char"]=0

                else:
                    anim["finished"]=True

    # ---------------------
    # EVENTS
    # ---------------------

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type==pygame.KEYDOWN:

            if event.key==pygame.K_f:
                screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)

        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:

            if not anim["finished"]:
                complete_anim(scene)

            else:

                if scene["type"]=="story":

                    current_scene = scene["next"]
                    active_buttons.clear()
                    reset_anim(scenes[current_scene])

                elif scene["type"]=="menu":

                    for b in active_buttons:
                        if b.clicked(mouse,event):

                            if b.target=="quit":
                                pygame.quit()
                                sys.exit()

                            current_scene=b.target
                            active_buttons.clear()
                            reset_anim(scenes[current_scene])

                elif scene["type"]=="choice":

                    for b in active_buttons:

                        if b.clicked(mouse,event):

                            current_scene=b.target
                            active_buttons.clear()
                            reset_anim(scenes[current_scene])

    # ---------------------
    # DRAW
    # ---------------------

    screen.fill(BLACK)

    if scene["bg"] in loaded_assets:
        screen.blit(loaded_assets[scene["bg"]],(0,0))

    if scene["char"]!="none":

        char = loaded_assets[scene["char"]]

        x = WIDTH//2 - char.get_width()//2
        y = 50 + bob

        screen.blit(char,(x,y))

    # ---------------------
    # TITLE SCREEN
    # ---------------------

    if scene["type"]=="menu":

        overlay = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        overlay.fill((0,0,0,120))
        screen.blit(overlay,(0,0))

        title = title_font.render("WHY AM I ANGRY TODAY?",True,WHITE)
        subtitle = small_font.render("A Relationship Survival Simulator",True,WHITE)

        screen.blit(title,(WIDTH//2-title.get_width()//2,HEIGHT//4))
        screen.blit(subtitle,(WIDTH//2-subtitle.get_width()//2,HEIGHT//4+80))

    # ---------------------
    # TEXT BOX
    # ---------------------

    box_h=180

    box = pygame.Surface((WIDTH,box_h),pygame.SRCALPHA)
    box.fill(TEXT_BOX_BG)

    screen.blit(box,(0,HEIGHT-box_h))

    start_y = HEIGHT-box_h+30

    for i,text in enumerate(anim["display"]):

        render = font.render(text,True,WHITE)
        screen.blit(render,(40,start_y+i*40))

    # ---------------------
    # BUTTONS
    # ---------------------

    if scene["type"]=="menu":

        if not active_buttons:

            start = Button("Start Game",WIDTH//2-150,HEIGHT//2,300,50,"intro")
            quit = Button("Quit",WIDTH//2-150,HEIGHT//2+70,300,50,"quit")

            active_buttons=[start,quit]

        for b in active_buttons:
            b.draw(screen,mouse)

    elif scene["type"]=="choice" and anim["finished"]:

        if not active_buttons:

            x = WIDTH-280
            y = 20

            for c in scene["choices"]:

                btn = Button(c["text"],x,y,260,40,c["next"])
                active_buttons.append(btn)

                y += 50

        for b in active_buttons:
            b.draw(screen,mouse)

    pygame.display.update()
    clock.tick(60)