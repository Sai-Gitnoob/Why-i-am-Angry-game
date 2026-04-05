import pygame
import sys
import math
import os
import asyncio

pygame.mixer.pre_init(22050, -16, 1, 1024)
pygame.init()
pygame.mixer.init(22050, -16, 1, 1024)

BASE_PATH = os.path.dirname(__file__)

def asset_path(*path):
    return os.path.join(BASE_PATH, *path)

current_music = None

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Why Am I Angry Today?")

try:
    icon = pygame.image.load(asset_path("assets", "icon.png"))
    pygame.display.set_icon(icon)
except:
    pass

clock = pygame.time.Clock()

WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0  )
BLUE       = (70,  100, 220)
HOVER_BLUE = (110, 140, 255)

font       = pygame.font.SysFont("arial", 28, bold=True)
small_font = pygame.font.SysFont("arial", 22)
title_font = pygame.font.SysFont("arial", 64, bold=True)

# -------------------------
# FADE SYSTEM
# -------------------------
fade_alpha     = 0
fade_speed     = 10
fading         = False
fade_direction = 1
next_scene     = None

def start_fade(scene_id):
    global fading, fade_direction, next_scene
    fading         = True
    fade_direction = 1
    next_scene     = scene_id

# -------------------------
# ASSETS
# -------------------------
asset_map = {
    "bg_livingroom": {"file": asset_path("assets", "background_light.png")},
    "bg_couch":      {"file": asset_path("assets", "background_dark.png")},
    "bg_bedroom":    {"file": asset_path("assets", "bedroom.png")},
    "game_icon":     {"file": asset_path("assets", "icon.png")},
    "char_neutral":  {"file": asset_path("assets", "char_neutral.png")},
    "char_angry":    {"file": asset_path("assets", "char_angry.png")},
    "char_furious":  {"file": asset_path("assets", "char_angry.png")},
    "char_happy":    {"file": asset_path("assets", "char_happy.png")},
    "none": None
}

loaded_assets = {}

def load_assets():
    for name, data in asset_map.items():
        if data is None:
            continue
        try:
            img = pygame.image.load(data["file"]).convert_alpha()
            if name.startswith("bg"):
                img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            else:
                max_height = 420
                scale  = max_height / img.get_height()
                new_w  = int(img.get_width()  * scale)
                new_h  = int(img.get_height() * scale)
                img    = pygame.transform.smoothscale(img, (new_w, new_h))
            loaded_assets[name] = img
        except Exception as e:
            print("ERROR LOADING:", data["file"], e)
            surf = pygame.Surface((WIDTH, HEIGHT) if name.startswith("bg") else (300, 400))
            surf.fill((200, 200, 200))
            txt = small_font.render(name, True, BLACK)
            surf.blit(txt, (20, 20))
            loaded_assets[name] = surf

# -------------------------
# MUSIC
# -------------------------
def play_music(track):
    global current_music
    if current_music == track:
        return
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(track)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        current_music = track
    except Exception as e:
        print("Music error:", e)

# -------------------------
# BUTTON CLASS
# -------------------------
class Button:
    def __init__(self, text, x, y, w, h, target):
        self.rect   = pygame.Rect(x, y, w, h)
        self.text   = text
        self.target = target

    def draw(self, surface, mouse):
        color = HOVER_BLUE if self.rect.collidepoint(mouse) else BLUE
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        label = small_font.render(self.text, True, WHITE)
        rect  = label.get_rect(center=self.rect.center)
        surface.blit(label, rect)

    def clicked(self, mouse, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(mouse))

# -------------------------
# STORY DATA
# -------------------------
scenes = {

    "title": {
        "texts": [""],
        "type":  "menu",
        "bg":    "bg_livingroom",
        "char":  "none",
        "music": asset_path("music", "intro.ogg")
    },

    "intro": {
        "texts": ["You come home after a long day...",
                  "Your girlfriend looks angry.",
                  "(Click to continue)"],
        "type":  "story",
        "next":  "ask",
        "bg":    "bg_livingroom",
        "char":  "char_angry",
        "music": asset_path("music", "normal.ogg")
    },

    "ask": {
        "texts": ["You: Hey... why are you angry?", "(Click)"],
        "type":  "story",
        "next":  "nothing",
        "bg":    "bg_livingroom",
        "char":  "char_angry",
        "music": asset_path("music", "normal.ogg")
    },

    "nothing": {
        "texts": ["Her: Nothing.",
                  "(She is clearly lying)",
                  "(Click to guess)"],
        "type":  "story",
        "next":  "guess",
        "bg":    "bg_livingroom",
        "char":  "char_angry",
        "music": asset_path("music", "normal.ogg")
    },

    "guess": {
        "texts":   ["You try to guess the reason..."],
        "type":    "choice",
        "choices": [
            {"text": "Forgot anniversary",        "next": "anniversary"},
            {"text": "Liked another girl's post", "next": "post"},
            {"text": "Because I exist",           "next": "exist"}
        ],
        "bg":    "bg_livingroom",
        "char":  "char_neutral",
        "music": asset_path("music", "guessing.ogg")
    },

    "anniversary": {
        "texts": ["Her: IT'S IN JUNE!",
                  "YOU DON'T EVEN KNOW?!",
                  "She is furious."],
        "type":  "story",
        "next":  "game_over",
        "bg":    "bg_livingroom",
        "char":  "char_furious",
        "music": asset_path("music", "angry.ogg")
    },

    "post": {
        "texts": ["Her: WOW.", "JUST WOW.", "She starts crying."],
        "type":  "story",
        "next":  "game_over",
        "bg":    "bg_livingroom",
        "char":  "char_furious",
        "music": asset_path("music", "angry.ogg")
    },

    "exist": {
        "texts": ["Her: ...",
                  "She tries not to laugh.",
                  "She smirks."],
        "type":  "story",
        "next":  "good",
        "bg":    "bg_livingroom",
        "char":  "char_happy",
        "music": asset_path("music", "normal.ogg")
    },

    "game_over": {
        "texts":   ["Tonight's sleeping arrangement:", "THE COUCH", "GAME OVER"],
        "type":    "choice",
        "choices": [
            {"text": "Restart",   "next": "intro"},
            {"text": "Main Menu", "next": "title"}
        ],
        "bg":    "bg_couch",
        "char":  "none",
        "music": asset_path("music", "couch.ogg")
    },

    "good": {
        "texts":   ["Crisis Averted.", "You get to sleep in the bed!"],
        "type":    "choice",
        "choices": [
            {"text": "Play Again", "next": "intro"},
            {"text": "Main Menu",  "next": "title"}
        ],
        "bg":    "bg_bedroom",
        "char":  "char_happy",
        "music": asset_path("music", "success.ogg")
    },

    "credits": {
        "texts": [
            "WHY AM I ANGRY TODAY? Version: 1.0",
            "All Rights Reserved",
            "",
            "Created by Sai Tukrul",
            "BS in DS AI/ML  |  IIT Jodhpur",
            "",
            "Built using Python and Pygame",
            "",
            "Thanks for playing!"
        ],
        "type":  "story",
        "next":  "title",
        "bg":    "bg_livingroom",
        "char":  "game_icon",
        "music": asset_path("music", "intro.ogg")
    }
}

# -------------------------
# ANIMATION STATE
# -------------------------
anim = {
    "line": 0, "char": 0,
    "display": [], "finished": False,
    "last": 0, "speed": 30
}

def reset_anim(scene):
    anim["line"]     = 0
    anim["char"]     = 0
    anim["display"]  = [""] * len(scene["texts"])
    anim["finished"] = False
    anim["last"]     = pygame.time.get_ticks()

def complete_anim(scene):
    anim["display"]  = scene["texts"].copy()
    anim["finished"] = True

# -------------------------
# ASYNC MAIN
# -------------------------
async def main():
    global current_scene, active_buttons
    global fade_alpha, fading, fade_direction, next_scene

    load_assets()
    await asyncio.sleep(0)

    current_scene  = "title"
    active_buttons = []
    reset_anim(scenes[current_scene])

    # cached surfaces — created once, reused every frame
    box_h         = 160
    box_surf_cache = pygame.Surface((WIDTH - 80, box_h), pygame.SRCALPHA)
    box_surf_cache.fill((0, 0, 0, 180))

    fade_surf = pygame.Surface((WIDTH, HEIGHT))
    fade_surf.fill(BLACK)

    running = True

    while running:
        scene = scenes[current_scene]

        if "music" in scene:
            play_music(scene["music"])

        time  = pygame.time.get_ticks()
        mouse = pygame.mouse.get_pos()
        bob   = math.sin(time * 0.005) * 5 if scene["char"] != "none" else 0

        # ---- TEXT ANIMATION ----
        if not anim["finished"]:
            if time - anim["last"] > anim["speed"]:
                target = scene["texts"][anim["line"]]
                if anim["char"] < len(target):
                    anim["display"][anim["line"]] += target[anim["char"]]
                    anim["char"] += 1
                    anim["last"]  = time
                else:
                    if anim["line"] < len(scene["texts"]) - 1:
                        anim["line"] += 1
                        anim["char"]  = 0
                    else:
                        anim["finished"] = True

        # ---- EVENTS ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not anim["finished"]:
                    complete_anim(scene)
                else:
                    if scene["type"] == "story":
                        start_fade(scene["next"])
                    elif scene["type"] in ("choice", "menu"):
                        for b in active_buttons:
                            if b.clicked(mouse, event):
                                start_fade(b.target)

        # ---- DRAW BACKGROUND ----
        screen.fill(BLACK)
        if scene["bg"] in loaded_assets:
            screen.blit(loaded_assets[scene["bg"]], (0, 0))

        # ---- DRAW CHARACTER ----
        if scene["char"] != "none" and scene["char"] in loaded_assets:
            char_img = loaded_assets[scene["char"]]
            char_x   = WIDTH  // 2 - char_img.get_width()  // 2
            char_y   = HEIGHT - char_img.get_height() - 20 + int(bob)
            screen.blit(char_img, (char_x, char_y))

        # ---- MENU SCREEN ----
        if scene["type"] == "menu":
            shadow     = title_font.render("Why Am I Angry Today?", True, (30, 30, 30))
            title_surf = title_font.render("Why Am I Angry Today?", True, WHITE)
            screen.blit(shadow,     shadow.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 3 + 3)))
            screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3)))

            sub = small_font.render("A Visual Novel", True, (200, 200, 200))
            screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 70)))

            active_buttons = [
                Button("Start Game", WIDTH // 2 - 110, HEIGHT // 2,      220, 50, "intro"),
                Button("Credits",    WIDTH // 2 - 110, HEIGHT // 2 + 70, 220, 50, "credits"),
            ]
            for b in active_buttons:
                b.draw(screen, mouse)

        else:
            # ---- TEXT BOX (using cached surface) ----
            box_rect = pygame.Rect(40, HEIGHT - box_h - 20, WIDTH - 80, box_h)
            screen.blit(box_surf_cache, (box_rect.x, box_rect.y))
            pygame.draw.rect(screen, WHITE, box_rect, 2, border_radius=8)

            y_offset = box_rect.y + 15
            for line in anim["display"]:
                txt_surf = small_font.render(line, True, WHITE)
                screen.blit(txt_surf, (box_rect.x + 15, y_offset))
                y_offset += 32

            # ---- CHOICE BUTTONS ----
            if scene["type"] == "choice" and anim["finished"]:
                active_buttons = []
                choices = scene["choices"]
                btn_w, btn_h = 260, 48
                gap     = 20
                total_w = len(choices) * btn_w + (len(choices) - 1) * gap
                start_x = WIDTH  // 2 - total_w // 2
                btn_y   = HEIGHT // 2 - btn_h   // 2

                for i, c in enumerate(choices):
                    bx = start_x + i * (btn_w + gap)
                    b  = Button(c["text"], bx, btn_y, btn_w, btn_h, c["next"])
                    active_buttons.append(b)
                    b.draw(screen, mouse)
            else:
                active_buttons = []

        # ---- FADE OVERLAY (using cached surface) ----
        if fading:
            fade_alpha += fade_speed * fade_direction
            if fade_direction == 1 and fade_alpha >= 255:
                fade_alpha     = 255
                current_scene  = next_scene
                reset_anim(scenes[current_scene])
                fade_direction = -1
            elif fade_direction == -1 and fade_alpha <= 0:
                fade_alpha = 0
                fading     = False

            fade_surf.set_alpha(int(fade_alpha))
            screen.blit(fade_surf, (0, 0))

        pygame.display.update()
        clock.tick(30)

        await asyncio.sleep(0)

asyncio.run(main())