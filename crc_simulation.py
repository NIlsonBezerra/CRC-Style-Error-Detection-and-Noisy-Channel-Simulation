import pygame
import random
import time

# Constants
WIDTH, HEIGHT = 1000, 450
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (240, 240, 240)
GREEN = (0, 255, 0)
RED = (255, 80, 80)
YELLOW = (255, 255, 0)
BLUE = (80, 180, 255)
GRAY = (100, 100, 100)
ORANGE = (255, 165, 0)

result_colors = {
    "GG": GREEN,
    "GB": ORANGE,
    "BB": RED,
    "BG": YELLOW
}

# Initialize
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CRC Conveyor Belt Simulation")
font = pygame.font.SysFont("Arial", 20)
bold_font = pygame.font.SysFont("Arial", 22, bold=True)
clock = pygame.time.Clock()


class Bit:
    def __init__(self, value, x, y, color=WHITE):
        self.value = value
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 40, 40), border_radius=6)
        text = font.render(str(self.value), True, BLACK)
        screen.blit(text, (self.x + 14, self.y + 10))


def generate_message():
    bits = [random.randint(0, 1) for _ in range(8)]
    base10 = sum(bits[i] * (2 ** (7 - i)) for i in range(8))
    checksum = base10 % 7
    cs_bits = [int(b) for b in format(checksum, '03b')]
    return bits + cs_bits, base10


def apply_noise(bits, p=0.05):
    noisy = bits.copy()
    for i in range(len(noisy)):
        if random.random() < p:
            noisy[i] = 1 - noisy[i]
    return noisy


def check_crc(bits):
    base = sum(bits[i] * (2 ** (7 - i)) for i in range(8))
    checksum = base % 7
    return [int(b) for b in format(checksum, '03b')], base


def draw_belt(y):
    pygame.draw.rect(screen, GRAY, (0, y + 20, WIDTH, 10))


def draw_gradient_bg():
    for i in range(HEIGHT):
        shade = 20 + int((i / HEIGHT) * 80)
        pygame.draw.line(screen, (shade, shade, shade), (0, i), (WIDTH, i))


def draw_stats(counts, result, ack, frame_count):
    result_color = result_colors.get(result, WHITE)
    screen.blit(font.render(f"ACK Bit: {ack}", True, GREEN if ack == 0 else RED), (580, 250))
    screen.blit(font.render(f"Result: {result}", True, result_color), (700, 250))
    screen.blit(font.render(f"Message #: {frame_count}", True, YELLOW), (800, 20))

    max_result = max(counts, key=counts.get)
    max_count = max(counts.values())
    max_bar_height = 100  # Total space allocated for bar height
    bar_bottom_y = HEIGHT - 20  # Where bars "sit" at the bottom

    x_pos = 50
    for label in ["GG", "GB", "BB", "BG"]:
        color = result_colors[label]
        count = counts[label]
        prefix = f"{label}: {count}"
        if label == max_result:
            prefix = f">>> {prefix} <<<"

        # Draw count label above the bar
        count_text = font.render(prefix, True, color)
        screen.blit(count_text, (x_pos, bar_bottom_y - max_bar_height - 30))

        # Calculate dynamic bar height
        if max_count > 0:
            bar_height = int((count / max_count) * max_bar_height)
        else:
            bar_height = 0

        # Draw bar safely below everything
        pygame.draw.rect(screen, color, (x_pos + 30, bar_bottom_y - bar_height, 30, bar_height), border_radius=3)

        x_pos += 220



def run_simulation():
    counts = {"GG": 0, "GB": 0, "BB": 0, "BG": 0}
    running = True
    frame_count = 0

    while running:
        bits, base = generate_message()
        noisy_bits = apply_noise(bits)
        received_checksum = noisy_bits[8:]
        recalculated_checksum, new_base = check_crc(noisy_bits)
        call_correct = received_checksum == recalculated_checksum

        if call_correct and base == new_base:
            result, ack = "GG", 0
        elif not call_correct and base == new_base:
            result, ack = "GB", 1
        elif not call_correct and base != new_base:
            result, ack = "BB", 1
        else:
            result, ack = "BG", 1

        counts[result] += 1
        frame_count += 1

        # Draw everything statically
        draw_gradient_bg()
        draw_belt(60)
        draw_belt(180)
        screen.blit(bold_font.render("Original Message + CRC (Sent)", True, WHITE), (50, 110))
        screen.blit(bold_font.render("Received Message (After Noise)", True, WHITE), (50, 230))

        for i in range(11):
            Bit(bits[i], 50 + i * 45, 60, GREEN if i < 8 else BLUE).draw()
            is_flipped = bits[i] != noisy_bits[i]
            color = RED if is_flipped else WHITE
            Bit(noisy_bits[i], 50 + i * 45, 180, color).draw()

        draw_stats(counts, result, ack, frame_count)
        pygame.display.flip()
        time.sleep(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


run_simulation()
