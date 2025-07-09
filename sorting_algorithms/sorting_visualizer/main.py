import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting and Searching Algorithm Visualization")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font
FONT = pygame.font.SysFont('arial', 20)

def generate_array(n, min_val, max_val):
    """Generates an array of n random integers."""
    return [random.randint(min_val, max_val) for _ in range(n)]

def draw_array(arr, color_positions={}):
    """Draws the array as bars."""
    bar_width = WIDTH / len(arr)
    for i, val in enumerate(arr):
        color = color_positions.get(i, WHITE)
        pygame.draw.rect(SCREEN, color, (i * bar_width, HEIGHT - val, bar_width, val))

def draw_text(text, x, y):
    """Draws text on the screen."""
    text_surface = FONT.render(text, True, WHITE)
    SCREEN.blit(text_surface, (x, y))

def bubble_sort(arr, draw_array_callback):
    """Sorts an array using the Bubble Sort algorithm."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                draw_array_callback(arr, {j: GREEN, j + 1: RED})
                yield True
    return arr

def insertion_sort(arr, draw_array_callback):
    """Sorts an array using the Insertion Sort algorithm."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            draw_array_callback(arr, {j + 1: GREEN, i: RED})
            yield True
        arr[j + 1] = key
    return arr

def merge_sort(arr, draw_array_callback):
    """Sorts an array using the Merge Sort algorithm."""
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        yield from merge_sort(L, draw_array_callback)
        yield from merge_sort(R, draw_array_callback)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            draw_array_callback(arr, {k - 1: GREEN})
            yield True

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            draw_array_callback(arr, {k - 1: GREEN})
            yield True

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            draw_array_callback(arr, {k - 1: GREEN})
            yield True
    return arr

def quick_sort(arr, low, high, draw_array_callback):
    """Sorts an array using the Quick Sort algorithm."""
    if low < high:
        pi = yield from partition(arr, low, high, draw_array_callback)
        yield from quick_sort(arr, low, pi - 1, draw_array_callback)
        yield from quick_sort(arr, pi + 1, high, draw_array_callback)
    return arr

def partition(arr, low, high, draw_array_callback):
    """Partitions the array for Quick Sort."""
    i = (low - 1)
    pivot = arr[high]

    for j in range(low, high):
        if arr[j] < pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
            draw_array_callback(arr, {i: GREEN, j: RED, high: BLUE})
            yield True
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    draw_array_callback(arr, {i + 1: GREEN, high: RED})
    yield True
    return (i + 1)

BLUE = (0, 0, 255)

def linear_search(arr, target, draw_array_callback):
    """Searches for a target in an array using Linear Search."""
    for i in range(len(arr)):
        if arr[i] == target:
            draw_array_callback(arr, {i: GREEN})
            yield True
            return i
        draw_array_callback(arr, {i: RED})
        yield True
    return -1

def binary_search(arr, target, draw_array_callback):
    """Searches for a target in a sorted array using Binary Search."""
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            draw_array_callback(arr, {mid: GREEN})
            yield True
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
        draw_array_callback(arr, {low: RED, high: RED, mid: BLUE})
        yield True
    return -1

def main():
    """Main application loop."""
    run = True
    clock = pygame.time.Clock()

    array = generate_array(50, 50, 500)
    sorting_algorithm = None
    sorting_algorithm_generator = None
    searching_algorithm = None
    searching_algorithm_generator = None
    target = None

    while run:
        clock.tick(60)
        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    array = generate_array(50, 50, 500)
                    sorting_algorithm = None
                    sorting_algorithm_generator = None
                    searching_algorithm = None
                    searching_algorithm_generator = None
                if event.key == pygame.K_b:
                    sorting_algorithm = bubble_sort
                    sorting_algorithm_generator = sorting_algorithm(array, lambda arr, cp: (draw_array(arr, cp), pygame.display.update()))
                if event.key == pygame.K_i:
                    sorting_algorithm = insertion_sort
                    sorting_algorithm_generator = sorting_algorithm(array, lambda arr, cp: (draw_array(arr, cp), pygame.display.update()))
                if event.key == pygame.K_m:
                    sorting_algorithm = merge_sort
                    sorting_algorithm_generator = sorting_algorithm(array, lambda arr, cp: (draw_array(arr, cp), pygame.display.update()))
                if event.key == pygame.K_q:
                    sorting_algorithm = quick_sort
                    sorting_algorithm_generator = sorting_algorithm(array, 0, len(array) - 1, lambda arr, cp: (draw_array(arr, cp), pygame.display.update()))
                if event.key == pygame.K_l:
                    target = random.choice(array)
                    searching_algorithm = linear_search
                    searching_algorithm_generator = searching_algorithm(array, target, lambda arr, cp: (draw_array(arr, cp), pygame.display.update()))
                if event.key == pygame.K_s:
                    array.sort()
                    target = random.choice(array)
                    searching_algorithm = binary_search
                    searching_algorithm_generator = searching_algorithm(array, target, lambda arr, cp: (draw_array(arr, cp), pygame.display.update()))

        if sorting_algorithm_generator:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting_algorithm_generator = None
        
        if searching_algorithm_generator:
            try:
                next(searching_algorithm_generator)
            except StopIteration:
                searching_algorithm_generator = None

        draw_array(array)
        draw_text("R - Reset | B - Bubble | I - Insertion | M - Merge | Q - Quick | L - Linear Search | S - Binary Search", 10, 10)
        if target:
            draw_text(f"Target: {target}", 10, 40)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
