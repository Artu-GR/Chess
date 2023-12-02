
# We'll store the data inputed in the 'main', in other words store all the information about the current state of the chess game
# Responsible for determining the valid moves (p/piece)
# Move log

import ChessMain
from dataclasses import dataclass
from re import A
from tkinter import W


class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteMove = True
        self.log = []
        self.moveLog = []
        self.pieceLog = []
    
    def promotion(self, move):
        #print(self.log[-1], "  Normal log\n", self.moveLog[-1], "  Move log\n")
        promotion = input("Press the letter according to the piece you want: \n 'Q'\t Queen\n 'R'\t Rook\n 'N'\t Night\n 'B'\t Bishop\n")
        move.PieceMoved = move.PieceMoved[0] + promotion.upper()
        self.pieceLog.pop
        self.pieceLog.append(move.PieceMoved)
        
    def castling(self, move):
        if move.S_row == move.E_row and abs(move.E_col - move.S_col) == 2:
            for p_move in self.log:
                if p_move.PieceMoved == "wK" and move.PieceMoved == "wK":
                    return False
                elif p_move.PieceMoved == "bK" and move.PieceMoved == "bK":
                    return False

            if move.E_col > move.S_col: #Move to the right (Castled right)
                for i in range(move.S_col+1, 7):
                    if self.board[move.E_row][i] != "--":
                        return False
                for p_move in self.log:
                    if p_move.PieceMoved[1] == 'R' and p_move.PieceMoved[0] == move.PieceMoved[0]:
                        if p_move.S_row == 7 and p_move.S_col == 7:
                            return False
                        elif p_move.S_row == 0 and p_move.S_col == 7:
                            return False
                if move.PieceMoved[0] == 'w':
                    self.board[7][7] = "--"
                    self.board[7][5] = "wR"
                else:
                    self.board[0][7] = "--"
                    self.board[0][5] = "bR"

            else: #Move to the left (Castled left)
                for i in range(move.S_col-1, 0, -1):
                    if self.board[move.E_row][i] != "--":
                        return False
                for p_move in self.log:
                    if p_move.PieceMoved[1] == 'R' and p_move.PieceMoved[0] == move.PieceMoved[0]:
                        if p_move.S_row == 7 and p_move.S_col == 0:
                            return False
                        elif p_move.S_row == 0 and p_move.S_col == 0:
                            return False
                if move.PieceMoved[0] == 'w':
                    self.board[7][0] = "--"
                    self.board[7][3] = "wR"
                else:
                    self.board[0][0] = "--"
                    self.board[0][3] = "bR"
        
        return True

    def findKings(self):
        positions = [-1, -1, -1, -1]

        for row in range (0, 8):
            for col in range (0, 8):
                if(self.board[row][col] == "wK"):
                    positions[0] = row
                    positions[1] = col
                elif(self.board[row][col] == "bK"):
                    positions[2] = row
                    positions[3] = col
        
        return positions

    def illegalByCheck(self, move):
        #Make a continious analysis of the board. Determine what positions are attacked by a opponent's piece
        blocked4white = []

        blocked4black = []

        for row in range(0, 8):
            for col in range(0, 8):
                if self.board[row][col] == "bR":
                    for i in range(row+1, 8): #below
                        blocked4white.append([i, col])
                        if self.board[i][col] != "--":
                            break
                    for i in range(row-1, -1, -1): #above
                        blocked4white.append([i, col])
                        if self.board[i][col] != "--":
                            break
                    for i in range(col+1, 8): #right
                        blocked4white.append([row, i])
                        if self.board[row][i] != "--":
                            break
                    for i in range(col-1, -1, -1): #left
                        blocked4white.append([row, i])
                        if self.board[row][i] != "--":
                            break

                elif self.board[row][col] == "bB":
                    k = col
                    for i in range(row+1, 8):
                        k += 1
                        if k > 7: break
                        blocked4white.append([i, k])
                        if self.board[i][k] != "--":
                            break
                    k = col
                    for i in range(row+1, 8):
                        k -= 1
                        if k < 0: break
                        blocked4white.append([i, k])
                        if self.board[i][k] != "--":
                            break
                    k = col
                    for i in range(row-1, -1, -1):
                        k += 1
                        if k > 7: break
                        blocked4white.append([i, k])
                        if self.board[i][k] != "--":
                            break
                    k = col
                    for i in range(row-1, -1, -1):
                        k -= 1
                        if k < 0: break
                        blocked4white.append([i, k])
                        if self.board[i][k] != "--":
                            break

                elif self.board[row][col] == "bN":
                    if row+2 <= 7:
                        if col+1 <= 7:
                            blocked4white.append([row+2, col+1])
                        if col-1 >= 0:
                            blocked4white.append([row+2, col-1])
                    if row-2 >= 0:
                        if col+1 <= 7:
                            blocked4white.append([row-2, col+1])
                        if col-1 >= 0:
                            blocked4white.append([row-2, col-1])
                    if col+2 <= 7:
                        if row+1 <= 7:
                            blocked4white.append([row+1, col+2])
                        if row-1 >= 0:
                            blocked4white.append([row-1, col+2])
                    if col-2 >= 0:
                        if row+1 <= 7:
                            blocked4white.append([row+1, col-2])
                        if row-1 >= 0:
                            blocked4white.append([row-1, col-2])

                elif self.board[row][col] == "bP":
                    if row+1 <= 7:
                        if col+1 <= 7:
                            blocked4white.append([row+1, col+1])
                        if col-1 >= 0:
                            blocked4white.append([row+1, col-1])

                elif self.board[row][col] == "bQ":
                    for i in range(row+1, 8): #below
                        blocked4white.append([i, col])
                        if self.board[i][col] != "--":
                            break
                    for i in range(row-1, -1, -1): #above
                        blocked4white.append([i, col])
                        if self.board[i][col] != "--":
                            break
                    for i in range(col+1, 8): #right
                        blocked4white.append([row, i])
                        if self.board[row][i] != "--":
                            break
                    for i in range(col-1, -1, -1): #left
                        blocked4white.append([row, i])
                        if self.board[row][i] != "--":
                            break

                    k = col
                    for i in range(row+1, 8):
                        k += 1
                        if k > 7: break
                        blocked4white.append([i, k])
                        if self.board[i][k] != "--":
                            break
                    k = col
                    for i in range(row+1, 8):
                        k -= 1
                        if k < 0: break
                        blocked4white.append([i, k])
                        if self.board[i][k] != "--":
                            break
                    k = col
                    for i in range(row-1, -1, -1):
                        k += 1
                        if k > 7: break
                        blocked4white.append([i, k])
                        if self.board[i][k] != "--":
                            break
                    k = col
                    for i in range(row-1, -1, -1):
                        k -= 1
                        if k < 0: break
                        blocked4white.append([i, k])
                        if self.board[i][k] != "--":
                            break

                elif self.board[row][col] == 'bK':
                    if row+1 <= 7:
                        blocked4white.append([row+1, col])
                        if col+1 <= 7:
                            blocked4white.append([row+1, col+1])
                        if col-1 >= 0:
                            blocked4white.append([row+1, col-1])
                    if row-1 >= 0:
                        blocked4white.append([row-1, col])
                        if col+1 <= 7:
                            blocked4white.append([row-1, col+1])
                        if col-1 >= 0:
                            blocked4white.append([row-1, col-1])
                    if col+1 <= 7:
                        blocked4white.append([row, col+1])
                    if col-1 >= 0:
                        blocked4white.append([row, col-1])


                elif self.board[row][col] == "wR":
                    for i in range(row+1, 8): #below
                        blocked4black.append([i, col])
                        if self.board[i][col] != "--":
                            break
                    for i in range(row-1, -1, -1): #above
                        blocked4black.append([i, col])
                        if self.board[i][col] != "--":
                            break
                    for i in range(col+1, 8): #right
                        blocked4black.append([row, i])
                        if self.board[row][i] != "--":
                            break
                    for i in range(col-1, -1, -1): #left
                        blocked4black.append([row, i])
                        if self.board[row][i] != "--":
                            break

                elif self.board[row][col] == "wB":
                    k = col
                    for i in range(row+1, 8):
                        k += 1
                        if k > 7: break
                        blocked4black.append([i, k])
                        if self.board[i][k] != "--":
                            break
                    k = col
                    for i in range(row+1, 8):
                        k -= 1
                        if k < 0: break
                        blocked4black.append([i, k])
                        if self.board[i][k] != "--":
                            break
                    k = col
                    for i in range(row-1, -1, -1):
                        k += 1
                        if k > 7: break
                        blocked4black.append([i, k])
                        if self.board[i][k] != "--":
                            break
                    k = col
                    for i in range(row-1, -1, -1):
                        k -= 1
                        if k < 0: break
                        blocked4black.append([i, k])
                        if self.board[i][k] != "--":
                            break

                elif self.board[row][col] == "wN":
                    if row+2 <= 7:
                        if col+1 <= 7:
                            blocked4black.append([row+2, col+1])
                        if col-1 >= 0:
                            blocked4black.append([row+2, col-1])
                    if row-2 >= 0:
                        if col+1 <= 7:
                            blocked4black.append([row-2, col+1])
                        if col-1 >= 0:
                            blocked4black.append([row-2, col-1])
                    if col+2 <= 7:
                        if row+1 <= 7:
                            blocked4black.append([row+1, col+2])
                        if row-1 >= 0:
                            blocked4black.append([row-1, col+2])
                    if col-2 >= 0:
                        if row+1 <= 7:
                            blocked4black.append([row+1, col-2])
                        if row-1 >= 0:
                            blocked4black.append([row-1, col-2])

                elif self.board[row][col] == "wP":
                    if row-1 <= 7:
                        if col+1 <= 7:
                            blocked4black.append([row-1, col+1])
                        if col-1 >= 0:
                            blocked4black.append([row-1, col-1])

                elif self.board[row][col] == "wQ":
                    for i in range(row+1, 8): #below
                        blocked4black.append([i, col])
                        if self.board[i][col] != "--":
                            break
                    for i in range(row-1, -1, -1): #above
                        blocked4black.append([i, col])
                        if self.board[i][col] != "--":
                            break
                    for i in range(col+1, 8): #right
                        blocked4black.append([row, i])
                        if self.board[row][i] != "--":
                            break
                    for i in range(col-1, -1, -1): #left
                        blocked4black.append([row, i])
                        if self.board[row][i] != "--":
                            break

                    k = col
                    for i in range(row+1, 8):
                        k += 1
                        if k > 7: break
                        blocked4black.append([i, k])
                        if self.board[i][k] != "--":
                            break
                    k = col
                    for i in range(row+1, 8):
                        k -= 1
                        if k < 0: break
                        blocked4black.append([i, k])
                        if self.board[i][k] != "--":
                            break
                    k = col
                    for i in range(row-1, -1, -1):
                        k += 1
                        if k > 7: break
                        blocked4black.append([i, k])
                        if self.board[i][k] != "--":
                            break
                    k = col
                    for i in range(row-1, -1, -1):
                        k -= 1
                        if k < 0: break
                        blocked4black.append([i, k])
                        if self.board[i][k] != "--":
                            break

                elif self.board[row][col] == 'wK':
                    if row+1 <= 7:
                        blocked4black.append([row+1, col])
                        if col+1 <= 7:
                            blocked4black.append([row+1, col+1])
                        if col-1 >= 0:
                            blocked4black.append([row+1, col-1])
                    if row-1 >= 0:
                        blocked4black.append([row-1, col])
                        if col+1 <= 7:
                            blocked4black.append([row-1, col+1])
                        if col-1 >= 0:
                            blocked4black.append([row-1, col-1])
                    if col+1 <= 7:
                        blocked4black.append([row, col+1])
                    if col-1 >= 0:
                        blocked4black.append([row, col-1])

        return [blocked4white, blocked4black]
    #End illegalByCheck

    def check4check(self, move, blocked4white, blocked4black):
        positions = self.findKings()

        if self.whiteMove:
            valid_move = any([positions[0], positions[1]] == checked for checked in blocked4white)
            if not valid_move:
                return True
            else:
                return False     

        else:
            valid_move = any([positions[2], positions[3]] == checked for checked in blocked4black)
            if not valid_move:
                return True
            else:
                return False
    #End check4check

    def checkMove(self, move):

        self.board[move.E_row][move.E_col] = move.PieceMoved
        self.board[move.S_row][move.S_col] = "--"

        blocked = self.illegalByCheck(move)

        if self.check4check(move, blocked[0], blocked[1]) == False:
            self.board[move.S_row][move.S_col] = move.PieceMoved
            self.board[move.E_row][move.E_col] = move.PieceCaptured
            return False
        else:
            self.board[move.S_row][move.S_col] = move.PieceMoved
            self.board[move.E_row][move.E_col] = move.PieceCaptured
            return True
    #End checkMove

    def CheckMate(self, move):
        blocked = self.illegalByCheck(move)
        blockedCounter = 0

        positions = self.findKings()

        if self.check4check(move, blocked[0], blocked[1]) == False:
            if self.whiteMove:
                #Check by black
                kR = positions[0]
                kC = positions[1]
                kingMoves = [[kR, kC+1], [kR, kC-1], [kR-1, kC], [kR-1, kC-1], [kR-1, kC+1], [kR+1, kC], [kR+1, kC-1], [kR+1, kC+1]]
                for partial_move in kingMoves:
                    if partial_move[0] < 8 and partial_move[1] < 8 and partial_move[0] > -1 and partial_move[1] > -1:
                        if self.board[partial_move[0]][partial_move[1]][0] == 'w':
                            blockedCounter += 1
                        else:
                            valid_move = any([partial_move[0], partial_move[1]] == block for block in blocked[0])
                            if valid_move == True:
                                blockedCounter += 1
                    else:
                        blockedCounter += 1

                if blockedCounter == 8:
                    #Attackers vs king
                    attackers = self.attackLine(move, kR, kC)
                    if len(attackers) > 1:
                        return True
                    #There's only one attacker
                    else:
                        row = attackers[0][0]
                        col = attackers[0][1]
                        
                        #Attackers vs attacker
                        attackers = self.attackLine(move, row, col)

                        if len(attackers) == 0:
                            return True
                        else:
                            return False
                else:
                    return False

            else:
                #Check by white
                kR = positions[2]
                kC = positions[3]
                kingMoves = [[kR, kC+1], [kR, kC-1], [kR-1, kC], [kR-1, kC-1], [kR-1, kC+1], [kR+1, kC], [kR+1, kC-1], [kR+1, kC+1]]
                for partial_move in kingMoves:
                    if partial_move[0] < 8 and partial_move[1] < 8 and partial_move[0] > -1 and partial_move[1] > -1:
                        if self.board[partial_move[0]][partial_move[1]][0] == 'b':
                            blockedCounter += 1
                        else:
                            valid_move = any([partial_move[0], partial_move[1]] == block for block in blocked[1])
                            if valid_move == True:
                                blockedCounter += 1
                    else:
                        blockedCounter += 1

                attacekrs = []

                if blockedCounter == 8:
                    #Attackers vs king
                    attackers = self.attackLine(move, kR, kC)
                    if len(attackers) > 1:
                        return True
                    #There's only one attacker
                    else:
                        row = attackers[0][0]
                        col = attackers[0][1]
                        
                        #Attackers vs attacker
                        attackers = self.attackLine(move, row, col)

                        if len(attackers) == 0:
                            return True
                        else:
                            return False
                else:
                    return False


    def attackLine(self, move, row, col):
        attacks = []

        #right
        for i in range(col+1, 8):
            if self.board[row][i][0] == move.PieceMoved[0]:
                break
            elif self.board[row][i] == "--":
                continue
            elif self.board[row][i][1] == 'Q' or self.board[row][i][1] == 'R':
                attacks.append([row, i])
                break
            else:
                break

        #left
        for i in range(col-1, -1, -1):
            if self.board[row][i][0] == move.PieceMoved[0]:
                break
            elif self.board[row][i] == "--":
                continue
            elif self.board[row][i][1] == 'Q' or self.board[row][i][1] == 'R':
                attacks.append([row, i])
                break
            else:
                break

        #down
        for i in range(row+1, 8):
            if self.board[i][col][0] == move.PieceMoved[0]:
                break
            elif self.board[i][col] == "--":
                continue
            elif self.board[i][col][1] == 'Q' or self.board[i][col][1] == 'R':
                attacks.append([i, col])
                break
            else:
                break

        #up
        for i in range(row-1, -1, -1):
            if self.board[i][col][0] == move.PieceMoved[0]:
                break
            elif self.board[i][col] == "--":
                continue
            elif self.board[i][col][1] == 'Q' or self.board[i][col][1] == 'R':
                attacks.append([i, col])
                break
            else:
                break

        #up and right
        r = row
        for i in range(col+1, 8):
            r -= 1
            if r < 0:
                break
            if self.board[r][i][0] == move.PieceMoved[0]:
                break
            elif self.board[r][i] == "--":
                continue
            elif self.board[r][i][1] == 'Q' or self.board[r][i][1] == 'B':
                attacks.append([r, i])
                break
            else:
                break

        #down and right
        r = row
        for i in range(col+1, 8):
            r += 1
            if r > 7:
                break
            if self.board[r][i][0] == move.PieceMoved[0]:
                break
            elif self.board[r][i] == "--":
                continue
            elif self.board[r][i][1] == 'Q' or self.board[r][i][1] == 'B':
                attacks.append([r, i])
                break
            else:
                break

        #up and left
        r = row
        for i in range(col-1, -1, -1):
            r -= 1
            if r < 0:
                break
            if self.board[r][i][0] == move.PieceMoved[0]:
                break
            elif self.board[r][i] == "--":
                continue
            elif self.board[r][i][1] == 'Q' or self.board[r][i][1] == 'B':
                attacks.append([r, i])
                break
            else:
                break

        #down and left
        r = row
        for i in range(col-1, -1, -1):
            r += 1
            if r > 7:
                break
            if self.board[r][i][0] == move.PieceMoved[0]:
                break
            elif self.board[r][i] == "--":
                continue
            elif self.board[r][i][1] == 'Q' or self.board[r][i][1] == 'B':
                attacks.append([r, i])
                break
            else:
                break

        #knights
        if row+2 <= 7:
            if col+1 <= 7:
                if self.board[row+2][col+1][0] != move.PieceMoved[0] and self.board[row+2][col+1][1] == 'N':
                    attacks.append([row+2, col+1])
            if col-1 >= 0:
                if self.board[row+2][col-1][0] != move.PieceMoved[0] and self.board[row+2][col-1][1] == 'N':
                    attacks.append([row+2, col-1])
        if row-2 >= 0:
            if col+1 <= 7:
                if self.board[row-2][col+1][0] != move.PieceMoved[0] and self.board[row-2][col+1][1] == 'N':
                    attacks.append([row-2, col+1])
            if col-1 >= 0:
                if self.board[row-2][col-1][0] != move.PieceMoved[0] and self.board[row-2][col-1][1] == 'N':
                    attacks.append([row-2, col-1])
        if col+2 <= 7:
            if row+1 <= 7:
                if self.board[row+1][col+2][0] != move.PieceMoved[0] and self.board[row+1][col+2][1] == 'N':
                    attacks.append([row+1, col+2])
            if row-1 >= 0:
                if self.board[row-1][col+2][0] != move.PieceMoved[0] and self.board[row-1][col+2][1] == 'N':
                    attacks.append([row-1, col+2])
        if col-2 >= 0:
            if row+1 <= 7:
                if self.board[row+1][col-2][0] != move.PieceMoved[0] and self.board[row+1][col-2][1] == 'N':
                    attacks.append([row+1, col-2])
            if row-1 >= 0:
                if self.board[row-1][col-2][0] != move.PieceMoved[0] and self.board[row-1][col-2][1] == 'N':
                    attacks.append([row-1, col-2])

        return attacks

    def pawnMove(self, move):
        #Determines if it's possible or not to make an en passant
        if(len(self.moveLog) > 0):
            last = self.moveLog[-1]
            if( abs(int(last[2])-int(last[5]))==2 and abs( int(ord(last[1])-96) - move.E_col)==1 and move.S_row==56-ord(last[5]) ):
                self.board[move.S_row][move.S_col-1] = "--"
                return True

        dif_Up = abs(move.E_row - move.S_row)
        dif_Side = abs(move.E_col - move.S_col)

        #Verify if the movement is just in the direction the pawn is able to move depending on the color
        if(move.PieceMoved[0] == 'w'):
            if move.E_row > move.S_row:
                return False
        else:
            if move.E_row < move.S_row:
                return False

        #Check if the move is possible
        if (move.E_col == move.S_col) and (dif_Up == 1) and (self.board[move.E_row][move.E_col] == '--'):
            if(move.E_row == 0 or move.E_row == 7):
               self.promotion(move)
            return True
        #The next lines check the initial position to know wether it's legal to make a 2-square move or not
        elif (dif_Up == 2) and (move.S_row == 1 or move.S_row == 6) and (self.board[move.E_row][move.E_col] == '--'):
            if(move.PieceMoved[0] == 'w'):
                if(self.board[move.E_row+1][move.E_col] == "--") and (move.E_col == move.S_col):
                    return True
                else:
                    return False
            else:
                if(self.board[move.E_row-1][move.E_col] == "--") and (move.E_col == move.S_col):
                    return True
                else:
                    return False
        #Check if we can attack diagonally
        elif (dif_Up < 2) and (dif_Side == 1) and (self.board[move.E_row][move.E_col] != '--'):
            if(move.E_row == 0 or move.E_row == 7):
               self.promotion(move)
            return True
        else:
            return False

    def rookMove(self, move):
        if move.S_row == move.E_row:
            if move.E_col > move.S_col:
                #Movement to the right
                for x in range(move.S_col+1, move.E_col):
                    if self.board[move.S_row][x] != "--" :
                        return False
            else:
                #Movement to the left
                for x in range(move.S_col-1, move.E_col, -1):
                    if self.board[move.S_row][x] != "--" : 
                        return False
            return True
        elif move.S_col == move.E_col:
            if move.E_row > move.S_row:
                #Movement downwards
                for x in range(move.S_row+1, move.E_row):
                    if self.board[x][move.S_col] != "--" : 
                        return False
            else:
                #Movement upwards
                for x in range(move.S_row-1, move.E_row, -1):
                    if self.board[x][move.S_col] != "--" :
                        return False
            return True
        else:
            return False

    def bishopMove(self, move):
        dif_Up = abs(move.E_row - move.S_row)
        dif_Side = abs(move.E_col - move.S_col)
        if dif_Side == dif_Up:
        #IN THE FOLLOWING LINES
            if move.E_row > move.S_row: #This means it moves downwards
                if move.E_col > move.S_col: # -Downward and right-
                    x = move.S_col + 1
                    for y in range(move.S_row+1, move.E_row):
                        if self.board[y][x] != "--" : 
                            return False
                        x += 1
                else: # -Downward and left-
                    x = move.S_col - 1
                    for y in range(move.S_row+1, move.E_row):
                        if self.board[y][x] != "--" : 
                            return False
                        x -= 1
            else: #This means it moves upwards
                if move.E_col > move.S_col: # -Upward and right-
                    x = move.S_col + 1
                    for y in range(move.S_row-1, move.E_row, -1):
                        if self.board[y][x] != "--" : 
                            return False
                        x += 1
                else: # -Upward and left-
                    x = move.S_col - 1
                    for y in range(move.S_row-1, move.E_row, -1):
                        if self.board[y][x] != "--" : 
                            return False
                        x -= 1
            return True
        else:
            return False

    def queenMove(self, move):
        if (move.S_row == move.E_row) or (move.S_col == move.E_col):
            return self.rookMove(move)
        else:
            return self.bishopMove(move)
      
    def legalToMove(self, move):
        dif_Up = abs(move.E_row - move.S_row)
        dif_Side = abs(move.E_col - move.S_col)
        #Torres / Rooks
        if move.PieceMoved == "bR" or move.PieceMoved == "wR":
            return self.rookMove(move)
        #Alfiles / Bishops
        elif move.PieceMoved == "bB" or move.PieceMoved == "wB":
            return self.bishopMove(move)
        #Caballos / Knigths (sin edición)
        elif move.PieceMoved == "bN" or move.PieceMoved == "wN":
            if (dif_Up == 1 and dif_Side == 2) or (dif_Up == 2 and dif_Side == 1):
                return True
        #Reyes / Kings (sin edición)
        elif move.PieceMoved == "bK" or move.PieceMoved == "wK":
            if dif_Side < 2 and dif_Up < 2 or self.castling(move):
                return True
        #Reinas / Queens (rook + bishop)
        elif move.PieceMoved == "bQ" or move.PieceMoved == "wQ":
            return self.queenMove(move)
        #Peones / Pawns
        elif move.PieceMoved == "bP" or move.PieceMoved == "wP":
            return self.pawnMove(move)
        return False

    #It determines if it's possible to eat the pieces *it takes in consideration the first letter of the piece's name, it being 'b' or 'w'*
    def edible(self, move):
        if(move.PieceMoved[0] == self.board[move.E_row][move.E_col][0]):
            return False
        else:
            return True

    def EndGame(self, value):
        print("\a\n\t CHEKCMATE!!!\n\t", "White" if not self.whiteMove else "Black", " wins!!")
        return False

    def MakeMove(self, move):
        if self.CheckMate(move) == True :
            ChessMain.running = self.EndGame(0)
            return
        if self.checkMove(move) == False :
            print("\a\n    Illegal move\n")
            return
        if self.edible(move) == False : 
            print("\a\n    Illegal move\n")
            return
        if self.legalToMove(move) == False : 
            print("\a\n    Illegal move\n")
            return
        #Movement order
        if (self.whiteMove != True) and (move.PieceMoved[0] == 'w') : return
        if (self.whiteMove == True) and (move.PieceMoved[0] == 'b') : return
        self.board[move.S_row][move.S_col] = "--"        
        self.board[move.E_row][move.E_col] = move.PieceMoved
        #self.log.append((move.PieceMoved + Move.getChessNot(move, True)))
        self.log.append(move)
        self.moveLog.append(move.PieceMoved[1] + Move.getChessNot(move, True))
        self.pieceLog.append(move.PieceMoved)
        if self.whiteMove: print(self.moveLog[-1], "                 ", end="")
        else: print(self.moveLog[-1])
        self.whiteMove = not self.whiteMove

    #Undo function: let's the player undo the most recent move done by him
    #Correct function when promotion done
    def undoMove(self):
        if len(self.log) != 0: #Make sure the log is not size 0, because we need to have a Move to undo it
            move = self.log.pop()
            self.board[move.S_row][move.S_col] = move.PieceMoved
            self.board[move.E_row][move.E_col] = move.PieceCaptured
            self.whiteMove = not self.whiteMove

class Move():
     ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
     rowsToRanks = {v : k for k, v in ranksToRows.items()}
     
     filesToCols = {"h":7, "g":6, "f":5, "e":4, "d":3, "c":2, "b":1, "a":0}
     colsToFiles = {v : k for k, v in filesToCols.items()}

     def __init__(self, pos1, pos2, board):
         self.S_row = pos1[0]
         self.S_col = pos1[1]
         self.E_row = pos2[0]
         self.E_col = pos2[1]
         self.PieceMoved = board[self.S_row][self.S_col]       
         self.PieceCaptured = board[self.E_row][self.E_col]
         
     def getChessNot(self, h): #h is a boolean that will allow me to decide waht type of notation I want
         #If I want that getChessNot returns from what position to which position was the move, I'll enable it
         if h: return self.getRankFile(self.S_row, self.S_col) + ":" + self.getRankFile(self.E_row, self.E_col)
         else: return self.getRankFile(self.E_row, self.E_col)

     def getRankFile(self, r, c):
         return self.colsToFiles[c] + self.rowsToRanks[r]