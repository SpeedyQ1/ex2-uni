import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lemonade Stand Game")

# Colors
WHITE = (255,255,255)
BLUE = (28,178,173)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Images
lemon_icon = pygame.image.load("assets/lemon_icon.png")
bill_icon = pygame.image.load("assets/bill_icon.png")
forecast_icon = pygame.image.load("assets/forecast_icon.png")
stand_image = pygame.image.load("assets/lemonade_stand.jpg")
line_image = pygame.image.load("assets/line.png")
sun_icon = pygame.image.load("assets/sun.png")
rain_icon = pygame.image.load("assets/rain.png")
storm_icon = pygame.image.load("assets/storm.png")

# Resize images
stand_image = pygame.transform.scale(stand_image, (300, 300))
line_image = pygame.transform.smoothscale(line_image, (line_image.get_width() * 150 // line_image.get_height(), 150))

# Resize icons
ICON_SIZE = (40, 40)
lemon_icon = pygame.transform.scale(lemon_icon, ICON_SIZE)
bill_icon = pygame.transform.scale(bill_icon, ICON_SIZE)
sun_icon = pygame.transform.scale(sun_icon, ICON_SIZE)
rain_icon = pygame.transform.scale(rain_icon, ICON_SIZE)
storm_icon = pygame.transform.scale(storm_icon, ICON_SIZE)

# Clock
clock = pygame.time.Clock()
FPS = 30

def get_weather():
    """Returns a random weather condition."""
    return random.choice(["Sunny", "Rainy", "Stormy"])

def draw_text(text, font, color, x, y):
    """Helper function to draw text on the screen."""
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def draw_header(day, lemons, lemons_age, dollars, today_weather):
    """Draws the header with current day information."""
    # Background for header
    pygame.draw.rect(screen, YELLOW, (0, 0, WIDTH, 100))

    # Lemon icon and quantity
    screen.blit(lemon_icon, (10, 30))  # Vertically center the icon
    draw_text(f"Fresh: {lemons_age[0]} | Old: {lemons_age[1]}", small_font, BLACK, 60, 45)

    # Determine weather icon
    if today_weather == "Sunny":
        weather_icon = sun_icon
    elif today_weather == "Rainy":
        weather_icon = rain_icon
    else:
        weather_icon = storm_icon

    # Display today's weather with icon
    weather_text_x = WIDTH // 2 - 70
    weather_icon_x = weather_text_x + 145
    draw_text("Today's Weather:", small_font, BLACK, weather_text_x, 45)
    screen.blit(weather_icon, (weather_icon_x, 45))

    # Bill icon and money
    screen.blit(bill_icon, (WIDTH - 150, 30))  # Vertically center the icon
    draw_text(f"${dollars:.2f}", small_font, BLACK, WIDTH - 100, 45)

    # Day number
    draw_text(f"Day {day}", font, BLACK, WIDTH // 2 - 50, 70)

def draw_start_screen():
    """Displays the start screen with instructions."""
    screen.fill(BLUE)
    draw_text("Welcome to the Lemonade Stand Game!", font, BLACK, WIDTH // 2 - 250, HEIGHT // 2 - 100)
    draw_text("Instructions:", small_font, BLACK, WIDTH // 2 - 100, HEIGHT // 2 - 50)
    draw_text("1. Use UP/DOWN to set lemon quantity.", small_font, BLACK, WIDTH // 2 - 100, HEIGHT // 2 - 20)
    draw_text("2. Press ENTER to confirm purchase.", small_font, BLACK, WIDTH // 2 - 100, HEIGHT // 2 + 10)
    draw_text("3. Sell lemonade based on weather.", small_font, BLACK, WIDTH // 2 - 100, HEIGHT // 2 + 40)
    draw_text("4. Maximize your profit over 4 days!", small_font, BLACK, WIDTH // 2 - 100, HEIGHT // 2 + 70)
    draw_text("Press SPACE to start!", font, WHITE, WIDTH // 2 - 150, HEIGHT // 2 + 120)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def simulate_day(day, lemons, lemons_age, dollars, forecast):
    """Simulates a single day in the lemonade stand game."""
    today_weather = forecast.pop(0)

    # Simulate customers
    if today_weather == "Sunny":
        customers = random.randint(15, 25)
    elif today_weather == "Rainy":
        customers = random.randint(5, 15)
    else:
        customers = random.randint(0, 5)

    buying = True
    lemons_to_buy = 0

    while buying:
        screen.fill(BLUE)
        draw_header(day, lemons, lemons_age, dollars, today_weather)

        # Calculate positions for stand and line
        stand_x = WIDTH // 2 - stand_image.get_width() // 2
        stand_y = HEIGHT - stand_image.get_height() - 10
        line_x = stand_x + stand_image.get_width() + 10  # Positioned to the right of the stand
        line_y = HEIGHT - line_image.get_height() - 10

        # Draw the stand image and line
        screen.blit(stand_image, (stand_x, stand_y))  # Stand centered at the bottom
        screen.blit(line_image, (line_x, line_y))  # Line to the right of the stand

        # Draw customer count on the line image
        draw_text(f"{customers} Customers", font, BLACK, line_x + line_image.get_width() // 2 - 50, line_y - 30)

        draw_text("How many lemons would you like to buy?", font, BLACK, WIDTH // 2 - 200, HEIGHT // 2 - 150)
        draw_text(f"Lemons to buy: {lemons_to_buy}", small_font, BLACK, WIDTH // 2 - 100, HEIGHT // 2 - 100)
        draw_text("(Use UP/DOWN to change, ENTER to confirm)", small_font, BLACK, WIDTH // 2 - 200, HEIGHT // 2 - 70)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    lemons_to_buy += 1
                elif event.key == pygame.K_DOWN:
                    lemons_to_buy = max(0, lemons_to_buy - 1)
                elif event.key == pygame.K_RETURN:
                    cost = lemons_to_buy * 0.50
                    if cost > dollars:
                        lemons_to_buy = 0
                    else:
                        dollars -= cost
                        lemons += lemons_to_buy
                        lemons_age[0] += lemons_to_buy
                    buying = False

    lemons_sold = min(customers, lemons)
    revenue = lemons_sold * 2
    dollars += revenue
    lemons -= lemons_sold
    lemons_age[0] = max(0, lemons_age[0] - lemons_sold)
    lemons_age[1] = max(0, lemons_age[1] - (lemons_sold - lemons_age[0]))

    # Age lemons
    lemons_age[1] += lemons_age[0]
    lemons_age[0] = 0

    # Discard lemons older than 2 days
    discarded_lemons = lemons - (lemons_age[0] + lemons_age[1])
    lemons -= discarded_lemons

    return lemons, lemons_age, dollars

def draw_game_over_screen(dollars):
    """Displays the game over screen with the option to restart."""
    screen.fill(BLUE)
    draw_text("Game Over!", font, BLACK, WIDTH // 2 - 100, HEIGHT // 2 - 100)
    draw_text(f"Your final score: ${dollars:.2f}", font, GREEN, WIDTH // 2 - 150, HEIGHT // 2 - 50)
    draw_text("Thank you for playing!", font, BLACK, WIDTH // 2 - 150, HEIGHT // 2)
    draw_text("Press R to restart or Q to quit.", small_font, BLACK, WIDTH // 2 - 150, HEIGHT // 2 + 50)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    play_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def play_game():
    """Main game loop for the lemonade stand game."""
    lemons = 20
    lemons_age = [20, 0]  # Fresh lemons and 1-day-old lemons
    dollars = 0.0
    days = 4  # Adjusted to 4 days

    # Generate initial weather forecast
    forecast = [get_weather() for _ in range(4)]

    draw_start_screen()

    for day in range(1, days + 1):
        # Ensure the forecast always has 4 days ahead
        if len(forecast) < 4:
            forecast.append(get_weather())

        # Simulate the day
        lemons, lemons_age, dollars = simulate_day(day, lemons, lemons_age, dollars, forecast)

        # End of day summary
        screen.fill(BLUE)
        draw_header(day, lemons, lemons_age, dollars, forecast[0])
        draw_text(f"End of Day {day}", font, BLACK, WIDTH // 2 - 100, HEIGHT // 2 - 50)
        draw_text(f"You have ${dollars:.2f}", small_font, BLACK, WIDTH // 2 - 100, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(2000)

    # Game over screen
    draw_game_over_screen(dollars)

if __name__ == "__main__":
    play_game()
    pygame.quit()
