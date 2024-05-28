from flask import Flask, render_template
import pygame
import math
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_animation')
def get_animation():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    BLACK = (0, 0, 0)

    clock = pygame.time.Clock()

    def draw_lights(angle):
        light_radius = 10
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        distance_from_center = 200

        x = center_x + distance_from_center * math.cos(math.radians(angle))
        y = center_y + distance_from_center * math.sin(math.radians(angle)))

        pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), light_radius)

    angle = 0

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "Animation stopped"

        for i in range(0, 360, 30):
            draw_lights(angle + i)

        angle += 2
        angle %= 360

        # Save the animation as an image
        pygame.image.save(screen, 'https://images.rawpixel.com/image_png_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvdjk1OC1iYWNrZ3JvdW5kLWhlaW4tMDJfMS5wbmc.png')

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    # Check if the animation image exists, if not, generate it
    if not os.path.exists('https://images.rawpixel.com/image_png_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvdjk1OC1iYWNrZ3JvdW5kLWhlaW4tMDJfMS5wbmc.png'):
        get_animation()
    
    app.run(debug=True)
