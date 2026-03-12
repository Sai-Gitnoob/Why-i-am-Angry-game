import pygame
import sys
import math

pygame.init()

# --- Configuration ---
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Why Am I Angry Today?")

# --- Fonts & Colors ---
font = pygame.font.SysFont("arial", 28, bold=True)
small_font = pygame.font.SysFont("arial", 22)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 100, 220)
HOVER_BLUE = (100, 130, 255)
TEXT_BOX_BG = (0, 0, 0, 180) # Black with transparency

# --- SMART ASSET LOADER ---
# This dictionary maps names to filenames. 
# If the file isn't found, it generates a colored rectangle instead.
asset_map = {
    # Backgrounds
    'bg_livingroom': {'file': '/home/sai/College/Why i am angry/Game Images/backgroundLight.png'}, 
    'bg_couch':      {'file': '/home/sai/College/Why i am angry/Game Images/backgroundDark.png'},
    'bg_happy':      {'file':'/home/sai/College/Why i am angry/Game Images/backgroundDark.png'},
    'bg_bedroom':    {'file': 'Game Images/bedroom.png'}, 
    
    # Character Expressions
    'char_neutral':  {'file': 'Game Images/charNeutral.png',  },
    'char_angry':    {'file': 'Game Images/charAngry.png'},
    'char_furious':  {'file': 'Game Images/charAngry.png'},
    'char_happy':    {'file': 'Game Images/charHappy.png'},
    'none':          None # For scenes with no character
}

loaded_assets = {}

def load_assets():
    for name, data in asset_map.items():
        if data is None: continue
        try:
            # Try loading the real image
            img = pygame.image.load(data['file']).convert_alpha()
            # Scale backgrounds to screen, characters to stand in middle
            if name.startswith('bg'):
                img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            else:
                # Maintain aspect ratio
                max_height = 400
                scale = max_height / img.get_height()
                new_width = int(img.get_width() * scale)
                new_height = int(img.get_height() * scale)

                img = pygame.transform.smoothscale(img, (new_width, new_height))
            loaded_assets[name] = img
        except FileNotFoundError:
            # Fallback: Create a placeholder rectangle with text
            surf = pygame.Surface((WIDTH, HEIGHT) if name.startswith('bg') else (300, 400))
            surf.fill(data['color'])
            # Draw name on placeholder
            text = small_font.render(name, True, BLACK)
            surf.blit(text, (20, 20))
            loaded_assets[name] = surf

load_assets()

# --- Classes ---
class Button:
    def __init__(self, text, x, y, w, h, target_scene):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.target_scene = target_scene

    def draw(self, surface, mouse_pos):
        color = HOVER_BLUE if self.rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        
        label = small_font.render(self.text, True, WHITE)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def is_clicked(self, mouse_pos, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(mouse_pos)

# --- Game Data ---
# Added 'bg' and 'char' keys to every scene
scenes = {
    'intro': {
        'texts': ["You come home after a long day...", "Your girlfriend looks angry.", "(Click to continue)"],
        'type': 'story', 'next': 'ask', 
        'bg': 'bg_livingroom', 'char': 'char_angry'
    },
    'ask': {
        'texts': ["You: Hey... why are you angry?", "(Click)"],
        'type': 'story', 'next': 'nothing',
        'bg': 'bg_livingroom', 'char': 'char_angry'
    },
    'nothing': {
        'texts': ["Her: Nothing.", "(She is clearly lying)", "(Click to guess)"],
        'type': 'story', 'next': 'guess',
        'bg': 'bg_livingroom', 'char': 'char_angry'
    },
    'guess': {
        'texts': ["You try to guess the reason..."],
        'type': 'choice',
        'choices': [
            {'text': "Forgot our anniversary", 'next': 'anniversary'},
            {'text': "Liked another girl's post", 'next': 'post'},
            {'text': "Because I exist", 'next': 'exist'}
        ],
        'bg': 'bg_livingroom', 'char': 'char_neutral'
    },
    'anniversary': {
        'texts': ["Her: IT'S IN MARCH!", "YOU DON'T EVEN KNOW?!", "She is furious.", "(Click)"],
        'type': 'story', 'next': 'game_over',
        'bg': 'bg_livingroom', 'char': 'char_furious'
    },
    'post': {
        'texts': ["Her: WOW. JUST WOW.", "She starts crying.", "(Click)"],
        'type': 'story', 'next': 'game_over',
        'bg': 'bg_livingroom', 'char': 'char_furious'
    },
    'exist': {
        'texts': ["Her: ...", "(She tries not to laugh, but smirks.)", "(Click)"],
        'type': 'story', 'next': 'good_ending',
        'bg': 'bg_livingroom', 'char': 'char_happy'
    },
    'game_over': {
        'texts': ["Tonight's sleeping arrangement:", "THE COUCH", "GAME OVER", "(Click to restart)"],
        'type': 'story', 'next': 'intro',
        'bg': 'bg_couch', 'char': 'none'
    },
    'good_ending': {
        'texts': ["Crisis Averted.", "She appreciates the joke.", "YOU GET TO SLEEP IN THE BED!"],
        'type': 'story', 'next': 'intro',
        'bg': 'bg_bedroom', 'char': 'char_happy'
    }
}

# --- Animation State ---
anim_state = {
    'current_line': 0, 'current_char': 0, 'displayed_texts': [],
    'last_update': 0, 'finished': False, 'speed': 30
}

def reset_animation(scene_data):
    anim_state['current_line'] = 0
    anim_state['current_char'] = 0
    anim_state['displayed_texts'] = [""] * len(scene_data['texts'])
    anim_state['finished'] = False
    anim_state['last_update'] = pygame.time.get_ticks()

def complete_animation(scene_data):
    anim_state['displayed_texts'] = scene_data['texts'].copy()
    anim_state['finished'] = True

# --- Main Game Loop ---
clock = pygame.time.Clock()
current_scene_id = 'intro'
active_buttons = []
reset_animation(scenes[current_scene_id])

running = True
while running:
    # 1. Update Logic
    current_time = pygame.time.get_ticks()
    scene_data = scenes[current_scene_id]
    
    # Breathing Animation (Math: Sine wave creates smooth bobbing)
    # Only bob if there is a character
    bob_offset = 0
    if scene_data['char'] != 'none':
        bob_offset = math.sin(current_time * 0.005) * 5  # Speed * 0.005, Amplitude 5px

    # Typewriter Logic
    if not anim_state['finished']:
        if current_time - anim_state['last_update'] > anim_state['speed']:
            target_line = scene_data['texts'][anim_state['current_line']]
            if anim_state['current_char'] < len(target_line):
                anim_state['displayed_texts'][anim_state['current_line']] += target_line[anim_state['current_char']]
                anim_state['current_char'] += 1
                anim_state['last_update'] = current_time
            else:
                if anim_state['current_line'] < len(scene_data['texts']) - 1:
                    anim_state['current_line'] += 1
                    anim_state['current_char'] = 0
                else:
                    anim_state['finished'] = True

    # 2. Event Handling
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not anim_state['finished']:
                complete_animation(scene_data)
            else:
                if scene_data['type'] == 'story':
                    current_scene_id = scene_data['next']
                    reset_animation(scenes[current_scene_id])
                elif scene_data['type'] == 'choice':
                    for button in active_buttons:
                        if button.is_clicked(mouse_pos, event):
                            current_scene_id = button.target_scene
                            active_buttons.clear()
                            reset_animation(scenes[current_scene_id])
                            break

    # 3. Drawing
    screen.fill(BLACK)
    
    # A. Draw Background
    if scene_data['bg'] in loaded_assets:
        screen.blit(loaded_assets[scene_data['bg']], (0, 0))
    
    # B. Draw Character (with Breathing Animation)
    char_key = scene_data['char']
    if char_key != 'none' and char_key in loaded_assets:
        char_surf = loaded_assets[char_key]
        # Draw centered horizontally, slightly down, plus bobbing
        x_pos = WIDTH // 2 - char_surf.get_width() // 2
        y_pos = 50 + bob_offset 
        screen.blit(char_surf, (x_pos, y_pos))

    # C. Draw Text Box (Semi-transparent overlay)
    box_height = 200
    box_surface = pygame.Surface((WIDTH, box_height), pygame.SRCALPHA)
    box_surface.fill(TEXT_BOX_BG)
    screen.blit(box_surface, (0, HEIGHT - box_height))

    # D. Draw Text
    start_y = HEIGHT - box_height + 30
    for i, text in enumerate(anim_state['displayed_texts']):
        rendered = font.render(text, True, WHITE)
        screen.blit(rendered, (40, start_y + (i * 40)))

    # E. Draw Buttons
    if scene_data['type'] == 'choice' and anim_state['finished']:
        if not active_buttons:
            button_width = 420
            button_height = 45
            button_spacing = 15
            total_height = len(scene_data['choices']) * (button_height + button_spacing)
            start_y = HEIGHT - box_height + (box_height // 2) - (total_height // 2)
            for i, choice in enumerate(scene_data['choices']):
                x = WIDTH // 2 - button_width // 2
                y = start_y + i * (button_height + button_spacing)
                new_btn = Button(choice['text'], x, y, button_width, button_height, choice['next'])
                active_buttons.append(new_btn)
        for button in active_buttons:
            button.draw(screen, mouse_pos)

    pygame.display.update()
    clock.tick(60)