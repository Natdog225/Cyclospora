
import random
import time
from battle.battle import start_battle, render_battle_screen
from characters.creature import PlayerCharacter, Creature
from characters.npc import Caveman, Knight, Ninja, British_Soldier, Nazi_Soldier, Alien
import pygame
import sys
from main_menu import main_menu_screen

class ScrollingText:
    def __init__(self, text, font, color, screen_width, screen_height, scroll_speed=1, line_spacing=50):
        self.text = text
        self.font = font
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scroll_speed = scroll_speed
        self.line_spacing = line_spacing
        self.text_surface = self.render_text()
        self.y = 0

    def render_text(self):
        lines = self.text.split('\n')
        max_width = self.screen_width - 25  # Leave some margin on the sides
        total_height = 0
        for line in lines:
            width, height = self.font.size(line)
            total_height += height + self.line_spacing

        surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
        y = 0
        for line in lines:
            text_surface = self.font.render(line, True, self.color)
            surface.blit(text_surface, (0, y))
            y += text_surface.get_height() + self.line_spacing

        return surface

    def update(self):
        self.y -= self.scroll_speed
        if self.y < -self.text_surface.get_height():
            self.y = 0

    def draw(self, screen):
        screen.blit(self.text_surface, (self.screen_width // 2 - self.text_surface.get_width() // 2, self.y))

def start_game():
    global current_scene, player, enemy, battle_turn, selected_action, battle_actions, screen, font, text_color, screen_width, screen_height, clock
    pygame.init()
    pygame.mixer.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Cyclospora")

    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)

    # Load images
    main_menu_image = pygame.image.load("images/main.jpeg").convert()
    intro_image = pygame.image.load("images/deaths_via_berry.jpg").convert()
    stone_age_bg = pygame.image.load("images/caveman-bg.jpg").convert()
    battle_bg = pygame.Surface((screen_width, screen_height))
    battle_bg.fill((128, 128, 128))  # Gray background for battle scene

    main_menu_image = pygame.transform.scale(main_menu_image, (screen_width, screen_height))
    intro_image = pygame.transform.scale(intro_image, (screen_width, screen_height))
    stone_age_bg = pygame.transform.scale(stone_age_bg, (screen_width, screen_height))

    # Load sounds
    intro_music = pygame.mixer.Sound("Ambience/ObservingTheStar.ogg")
    stone_age_music = pygame.mixer.Sound("Ambience/caveman-bg.ogg")
    battle_music = pygame.mixer.Sound("Ambience/ST_1_Fight(wave).wav")
    club_hit_sound = pygame.mixer.Sound('Sounds/CyclosporaSFX/Bonk Sound Effect.mp3')

    # Text-related variables
    text_lines = [
        "Cyclospora",
        "In recent events, there has been an outbreak.",
        "A parasitic contamination of our local berries",
        "including; blueberries, raspberries, blackberries and strawberries",
        "Ugh, I'm starving....",
        "What's in the fridge?",
        "You walk into the kitchen and open the fridge",
        "You see there's nothing to prepare for breakfast,",
        "Well there's a boysenberry pie your neighbor brought over,",
        "that definitely looks older than a week",
        "Well it's not the worst thing I've eaten...",
        "I should at least try it to be respectful",
        "As you munch on the pie, you remember the news and think...",
        "Did the news say boysenberry?...",
        "Meh. Should be fine.",
        "(You've eaten the pie)",
        "That wasn't too bad",
        "Ugh, spoke too soon...",
        "(Stomach starts bubbling and hurting)",
        "ugh...I think I'll sleep it off...",
        "You lay down..."
    ]
    stone_age_text_lines = [
        "(There's an unfamiliar cold hard surface that you knew couldn't be you're bed)",
        "Oww, my back...",
        "(As you start adjusting yourself to your surroundings, You see foliage and start hearing loud noises you feel like you've heard in a movie)",
        "What the....",
        "(You shoot up and start scrambling around)",
        "How did I get here?!",
        "Am I dreaming?",
        "(As you look around you see what you believe to be a man)",
        "Excuse Me!",
        "(He notices you and starts sprinting with explosive power towards you)"
    ]
    medieval_time_text_lines = [
    "(Your head is pounding and your arms and legs are aching)"
    "Damn it...(You hold your head in your hands)"
    "(As you lay in pain from the unexpected battle, the sound of metal clanging together gets louder and louder)"
    "HARK!! Who goes there?!"
    "(You hurriedly stand up and adrenaline courses through you're veins. As you look around, you notice your in some medieval era)"
    "Please, not again"
    ]
    reddistrict_text_lines = [
        "WHY IS THIS HAPPENING TO ME?!"
        "(You start trembling with anger and feelings of helplessness...)"
        "Where am I now?!"
        "(YOu hear a commotion to your left and see  Geisha in the midst of a crowd walking , almost like a parade)"
        "(The lights start turning on and the sun is setting, you realize it's getting dark out)"
        "Crap, gotta find somewhere to sleep"
        "(You wonder the district and see food vendors and the area becoming livelier)"
        "(You're stomach still hurts from that pie you ate. But you feel an insatuated hunger)"
        "Can I get some food please?(You ask a vendor, she clearly doesn't understand you)"
        "Well damn..."
        "Well maybe if I...(You start to rummage your pockets and pull out your wallet. The vendor starts to panic)"
        "(You gaze to see what she's fretting about. As you try to see where your gaze ends, you realize it's the weapons you've collected along the way. )"
        "(You're shocked, and start explaining that you mean no harm, but fail)"
        "(Some person you can only describe as a stereotypical ninja approaches you with sword drawn.)"
        "(You quickly put your weapon away, back up and sheathe it and apologize profusely to the lady and wander away from the body you just left in the street.)"
        "(After panic walking away from the murder you just committed. You find another vender and ask about a nearby inn. She seems to understand and points you in the direction of an Inn)"
        "(You thank her and start walking towards the Inn, as you walk you begin to feel light-headed and blackout again.)" 
    ]
    wwii_text_lines = [
        "(You awake and look around, you notice a city-scape bombed to a point it resembled rubble more than a city.)"
        "Halt! You there!"
        "(You stop and slowly turn around)"
        "(You are face to face with a Nazi soldier, obviously there isn't much to say at this point, you look to your right and find a discarded rifle, pick it up and point)"
    ]
    modern_times_text_lines = [
        "(Well, that one doesn't feel quite like murder as the previous ones."
        "That was a pretty easy choice.)"
        "(You begin to look around, you debate just laying down and waiting"
        "(But you're just guessing at this point.)"
        "Oh there's the sleepy."
        "You fall asleep"
        "(You awaken to the sound of cars and people talking)"
        "(You look around and realize you're in a modern city)"
        "Where am I now?"
        "(You see a soldier patrolling the street)"
        "Hey, you! Stop right there!"
        "(You realize you're just a dude holding a bunch of weapons)"
        "Somewhere in the middle of what appears to be the United Kingdom." 
        "They don't like guns and obviously do not like you right now.)"
    ]
    mars_text_lines = [
        "Well, guess I'm just a murderer now with some kind of berry monster helping me commit more crimes in various ages."
        "(You begin to wander off attempting to hide somewhere not in the middle of the street. You find yourself wandering down an alley.)"
        "(At the end of the alley, a bright light suddenly bursts out of the wall. It resembles a portal that you would see in Star Trek or something else sci-fi.)"
        "Well guess I really don't have much to lose now."
        "(You reload your rifle, take a look around and walk through the portal.)"
    ]

    # Game variables
    current_scene = "main_menu"
    player = None
    menu_options = ["Play", "Quit"]
    selected_option = 0

    # Scrolling text objects
    intro_text = ScrollingText('\n'.join(text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    stone_age_text = ScrollingText('\n'.join(stone_age_text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)

    # Battle variables
    battle_active = False
    player = PlayerCharacter("Player", 100, 100)
    enemy = None
    battle_turn = "player"
    battle_actions = ["Attack", "Run away", "Try to reason", "Do nothing"]
    selected_action = 0

    # --- Game loop ---
    running = True
    clock = pygame.time.Clock()
    while running:
        # 1. Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_action = (selected_action + 1) % len(battle_actions)
                elif event.key == pygame.K_UP:
                    selected_action = (selected_action - 1) % len(battle_actions)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    handle_battle_action()

        # 2. Update game state
        if current_scene == "main_menu":
            main_menu_screen(screen, font, text_color, screen_width, screen_height, clock, main_menu_image, menu_options, selected_option)
        elif current_scene == "intro":
            intro_screen()
        elif current_scene == "stone_age":
            stone_age_screen()
        elif current_scene == "medieval_time":
            medieval_time_screen()
        elif current_scene == "red_district":
            red_district_screen()
        elif current_scene == "wwii":
            wwii_screen()
        elif current_scene == "modern_times":
            modern_times_screen()
        elif current_scene == "mars":
            mars_screen()
        if current_scene in ["stone_age", "medieval_time", "red_district", "wwii", "modern_times", "mars"]:
            if enemy is None or enemy.hp <= 0:
                enemy = choose_enemy(current_scene)
                battle_turn = "player"

        # 3. Render
        screen.fill((0, 0, 0))  # Clear the screen with a black background

        if enemy is not None:
            render_battle_screen(screen, font, text_color, player, enemy, battle_turn, battle_actions, selected_action)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def choose_enemy(current_scene):
    if current_scene == "stone_age":
        return Caveman()
    elif current_scene == "medieval_time":
        return Knight()
    elif current_scene == "red_district":
        return Ninja()
    elif current_scene == "wwii":
        return Nazi_Soldier()
    elif current_scene == "modern_times":
        return British_Soldier()
    elif current_scene == "mars":
        return Alien()
    else:
        raise ValueError("Invalid scene for enemy selection")

def intro_screen(screen, font, text_color, screen_width, screen_height, clock, text_lines):
    global current_scene
    screen.fill((0, 0, 0))
    intro_text = ScrollingText('\n'.join(text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        intro_text.update()
        screen.fill((0, 0, 0))
        intro_text.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    current_scene = "stone_age"

def stone_age_screen(screen, font, text_color, screen_width, screen_height, clock, stone_age_text_lines):
    global current_scene
    screen.fill((0, 0, 0))
    stone_age_text = ScrollingText('\n'.join(stone_age_text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        stone_age_text.update()
        screen.fill((0, 0, 0))
        stone_age_text.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    enemy = Caveman()

def medieval_time_screen(screen, font, text_color, screen_width, screen_height, clock, medieval_time_text_lines):
    global current_scene
    screen.fill((0, 0, 0))
    medieval_time_text = ScrollingText('\n'.join(medieval_time_text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        medieval_time_text.update()
        screen.fill((0, 0, 0))
        medieval_time_text.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    enemy = Knight()

def red_district_screen(screen, font, text_color, screen_width, screen_height, clock, reddistrict_text_lines):
    global current_scene, player, enemy
    screen.fill((0, 0, 0))
    red_district_text = ScrollingText('\n'.join(reddistrict_text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        red_district_text.update()
        screen.fill((0, 0, 0))
        red_district_text.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    enemy = Ninja()

def wwii_screen(screen, font, text_color, screen_width, screen_height, clock, wwii_text_lines):
    global current_scene, player, enemy
    screen.fill((0, 0, 0))
    wwii_text = ScrollingText('\n'.join(wwii_text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        wwii_text.update()
        screen.fill((0, 0, 0))
        wwii_text.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    enemy = Nazi_Soldier()

def modern_times_screen(screen, font, text_color, screen_width, screen_height, clock, modern_times_text_lines):
    global current_scene, player, enemy
    screen.fill((0, 0, 0))
    modern_times_text = ScrollingText('\n'.join(modern_times_text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        modern_times_text.update()
        screen.fill((0, 0, 0))
        modern_times_text.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    enemy = British_Soldier()

def mars_screen(screen, font, text_color, screen_width, screen_height, clock, mars_text_lines):
    global current_scene, player, enemy
    screen.fill((0, 0, 0))
    mars_text = ScrollingText('\n'.join(mars_text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        mars_text.update()
        screen.fill((0, 0, 0))
        mars_text.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    enemy = Alien()


def handle_battle_action():
    global battle_turn, current_scene, selected_action
    if battle_turn == "player":
        if selected_action == 0:
            player.attack(enemy)
        elif selected_action == 1:
            if random.random() < player.special["Luck"] * 0.1:
                print("You successfully escaped!")
                next_scene()
            else:
                print("You failed to escape!")
        elif selected_action == 2:
            if random.random() < player.special["Perception"] * 0.05:
                print("You successfully reasoned with the enemy!")
                next_scene()
            else:
                print(f"The {enemy.name} doesn't understand you.")
        elif selected_action == 3:
            print("You do nothing.")
        battle_turn = "enemy"

def next_scene():
    global current_scene
    if current_scene == "stone_age" and enemy.name == "Caveman":
        current_scene = "medieval_time"
    elif current_scene == "medieval_time" and enemy.name == "Knight":
        current_scene = "red_district"
    elif current_scene == "red_district" and enemy.name == "Ninja":
        current_scene = "wwii"
    elif current_scene == "wwii" and enemy.name == "Nazi Soldier":
        current_scene = "modern_times"
    elif current_scene == "modern_times" and enemy.name == "British Soldier":
        current_scene = "mars"
    elif current_scene == "mars" and enemy.name == "Alien":
        # Game won!
        pass  # Implement victory screen here


if __name__ == "__main__":
    start_game()
