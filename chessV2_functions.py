import pygame, copy, sys, math, random, cProfile, time


def quit_chess(game, result):
    if game[-1] == '.':
        game = game[:-3]
    if result == 'white' or result == 'black':
        print(game, result + ' wins', sep='\n')
    elif result == 'draw':
        print(game, "draw")
    else:
        print(game)
    pygame.quit()
    sys.exit()


def sign(x):
    return x // abs(x)


def convert_to_number(place):
    letter_to_number = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    return letter_to_number[place[0]], int(place[1])


def convert_to_number_import(place):
    letter_to_number = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    return 8 - int(place[1]), letter_to_number[place[0]]


def convert_to_letter(column):
    number_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    return number_to_letter[column]


def fen_to_board(fen):
    conversion = {'b': 'black_bishop', 'k': 'black_king', 'n': 'black_knight', 'p': 'black_pawn', 'q': 'black_queen',
                  'r': 'black_rook', 'B': 'white_bishop', 'K': 'white_king', 'N': 'white_knight', 'P': 'white_pawn',
                  'Q': 'white_queen', 'R': 'white_rook'}
    board = [[] for _ in range(8)]
    piecelist = []
    counter = 0
    for index, letter in enumerate(fen):
        if letter == '/':
            counter += 1
            continue
        elif letter.isdigit():
            for i in range(int(letter)):
                board[counter].append('')
        elif letter == ' ':
            if fen[index + 1] == 'w':
                turn = 'white'
            else:
                turn = 'black'
            rest_of_fen = fen[index + 3:]
            break
        else:
            board[counter].append(conversion[letter])
            piecelist.append(conversion[letter])
    return board, piecelist, turn, rest_of_fen


def draw_pieces(board, square, chessboard):
    for row_number, row in enumerate(board):
        for spot_number, spot in enumerate(row):
            if spot == '':
                continue
            else:
                piece = pygame.transform.scale(pygame.image.load(f'{spot}.png'), (square, square))
                chessboard.blit(piece, (spot_number * square, row_number * square))


def draw_board(chessboard, board, light, dark, square):
    chessboard.fill(light)
    for i in range(8):
        for j in range((lambda x: 1 if (i % 2 == 0) else 0)(i), 8, 2):
            black_square = pygame.Rect(j * square, i * square, square, square)
            pygame.draw.rect(chessboard, dark, black_square)
    draw_pieces(board, square, chessboard)


def draw_piece(chessboard, piece, square, x, y):
    piece = pygame.transform.scale(pygame.image.load(f'{piece}.png'), (square, square))
    chessboard.blit(piece, (x - square / 2, y - square / 2))


def spot_colour(row, column, light, dark):
    if row % 2 == 0:
        if column % 2 == 0:
            return light
        else:
            return dark
    else:
        if column % 2 == 0:
            return dark
        else:
            return light


def legal_moves(piece, row, column, board, castling, en_passant_row, en_passant_column):
    legal_moves = []
    colour = piece[:5]
    type = piece[6:]
    if type == 'rook' or type == 'queen':
        for i in range(1, 8):
            if row - i >= 0:
                if board[row - i][column] == '':
                    legal_moves.append((row - i, column))
                elif board[row - i][column][:5] != colour:
                    legal_moves.append((row - i, column))
                    break
                else:
                    break
        for i in range(1, 8):
            if row + i <= 7:
                if board[row + i][column] == '':
                    legal_moves.append((row + i, column))
                elif board[row + i][column][:5] != colour:
                    legal_moves.append((row + i, column))
                    break
                else:
                    break
        for i in range(1, 8):
            if column + i <= 7:
                if board[row][column + i] == '':
                    legal_moves.append((row, column + i))
                elif board[row][column + i][:5] != colour:
                    legal_moves.append((row, column + i))
                    break
                else:
                    break
        for i in range(1, 8):
            if column - i >= 0:
                if board[row][column - i] == '':
                    legal_moves.append((row, column - i))
                elif board[row][column - i][:5] != colour:
                    legal_moves.append((row, column - i))
                    break
                else:
                    break
    if type == 'bishop' or type == 'queen':
        for i in range(1, 8):
            if row + i <= 7 and column + i <= 7:
                if board[row + i][column + i] == '':
                    legal_moves.append((row + i, column + i))
                elif board[row + i][column + i][:5] != colour:
                    legal_moves.append((row + i, column + i))
                    break
                else:
                    break
        for i in range(1, 8):
            if row + i <= 7 and column - i >= 0:
                if board[row + i][column - i] == '':
                    legal_moves.append((row + i, column - i))
                elif board[row + i][column - i][:5] != colour:
                    legal_moves.append((row + i, column - i))
                    break
                else:
                    break
        for i in range(1, 8):
            if row - i >= 0 and column - i >= 0:
                if board[row - i][column - i] == '':
                    legal_moves.append((row - i, column - i))
                elif board[row - i][column - i][:5] != colour:
                    legal_moves.append((row - i, column - i))
                    break
                else:
                    break
        for i in range(1, 8):
            if row - i >= 0 and column + i <= 7:
                if board[row - i][column + i] == '':
                    legal_moves.append((row - i, column + i))
                elif board[row - i][column + i][:5] != colour:
                    legal_moves.append((row - i, column + i))
                    break
                else:
                    break
    elif type == 'pawn':
        if colour == 'white':
            if row - 1 >= 0:
                if board[row - 1][column] == '':
                    legal_moves.append((row - 1, column))
                    if row == 6 and board[row - 2][column] == '':
                        legal_moves.append((row - 2, column))
            if row - 1 >= 0 and column - 1 >= 0:
                if ('' != board[row - 1][column - 1][:5] != colour) or (
                        row - 1 == en_passant_row and column - 1 == en_passant_column):
                    legal_moves.append((row - 1, column - 1))
            if row - 1 >= 0 and column + 1 <= 7:
                if ('' != board[row - 1][column + 1][:5] != colour) or (
                        row - 1 == en_passant_row and column + 1 == en_passant_column):
                    legal_moves.append((row - 1, column + 1))
        else:
            for i in range(1, 3):
                if row + 1 <= 7:
                    if board[row + 1][column] == '':
                        legal_moves.append((row + 1, column))
                        if row == 1 and board[row + 2][column] == '':
                            legal_moves.append((row + 2, column))
            if row + 1 <= 7 and column - 1 >= 0:
                if ('' != board[row + 1][column - 1][:5] != colour) or (
                        row + 1 == en_passant_row and column - 1 == en_passant_column):
                    legal_moves.append((row + 1, column - 1))
            if row + 1 <= 7 and column + 1 <= 7:
                if ('' != board[row + 1][column + 1][:5] != colour) or (
                        row + 1 == en_passant_row and column + 1 == en_passant_column):
                    legal_moves.append((row + 1, column + 1))
    elif type == 'knight':
        for i in range(1, 3):
            for j in range(1, 3):
                if i != j:
                    if row + i <= 7 and column + j <= 7:
                        if board[row + i][column + j] == '' or board[row + i][column + j][:5] != colour:
                            legal_moves.append((row + i, column + j))
                    if row - i >= 0 and column - j >= 0:
                        if board[row - i][column - j] == '' or board[row - i][column - j][:5] != colour:
                            legal_moves.append((row - i, column - j))
                    if row - i >= 0 and column + j <= 7:
                        if board[row - i][column + j] == '' or board[row - i][column + j][:5] != colour:
                            legal_moves.append((row - i, column + j))
                    if row + i <= 7 and column - j >= 0:
                        if board[row + i][column - j] == '' or board[row + i][column - j][:5] != colour:
                            legal_moves.append((row + i, column - j))
    elif type == 'king':
        if row + 1 <= 7:
            if board[row + 1][column] == '' or board[row + 1][column][:5] != colour:
                legal_moves.append((row + 1, column))
            if column + 1 <= 7:
                if board[row + 1][column + 1] == '' or board[row + 1][column + 1][:5] != colour:
                    legal_moves.append((row + 1, column + 1))
            if column - 1 >= 0:
                if board[row + 1][column - 1] == '' or board[row + 1][column - 1][:5] != colour:
                    legal_moves.append((row + 1, column - 1))
        if row - 1 >= 0:
            if board[row - 1][column] == '' or board[row - 1][column][:5] != colour:
                legal_moves.append((row - 1, column))
            if column + 1 <= 7:
                if board[row - 1][column + 1] == '' or board[row - 1][column + 1][:5] != colour:
                    legal_moves.append((row - 1, column + 1))
            if column - 1 >= 0:
                if board[row - 1][column - 1] == '' or board[row - 1][column - 1][:5] != colour:
                    legal_moves.append((row - 1, column - 1))
        if column - 1 >= 0:
            if board[row][column - 1][:5] != colour:
                legal_moves.append((row, column - 1))
        if column + 1 <= 7:
            if board[row][column + 1][:5] != colour:
                legal_moves.append((row, column + 1))
        if column + 3 <= 7:
            if board[row][column + 1] == '' and board[row][column + 2] == '':
                if (colour == 'white' and 'K' in castling) or (colour == 'black' and 'k' in castling):
                    legal_moves.append((row, column + 2))
        if column - 4 >= 0:
            if board[row][column - 1] == '' and board[row][column - 2] == '' and board[row][column - 3] == '':
                if (colour == 'white' and 'Q' in castling) or (colour == 'black' and 'q' in castling):
                    legal_moves.append((row, column - 2))
    return legal_moves


def kingmoves(board, row, column, colour):
    kingmoves = []
    knightmoves = []
    for i in range(1, 8):
        if row - i >= 0:
            if board[row - i][column] == '':
                kingmoves.append((row - i, column))
            elif board[row - i][column][:5] != colour:
                kingmoves.append((row - i, column))
                break
            else:
                break
    for i in range(1, 8):
        if row + i <= 7:
            if board[row + i][column] == '':
                kingmoves.append((row + i, column))
            elif board[row + i][column][:5] != colour:
                kingmoves.append((row + i, column))
                break
            else:
                break
    for i in range(1, 8):
        if column + i <= 7:
            if board[row][column + i] == '':
                kingmoves.append((row, column + i))
            elif board[row][column + i][:5] != colour:
                kingmoves.append((row, column + i))
                break
            else:
                break
    for i in range(1, 8):
        if column - i >= 0:
            if board[row][column - i] == '':
                kingmoves.append((row, column - i))
            elif board[row][column - i][:5] != colour:
                kingmoves.append((row, column - i))
                break
            else:
                break
    for i in range(1, 8):
        if row + i <= 7 and column + i <= 7:
            if board[row + i][column + i] == '':
                kingmoves.append((row + i, column + i))
            elif board[row + i][column + i][:5] != colour:
                kingmoves.append((row + i, column + i))
                break
            else:
                break
    for i in range(1, 8):
        if row + i <= 7 and column - i >= 0:
            if board[row + i][column - i] == '':
                kingmoves.append((row + i, column - i))
            elif board[row + i][column - i][:5] != colour:
                kingmoves.append((row + i, column - i))
                break
            else:
                break
    for i in range(1, 8):
        if row - i >= 0 and column - i >= 0:
            if board[row - i][column - i] == '':
                kingmoves.append((row - i, column - i))
            elif board[row - i][column - i][:5] != colour:
                kingmoves.append((row - i, column - i))
                break
            else:
                break
    for i in range(1, 8):
        if row - i >= 0 and column + i <= 7:
            if board[row - i][column + i] == '':
                kingmoves.append((row - i, column + i))
            elif board[row - i][column + i][:5] != colour:
                kingmoves.append((row - i, column + i))
                break
            else:
                break
    for i in range(1, 3):
        for j in range(1, 3):
            if i != j:
                if row + i <= 7 and column + j <= 7:
                    if board[row + i][column + j] == '' or board[row + i][column + j][:5] != colour:
                        knightmoves.append((row + i, column + j))
                if row - i >= 0 and column - j >= 0:
                    if board[row - i][column - j] == '' or board[row - i][column - j][:5] != colour:
                        knightmoves.append((row - i, column - j))
                if row - i >= 0 and column + j <= 7:
                    if board[row - i][column + j] == '' or board[row - i][column + j][:5] != colour:
                        knightmoves.append((row - i, column + j))
                if row + i <= 7 and column - j >= 0:
                    if board[row + i][column - j] == '' or board[row + i][column - j][:5] != colour:
                        knightmoves.append((row + i, column - j))
    return kingmoves, knightmoves


def check_check(colour, board):
    enemy_pieces = []
    for rowindex, row in enumerate(board):
        for columnindex, piece in enumerate(row):
            if piece != '':
                if piece[:5] != colour:
                    enemy_pieces.append([piece, (rowindex, columnindex)])
                elif piece[6:] == 'king' and piece[:5] == colour:
                    kings_row, kings_column = rowindex, columnindex
                    kings_moves, knightmoves = kingmoves(board, kings_row, kings_column, colour)
    for piece in enemy_pieces:
        if piece[1] in kings_moves:
            if 'queen' in piece[0]:
                return False
            elif 'rook' in piece[0]:
                if piece[1][0] == kings_row or piece[1][1] == kings_column:
                    return False
            elif 'bishop' in piece[0]:
                if piece[1][0] != kings_row and piece[1][1] != kings_column:
                    return False
            elif 'pawn' in piece[0]:
                if colour == 'white':
                    if abs(kings_column - piece[1][1]) == 1 and kings_row - 1 == piece[1][0]:
                        return False
                else:
                    if abs(kings_column - piece[1][1]) == 1 and kings_row + 1 == piece[1][0]:
                        return False
            elif 'king' in piece[0]:
                if abs(kings_column - piece[1][1]) <= 1 >= abs(kings_row - piece[1][0]):
                    return False
        elif 'knight' in piece[0]:
            if piece[1] in knightmoves:
                return False
    return True


def use_extra_info(extra_info):
    castling = ''
    for index, letter in enumerate(extra_info):
        if letter != '-' and letter != ' ':
            castling += letter
        elif letter == ' ':
            break
    if castling == '':
        castling = '-'
        extra_info = extra_info[2:]
    else:
        extra_info = extra_info.lstrip(castling + ' ')
    if extra_info[0] == '-':
        en_passant_row = '-'
        en_passant_column = '-'
    else:
        en_passant_column, en_passant_row = convert_to_number(extra_info[0:2])
    if en_passant_column != '-':
        extra_info = extra_info.lstrip(str(en_passant_row) + convert_to_letter(en_passant_column))
    else:
        extra_info = extra_info.lstrip('-')
    extra_info = extra_info.lstrip()
    halfmoves = ''
    for letter in extra_info:
        if letter == ' ':
            break
        else:
            halfmoves = halfmoves + letter
    extra_info = extra_info.lstrip(halfmoves)
    extra_info = extra_info.lstrip()
    moves = ''
    for letter in extra_info:
        if letter == ' ':
            break
        else:
            moves = moves + letter

    return castling, en_passant_row, en_passant_column, int(halfmoves), int(moves)


def handle_castling(board, newrow, newcolumn, castling):
    if newcolumn == 6:
        rook = board[newrow][7]
        board[newrow][7] = ''
        board[newrow][newcolumn - 1] = rook
        if rook[:5] == 'white':
            castling = castling.replace('K', '')
        else:
            castling = castling.replace('k', '')
    else:
        rook = board[newrow][0]
        board[newrow][0] = ''
        board[newrow][newcolumn + 1] = rook
        if rook[:5] == 'white':
            castling = castling.replace('Q', '')
        else:
            castling = castling.replace('q', '')
    return board, castling


def draw_promotion(chessboard, colour, square):
    width = square * 8
    piece = pygame.transform.scale(pygame.image.load(f'{colour}_knight.png'), (square, square))
    chessboard.blit(piece, ((3 * width) // 8, (3 * width) // 8))
    piece = pygame.transform.scale(pygame.image.load(f'{colour}_bishop.png'), (square, square))
    chessboard.blit(piece, ((3 * width) // 8, width // 2))
    piece = pygame.transform.scale(pygame.image.load(f'{colour}_rook.png'), (square, square))
    chessboard.blit(piece, (width // 2, (3 * width) // 8))
    piece = pygame.transform.scale(pygame.image.load(f'{colour}_queen.png'), (square, square))
    chessboard.blit(piece, (width // 2, width // 2))


def add_turn(all_moves, board, piece, oldrow, oldcolumn, newrow, newcolumn, en_passant_row, en_passant_column):
    name_conversion = {'knight': 'N', 'king': 'K', 'rook': 'R', 'queen': 'Q', 'bishop': 'B', 'pawn': ''}
    added_turn = ' '
    type = piece[6:]
    if type == 'king' and abs(oldcolumn - newcolumn) == 2:
        if oldcolumn - newcolumn == -2:
            return ' 0-0'
        else:
            return ' 0-0-0'
    added_turn += name_conversion[type]
    for piece_list in all_moves:
        if piece_list[0] == piece and (piece_list[1] != oldrow or piece_list[2] != oldcolumn):
            for move in all_moves[piece_list]:
                if move[0] == newrow and move[1] == newcolumn:
                    if piece_list[1] == newrow:
                        added_turn += convert_to_letter(oldcolumn)
                    if piece_list[2] == oldcolumn:
                        added_turn += str(abs(8 - newrow))
    if board[newrow][newcolumn] != '' or (
            type == 'pawn' and newrow == en_passant_row and newcolumn == en_passant_column):
        if added_turn == ' ':
            added_turn += convert_to_letter(oldcolumn)
        added_turn += 'x'
    added_turn += convert_to_letter(newcolumn)
    added_turn += str(abs(8 - newrow))
    if type == 'pawn':
        if piece[:5] == 'white' and newrow == 0:
            added_turn += 'Q'
        elif piece[:5] == 'black' and newrow == 7:
            added_turn += 'Q'
    return added_turn


def evaluate_position(board, castling, en_passant_row, en_passant_column):
    white_loss = True
    black_loss = True
    position = 0
    eval_pieces = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 0}
    real_moves = {}
    for rowindex, row in enumerate(board):
        for columnindex, piece in enumerate(row):
            if piece != '':
                real_moves[piece + str(rowindex) + str(columnindex)] = []
                value = 0
                legalmoves = legal_moves(piece, rowindex, columnindex, board, castling, en_passant_row,
                                         en_passant_column)
                for legalrow, legalcolumn in legalmoves:
                    newboard = [i[:] for i in board]
                    newboard[legalrow][legalcolumn] = piece
                    newboard[rowindex][columnindex] = ''
                    if check_check(piece[:5], newboard):
                        if 'black' in piece:
                            black_loss = False
                        elif 'white' in piece:
                            white_loss = False
                        real_moves[piece + str(rowindex) + str(columnindex)].append((legalrow, legalcolumn))
                value += eval_pieces[piece[6:]]
                if 'king' in piece:
                    if piece[:5] == 'white':
                        white_king_pos = (rowindex, columnindex)
                    else:
                        black_king_pos = (rowindex, columnindex)
                if 'black' in piece:
                    position -= value
                else:
                    position += value
    if white_loss:
        if black_loss:
            return 0
        else:
            for key in real_moves:
                if white_king_pos in real_moves[key]:
                    position = -9999
                    return position
            else:
                position = 0
                return position
    if black_loss:
        if white_loss:
            return 0
        else:
            for key in real_moves:
                if black_king_pos in real_moves[key]:
                    position = 9999
                    return position
            else:
                position = 0
                return position
    position = 0
    if len(real_moves) > 27:  # early game
        for key in real_moves:
            value = eval_pieces[key[6:-2]]
            if 'pawn' in key:
                value *= (0.03 / abs(3.5 - int(key[-2]))) + 1
                value *= (0.03 / abs(3.5 - int(key[-1]))) + 1
            if 'rook' in key or 'knight' in key or 'bishop' in key:
                value *= 1 + (len(real_moves[key]) * 0.03)
            if 'black' in key:
                if white_king_pos in real_moves[key]:
                    position -= 0.2
                position -= value
            else:
                if black_king_pos in real_moves[key]:
                    position += 0.2
                position += value
    elif 14 < len(real_moves) < 28:  # midgame
        for key in real_moves:
            value = eval_pieces[key[6:-2]]
            if 'rook' in key or 'knight' in key or 'bishop' in key:
                value *= 1 + (len(real_moves[key]) * 0.035)
            if 'black' in key:
                if white_king_pos in real_moves[key]:
                    position -= 0.4
                position -= value
            else:
                if black_king_pos in real_moves[key]:
                    position += 0.4
                position += value
    else:  # endgame
        for key in real_moves:
            value = eval_pieces[key[6:-2]]
            if 'black' in key:
                if white_king_pos in real_moves[key]:
                    position -= 0.8
                if 'pawn' in key:
                    value = 0
                    value += int(key[-1]) / 2
                position -= value
            else:
                if black_king_pos in real_moves[key]:
                    position += 0.8
                if 'pawn' in key:
                    value = 0
                    value += 4 - int(key[-1]) / 2
                position += value
    return position


def minimax(board, depth, turn, castling, en_passant_row, en_passant_column, halfturns, game_for_ai, alpha=-9999,
            beta=9999):
    if game_for_ai is None:
        game_for_ai = []
    if depth == 0:
        return evaluate_position(board, castling, en_passant_row, en_passant_column), game_for_ai
    if turn == 'white':
        maxeval = -9999
        possible_moves = {}
        for rowindex, row in enumerate(board):
            for columnindex, piece in enumerate(row):
                if piece != '':
                    if piece[:5] == turn:
                        real_moves = []
                        legalmoves = legal_moves(piece, rowindex, columnindex, board, castling, en_passant_row,
                                                 en_passant_column)
                        for legalrow, legalcolumn in legalmoves:
                            if 'king' in board[legalrow][legalcolumn]:
                                continue
                            if 'king' in piece and abs(legalcolumn - columnindex) > 1:
                                if not check_check(piece[:5], board):
                                    continue
                                for i in range(abs(legalcolumn - columnindex) - 2):
                                    newboard = [i[:] for i in board]
                                    newboard[legalrow][columnindex + sign(legalcolumn - columnindex) * i + 1] = piece
                                    newboard[rowindex][columnindex] = ''
                                    if not check_check(piece[:5], newboard):
                                        continue
                            newboard = [i[:] for i in board]
                            newboard[legalrow][legalcolumn] = piece
                            newboard[rowindex][columnindex] = ''
                            if check_check(piece[:5], newboard):
                                real_moves.append((legalrow, legalcolumn))
                        possible_moves[piece, rowindex, columnindex] = real_moves
        for key in possible_moves:
            currentpiece, oldrow, oldcolumn = key
            for move in possible_moves[key]:
                newboard = [i[:] for i in board]
                newrow, newcolumn = move
                newcastling = copy.deepcopy(castling)
                if board[newrow][newcolumn] != '':
                    halfturns = 0
                    if newrow == 7 and newcolumn == 7:
                        newcastling = newcastling.replace('K', '')
                    elif newrow == 7 and newcolumn == 0:
                        newcastling = newcastling.replace('Q', '')
                    elif newrow == 0 and newcolumn == 0:
                        newcastling = newcastling.replace('q', '')
                    elif newrow == 0 and newcolumn == 7:
                        newcastling = newcastling.replace('k', '')
                if 'pawn' in currentpiece:
                    halfturns = 0
                    if (newrow == en_passant_row) and (newcolumn == en_passant_column):
                        newboard[newrow + 1][en_passant_column] = ''
                newen_passant_row = -1
                newen_passant_column = -1
                if 'pawn' in currentpiece:
                    if abs(newrow - oldrow) == 2:
                        newen_passant_column = oldcolumn
                        newen_passant_row = oldrow - 1
                elif 'king' in currentpiece:
                    if abs(newcolumn - oldcolumn) == 2:
                        newboard, castling = handle_castling(newboard, newrow, newcolumn, castling)
                    else:
                        castling = castling.replace('K', '')
                        castling = castling.replace('Q', '')
                elif 'rook' in currentpiece:
                    if oldrow == 7 and oldcolumn == 7:
                        castling = castling.replace('K', '')
                    elif oldrow == 7 and oldcolumn == 0:
                        castling = castling.replace('Q', '')
                if 'pawn' not in currentpiece or newrow != 0:
                    newboard[newrow][newcolumn] = currentpiece
                else:
                    newboard[newrow][newcolumn] = 'white_queen'
                newboard[oldrow][oldcolumn] = ''
                newgame_for_ai = copy.deepcopy(game_for_ai)
                newgame_for_ai.append(f'{currentpiece[6:]}{oldrow}{oldcolumn}{newrow}{newcolumn}')
                childeval, potential_game = minimax(newboard, depth - 1, 'black', newcastling, newen_passant_row,
                                                    newen_passant_column, halfturns + 1, newgame_for_ai, alpha, beta)
                if childeval > maxeval:
                    potential_game_for_ai = potential_game
                    maxeval = childeval
                alpha = max(alpha, childeval)
                if beta <= alpha:
                    break
            else:
                continue
            break
        try:
            return maxeval, potential_game_for_ai
        except UnboundLocalError:
            return maxeval, game_for_ai
    if turn == 'black':
        mineval = 9999
        possible_moves = {}
        for rowindex, row in enumerate(board):
            for columnindex, piece in enumerate(row):
                if piece != '':
                    if piece[:5] == turn:
                        real_moves = []
                        legalmoves = legal_moves(piece, rowindex, columnindex, board, castling, en_passant_row,
                                                 en_passant_column)
                        for legalrow, legalcolumn in legalmoves:
                            if 'king' in board[legalrow][legalcolumn]:
                                continue
                            if 'king' in piece and abs(legalcolumn - columnindex) > 1:
                                if not check_check(piece[:5], board):
                                    continue
                                for i in range(abs(legalcolumn - columnindex) - 2):
                                    newboard = [i[:] for i in board]
                                    newboard[legalrow][columnindex + sign(legalcolumn - columnindex) * i + 1] = piece
                                    newboard[rowindex][columnindex] = ''
                                    if not check_check(piece[:5], newboard):
                                        continue
                            newboard = [i[:] for i in board]
                            newboard[legalrow][legalcolumn] = piece
                            newboard[rowindex][columnindex] = ''
                            if check_check(piece[:5], newboard):
                                real_moves.append((legalrow, legalcolumn))
                        possible_moves[piece, rowindex, columnindex] = real_moves
        for key in possible_moves:
            currentpiece, oldrow, oldcolumn = key
            for move in possible_moves[key]:
                newboard = [i[:] for i in board]
                newrow, newcolumn = move
                newcastling = copy.deepcopy(castling)
                if board[newrow][newcolumn] != '':
                    halfturns = 0
                    if newrow == 7 and newcolumn == 7:
                        newcastling = newcastling.replace('K', '')
                    elif newrow == 7 and newcolumn == 0:
                        newcastling = newcastling.replace('Q', '')
                    elif newrow == 0 and newcolumn == 0:
                        newcastling = newcastling.replace('q', '')
                    elif newrow == 0 and newcolumn == 7:
                        newcastling = newcastling.replace('k', '')
                if 'pawn' in currentpiece:
                    if (newrow == en_passant_row) and (newcolumn == en_passant_column):
                        newboard[newrow - 1][newcolumn] = ''
                newen_passant_row = -1
                newen_passant_column = -1
                if 'pawn' in currentpiece:
                    if abs(newrow - oldrow) == 2:
                        newen_passant_column = oldcolumn
                        newen_passant_row = oldrow + 1
                elif 'king' in currentpiece:
                    if abs(newcolumn - oldcolumn) == 2:
                        newboard, castling = handle_castling(newboard, newrow, newcolumn, castling)
                    else:
                        castling = castling.replace('k', '')
                        castling = castling.replace('q', '')
                elif 'rook' in currentpiece:
                    if oldrow == 0 and oldcolumn == 0:
                        castling = castling.replace('q', '')
                    elif oldrow == 0 and oldcolumn == 7:
                        castling = castling.replace('k', '')
                if 'pawn' not in currentpiece or newrow != 7:
                    newboard[newrow][newcolumn] = currentpiece
                else:
                    newboard[newrow][newcolumn] = 'black_queen'
                newboard[oldrow][oldcolumn] = ''
                newgame_for_ai = copy.deepcopy(game_for_ai)
                newgame_for_ai.append(f'{currentpiece[6:]}{oldrow}{oldcolumn}{newrow}{newcolumn}')
                childeval, potential_game = minimax(newboard, depth - 1, 'white', newcastling, newen_passant_row,
                                                    newen_passant_column, halfturns + 1, newgame_for_ai, alpha, beta)
                if childeval < mineval:
                    potential_game_for_ai = potential_game
                    mineval = childeval
                beta = min(beta, childeval)
                if beta <= alpha:
                    break
            else:
                continue
            break
        try:
            return mineval, potential_game_for_ai
        except UnboundLocalError:
            return mineval, game_for_ai


if __name__ == '__main__':
    board = [['', 'black_knight', 'black_bishop', 'black_queen', 'black_king', 'black_bishop', 'black_knight',
              'black_rook'],
             ['black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn',
              'black_pawn'], ['', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', ''],
             ['', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', ''],
             ['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', '', 'white_pawn', 'white_pawn',
              'white_pawn'],
             ['white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'white_bishop',
              'white_knight', 'white_rook']]
    def stuff(colour, board):
        for i in range(50000):
            check_check(colour, board)
    cProfile.run('minimax(board, 3, "white", "KQkq", "-", "-", 0, [])')
