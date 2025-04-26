import pygame

pygame.init()

# Screen setup
screen = pygame.display.set_mode((920, 600))
pygame.display.set_caption("My First Game")

# Hover button for lockdownHome.png
hover_button_rect = pygame.Rect(380, 415, 190, 140)

# Buttons for playerSelection.png
player_button_rects = [
    pygame.Rect(70, 170, 230, 330),
    pygame.Rect(360, 170, 230, 330),
    pygame.Rect(640, 170, 230, 330)
]

# New button rectangle for states 2 and up (at coordinates (317, 480), width 293, height 100)
new_button_rect = pygame.Rect(317, 480, 293, 100)
new_button_rect2 = pygame.Rect(40, 165, 330, 25)

# Game state
state = 7  # Start at the home screen
running = True

# Load and scale all images
homePage = pygame.transform.scale(pygame.image.load('lockdownHome.png'), (920, 600))
player_select_image = pygame.transform.scale(pygame.image.load('playerSelection.png'), (920, 600))
image_state_2 = pygame.transform.scale(pygame.image.load('Endscreen1Wins.png'), (920, 600))
image_state_3 = pygame.transform.scale(pygame.image.load('Endscreen2Wins.png'), (920, 600))
image_state_4 = pygame.transform.scale(pygame.image.load('EndscreenBothWin.png'), (920, 600))  # State 4 Image
image_3_player_1_win = pygame.transform.scale(pygame.image.load('3Player1Wins.png'), (920, 600))
image_3_player_2_win = pygame.transform.scale(pygame.image.load('3Player2Wins.png'), (920, 600))
image_3_player_3_win = pygame.transform.scale(pygame.image.load('3Player3Wins.png'), (920, 600))
image_3_player_no_winner = pygame.transform.scale(pygame.image.load('3PlayerNoWinner.png'), (920, 600))
image_blank = pygame.transform.scale(pygame.image.load('EndScreenBlank.png'), (920, 600))

# New state 8 image (SongSelectionNoImage.png)
song_selection_image = pygame.transform.scale(pygame.image.load('SongSelectionNoImage.png'), (920, 600))
song_selection_hover_image = pygame.transform.scale(pygame.image.load('SongSelection.png'), (920, 600))
fromTheStart_image = pygame.transform.scale(pygame.image.load('FromTheStartPlayer1.png'), (920, 600))

# Function to enlarge a portion of an image
def enlarge_image_portion(image, rect, factor=1.1):
    portion = image.subsurface(rect).copy()
    new_size = (int(rect.width * factor), int(rect.height * factor))
    enlarged_portion = pygame.transform.scale(portion, new_size)
    enlarged_image = image.copy()
    new_x = rect.x - (new_size[0] - rect.width) // 2
    new_y = rect.y - (new_size[1] - rect.height) // 2
    enlarged_image.blit(enlarged_portion, (new_x, new_y))
    return enlarged_image

# Fade transition setup
fade_done = {2: False, 3: False, 4: False, 5: False, 6: False, 7: False}  # Ensure fade_done tracks all states
fade_images = {
    2: (image_blank, image_state_2),
    3: (image_blank, image_state_3),
    4: (image_blank, image_state_4),
    5: (image_3_player_no_winner, image_3_player_1_win),
    6: (image_3_player_no_winner, image_3_player_2_win),
    7: (image_3_player_no_winner, image_3_player_3_win)
}

# Function to do a one-time fade
def fade_to_win(no_winner, winner, duration=1.0):
    steps = int(60 * duration)
    clock = pygame.time.Clock()
    for i in range(steps):
        alpha_no_winner = 255 - int(255 * (i / steps))
        alpha_winner = int(255 * (i / steps))

        temp_no_winner = no_winner.copy()
        temp_winner = winner.copy()
        temp_no_winner.set_alpha(alpha_no_winner)
        temp_winner.set_alpha(alpha_winner)

        screen.fill((0, 0, 0))
        screen.blit(temp_no_winner, (0, 0))
        screen.blit(temp_winner, (0, 0))
        pygame.display.flip()
        clock.tick(60)

# Timer variables
transition_time = 0  # The time when the transition happens
transition_delay = 500  # Delay in milliseconds (e.g., 500ms = 0.5 seconds)
can_click_buttons = True  # A flag to determine if buttons are clickable

# Main loop
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Quit the game when the window is closed

        # Handle State 1 (Home Page)
        if state == 1:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hover_button_rect.collidepoint(event.pos):
                    # Set the transition time when going to state 0
                    transition_time = pygame.time.get_ticks()
                    can_click_buttons = False  # Disable clicks temporarily
                    state = 0  # Transition to Player Selection (State 0)

        # Handle State 0 (Player Selection)
        if state == 0:
            if not can_click_buttons:
                # Check if enough time has passed since the transition to enable button clicks
                if pygame.time.get_ticks() - transition_time >= transition_delay:
                    can_click_buttons = True  # Enable button clicks

            if can_click_buttons and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if player_button_rects[0].collidepoint(event.pos):
                    numPlayers = 2
                    print(f"Number of players: {numPlayers}")
                    state = 8  # Transition to Song Selection (State 8)
                elif player_button_rects[1].collidepoint(event.pos):
                    numPlayers = 3
                    print(f"Number of players: {numPlayers}")
                    state = 8  # Transition to Song Selection (State 8)
                elif player_button_rects[2].collidepoint(event.pos):
                    numPlayers = 4
                    print(f"Number of players: {numPlayers}")
                    state = 8  # Transition to Song Selection (State 8)

        # Handle click on the new button in states 2, 3, 4, 5, 6, and 7
        if state in [2, 3, 4, 5, 6, 7]:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if new_button_rect.collidepoint(event.pos):
                    state = 1  # Go back to state 1 (main menu)

    # Drawing for different states
    if state == 1:
        # Home Page (State 1)
        if hover_button_rect.collidepoint(mouse_x, mouse_y):
            display = enlarge_image_portion(homePage, hover_button_rect)
        else:
            display = homePage
        screen.blit(display, (0, 0))

    elif state == 0:
        # Player Selection (State 0)
        display = player_select_image.copy()
        for rect in player_button_rects:
            if rect.collidepoint(mouse_x, mouse_y):
                display = enlarge_image_portion(player_select_image, rect)
                break
        screen.blit(display, (0, 0))

    elif state == 8:
        # Song Selection (State 8)
        if new_button_rect2.collidepoint(mouse_x, mouse_y):
            # Only change image if we are in state 8 and hovering over the button
            screen.blit(song_selection_hover_image, (0, 0))  # Change to SongSelection.png when hovered
            # Enlarge background portion when hovering over the new button area
            enlarged_background = enlarge_image_portion(song_selection_hover_image, new_button_rect2, factor=1.1)
            screen.blit(enlarged_background, (0, 0))  # Blit the enlarged portion of the background
        else:
            screen.blit(song_selection_image, (0, 0))  # Default Song Selection image
            # Enlarge background portion when not hovering (optional, or you can skip this step if you don't want it)
            enlarged_background = enlarge_image_portion(song_selection_image, new_button_rect2, factor=1.1)
            screen.blit(enlarged_background, (0, 0))  # Blit the enlarged portion of the background

    elif state in [2, 3, 4]:
        # Fade Transition for States 2, 3, 4
        if not fade_done[state]:
            fade_to_win(fade_images[state][0], fade_images[state][1], duration=1.0)
            fade_done[state] = True
        else:
            screen.blit(fade_images[state][1], (0, 0))

    elif state in [5, 6, 7]:
        # Fade Transition for States 5, 6, 7
        if not fade_done[state]:
            fade_to_win(fade_images[state][0], fade_images[state][1], duration=1.0)
            fade_done[state] = True
        else:
            screen.blit(fade_images[state][1], (0, 0))

    # Enlarge background on hover over new button area (only the specified rectangle)
    if state in [2, 3, 4, 5, 6, 7]:
        if new_button_rect.collidepoint(mouse_x, mouse_y):
            # Only enlarge and change image if hovering over the button area
            enlarged_background = enlarge_image_portion(fade_images[state][1], new_button_rect, factor=1.1)
            screen.blit(enlarged_background, (0, 0))  # Blit the enlarged portion of the background
        else:
            screen.blit(fade_images[state][1], (0, 0))

    pygame.display.flip()

pygame.quit()
