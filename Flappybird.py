import os
import random
import sys
import tempfile
from pathlib import Path

import pygame

# Optional mobile-friendly support for touch devices
try:
    from android import activity
except ImportError:
    activity = None

# Initialize pygame
try:
    pygame.init()
    pygame.mixer.init()
except pygame.error:
    pass

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
PIPE_WIDTH = 50
PIPE_GAP = 180

# Use a scale factor based on the actual display size so the game looks better on different phone screens.
try:
    info = pygame.display.Info()
except pygame.error:
    info = None

if info is not None:
    BASE_SCALE = min(info.current_w / SCREEN_WIDTH, info.current_h / SCREEN_HEIGHT)
    scale = max(0.8, min(1.0, BASE_SCALE))
    scaled_width = int(SCREEN_WIDTH * scale)
    scaled_height = int(SCREEN_HEIGHT * scale)
else:
    scale = 1.0
    scaled_width = SCREEN_WIDTH
    scaled_height = SCREEN_HEIGHT

try:
    pygame.display.set_mode((scaled_width, scaled_height), pygame.SCALED)
    screen = pygame.display.get_surface()
except pygame.error:
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
font_name = "Arial"
game_font = pygame.font.SysFont(font_name, 40)
small_font = pygame.font.SysFont(font_name, 24)
large_font = pygame.font.SysFont(font_name, 48, bold=True)

base_dir = Path(__file__).resolve().parent
HIGH_SCORE_FILE = base_dir / "highscore.txt"
ALLOWED_ASSET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".wav", ".ogg", ".mp3"}


def sanitize_high_score(value):
    try:
        numeric_value = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, min(numeric_value, 1_000_000))


def resolve_asset_path(filename):
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("Asset filename must be a non-empty string")

    raw_name = filename.strip()
    path_parts = Path(raw_name).parts
    if os.path.isabs(raw_name) or raw_name in {".", ".."} or raw_name.startswith("~") or ".." in path_parts:
        raise ValueError("Asset filename must remain inside the project folder")

    candidate_names = []
    if Path(raw_name).suffix:
        candidate_names.append(raw_name)
    else:
        candidate_names.append(raw_name)
        for extension in [".png", ".jpg", ".jpeg", ".wav", ".ogg", ".mp3"]:
            candidate_names.append(f"{raw_name}{extension}")

    for candidate in candidate_names:
        candidate_path = Path(candidate)
        if candidate_path.name != candidate or ".." in candidate_path.parts:
            continue

        full_path = (base_dir / candidate).resolve()
        try:
            full_path.relative_to(base_dir.resolve())
        except ValueError:
            continue

        if full_path.exists() and full_path.is_file():
            if full_path.suffix.lower() in ALLOWED_ASSET_EXTENSIONS:
                return full_path

    raise FileNotFoundError(f"Could not find a safe asset for '{filename}' in {base_dir}")


def load_image(filename, convert_alpha=False):
    path = resolve_asset_path(filename)
    image = pygame.image.load(str(path))
    return image.convert_alpha() if convert_alpha else image.convert()


def load_sound(filename):
    try:
        path = resolve_asset_path(filename)
        return pygame.mixer.Sound(str(path))
    except (FileNotFoundError, ValueError, pygame.error):
        return None


def load_high_score():
    if not HIGH_SCORE_FILE.exists():
        return 0
    try:
        return sanitize_high_score(HIGH_SCORE_FILE.read_text(encoding="utf-8").strip())
    except (ValueError, OSError):
        return 0


def save_high_score(value):
    safe_value = sanitize_high_score(value)
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(base_dir)) as handle:
            handle.write(str(safe_value))
            temp_name = handle.name
        os.replace(temp_name, HIGH_SCORE_FILE)
    except OSError:
        pass


def draw_text(surface, text, font, x, y, color, shadow=True):
    if shadow:
        shadow_surface = font.render(text, True, (0, 0, 0))
        surface.blit(shadow_surface, (x + 2, y + 2))
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))


def safe_audio_play(sound):
    try:
        if sound is not None:
            sound.play()
    except pygame.error:
        pass


# Load assets using the script directory so they work reliably
background = load_image("background")
bird_image = load_image("player", convert_alpha=True)
pipe_image = load_image("pipe", convert_alpha=True)

# Scale assets to match the game window so they don't appear oversized
background = pygame.transform.scale(background, screen.get_size())
bird_image = pygame.transform.smoothscale(bird_image, (max(24, int(34 * scale)), max(18, int(24 * scale))))
pipe_image = pygame.transform.smoothscale(pipe_image, (max(30, int(PIPE_WIDTH * scale)), max(300, int(500 * scale))))

jump_sound = load_sound("jump.wav")
point_sound = load_sound("point.wav")
die_sound = load_sound("die.wav")

# Game variables
bird_y = 300
bird_movement = 0
gravity = 0.20
pipe_list = []
score = 0
score_counted = []
high_score = load_high_score()
ad_option_visible = False
ad_option_timer = 0.0
ad_option_claimed = False
ad_option_started = False
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

game_active = True


def reset_game():
    global bird_y, bird_movement, pipe_list, score, score_counted, game_active, ad_option_visible, ad_option_timer, ad_option_claimed, ad_option_started
    bird_y = 300
    bird_movement = 0
    pipe_list.clear()
    score_counted.clear()
    score = 0
    game_active = True
    ad_option_visible = False
    ad_option_timer = 0.0
    ad_option_claimed = False
    ad_option_started = False


def revive_from_ad():
    global bird_y, bird_movement, pipe_list, score_counted, game_active, ad_option_visible, ad_option_timer, ad_option_claimed, ad_option_started
    bird_y = 300
    bird_movement = 0
    pipe_list.clear()
    score_counted.clear()
    game_active = True
    ad_option_visible = False
    ad_option_timer = 0.0
    ad_option_claimed = False
    ad_option_started = False


def check_collision(bird_rect, pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            safe_audio_play(die_sound)
            return False

    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        safe_audio_play(die_sound)
        return False

    return True


def main():
    global bird_y, bird_movement, pipe_list, score, score_counted, game_active, high_score, ad_option_visible, ad_option_timer, ad_option_claimed, ad_option_started

    reset_game()

    if activity is not None:
        activity.set_orientation("portrait")

    running = True
    while running:
        dt = clock.tick(120) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = -6
                    safe_audio_play(jump_sound)
                elif event.key == pygame.K_SPACE and not game_active:
                    reset_game()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_active:
                    bird_movement = -6
                    safe_audio_play(jump_sound)
                elif not game_active and ad_option_visible:
                    ad_button_rect = pygame.Rect(110, 365, 180, 38)
                    if ad_button_rect.collidepoint(event.pos):
                        revive_from_ad()
                    else:
                        reset_game()
                else:
                    reset_game()

            elif event.type == SPAWNPIPE and game_active:
                pipe_top_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 120)
                top_pipe = pygame.Rect(
                    SCREEN_WIDTH,
                    0,
                    max(30, int(PIPE_WIDTH * scale)),
                    pipe_top_height,
                )
                bottom_pipe = pygame.Rect(
                    SCREEN_WIDTH,
                    pipe_top_height + PIPE_GAP,
                    max(30, int(PIPE_WIDTH * scale)),
                    SCREEN_HEIGHT - (pipe_top_height + PIPE_GAP),
                )
                pipe_list.append(top_pipe)
                pipe_list.append(bottom_pipe)

        if (
            not game_active
            and not ad_option_claimed
            and not ad_option_started
        ):
            ad_option_started = True
            ad_option_visible = True
            ad_option_timer = 5.0

        if ad_option_visible and not game_active:
            ad_option_timer = max(0.0, ad_option_timer - dt)
            if ad_option_timer <= 0:
                ad_option_visible = False
                ad_option_timer = 0.0
                ad_option_started = False

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        if game_active:
            bird_movement += gravity
            bird_y += bird_movement
            bird_rect = pygame.Rect(
                50,
                int(bird_y),
                bird_image.get_width(),
                bird_image.get_height(),
            )
            screen.blit(bird_image, bird_rect)

            for pipe in pipe_list:
                pipe.centerx -= 3
                pipe_surface = pygame.transform.scale(pipe_image, (pipe.width, pipe.height))

                if pipe.top <= 0:
                    flipped_pipe = pygame.transform.flip(pipe_surface, False, True)
                    screen.blit(flipped_pipe, pipe)
                else:
                    screen.blit(pipe_surface, pipe)

                if (
                    pipe.top > 0
                    and 45 < pipe.centerx < 55
                    and pipe not in score_counted
                ):
                    safe_audio_play(point_sound)
                    score_counted.append(pipe)
                    score += 1
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)

            game_active = check_collision(bird_rect, pipe_list)
            pipe_list = [pipe for pipe in pipe_list if pipe.right > 0]
        else:
            panel_x = 60
            panel_y = 210
            panel_w = 280
            panel_h = 170
            pygame.draw.rect(
                screen,
                (20, 20, 30),
                (panel_x, panel_y, panel_w, panel_h),
            )
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (panel_x, panel_y, panel_w, panel_h),
                3,
            )

            draw_text(
                screen,
                "GAME OVER",
                large_font,
                panel_x + 28,
                panel_y + 18,
                (255, 255, 255),
            )
            draw_text(
                screen,
                f"Score: {score}",
                game_font,
                panel_x + 78,
                panel_y + 78,
                (255, 240, 120),
            )
            draw_text(
                screen,
                f"Best: {high_score}",
                game_font,
                panel_x + 83,
                panel_y + 122,
                (120, 230, 255),
            )

            if ad_option_visible:
                ad_button_rect = pygame.Rect(panel_x + 50, panel_y + 155, 180, 38)
                pygame.draw.rect(
                    screen,
                    (0, 180, 90),
                    ad_button_rect,
                )
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    ad_button_rect,
                    3,
                )
                draw_text(
                    screen,
                    f"Watch Ad ({int(ad_option_timer) + 1}s)",
                    small_font,
                    ad_button_rect.x + 18,
                    ad_button_rect.y + 8,
                    (255, 255, 255),
                )
            else:
                draw_text(
                    screen,
                    "Press SPACE to Retry",
                    small_font,
                    panel_x + 38,
                    panel_y + 165,
                    (255, 255, 255),
                )

        draw_text(screen, f"Score: {score}", small_font, 10, 10, (255, 240, 120))
        draw_text(screen, f"Best: {high_score}", small_font, 10, 38, (120, 230, 255))

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()