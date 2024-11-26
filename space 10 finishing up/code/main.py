import pygame
from os.path import join
from random import randint, uniform

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
          
          
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        if keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()

# Star class
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

# Laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

# Meteor class
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.rotation_speed = randint(40, 80)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

# Animated Explosion class
class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        explosion_sound.play()

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

# Collision handling
def collisions():
    global running
    if pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask):
        global final_score
        final_score = (pygame.time.get_ticks() - start_time) // 1000
        running = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)

# Display the score
def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    text_surf = font.render(f"Score: {current_time}", True, (240, 240, 240))
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)

# Show Game Over screen
def show_game_over(screen):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    font = pygame.font.Font(None, 100)
    text_surface = font.render("GAME OVER", True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
    screen.blit(overlay, (0, 0))
    screen.blit(text_surface, text_rect)

    score_font = pygame.font.Font(None, 50)
    score_surface = score_font.render(f"Your Score: {final_score}", True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 20))
    screen.blit(score_surface, score_rect)

    restart_surface = score_font.render("Press ENTER to Restart or ESC to Exit", True, (255, 255, 255))
    restart_rect = restart_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 80))
    screen.blit(restart_surface, restart_rect)

# Show Start screen
def show_start_screen(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 100)
    title_surface = font.render("SPACE SHOOTER", True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
    screen.blit(title_surface, title_rect)

    instruction_font = pygame.font.Font(None, 50)
    instruction_surface = instruction_font.render("Press ENTER to Start", True, (200, 200, 200))
    instruction_rect = instruction_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 20))
    screen.blit(instruction_surface, instruction_rect)

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# Initialize Pygame
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 950
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()
running = True

# Load assets
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]
laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_music.play(loops=-1)

# Sprite groups
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

# Show the start screen
show_start_screen(display_surface)

# Add initial sprites
for _ in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 200)

# Initialize variables
start_time = pygame.time.get_ticks()
final_score = 0

# Game loop
while True:
    dt = clock.tick(60) / 1000  # Limit to 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # User clicked the close button
            pygame.quit()
            exit()
        if event.type == meteor_event:  # Spawn a meteor
            Meteor(meteor_surf, (randint(0, WINDOW_WIDTH), 0), (all_sprites, meteor_sprites))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()

    if running:
        collisions()
        all_sprites.update(dt)
        display_surface.fill((0, 0, 0))
        all_sprites.draw(display_surface)
        display_score()
    else:
        show_game_over(display_surface)
        if keys[pygame.K_RETURN]:
            running = True
            start_time = pygame.time.get_ticks()
            meteor_sprites.empty()
            laser_sprites.empty()
            all_sprites.empty()
            for _ in range(20):
                Star(all_sprites, star_surf)
            player = Player(all_sprites)

    pygame.display.flip()

pygame.quit()
