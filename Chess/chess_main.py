import chess
import chess.pgn
import chess.svg

import pygame

import chess_ai

# SETTINGS

# The color that you will play as
p_color = "w"

# Depth of the Ai, Recomended: 3, for a Challenge: 6
# Anything above 4 might take a while
depth = 2

pygame.init()
pygame.mixer.init()

window_w = 600
window_h = window_w

square_size = round(window_w / 8)

window = pygame.display.set_mode((window_w, window_h))

black = ((0, 0, 0))
white = ((255, 255, 255))
grey = ((100, 100, 100))


images = {}
move = []
squares = []

cols = ["a", "b", "c", "d", "e", "f", "g", "h"]

# Loading the images
pieces = ["P", "N", "B", "R", "Q", "K"]
for piece in pieces:
    images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece.lower() + "w.png"), (square_size, square_size))

pieces = ["p", "n", "b", "r", "q", "k"]
for piece in pieces:
    images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + "b.png"), (square_size, square_size))


board = chess.Board()

if p_color == "w":
    ai_color = "b"
else:
    ai_color = "w"

turn = "w"

run = True

def show_board():
    # print(board.unicode())

    window.fill(grey)

    # Drawing the chess board
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(window, white, (j * square_size * 2, i * square_size * 2, square_size, square_size))

    for i in range(4):
        for j in range(4):
            pygame.draw.rect(window, white, (j * square_size * 2 + square_size, i * square_size * 2 + square_size, square_size, square_size))

    # Drawing the pieces
    pygame.font.init()

    if p_color == "w":

        i = -1
        for row in range(8):
            i += 1
            j = -1
            for col in range(-7, 1):
                j += 1
                square_index = j * 8 + i
                square = chess.SQUARES[square_index]
                piece = board.piece_at(square)

                if piece != None:
                    piece_symbol = piece.symbol()

                    window.blit(images[piece_symbol], (row * square_size, -col * square_size))

    else:

        i = -1
        for row in range(-7, 1):
            i += 1
            j = -1
            for col in range(8):
                j += 1
                square_index = j * 8 + i
                square = chess.SQUARES[square_index]
                piece = board.piece_at(square)

                if piece != None:
                    piece_symbol = piece.symbol()

                    window.blit(images[piece_symbol], (-row * square_size, col * square_size))

    pygame.display.update()

def take_input():

    global board
    global turn
    global move
    global squares

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            if p_color == "w":
                for i in range(8):
                    for j in range(8):
                        if pos[0] > i * square_size and pos[0] < i * square_size + square_size:
                            if pos[1] > j * square_size and pos[1] < j * square_size + square_size:
                                move.append(str(cols[i]))
                                move.append(str(-j + 8))
                                squares.append(chess.square(j, i))

            else:
                for i in range(8):
                    for j in range(8):
                        if pos[0] > i * square_size and pos[0] < i * square_size + square_size:
                            if pos[1] > j * square_size and pos[1] < j * square_size + square_size:
                                move.append(str(cols[-i + 7]))
                                move.append(str(j + 1))
                                squares.append(chess.square(j, i))


    if len(move) == 4:
        final_move = move[0] + move[1] + move[2] + move[3]
        try:
            board.push_uci(final_move)
            print("Move Made")

            if board.is_check():
                pygame.mixer.music.load("sounds/check.wav")
                pygame.mixer.music.play(0)
            else:
                pygame.mixer.music.load("sounds/move.wav")
                pygame.mixer.music.play(0)

            turn = ai_color
        except:
            try:
                final_move = final_move + "q"
                board.push_uci(final_move)
                print("Move Made")

                if board.is_check():
                    pygame.mixer.music.load("sounds/check.wav")
                    pygame.mixer.music.play(0)
                else:
                    pygame.mixer.music.load("sounds/move.wav")
                    pygame.mixer.music.play(0)

                turn = ai_color
            except:
                print("Illegal Move")
                move = []
                squares = []

    show_board()

def main():
    global turn
    global run
    global move
    global squares

    turn = "w"
    while run:
        if turn == p_color:
            take_input()
        if turn == ai_color:

            move = chess_ai.minimax(board, depth, ai_color)
            print("Ai plays: " + move)
            board.push_san(move)

            turn = p_color
            move = []
            squares = []

            if board.is_check():
                pygame.mixer.music.load("sounds/check.wav")
                pygame.mixer.music.play(0)
            else:
                pygame.mixer.music.load("sounds/move.wav")
                pygame.mixer.music.play(0)

main()
