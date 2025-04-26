import turtle

# Screen
screen = turtle.Screen()
screen.title("Button Example")

# Global variable to track screen state
current_screen = "menu"

# Button details
button = turtle.Turtle()
button.hideturtle()
button_size = 1  # Normal size
hovered = False  # Track if hovering

# Draw menu function
def draw_menu():
    screen.bgcolor("yellow")
    button.clear()
    button.penup()
    button.goto(-50 * button_size, 0 * button_size)
    button.pendown()
    button.begin_fill()
    for _ in range(2):
        button.forward(100 * button_size)
        button.right(90)
        button.forward(50 * button_size)
        button.right(90)
    button.end_fill()

    # Draw button text
    button.penup()
    button.goto(0, -20 * button_size)
    button.color("white")
    button.write("Start", align="center", font=("Arial", int(16 * button_size), "normal"))
    button.color("black")  # reset color

# When clicking the button
def go_to_game(x, y):
    if -50 * button_size < x < 50 * button_size and -50 * button_size < y < 0 * button_size:
        global current_screen
        current_screen = "game"
        draw_game()

# Draw the second screen
def draw_game():
    screen.clear()
    button.clear()
    button.penup()
    button.goto(0, 0)
    button.write("You're in the game now! 🎮", align="center", font=("Arial", 24, "bold"))

# Check mouse hovering manually
def check_hover():
    global button_size, hovered
    x, y = turtle.getcanvas().winfo_pointerx() - screen.window_width() // 2, \
           screen.window_height() // 2 - turtle.getcanvas().winfo_pointery()

    if -50 < x < 50 and -50 < y < 0:
        if not hovered:
            button_size = 1.2
            hovered = True
            draw_menu()
    else:
        if hovered:
            button_size = 1
            hovered = False
            draw_menu()

    # Call this function again after a short delay
    screen.ontimer(check_hover, 50)  # Check every 50 milliseconds

# Draw menu first
draw_menu()

# Listen for clicks
screen.onclick(go_to_game)

# Start checking hover
check_hover()

# Keep the window open
turtle.done() 