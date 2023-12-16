from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Initialize the chatbot
chatbot = ChatBot('ChessBot')

# Initialize a trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot on the English language corpus
trainer.train('chatterbot.corpus.english')

# Add chess rules in English
trainer.train([
    "What is the goal of chess?",
    "The goal of chess is to checkmate the opponent's king, which means putting it in a position where it cannot escape capture.",
    
    "Explain pawn movements.",
    "The pawn can move forward one square but captures diagonally. On its first move, it has the option to advance two squares.",
    
    "Explain rook movements.",
    "The rook moves horizontally or vertically any number of squares.",
    
    "Explain knight movements.",
    "The knight has a special L-shaped move. It is the only piece that can jump over other pieces.",
    
    "Explain bishop movements.",
    "The bishop moves diagonally any number of squares.",
    
    "Explain queen movements.",
    "The queen moves horizontally, vertically, or diagonally any number of squares.",
    
    "Explain king movements.",
    "The king moves horizontally, vertically, or diagonally one square.",
    
    "What is check and checkmate?",
    "Check occurs when the king is under threat, and the player must protect it. Checkmate is when the king cannot be saved, and the game ends with the opponent winning.",
    
    "Explain castling.",
    "Castling is a special move where the king and one of the rooks move simultaneously. It cannot be used if the king is in check or if either piece has been moved previously.",
    
    "Explain en passant.",
    "En passant is a special pawn move where a pawn can capture another pawn that has moved two squares forward.",
    
    "Explain pawn promotion.",
    "If a pawn reaches the opponent's back rank, it is promoted to another piece, usually a queen."
])

# Test the chatbot
response = chatbot.get_response("Explain pawn promotion.")
print(response)
