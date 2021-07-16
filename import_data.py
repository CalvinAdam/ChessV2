import chess
from chessV2_functions import convert_to_number_import, convert_to_number
import chess.pgn
import sys
try:
    import cPickle as pickle
except ImportError:
    import pickle


def convert_data(move: str, piece: str):
    piece_conversion = {'b': 'bishop', 'k': 'king', 'n': 'knight', 'p': 'pawn',
                        'q': 'queen',
                        'r': 'rook', 'B': 'bishop', 'K': 'king', 'N': 'knight',
                        'P': 'pawn',
                        'Q': 'queen', 'R': 'rook'}
    move_for_ai = piece_conversion[piece]
    move_for_ai += ''.join(map(lambda x: str(x), (convert_to_number_import(move[:2:]))))
    move_for_ai += ''.join(map(lambda x: str(x), (convert_to_number_import(move[2:]))))
    return move_for_ai


def time_to_int(time: str):
    if time == '-':
        return 9999
    timestring = ''
    for letter in time:
        try:
            int(letter)
            timestring += letter
        except ValueError:
            break
    return int(timestring)


# Read pgn file:
# with open("C:/Users/Calvin/Downloads/chess_stuff/CORRUPT.lichess_db_standard_rated_2013-07.pgn") as f:
#     for i in range(20000):
#         game = chess.pgn.read_game(f)
#         print(str(game.variations[0])[3])

with open("H:/chess_stuff/lichess_db_standard_rated_2016-07.pgn/lichess_db_standard_rated_2016-07.pgn") as f:
    my_database = {}
    counter = 0
    for i in range(1000000):
        game = chess.pgn.read_game(f)
        if game:
            if game.headers['BlackElo'] != '?' != game.headers['WhiteElo'] and time_to_int(game.headers['TimeControl']) > 179:
                if int(game.headers['BlackElo']) + int(game.headers['WhiteElo']) > 4500:
                    counter += 1
                    game_for_ai = []
                    for index, turn in enumerate(game.mainline()):
                        if index < 8:
                            number_tuple = convert_to_number(str(turn.move)[-2:])
                            number = (number_tuple[1] - 1) * 8 + number_tuple[0]
                            piece = str(turn.board().piece_at(number))
                            move = str(turn.move)
                            game_for_ai.append(convert_data(move, piece))
                        else:
                            break
                    if len(game_for_ai) == 8:
                        if game_for_ai[0] not in my_database.keys():
                            my_database[game_for_ai[0]] = {}
                        if game_for_ai[1] not in my_database[game_for_ai[0]].keys():
                            my_database[game_for_ai[0]][game_for_ai[1]] = {}
                        if game_for_ai[2] not in my_database[game_for_ai[0]][game_for_ai[1]].keys():
                            my_database[game_for_ai[0]][game_for_ai[1]][game_for_ai[2]] = {}
                        if game_for_ai[3] not in my_database[game_for_ai[0]][game_for_ai[1]][game_for_ai[2]].keys():
                            my_database[game_for_ai[0]][game_for_ai[1]][game_for_ai[2]][game_for_ai[3]] = {}
                        if game_for_ai[4] not in my_database[game_for_ai[0]][game_for_ai[1]][game_for_ai[2]][
                            game_for_ai[3]].keys():
                            my_database[game_for_ai[0]][game_for_ai[1]][game_for_ai[2]][game_for_ai[3]][
                                game_for_ai[4]] = {}
                        if game_for_ai[5] not in my_database[game_for_ai[0]][game_for_ai[1]][game_for_ai[2]][game_for_ai[3]][
                            game_for_ai[4]].keys():
                            my_database[game_for_ai[0]][game_for_ai[1]][game_for_ai[2]][game_for_ai[3]][
                                game_for_ai[4]][game_for_ai[5]] = {}
                        if game_for_ai[6] not in my_database[game_for_ai[0]][game_for_ai[1]][game_for_ai[2]][game_for_ai[3]][
                                game_for_ai[4]][game_for_ai[5]].keys():
                            my_database[game_for_ai[0]][game_for_ai[1]][game_for_ai[2]][game_for_ai[3]][
                                game_for_ai[4]][game_for_ai[5]][game_for_ai[6]] = []
                        my_database[game_for_ai[0]][game_for_ai[1]][game_for_ai[2]][game_for_ai[3]][
                            game_for_ai[4]][game_for_ai[5]][game_for_ai[6]].append(game_for_ai[7])
pickle.dump(my_database, open('opening_moves_1000000.pkl', 'wb'))
