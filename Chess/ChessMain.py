

# Responsible for handling input for the engine to work
# We'll check and display the current GameState object


import pygame
from pygame.constants import SCRAP_SELECTION
import ChessEngine


# Pygame initializer
pygame.init()

# w = width, h = height
w = 512
h = 512

# Chess board dimensions = 8*8
dimension = 8

# Define square size
sq_size = h//dimension

# Movement animation
max_FPS = 15

# Image loading process
Images = {}

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wP", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:
        Images[piece] = pygame.transform.scale(pygame.image.load("Chess pieces/" + piece + ".png"), (sq_size, sq_size))

# End of image loading process

# Main function. Input and graphics management
def main():
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    selectSuqare = ()
    PlayerMove = []
    print("\nWhite        ***         Black")
    while running:
        for action in pygame.event.get():
            if action.type == pygame.QUIT:
                running = False
            elif action.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // sq_size
                row = location[1] // sq_size
                selectSquare = ()
                if selectSquare == (row, col):
                    selectSquare = ()
                    PlayerMove = []
                else:
                    selectSquare = (row ,col)
                    PlayerMove.append(selectSquare)
                if len(PlayerMove) == 2:
                    move = ChessEngine.Move(PlayerMove[0], PlayerMove[1], gs.board)  
                    gs.MakeMove(move)
                    selectSquare = ()
                    PlayerMove = []

                    if gs.CheckMate(move) == True :
                        drawGS(screen, gs)
                        clock.tick(max_FPS)
                        pygame.display.flip()
                        running = gs.EndGame(0)
                        x = input("Presione cualquier tecla para cerrar el tablero . . . . .\n\n\n")

            elif action.type == pygame.KEYDOWN:
                if action.key == pygame.K_z: 
                    gs.undoMove()

        drawGS(screen, gs)
        clock.tick(max_FPS)
        pygame.display.flip()

def drawBoard(screen):
    colors = [pygame.Color("white"), pygame.Color("burlywood4")]
    for i in range(dimension):
        for k in range(dimension):
            color = colors[(i+k)%2]
            pygame.draw.rect(screen, color, pygame.Rect(i*sq_size, k*sq_size, sq_size, sq_size))

def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(Images[piece], pygame.Rect(c*sq_size, r*sq_size, sq_size,sq_size))

def drawGS(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

if __name__ == "__main__":
    main()