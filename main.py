import pygame
from ai import getText
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
state = 1  # Start at the home screen
running = True

# Load and scale all images from the static folder
homePage = pygame.transform.scale(pygame.image.load('static/HomePage.png'), (920, 600))
player_select_image = pygame.transform.scale(pygame.image.load('static/Player Selection.png'), (920, 600))
image_state_2 = pygame.transform.scale(pygame.image.load('static/Endscreen1Wins.png'), (920, 600))
image_state_3 = pygame.transform.scale(pygame.image.load('static/Endscreen2Wins.png'), (920, 600))
image_state_4 = pygame.transform.scale(pygame.image.load('static/EndscreenBothWin.png'), (920, 600))  # State 4 Image
image_3_player_1_win = pygame.transform.scale(pygame.image.load('static/3Player1Wins.png'), (920, 600))
image_3_player_2_win = pygame.transform.scale(pygame.image.load('static/3Player2Wins.png'), (920, 600))
image_3_player_3_win = pygame.transform.scale(pygame.image.load('static/3Player3Wins.png'), (920, 600))
image_3_player_no_winner = pygame.transform.scale(pygame.image.load('static/3PlayerNoWinner.png'), (920, 600))
image_blank = pygame.transform.scale(pygame.image.load('static/EndScreenBlank.png'), (920, 600))

# New state 8 image (SongSelectionNoImage.png)
song_selection_image = pygame.transform.scale(pygame.image.load('static/SongSelectionNoImage.png'), (920, 600))
song_selection_hover_image = pygame.transform.scale(pygame.image.load('static/SongSelection.png'), (920, 600))
fromTheStart_image = pygame.transform.scale(pygame.image.load('static/FromTheStartPlayer1.png'), (920, 600))
fromTheStart_image2 = pygame.transform.scale(pygame.image.load('static/FromTheStartPlayer2.png'), (920, 600))

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

# Add a variable to store the AI response
ai_response1 = ""
ai_response2 = ""


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

        # Handle State 8 (Song Selection)
        elif state == 8:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if new_button_rect2.collidepoint(event.pos):
                    state = 9  # Transition to a new state (e.g., State 9) for FromTheStartPlayer1

        elif state == 9:
            # Display the FromTheStartPlayer1 image
            screen.blit(fromTheStart_image, (0, 0))
            # Add lyrics to the screen
            lyrics = [
                "Don't you notice how",
                "I get quiet when there's no one else around?",
                "Me and you and awkward silence",
                "Don't you dare look at me that way",
                "I don't need reminders of how you don't feel the same",
                "Oh, the burning pain",
                "Listening to you harp on 'bout some new soulmate",
                "'She's so perfect,' blah, blah, blah",
                "Oh, how I wish you'll wake up one day",
                "Run to me, confess your love, at least just let me say",
                "That when I talk to you, oh, Cupid walks right through",
                "And shoots an arrow through my heart",
                "And I sound like a loon, but don't you feel it too?",
                "Confess I loved you from the start",
                # "What's a girl to do?",
                # "Lying on my bed, staring into the blue",
                # "Unrequited, terrifying",
                # "Love is driving me a bit insane",
                # "Have to get this off my chest",
                # "I'm telling you today"
            ]

            font = pygame.font.Font(None, 24)  # Use a default font with size 36

            for i, line in enumerate(lyrics):
                lyrics_text = font.render(line, True, (255, 255, 255))  # White text color
                screen.blit(lyrics_text, (140, 70 + i * 30))  # Display each line with spacing

            # Call getText only once and store the result
            if ai_response1 == "":
                            
                # Render the frame before starting the recording
                pygame.display.flip()
                ai_response1 = getText()  # Call getText only the first time State 9 is entered
            
            # Render the stored AI response on the screen
            font = pygame.font.Font(None, 36)  # Use a default font with size 36
            rendered_text = font.render(ai_response1, True, (255, 255, 255))  # White text color
            screen.blit(rendered_text, (50, 500))  # Display the text at the bottom of the screen

            # Add a button to transition to Player 2 (State 10)
            next_button_rect = pygame.Rect(750, 300, 150, 50)  # Button for "Next Player"
            pygame.draw.rect(screen, (0, 255, 0), next_button_rect)  # Green button
            next_text = font.render("Next Player", True, (0, 0, 0))  # Black text
            screen.blit(next_text, (next_button_rect.x + 10, next_button_rect.y + 10))

            # Check for button click to transition to Player 2
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if next_button_rect.collidepoint(event.pos):
                    state = 10  # Transition to Player 2 (State 10)

        elif state == 10:
            # Display the FromTheStartPlayer1 image (reuse for Player 2)
            screen.blit(fromTheStart_image, (0, 0))
            
            # Add lyrics to the screen
            lyrics = [
                "Don't you notice how",
                "I get quiet when there's no one else around?",
                "Me and you and awkward silence",
                "Don't you dare look at me that way",
                "I don't need reminders of how you don't feel the same",
                "Oh, the burning pain",
                "Listening to you harp on 'bout some new soulmate",
                "'She's so perfect,' blah, blah, blah",
                "Oh, how I wish you'll wake up one day",
                "Run to me, confess your love, at least just let me say",
                "That when I talk to you, oh, Cupid walks right through",
                "And shoots an arrow through my heart",
                "And I sound like a loon, but don't you feel it too?",
                "Confess I loved you from the start",
                # "What's a girl to do?",
                # "Lying on my bed, staring into the blue",
                # "Unrequited, terrifying",
                # "Love is driving me a bit insane",
                # "Have to get this off my chest",
                # "I'm telling you today"
            ]

            font = pygame.font.Font(None, 24)  # Use a default font with size 36

            for i, line in enumerate(lyrics):
                lyrics_text = font.render(line, True, (255, 255, 255))  # White text color
                screen.blit(lyrics_text, (140, 70 + i * 30))  # Display each line with spacing

                
            # Call getText only once and store the result
            if ai_response2 == "":
                            
                # Render the frame before starting the recording
                pygame.display.flip()
                ai_response2 = getText()  # Call getText only the first time State 10 is entered
            
            # Render the stored AI response on the screen
            font = pygame.font.Font(None, 36)  # Use a default font with size 36
            rendered_text = font.render(ai_response2, True, (255, 255, 255))  # White text color
            screen.blit(rendered_text, (50, 500))  # Display the text at the bottom of the screen

            # Add a button to transition to results or next state
            finish_button_rect = pygame.Rect(750, 300, 150, 50)  # Button for "Finish"
            pygame.draw.rect(screen, (255, 0, 0), finish_button_rect)  # Red button
            finish_text = font.render("Finish", True, (0, 0, 0))  # Black text
            screen.blit(finish_text, (finish_button_rect.x + 10, finish_button_rect.y + 10))

            # Check for button click to transition to results or next state
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if finish_button_rect.collidepoint(event.pos):
                    state = 11  # Transition to results or next state

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
            screen.blit(song_selection_hover_image, (0, 0))  # Change to SongSelection.png when hovered
        else:
            screen.blit(song_selection_image, (0, 0))  # Default Song Selection image

    elif state == 9:
        # Display the FromTheStartPlayer1 image
        screen.blit(fromTheStart_image, (0, 0))
        
        # Add lyrics to the screen
        lyrics = [
            "Don't you notice how",
            "I get quiet when there's no one else around?",
            "Me and you and awkward silence",
            "Don't you dare look at me that way",
            "I don't need reminders of how you don't feel the same",
            "Oh, the burning pain",
            "Listening to you harp on 'bout some new soulmate",
            "'She's so perfect,' blah, blah, blah",
            "Oh, how I wish you'll wake up one day",
            "Run to me, confess your love, at least just let me say",
            "That when I talk to you, oh, Cupid walks right through",
            "And shoots an arrow through my heart",
            "And I sound like a loon, but don't you feel it too?",
            "Confess I loved you from the start",
            # "What's a girl to do?",
            # "Lying on my bed, staring into the blue",
            # "Unrequited, terrifying",
            # "Love is driving me a bit insane",
            # "Have to get this off my chest",
            # "I'm telling you today"
        ]
        font = pygame.font.Font(None, 24)  # Use a default font with size 36

        for i, line in enumerate(lyrics):
            lyrics_text = font.render(line, True, (255, 255, 255))  # White text color
            screen.blit(lyrics_text, (140, 70 + i * 30))  # Display each line with spacing

        
        # Call getText only once and store the result
        if ai_response1 == "":
            
            # Render the frame before starting the recording
            pygame.display.flip()
            ai_response1 = getText()  # Call getText only the first time State 9 is entered
        
        # Render the stored AI response on the screen
        font = pygame.font.Font(None, 24)  # Use a default font with size 36
        rendered_text = font.render(ai_response1, True, (255, 255, 255))  # White text color
        screen.blit(rendered_text, (50, 500))  # Display the text at the bottom of the screen

        # Add a button to transition to Player 2 (State 10)
        next_button_rect = pygame.Rect(750, 300, 150, 50)  # Button for "Next Player"
        pygame.draw.rect(screen, (0, 255, 0), next_button_rect)  # Green button
        next_text = font.render("Next Player", True, (0, 0, 0))  # Black text
        screen.blit(next_text, (next_button_rect.x + 10, next_button_rect.y + 10))

        # Check for button click to transition to Player 2
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if next_button_rect.collidepoint(event.pos):
                state = 10  # Transition to Player 2 (State 10)

    elif state == 10:
        # Display the FromTheStartPlayer1 image (reuse for Player 2)
        screen.blit(fromTheStart_image2, (0, 0))
        
        # Add lyrics to the screen
        lyrics = [
            "Don't you notice how",
            "I get quiet when there's no one else around?",
            "Me and you and awkward silence",
            "Don't you dare look at me that way",
            "I don't need reminders of how you don't feel the same",
            "Oh, the burning pain",
            "Listening to you harp on 'bout some new soulmate",
            "'She's so perfect,' blah, blah, blah",
            "Oh, how I wish you'll wake up one day",
            "Run to me, confess your love, at least just let me say",
            "That when I talk to you, oh, Cupid walks right through",
            "And shoots an arrow through my heart",
            "And I sound like a loon, but don't you feel it too?",
            "Confess I loved you from the start",
            # "What's a girl to do?",
            # "Lying on my bed, staring into the blue",
            # "Unrequited, terrifying",
            # "Love is driving me a bit insane",
            # "Have to get this off my chest",
            # "I'm telling you today"
        ]

        font = pygame.font.Font(None, 24)  # Use a default font with size 36

        for i, line in enumerate(lyrics):
            lyrics_text = font.render(line, True, (255, 255, 255))  # White text color
            screen.blit(lyrics_text, (140, 70 + i * 30))  # Display each line with spacing

        
        # Call getText only once and store the result
        if ai_response2 == "":
            # Render the frame before starting the recording
            pygame.display.flip()

            ai_response2 = getText()  # Call getText only the first time State 10 is entered
        
        # Render the stored AI response on the screen
        font = pygame.font.Font(None, 36)  # Use a default font with size 36
        rendered_text = font.render(ai_response2, True, (255, 255, 255))  # White text color
        screen.blit(rendered_text, (50, 500))  # Display the text at the bottom of the screen

        # Add a button to transition to results or next state
        finish_button_rect = pygame.Rect(750, 300, 150, 50)  # Button for "Finish"
        pygame.draw.rect(screen, (255, 0, 0), finish_button_rect)  # Red button
        finish_text = font.render("Finish", True, (0, 0, 0))  # Black text
        screen.blit(finish_text, (finish_button_rect.x + 10, finish_button_rect.y + 10))
        button_click_delay = 5000  # Delay in milliseconds (e.g., 2000ms = 2 seconds)
        button_click_time = 0  # Time when the button becomes clickable
        
        if pygame.time.get_ticks() - button_click_time >= button_click_delay:  # Check if delay has passed
            # Check for button click to transition to results or next state
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if finish_button_rect.collidepoint(event.pos):
                    print("ai_response2[10]: " + ai_response2[10])
                    print("ai_response1[10]: " + ai_response1[10])
                
                    if ai_response2[10] > ai_response1[10]:
                        # If the responses are the same, transition to state 11
                        state = 11
                    elif ai_response2[10] < ai_response1[10]:
                        # If the responses are different, transition to state 12
                        state = 12
                    else:
                        state = 13   
    elif state == 11:
        # Display the Player 1 Wins screen
        screen.blit(image_state_2, (0, 0))  # Use the Player 1 Wins image
        font = pygame.font.Font(None, 36)
        winner_text = font.render("Player 1 Wins!", True, (255, 255, 255))  # White text
        screen.blit(winner_text, (350, 500))  # Display the text at the bottom of the screen

        # Add a "Play Again" button using new_button_rect
        pygame.draw.rect(screen, (0, 255, 0), new_button_rect)  # Green button
        play_again_text = font.render("Play Again", True, (0, 0, 0))  # Black text
        screen.blit(play_again_text, (new_button_rect.x + 10, new_button_rect.y + 10))

        # Check for button click to play again
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if new_button_rect.collidepoint(event.pos):
                state = 1  # Transition back to the main menu
    elif state == 12:
        # Display the Player 2 Wins screen
        screen.blit(image_state_3, (0, 0))  # Use the Player 2 Wins image
        font = pygame.font.Font(None, 36)
        winner_text = font.render("Player 2 Wins!", True, (255, 255, 255))  # White text
        screen.blit(winner_text, (350, 500))  # Display the text at the bottom of the screen

        # Add a "Play Again" button using new_button_rect
        pygame.draw.rect(screen, (0, 255, 0), new_button_rect)  # Green button
        play_again_text = font.render("Play Again", True, (0, 0, 0))  # Black text
        screen.blit(play_again_text, (new_button_rect.x + 10, new_button_rect.y + 10))

        # Check for button click to play again
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if new_button_rect.collidepoint(event.pos):
                state = 1  # Transition back to the main menu

    elif state == 13:
        # Display the Player 2 Wins screen
        screen.blit(image_state_4, (0, 0))  # Use the Player 2 Wins image
        font = pygame.font.Font(None, 36)
        winner_text = font.render("Draw!", True, (255, 255, 255))  # White text
        screen.blit(winner_text, (350, 500))  # Display the text at the bottom of the screen

        # Add a "Play Again" button using new_button_rect
        pygame.draw.rect(screen, (0, 255, 0), new_button_rect)  # Green button
        play_again_text = font.render("Play Again", True, (0, 0, 0))  # Black text
        screen.blit(play_again_text, (new_button_rect.x + 10, new_button_rect.y + 10))

        # Check for button click to play again
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if new_button_rect.collidepoint(event.pos):
                state = 1  # Transition back to the main menu

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