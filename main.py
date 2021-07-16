from chessV2_functions import *

try:
    import cPickle as pickle
except ImportError:
    import pickle

pygame.init()
width = 1000
square = width // 8
chessboard = pygame.display.set_mode((width, width))
pygame.display.set_caption("Chess")
light = (200, 215, 200)
dark = (64, 110, 71)
black = (0, 0, 0)
white = (255, 255, 255)
currentpiece = None
currentrow = None
currentcolumn = None
gamestate = 'chessboard'
game_for_ai = []
game = '1.'
result = None
promotion_square = []
promotion_piece = ''
player = 'human'
# fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
# fen = '3r4/3r4/3k4/8/8/3K4/8/8 w - - 0 1'
fen = '8/PPPPPPPP/8/8/8/8/8/K2k4 w - - 0 1'
board, piecelist, turn, extra_info = fen_to_board(fen)
castling, en_passant_row, en_passant_column, halfturns, no_of_turns = use_extra_info(extra_info)
draw_board(chessboard, board, light, dark, square)
possible_moves = {}
opening_moves = pickle.load(open('opening_moves_100000.pkl', 'rb'))
print(opening_moves, type(opening_moves))
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
                            newboard[legalrow][
                                columnindex + sign(legalcolumn - columnindex) * i + 1] = piece
                            newboard[rowindex][columnindex] = ''
                            if not check_check(piece[:5], newboard):
                                continue
                    newboard = [i[:] for i in board]
                    newboard[legalrow][legalcolumn] = piece
                    newboard[rowindex][columnindex] = ''
                    if check_check(piece[:5], newboard):
                        real_moves.append((legalrow, legalcolumn))
                possible_moves[piece, rowindex, columnindex] = real_moves
while True:
    if gamestate == 'chessboard':
        events = pygame.event.get()
        for event in events:
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                quit_chess(game, result)
            if event.type == pygame.MOUSEBUTTONUP and currentpiece is not None or player == 'ai':
                if player == 'human':
                    mouse_row = y // square
                    mouse_column = x // square
                else:
                    mouse_row = int(ai_moves[0][-2])
                    mouse_column = int(ai_moves[0][-1])
                    currentrow = int(ai_moves[0][-4])
                    currentcolumn = int(ai_moves[0][-3])
                    currentpiece = f'{turn}_{ai_moves[0][:-4]}'
                if (mouse_row, mouse_column) in possible_moves[currentpiece, currentrow, currentcolumn]:
                    halfturns += 1
                    if board[mouse_row][mouse_column] != '':
                        halfturns = 0
                        if mouse_row == 7 and mouse_column == 7:
                            castling = castling.replace('K', '')
                        elif mouse_row == 7 and mouse_column == 0:
                            castling = castling.replace('Q', '')
                        elif mouse_row == 0 and mouse_column == 0:
                            castling = castling.replace('q', '')
                        elif mouse_row == 0 and mouse_column == 7:
                            castling = castling.replace('k', '')
                    if 'pawn' in currentpiece:
                        halfturns = 0
                        if turn == 'white':
                            if (mouse_row == en_passant_row) and (mouse_column == en_passant_column):
                                board[mouse_row + 1][en_passant_column] = ''
                            elif mouse_row == 0:
                                gamestate = 'promotion'
                                promotion_square = [mouse_row, mouse_column]
                        else:
                            if (mouse_row == en_passant_row) and (mouse_column == en_passant_column):
                                board[mouse_row - 1][mouse_column] = ''
                            elif mouse_row == 7:
                                gamestate = 'promotion'
                                promotion_square = [mouse_row, mouse_column]
                    game += add_turn(possible_moves, board, currentpiece, currentrow, currentcolumn, mouse_row,
                                     mouse_column, en_passant_row, en_passant_column)
                    game_for_ai.append(f'{currentpiece[6:]}{currentrow}{currentcolumn}{mouse_row}{mouse_column}')
                    en_passant_row = -1
                    en_passant_column = -1
                    if 'pawn' in currentpiece:
                        if abs(mouse_row - currentrow) == 2:
                            en_passant_column = currentcolumn
                            if turn == 'white':
                                en_passant_row = currentrow - 1
                            else:
                                en_passant_row = currentrow + 1
                    elif 'king' in currentpiece:
                        if abs(mouse_column - currentcolumn) == 2:
                            board, castling = handle_castling(board, mouse_row, mouse_column, castling)
                        else:
                            if turn == 'white':
                                castling = castling.replace('K', '')
                                castling = castling.replace('Q', '')
                            else:
                                castling = castling.replace('k', '')
                                castling = castling.replace('q', '')
                    elif 'rook' in currentpiece:
                        if currentrow == 7 and currentcolumn == 7:
                            castling = castling.replace('K', '')
                        elif currentrow == 7 and currentcolumn == 0:
                            castling = castling.replace('Q', '')
                        elif currentrow == 0 and currentcolumn == 0:
                            castling = castling.replace('q', '')
                        elif currentrow == 0 and currentcolumn == 7:
                            castling = castling.replace('k', '')
                    if player == 'ai':
                        board[currentrow][currentcolumn] = ''
                    board[mouse_row][mouse_column] = currentpiece
                    currentpiece = None
                    currentrow = None
                    currentcolumn = None
                    draw_board(chessboard, board, light, dark, square)
                    if turn == 'white':
                        turn = 'black'
                    else:
                        turn = 'white'
                        no_of_turns += 1
                        game += f'\n{no_of_turns}.'
                    if len(game_for_ai) >= 9:
                        if game_for_ai[-1] == game_for_ai[-5] == game_for_ai[-9] and game_for_ai[-2] == game_for_ai[-6]:
                            result = 'draw'
                            quit_chess(game, result)
                        elif halfturns >= 50:
                            result = 'draw'
                            print(halfturns)
                            quit_chess(game, result)
                    possible_moves = {}
                    for rowindex, row in enumerate(board):
                        for columnindex, piece in enumerate(row):
                            if piece != '':
                                if piece[:5] == turn:
                                    real_moves = []
                                    legalmoves = legal_moves(piece, rowindex, columnindex, board, castling,
                                                             en_passant_row, en_passant_column)
                                    for legalrow, legalcolumn in legalmoves:
                                        if 'king' in board[legalrow][legalcolumn]:
                                            continue
                                        if 'king' in piece and abs(legalcolumn - columnindex) > 1:
                                            if not check_check(piece[:5], board):
                                                continue
                                            for i in range(abs(legalcolumn - columnindex) - 2):
                                                newboard = [i[:] for i in board]
                                                newboard[legalrow][
                                                    columnindex + sign(legalcolumn - columnindex) * i + 1] = piece
                                                newboard[rowindex][columnindex] = ''
                                                if not check_check(piece[:5], newboard):
                                                    continue
                                        newboard = [i[:] for i in board]
                                        newboard[legalrow][legalcolumn] = piece
                                        newboard[rowindex][columnindex] = ''
                                        if check_check(piece[:5], newboard):
                                            real_moves.append((legalrow, legalcolumn))
                                    possible_moves[piece, rowindex, columnindex] = real_moves
                    for keys in possible_moves:
                        if possible_moves[keys]:  # if there are no available moves
                            break
                    else:
                        all_moves = []
                        for rowindex, row in enumerate(board):
                            for columnindex, piece in enumerate(row):
                                if piece != '':
                                    if piece[:5] != turn:
                                        legalmoves = legal_moves(piece, rowindex, columnindex, board, castling,
                                                                 en_passant_row, en_passant_column)
                                        for move in legalmoves:
                                            all_moves.append(move)
                                    else:
                                        if piece[6:] == 'king':
                                            kings_pos = (rowindex, columnindex)
                        if kings_pos in all_moves:
                            result = (lambda x: 'white' if x == 'black' else 'black')(turn)
                        else:
                            result = 'draw'
                        quit_chess(game, result)
                    if player == 'human':
                        player = 'ai'
                        pieces = 0
                        depth = 2
                        for row in board:
                            for space in row:
                                if space != '':
                                    pieces += 1
                        if 9 <= pieces <= 15:
                            depth = 3
                        elif pieces <= 8:
                            depth = 4
                        if len(game_for_ai) <= 6:
                            current_gameplan = copy.deepcopy(opening_moves)
                            for move in game_for_ai:
                                if move in current_gameplan.keys():
                                    current_gameplan = current_gameplan[move]
                                else:
                                    ai_moves = []
                                    break
                            else:
                                if len(game_for_ai) == 6:
                                    ai_moves = []
                                    ai_moves.append(random.choice(current_gameplan))
                                else:
                                    ai_moves = []
                                    try:
                                        ai_moves.append(random.choice(list(current_gameplan.keys())))
                                    except AttributeError:
                                        ai_moves.append(random.choice(current_gameplan))
                        else:
                            evaluation, ai_moves = minimax(board, depth, turn, castling, en_passant_row,
                                                           en_passant_column, halfturns, [])
                        if ai_moves == []:
                            evaluation, ai_moves = minimax(board, depth, turn, castling, en_passant_row,
                                                           en_passant_column, halfturns, [])
                        print(ai_moves)
                        if ai_moves == []:
                            result = (lambda x: 'white' if x == 'black' else 'black')(turn)
                            quit_chess(game, result)
                    else:
                        player = 'human'

                else:
                    board[currentrow][currentcolumn] = currentpiece
                    currentpiece = None
                    currentrow = None
                    currentcolumn = None
                    draw_board(chessboard, board, light, dark, square)
            if event.type == pygame.MOUSEBUTTONDOWN and currentpiece is None:
                mouse_row = y // square
                mouse_column = x // square
                if board[mouse_row][mouse_column][:5] == turn:
                    currentpiece = board[mouse_row][mouse_column]
                    currentrow = mouse_row
                    currentcolumn = mouse_column
                    board[mouse_row][mouse_column] = ''
                    spot = pygame.Rect(mouse_column * square, mouse_row * square, square, square)
                    pygame.draw.rect(chessboard, spot_colour(mouse_row, mouse_column, light, dark), spot)
        if currentpiece is not None:
            draw_board(chessboard, board, light, dark, square)
            draw_piece(chessboard, currentpiece, square, x, y)
    if gamestate == 'promotion':
        if player == 'ai':
            promotion_bg = pygame.Rect(3 * square, 3 * square, 2 * square, 2 * square)
            events = pygame.event.get()
            for event in events:
                x, y = pygame.mouse.get_pos()
                mouse_row = y // square
                mouse_column = x // square
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if turn == 'black':  # promotion for white
                    pygame.draw.rect(chessboard, dark, promotion_bg)
                else:  # promotion for black
                    pygame.draw.rect(chessboard, light, promotion_bg)
                draw_promotion(chessboard, (lambda x: 'white' if x == 'black' else 'black')(turn), square)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_row == 3 and mouse_column == 3:
                        promotion_piece = 'knight'
                    elif mouse_row == 3 and mouse_column == 4:
                        promotion_piece = 'rook'
                    elif mouse_row == 4 and mouse_column == 3:
                        promotion_piece = 'bishop'
                    elif mouse_row == 4 and mouse_column == 4:
                        promotion_piece = 'queen'
                    if promotion_piece != '':
                        board[promotion_square[0]][promotion_square[
                            1]] = f'{(lambda x: "white" if x == "black" else "black")(turn)}_{promotion_piece}'
                        promotion_piece = ''
                        gamestate = 'chessboard'
                        draw_board(chessboard, board, light, dark, square)
        else:
            board[promotion_square[0]][
                promotion_square[1]] = f'{(lambda x: "white" if x == "black" else "black")(turn)}_queen'
            gamestate = 'chessboard'
            draw_board(chessboard, board, light, dark, square)
        for rowindex, row in enumerate(board):
            for columnindex, piece in enumerate(row):
                if piece != '':
                    if piece[:5] == turn:
                        real_moves = []
                        legalmoves = legal_moves(piece, rowindex, columnindex, board, castling,
                                                 en_passant_row, en_passant_column)
                        for legalrow, legalcolumn in legalmoves:
                            if 'king' in board[legalrow][legalcolumn]:
                                continue
                            if 'king' in piece and abs(legalcolumn - columnindex) > 1:
                                if not check_check(piece[:5], board):
                                    continue
                                for i in range(abs(legalcolumn - columnindex) - 2):
                                    newboard = [i[:] for i in board]
                                    newboard[legalrow][
                                        columnindex + sign(legalcolumn - columnindex) * i + 1] = piece
                                    newboard[rowindex][columnindex] = ''
                                    if not check_check(piece[:5], newboard):
                                        continue
                            newboard = [i[:] for i in board]
                            newboard[legalrow][legalcolumn] = piece
                            newboard[rowindex][columnindex] = ''
                            if check_check(piece[:5], newboard):
                                real_moves.append((legalrow, legalcolumn))
                        possible_moves[piece, rowindex, columnindex] = real_moves
    pygame.display.flip()
