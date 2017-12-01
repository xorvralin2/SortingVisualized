import pygame
import math
from random import shuffle

# Define some colours
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

# Setting up important variables
unsorted = [x * 5 for x in range(1, 80)]
shuffle(unsorted)
global highlighted
global sorting_type
pygame.init()
#  stats = [Comparisons, Array accesses]
stats = [0, 0]

class Screen_text(object):
    """
    Wrapper class for pygame.font. 
    Used for easier syntax and method aliasing.
    """

    def __init__(self, text, pos):
        self.font = pygame.font.SysFont("Calibri", 25, True, False)
        self.screen_text = self.font.render(text, True, WHITE)
        self.pos = pos

    def draw(self):
        screen.blit(self.screen_text, self.pos)

    def update(self, new_text):
        self.screen_text = self.font.render(new_text, True, WHITE)

sorter = Screen_text(f"Sorter: None", (10, 10))
stats_text = Screen_text(f"Comparisons: {stats[0]}     Array Accesses: {stats[1]}", (300, 10))


def draw_list(array):
    """
    Draws input list onto the pygame window.
    Used for rendering the list during sorting.
    """
    offset = 10
    bar_width = 10
    gap = 5
    y_pos = 595
    for index, bar in enumerate(array):
        if index in highlighted:
            pygame.draw.rect(screen, RED, [offset, y_pos - bar, bar_width, bar])
        else:
            pygame.draw.rect(screen, WHITE, [offset, y_pos - bar, bar_width, bar])
        offset += bar_width + gap

# Setting up the pygame window and making it not resizable
size = (1200, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sorting Visualized")

done = False
clock = pygame.time.Clock()

def update(highlights):
    """
    Updates important variables and calls important methods for updating the pygame screen.
    Also draws everything except for the unsorted list. ( Although it calls the draw_list() function)
    """
    global highlighted
    highlighted = highlights
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True
    screen.fill(BLACK)
    draw_list(unsorted)

    sorter.update(f"Sorter: {sorting_type}")
    sorter.draw()
    stats_text.update(f"Comparisons: {stats[0]}     Array Accesses: {stats[1]}")
    stats_text.draw()

    pygame.display.flip()
    x = clock.tick(100)


def gnome_sort():
    """
    Sorts unsorted while updating the screen during every iteration.
    """
    i = 0
    while True:
        if update([i, i- 1]):
            return
        if i == len(unsorted):
            global sorting_type
            sorting_type = None
            return
        elif i == 0:
            i += 1
        elif unsorted[i - 1] > unsorted[i]:
            stats[0] += 1
            stats[1] += 2
            tmp = unsorted[i]
            stats[1] += 1
            unsorted[i] = unsorted[i - 1]
            stats[1] += 1
            unsorted[i - 1] = tmp
            i -= 1
        else:
            i+=1

def insertion_sort():
    """
    Sorts unsorted while updating the screen during every iteration.
    """
    global sorting_type
    for i in range(1,len(unsorted)):
        j = i
        temp = unsorted[j]
        stats[1] += 1
        while j > 0 and temp < unsorted[j-1]:
            stats[0] += 1
            update([j, i])
            unsorted[j] = unsorted[j-1]
            stats[1] += 2
            j=j-1
        unsorted[j] = temp
    sorting_type = None

def selection_sort():
    """
    Sorts unsorted while updating the screen during every iteration.
    """
    global sorting_type
    for i in range(0, len(unsorted)):
        small = i
        for j in range(i, len(unsorted)):
            update([i, j, small])
            if unsorted[j] < unsorted[small]:
                stats[0] += 1
                small = j
        unsorted[i], unsorted[small] = unsorted[small], unsorted[i]
        stats[1] += 3
    sorting_type = None

def bubble_sort():
    """
    Sorts unsorted while updating the screen during every iteration.
    """
    global sorting_type
    s_length = len(unsorted) - 1
    while s_length > 0:
        for j in range(0, s_length):
            update([j, j + 1])
            stats[0] += 1
            stats[1] += 2
            if unsorted[j] > unsorted[j + 1]:
                unsorted[j], unsorted[j + 1] = unsorted[j + 1], unsorted[j]
                stats[1] += 3
        s_length -=1
    sorting_type = None

def coctail_sort():
    """
    Sorts unsorted while updating the screen during every iteration.
    Basically a bi-directional bubble sort.
    """
    global sorting_type
    s_length = len(unsorted) - 1
    s_min = 0
    alt = False
    swapped = True
    while s_length > s_min and swapped:
        swapped = False
        if alt: # Decending
            for j in range(s_length, s_min, -1):
                update([j, j - 1])
                if unsorted[j - 1] > unsorted[j]:
                    swapped = True
                    unsorted[j], unsorted[j - 1] = unsorted[j - 1], unsorted[j]
            s_min += 1
            alt = False
        else: # Ascending
            for j in range(s_min, s_length):
                update([j, j + 1])
                if unsorted[j] > unsorted[j + 1]:
                    swapped = True
                    unsorted[j], unsorted[j + 1] = unsorted[j + 1], unsorted[j]
            s_length -=1
            alt = True
    sorting_type = None

def get_parent_index(node):
    """
    Finds the index of the parent node for a given node.
    Used for heapifying.
    """
    return math.floor(node / 2 - 0.5)

def heapify_node(node, array):
    """
    Places one node into its correct position by swapping it with every smaller parent node.
    """
    global stats
    i = node
    while i > 0:
        if array[i] > array[get_parent_index(i)]:
            array[i], array[get_parent_index(i)] = array[get_parent_index(i)], array[i]
            update([i, get_parent_index(i)])
            stats[0] += 1
            stats[1] += 5
            i = get_parent_index(i)
        else:
            break

def heapify_heap(array, partition):
    """
    Heapifies every node in the list.
    """
    # Heapifies from end to start
    n = partition
    while n > 0:
        heapify_node(n, array)
        n -= 1

def test_heap(array, partition):
    """
    Returns whether a partition of a list is following a max heap structure or not.
    The partition is from the start of the list to the partition index.
    """
    global stats
    i = partition
    while i > 0:
        if array[i] > array[get_parent_index(i)]:
            stats[0] += 1
            stats[1] += 2
            return False
        i -= 1
    return True

def heapify(array, partition):
    """
    Repeatedly calls heapify_heap if the list is not already a heap.
    """
    # Heapify_heap isn't always enough to create a heap
    # Sometimes smaller node are shifted down from positions higher up which aren't caught on the first try
    # This is semi-inefficient but it works for now
    while test_heap(unsorted, partition) != True:
        heapify_heap(unsorted, partition)

def heap_sort():
    """
    Sorts the list by removing the root node from the heap, replacing it with the last node and re-heapifying.
    """
    global sorting_type
    global stats
    heap_end = len(unsorted) - 1
    heapify(unsorted, heap_end)
    new_arr = []
    while heap_end >= 0:
        unsorted[0], unsorted[heap_end] = unsorted[heap_end], unsorted[0]
        stats[1] += 3
        heapify(unsorted, heap_end - 1)
        # Shrinking the heap to exclude already correctly placed items
        heap_end -= 1
    sorting_type = None

def help_me():
    """
    Prints availible sorting algorithms.
    Called by get_command().
    """
    availible_commands = ["Bubble", "Gnome", "Insertion", "Selection", "Coctail", "Heap"]
    print("Availible sorting algorithms:\n-----------------------------")
    for command in availible_commands:
        print(command)
    print("-----------------------------\nEnter one of the availible commands below to run that algorithm")

def set_alg(alg):
    """
    Sets sorting_type to the appropriate string based on the input.
    Called by get_command().
    """
    global sorting_type
    global unsorted
    stats[0] = 0
    stats[1] = 0
    sorting_type = alg.lower() + " sort"
    sorting_type = sorting_type.title()

def get_command():
    """
    Gets the desired action from the user..
    Then calls the appropriate function for that purpose.
    """
    command = input(">>> ").lower()
    if command == "help":
        help_me()
    elif command == "shuffle":
        shuffle(unsorted)
    elif command == "exit":
        return True
    else:
        set_alg(command)


sorting_type = None
# Main loop that drives the program until exited
while not update([]):
    if get_command():
        break
    if sorting_type == "Gnome Sort":
        gnome_sort()
    elif sorting_type == "Insertion Sort":
        insertion_sort()
    elif sorting_type == "Selection Sort":
        selection_sort()
    elif sorting_type == "Bubble Sort":
        bubble_sort()
    elif sorting_type == "Coctail Sort":
        coctail_sort()
    elif sorting_type == "Heap Sort":
        heap_sort()
# Safely quitting pygame without causing exception
pygame.quit()
