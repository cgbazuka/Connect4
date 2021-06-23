import numpy as np                  # For using matrix
import pygame                       # For game loop ,events, graphics and sound
import sys                          # We will use sys.exit to exit the program
import math                         # For using floor function

# Global Variables

BLUE = (0, 0, 255)                  # Defining RGB values of colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

GAME_SOUNDS = {}                    # Dictionary to store game sounds

ROW_COUNT = 6
COLUMN_COUNT = 7

# functions

def create_board():                             # creating game board with matrix
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):         # Assign player to board location (matrix)
    board[row][col] = piece


def is_valid_location(board, col):              # Checks if top row of a column is zero, it returns value true or false
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):              # filling empty spaces with player moves, replacing 0s with 1 and 2 by checking if position is 0
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):                         # flips board matrix
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def draw_board(board):                                      # filling game with graphics
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

# initalize pygame
pygame.init()

# Start sound
GAME_SOUNDS['background'] = pygame.mixer.Sound('Sounds/backgroung.wav')
GAME_SOUNDS['player'] = pygame.mixer.Sound('Sounds/move.wav')
GAME_SOUNDS['win'] = pygame.mixer.Sound('Sounds/win.wav')
GAME_SOUNDS['background'].play()

# caption
pygame.display.set_caption("Connect 4")

# define our screen size
SQUARESIZE = 100

# define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
# Calling function draw_board again
draw_board(board)
pygame.display.update()

# define font
myfont = pygame.font.SysFont("monospace", 75)                   # (name, size, bold, italics)

# ---------------------------------------------------------------------------------------------
# GAME LOOP

while not game_over:

    # Grapics part
    for event in pygame.event.get():                       # Take EVENT as input from player
        if event.type == pygame.QUIT:                      # Quitting game from cross click
            sys.exit()

        if event.type == pygame.MOUSEMOTION:               # This executes when you hover mouse on screen
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]                            # posx records x coordinate of mouse, event.pos gives array [x,y]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)      # draw player 1 motion
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)   # draw player 2 motion
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:            # This executes when you click mouse button on screen
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            GAME_SOUNDS['player'].play()                    # Sound to indicate player has chosen his position
            # ---------------------------------------------------------------------------------------------
            # Ask if it was Player 1 Input
            if turn == 0:
                posx = event.pos[0]                         # posx records x coordinate of mouse, event.pos gives array [x,y]
                col = int(math.floor(posx / SQUARESIZE))    # using floor functions to round off x coordinate

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        GAME_SOUNDS['background'].stop()     # background sound stops
                        GAME_SOUNDS['win'].play()            # winning sound starts
                        game_over = True                     # Exit from game loop game_over

            # ---------------------------------------------------------------------------------------------
            # # Ask if it was Player 2 Input
            else:
                posx = event.pos[0]                           # posx records x coordinate of mouse, event.pos gives array [x,y]
                col = int(math.floor(posx / SQUARESIZE))      # using floor functions to round off x coordinate

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        GAME_SOUNDS['background'].stop()        # posx records x coordinate of mouse
                        GAME_SOUNDS['win'].play()               # winning sound starts
                        game_over = True                        # Exit from game loop game_over

            print_board(board)                                  # print matrix
            draw_board(board)                                   # print graphics

            turn += 1                                           # turn changes in each while loop
            turn = turn % 2

            if game_over:
                pygame.time.wait(7000)