
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
        # screen.blit(self.text_surface, (self.screen_width // 2 - self.text_surface.get_width() // 2, self.y))
        for i, text_surface in enumerate(self.text_surfaces): surface.blit(text_surface, (10, self.y + i * self.line_spacing))

def start_game():
    # global current_scene, player, enemy, battle_turn, selected_action, battle_actions, screen, font, text_color, screen_width, screen_height, clock
    pygame.init()
    pygame.mixer.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Cyclospora")

    clock = pygame.time.Clock()
    
    rect_x = 0
    rect_y = 0
    rect_speed_x = 2
    rect_speed_y = 2
    rect_width = 50
    rect_height = 50

    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)

    # Load images
    main_menu_image = pygame.image.load("images/main.jpeg").convert()
    intro_image = pygame.image.load("images/deaths_via_berry.jpg").convert()
    stone_age_bg = pygame.image.load("images/caveman-bg.jpg").convert()
    battle_bg = pygame.Surface((screen_width, screen_height))
    battle_bg.fill((128, 128, 128))  # Gray background for battle scene
    medieval_time_bg = pygame.image.load("images/CastleBridge.jpg").convert()
    red_district_bg = pygame.image.load("images/RedDistrict.jpg").convert()
    Lexington_bg = pygame.image.load("images/Lexington.jpg").convert()
    WWII_bg = pygame.image.load("images/WWII-bg.jpg").convert()
    Alien = pygame.image.load("images/Alien.jpg").convert()
    AlienPlot = pygame.image.load("images/AlienPlot.jpg").convert()

    main_menu_image = pygame.transform.scale(main_menu_image, (screen_width, screen_height))
    intro_image = pygame.transform.scale(intro_image, (screen_width, screen_height))
    stone_age_bg = pygame.transform.scale(stone_age_bg, (screen_width, screen_height))
    medieval_time_bg = pygame.transform.scale(medieval_time_bg, (screen_width, screen_height))
    red_district_bg = pygame.transform.scale(red_district_bg, (screen_width, screen_height))
    Lexington_bg = pygame.transform.scale(Lexington_bg, (screen_width, screen_height))
    WWII_bg = pygame.transform.scale(WWII_bg, (screen_width, screen_height))
    Alien = pygame.transform.scale(Alien, (screen_width, screen_height))
    AlienPlot = pygame.transform.scale(AlienPlot, (screen_width, screen_height))



    # Load sounds
    intro_music = pygame.mixer.Sound("Ambience/ObservingTheStar.ogg")
    stone_age_music = pygame.mixer.Sound("Ambience/caveman-bg.ogg")
    battle_music = pygame.mixer.Sound("Ambience/ST_1_Fight(wave).wav")
    club_hit_sound = pygame.mixer.Sound('Sounds/CyclosporaSFX/Bonk Sound Effect.mp3')
    castle_music = pygame.mixer.Sound("Ambience/Alert! Outsider!.mp3")
    knight_music = pygame.mixer.Sound("Ambience/ST_1_Fight(mp3^320).mp3")
    red_district_music = pygame.mixer.Sound("Ambience/Socapex - Tokyo Chase.mp3")
    Ninja_music = pygame.mixer.Sound("Ambience/Theme of &#039;&#039;Ninja of A Great Sausage&#039;&#039;.ogg")
    Lexington_music = pygame.mixer.Sound("Ambience/civil-war-fanfares.mp3")
    Concord_soldier_music = pygame.mixer.Sound("Ambience/battle-march-action-loop.mp3")
    WWII_music = pygame.mixer.Sound("Ambience/warzone.mp3")
    Soldier_music = pygame.mixer.Sound("images/Soldier.mp3")
    
    # Load background music
    pygame.mixer.music.load("Ambience/ObservingTheStar.ogg")
    pygame.mixer.music.play(-1)

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
        '....IIIIT!!'
        "(the portal drops you on a cobblestone road)"
        "'OOOWW!!'",
        "(As you take a breathe in, you immediately start to feel sick)",
        "(You lean over to the side of a cobblestone ledge and vomit)",
        'That taste just as bad as it did when I ate that pie', 
        "(Wiping off the sides of your mouth, clanging metal sounds come from the road south of your position)",
        "Knight: 'HARK!! Who Goes There?!'"
    ]
    reddistrict_text_lines = [

        'WHY IS THIS HAPPENING TO ME?!',
        "(You start trembling with anger and feelings of helplessness...)",
        "Where am I now?!",
        "(You hear a commotion to your left and see  Geisha in the midst of a crowd walking , almost like a parade)",
        "(The lights start turning on and the sun is setting, you realize it's getting dark out)",
        "'Crap, gotta find somewhere to sleep'",
        "(You wonder the district and see food vendors and the area becoming livelier)",
        "(You're stomach still hurts from that pie you ate. But you feel an insatuated hunger)",
        "'Can I get some food please?'(You ask a vendor, she clearly doesn't understand you)",
        "'Well damn...'",
        "'Well maybe if I...',"
       "(You start to rummage your pockets and pull out your wallet. The vendor starts to panic)",
        "(You gaze to see what she's fretting about. As you try to see where your gaze ends, you realize it's the weapons you've collected along the way. )",
        "(You're shocked, and start explaining that you mean no harm, but fail)",
        "(Some person you can only describe as a stereotypical ninja approaches you with sword drawn.)"
    ]
    wwii_text_lines = [
        "(You awake and look around, you notice plains of grass and tents vicarously placed on the end that you're in and the opposite end.)",
        'I must have passed out from the pain',
        "Concord Militiaman: 'Halt! Who goes there? State your business on this land, or prepare to face the consequences!'",
        "(You stop and slowly turn around)",
        "(You are face to face with a Concord militiaman.)",
        "'...guns...'",
        "(You need too tread carefully or there will be a bullet between your eyes.)"
    ]
    modern_times_text_lines = [
        "(You start to panic and ponder, if wherever you landed will be changed from the history you know or if it remains the same)",
        "(You look around and you notice a city-scape, bombed to a point it resembled rubble more than a city)",
        "Where am I now?'",
        "(You see a soldier patrolling the area)",
        "Soldier: 'Hey! This is no place for you! Get to safety, now!'",
        "(You realize you are in another battlezone and start to panic.)",
        'Wooah...I just need some help...',
        "(The soldier you believe is American due to the uniform they have on.)"
        "Soldier: 'Identify yourself! What are you doing here? You better have a good reason, or you'll be answering to the higher-ups.'",
        'Okay what do I say now?'
    ]
    mars_text_lines = [
        "(As you wake up, you feel cold metal on the backside of your entire body)",
        "(Your gaze is met with what you believe to be an Alien)",
        "Alien: 'Awaken, human. You are now part of the great harvest. Your existence will contribute to the advancement of our species. Resistance is futile. Accept your fate.'",
        "(You scramble to your feet)",
        'What is going on?!',
        "Alien: 'Do not attempt to resist. Your kind has brought this upon yourselves. In the future, humans initiated a genocide against my people. I lost my arms in that war. Now, you will pay for your crimes.'",
        "(You feel a surge of panic but try to think of a way out.)",
        'Genocide? I... I had no idea. There must be another way. I can help you without... without this.'"),"
        "(The Alien's eyes narrow, filled with anger and pain.)",
        "Alien: 'Help?! You are the one that needs help! Aren't You wondering about the pain and circumstances that you are experiencing?'",
        "(The alien laughs)",
        'Well why am I here then?',
        "Alien: 'We are harvesting your kind to help restore ours. The parasites that were on the berries, have the ability to travel through time, hence you being here.'",
        "What? then how did the parasites get there if what we did was in the future and I'm in the past?",
        "Alien: 'As we foraged the planet for resources this parasite was of your planet once, but it had arrived on a meteor. It had evolved to survive the travel in space'",
        "Alien: 'We took it as an opportunity to go back in time after ingesting it. We failed many times'",
        "Alien: 'But grew closer and closer to success. The spread of the coronavirus wasn't as successful as we'd hoped. We had scraped virus outbreaks from the plan.'",
        "Alien: 'So why not use the parasite as we have been, to get revenge, to be the catalyst of our plight? Evidently ingesting this parasite for you humans has volatile symptoms.'",
        'What do you mean?',
        "Alien: 'Well the time travel being one of them, although it doesn't really matter how or if you humans got to us or died beforehand. The less of you vermin, the better'",
        "(You crouch once more, the pain is getting worse by the minute)",
        "Alien: 'Well, I better harvest you whilst I can, The parasites love human flesh and the only way to kill it is by drinking our blood and even though it would give me time to harvest you, I'd rather you be in as much pain as possible'",
        "(The alien is getting ready to probe you, what shall you do?)"
    ]

    home_text_lines = [
        "(No longer do you feel cold metal but soft sheets and cushions, You jolt up)",
        "Oh my god....I'm back home",
        "(You start getting up, relieved. As you make your way to the bedroom door and into the hallway.)",
        "(CRASH!!......SCREACH!!)",
        "(CYCLOSPORA)"
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
            intro_screen(screen, font, text_color, screen_width, screen_height, clock, main_menu_image, menu_options, selected_option)
        elif current_scene == "stone_age":
            stone_age_screen(screen, font, text_color, screen_width, screen_height, clock, main_menu_image, menu_options, selected_option)
        elif current_scene == "medieval_time":
            medieval_time_screen(screen, font, text_color, screen_width, screen_height, clock, main_menu_image, menu_options, selected_option)
        elif current_scene == "red_district":
            red_district_screen(screen, font, text_color, screen_width, screen_height, clock, main_menu_image, menu_options, selected_option)
        elif current_scene == "wwii":
            wwii_screen(screen, font, text_color, screen_width, screen_height, clock, main_menu_image, menu_options, selected_option)
        elif current_scene == "modern_times":
            modern_times_screen(screen, font, text_color, screen_width, screen_height, clock, main_menu_image, menu_options, selected_option)
        elif current_scene == "mars":
            mars_screen(screen, font, text_color, screen_width, screen_height, clock, main_menu_image, menu_options, selected_option)
        if current_scene in ["stone_age", "medieval_time", "red_district", "wwii", "modern_times", "mars"]:
            if enemy is None or enemy.hp <= 0:
                enemy = choose_enemy(current_scene)
                battle_turn = "player"
    #need outro screen

        # Move the rectangle
        rect_x += rect_speed_x
        rect_y += rect_speed_y

        # # Bounce the rectangle off the edges
        if rect_x < 0 or rect_x + rect_width > screen_width:
            rect_speed_x = -rect_speed_x
        if rect_y < 0 or rect_y + rect_height > screen_height:
            rect_speed_y = -rect_speed_y

        
        # 3. Render
        screen.fill((0, 0, 0))  # Clear the screen with a black background

        if enemy is not None:
            render_battle_screen(screen, font, text_color, player, enemy, battle_turn, battle_actions, selected_action)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    #system exit
    sys.exit()

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
    
    #needs main screen

def intro_screen(screen, font, text_color, screen_width, screen_height, clock, text_lines):
    global current_scene
    # screen.fill((0, 0, 0))
    intro_text = ScrollingText('\n'.join(text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    
    screen.blit(intro_image, (0, 0))
    intro_music.play(-1)

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()
            if event.type == pygame.KEYDOWN:
                current_scene = "intro_screen"
                return
        intro_text.update()
        screen.fill((0, 0, 0))
        intro_text.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    current_scene = "intro_screen"

def stone_age_screen(screen, font, text_color, screen_width, screen_height, clock, stone_age_text_lines):
    global current_scene
    # screen.fill((0, 0, 0))
    stone_age_text = ScrollingText('\n'.join(stone_age_text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    
    screen.blit(stone_age_bg, (0, 0))
    stone_age_music.play(-1)

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                current_scene = "stone_age"
                return
        stone_age_text.update()
        screen.fill((0, 0, 0))
        stone_age_text.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    enemy = Caveman()

def medieval_time_screen(screen, font, text_color, screen_width, screen_height, clock, medieval_time_text_lines):
    global current_scene
    # screen.fill((0, 0, 0))
    medieval_time_text = ScrollingText('\n'.join(medieval_time_text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    
    screen.blit(medieval_time_bg, (0, 0))
    castle_music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                current_scene = "medieval_time"
                return
        medieval_time_text.update()
        screen.fill((0, 0, 0))
        medieval_time_text.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    enemy = Knight()

def red_district_screen(screen, font, text_color, screen_width, screen_height, clock, reddistrict_text_lines):
    global current_scene, player, enemy
    # screen.fill((0, 0, 0))
    red_district_text = ScrollingText('\n'.join(reddistrict_text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    
    screen.blit(red_district_bg, (0, 0))
    red_district_music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                current_scene = "red_district"
                return
        red_district_text.update()
        screen.fill((0, 0, 0))
        red_district_text.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    enemy = Ninja()

def wwii_screen(screen, font, text_color, screen_width, screen_height, clock, wwii_text_lines):
    global current_scene, player, enemy
    # screen.fill((0, 0, 0))
    wwii_text = ScrollingText('\n'.join(wwii_text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    
    screen.blit(WWII_bg (0, 0))
    wwii_music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                current_scene = "wwii"
                return
        wwii_text.update()
        screen.fill((0, 0, 0))
        wwii_text.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    enemy = Nazi_Soldier()

def modern_times_screen(screen, font, text_color, screen_width, screen_height, clock, modern_times_text_lines):
    global current_scene, player, enemy
    # screen.fill((0, 0, 0))
    modern_times_text = ScrollingText('\n'.join(modern_times_text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    
    screen.blit(Lexington_bg, (0, 0))
    Lexington_music.play(-1)
   
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                current_scene = "modern_times"
                return
        modern_times_text.update()
        screen.fill((0, 0, 0))
        modern_times_text.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    enemy = British_Soldier()

def mars_screen(screen, font, text_color, screen_width, screen_height, clock, mars_text_lines):
    global current_scene, player, enemy
    # screen.fill((0, 0, 0))
    mars_text = ScrollingText('\n'.join(mars_text_lines), font, text_color, screen_width, screen_height, scroll_speed=1, line_spacing=180)
    
    screen.blit(AlienPlot_bg, (0, 0))
    Mars_music.play(-1)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                current_scene = "mars"
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
