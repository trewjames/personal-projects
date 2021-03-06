import os

import pygame as pg

from projects.chess.engine import Board, Move
from projects.chess.resources import *

pg.init()
pg.font.init()
pg.display.set_caption("GAY CHESS")


def load_images():
    """
    Create a dictionary of pieces and their respective png
    Access img by IMAGES['wp'] --> white pawn img
    """
    pieces = ['r', 'n', 'b', 'q', 'k', 'p']

    for piece in pieces:
        # load black pieces
        img = pg.image.load(os.path.join("images", "b" + piece + ".png"))
        IMAGES['b' + piece] = pg.transform.scale(img, (SQ_SIZE, SQ_SIZE))

        # load white pieces
        img = pg.image.load(os.path.join("images", "w" + piece + ".png"))
        IMAGES['w' + piece] = pg.transform.scale(img, (SQ_SIZE, SQ_SIZE))


def draw_board(screen):
    """ Draw the back board grid """

    # Background border
    pg.draw.rect(screen, pg.Color(BORDER),
                 (0, 0, B_WIDTH + 2 * BORD, B_HEIGHT + 2 * BORD)
                 )

    # Rank/file labels
    label_font = pg.font.SysFont('arial', 20)
    rank_list = [8, 7, 6, 5, 4, 3, 2, 1]
    file_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    for row, x in enumerate(range(BORD, B_WIDTH, SQ_SIZE)):

        # file label
        file_label = label_font.render(f"{file_list[row]}",
                                       1, pg.Color('black'))
        screen.blit(file_label,
                    (x + (SQ_SIZE // 2) - (file_label.get_width() // 2), 810))

        for col, y in enumerate(range(BORD, B_HEIGHT, SQ_SIZE)):
            # rank label
            if row == 0:  # ensures rank labels only draws onces
                rank_label = label_font.render(f"{rank_list[col]}",
                                               1, pg.Color('black'))
                screen.blit(rank_label,
                            (810, y + (SQ_SIZE // 2) - (rank_label.get_height() // 2)))

            # grid
            if x % 200 == BORD and y % 200 == BORD or \
                    x % 200 != BORD and y % 200 != BORD:
                pg.draw.rect(screen, pg.Color(LIGHT_GRID),
                             (x, y, SQ_SIZE, SQ_SIZE)
                             )
            else:
                pg.draw.rect(screen, pg.Color(DARK_GRID),
                             (x, y, SQ_SIZE, SQ_SIZE)
                             )


def draw_pos_moves(screen, board, selection):
    """ Draw all possible moves, incl takes/castle etc"""
    pass


def draw_pieces(screen, board):
    """
    Draw the moving of pieces.
    Likely requires the refreshing of draws
    """
    for row, x in enumerate(range(BORD, B_WIDTH, SQ_SIZE)):
        for col, y in enumerate(range(BORD, B_HEIGHT, SQ_SIZE)):
            piece = board[row][col].name
            if piece != '--':
                screen.blit(IMAGES[piece], pg.Rect(y, x, SQ_SIZE, SQ_SIZE))

    # draw_last_move(screen, game)  # for future


def draw_move_suggestions(screen, suggestions):
    """
    Highlight move suggestions (all possible moves for selected piece)
    """
    for row, x in enumerate(range(BORD, B_WIDTH, SQ_SIZE)):
        for col, y in enumerate(range(BORD, B_HEIGHT, SQ_SIZE)):
            if (col, row) in suggestions:
                pg.draw.circle(screen, pg.Color(SUGGEST),
                               (x + SQ_SIZE // 2, y + SQ_SIZE // 2), S_RADIUS)


def draw_last_move(screen, game):
    """
    Draw color indicating last played move.
    """
    pass


def draw_game(screen, game):
    draw_board(screen)
    # draw_pos_moves(screen, game.board, selection)  # for future
    draw_pieces(screen, game.board)


def main():
    """
    Handles user inputs and graphics updates
    """
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color(BACKGROUND))

    game = Board()
    load_images()

    select_pos = None

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                if location[0] < BORD or location[0] > B_WIDTH + BORD \
                        or location[1] < BORD or location[1] > B_HEIGHT + BORD:
                    # checks that click locations is within bound of the board
                    continue
                col = (location[0] // SQ_SIZE)
                row = (location[1] // SQ_SIZE)
                if game.board[row][col].name != '--' and select_pos is None:
                    select_pos = (row, col)
                    move = Move(select_pos, game)
                    suggestions = move.moves
                elif select_pos is not None:  # second click
                    move.complete_move((row, col))
                    select_pos = None

        draw_game(screen, game)
        if select_pos is not None and suggestions is not None:
            draw_move_suggestions(screen, suggestions)
        clock.tick(MAX_FPS)
        pg.display.flip()


if __name__ == '__main__':
    main()
