import chess
import chess.pgn
import io
from collections import Counter

def showMySeq(file_path):
    seqCounter = Counter()

    with open(file_path, 'r') as file:
        pgnData = file.read()
        sequences = pgnData.split('#')
    
    for sequence in sequences:
        board = chess.Board()
        pgnIo = io.StringIO(sequence.strip())
        game = chess.pgn.read_game(pgnIo)
        # print(game) # o sa punem si datele despre joc
        if game is not None:
            legalMoves = []
            for move in game.mainline_moves():
                if board.is_legal(move):
                    moveText = board.san(move).replace('+', '').replace('#', '')
                    legalMoves.append(moveText)
                    print(moveText)
                    board.push(move)

            print('end game moves --> show board :')            
            print('             ')
            print('-------------')
            print('             ')
            print(board)        
            print(f'legal_moves are : {legalMoves}')
            print('end game')
            if len(legalMoves) >= 3:
                last_three_moves = []

                for move in legalMoves[-3:]:
                    last_three_moves.append(move)
                
                if len(last_three_moves) == 3:
                    seqCounter[tuple(last_three_moves)] += 1
            
    return {seq: count for seq, count in seqCounter.items() if count >= 2}

file_path = 'games.pgn'
seqMoves = showMySeq(file_path)
print('Acum secventele :')
for sequence, count in seqMoves.items():
    print(f"{sequence}: ---> de {count} ori")