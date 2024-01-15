from collections import Counter
import re

def ReadFromGames(filePath):
    with open(filePath, 'r') as file:
        for line in file:
            yield line.strip()

def getLastThreeMoves(game):
    moves = re.sub(r'\+|\#', '', game).split()
    if len(moves) < 3:
        return []
    lastMoves = moves[-3:]
    return lastMoves

def frequentSequence(filePath, minimumFreq=2):
    games = ReadFromGames(filePath)
    seqCounter = Counter()
    
    for game in games:
        sequence = tuple(getLastThreeMoves(game))
        if sequence:
            seqCounter[sequence] += 1

    return {seq: count for seq, count in seqCounter.items() if count >= minimumFreq}

filePath = 'games.txt'
frequent_sequences = frequentSequence(filePath)
for sequence, count in frequent_sequences.items():
    print(f"{sequence}: ---> de {count} ori")
