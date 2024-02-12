import chess
import chess.svg
import chess.pgn
import io
import random
import tkinter as tk
from tkinter import filedialog, messagebox
import cairosvg
from PIL import Image, ImageTk
import time
import openai

openai.api_key = "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"

conversation = [
    {"role": "system", "content": "You are a chess expert answering questions."}
]

engine_path = "./stockfish/stockfish-windows-x86-64-modern.exe"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

root = tk.Tk()
root.title('Tabla de Sah')

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


def update_board():
    board_svg = chess.svg.board(board=board)
    board_svg = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + board_svg
    png_data = cairosvg.svg2png(bytestring=board_svg.encode('utf-8'))
    board_image = Image.open(io.BytesIO(png_data))
    board_photo = ImageTk.PhotoImage(board_image)
    canvas.create_image(0, 0, image=board_photo, anchor=tk.NW)
    canvas.image = board_photo
    update_turn_label()


def update_turn_label():
    turn_text = "Negru să mute" if board.turn == chess.BLACK else "Alb să mute"
    turn_label.config(text=turn_text)


def perform_move():
    move_uci = move_entry.get()
    if move_uci == "":
        computer_move()
    else:
        try:
            move = chess.Move.from_uci(move_uci)
            if move in board.legal_moves:
                board.push(move)
                # Adăugăm mutarea în joc
                node = game.add_variation(move)
                update_board()
            else:
                chat.insert(tk.END, "Mutare ilegală, încearcă din nou.\n")
        except ValueError:
            chat.insert(tk.END, "Format invalid, introdu mutarea din nou.\n")


def computer_move():
    if not board.is_game_over():
        move = engine.play(board, chess.engine.Limit(time=1.5)).move
        #time.sleep(10)
        board.push(move)
        node = game.add_variation(move)
        update_board()


def display_message():
    user_input = message_entry.get("1.0", tk.END)
    conversation.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-1106:personal::8jZ5HFKc",
        messages=conversation
    )
    chat.delete("1.0", tk.END)
    chat.insert(tk.END, response.choices[0].message["content"])
    conversation.append({"role": "assistant", "content": response.choices[0].message["content"]})


def load_pgn():
    global game
    filepath = filedialog.askopenfilename(filetypes=[("PGN Files", "*.pgn")])
    if filepath:
        with open(filepath, 'r') as pgn_file:
            game = chess.pgn.read_game(pgn_file)
            board.reset()
            for move in game.mainline_moves():
                board.push(move)
            update_board()


def save_pgn():
    filepath = filedialog.asksaveasfilename(defaultextension=".pgn", filetypes=[("PGN Files", "*.pgn")])
    if filepath:
        with open(filepath, 'w') as pgn_file:
            game = chess.pgn.Game.from_board(board)
            print(game, file=pgn_file, end="\n\n")


def show_moves():
    def display_moves(node, board, moves_text_widget):
        if node.move is not None:
            move_san = board.san(node.move) + "\n"
            moves_text_widget.insert(tk.END, move_san)
            board.push(node.move)

        for variation in node.variations:
            display_moves(variation, board.copy(), moves_text_widget)

        if node.move is not None:
            board.pop()

    moves_window = tk.Toplevel(root)
    moves_window.title("Mutările Partidei")
    moves_text = tk.Text(moves_window, height=20, width=50)
    moves_text.pack()

    display_moves(game, chess.Board(), moves_text)


def show_board():
    board_window = tk.Toplevel(root)
    board_window.title("Tabla in notatie algebrica:")
    board_text = tk.Text(board_window, height=20, width=50)
    board_text.pack()
    board_text.insert(tk.END, str(board))


turn_label = tk.Label(left_frame, text="Alb să mute", font=("Arial", 16))
turn_label.pack(pady=(10,10))

chat = tk.Text(left_frame, height=15, width=30, padx=5, pady=5)
chat.pack(padx=(10, 15), pady=(0,10))
chat.insert(tk.END, "Bun venit în jocul de șah!\n")

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack(side=tk.LEFT)

move_entry = tk.Entry(right_frame)
move_entry.pack(padx=(0, 10), pady=(10, 10))
move_button = tk.Button(right_frame, text="Efectuează mutarea", command=perform_move)
move_button.pack(padx=(0, 10), pady=(0, 10))

show_moves_button = tk.Button(right_frame, text="Afișează Mutările", command=show_moves)
show_moves_button.pack(padx=(0, 10), pady=(0, 10))

message_entry = tk.Text(right_frame, height=5, width=30)
message_entry.pack(padx=(0, 10), pady=(0, 10))

message_button = tk.Button(right_frame, text="Trimite Mesajul", command=display_message)
message_button.pack(padx=(0, 10), pady=(0, 10))

show_board_button = tk.Button(right_frame, text="Afișează Tabla In Notatie Algebrica", command=show_board)
show_board_button.pack(padx=(0, 10), pady=(0, 10))

pgn_button = tk.Button(right_frame, text="Încarcă PGN", command=load_pgn)
pgn_button.pack(padx=(0, 10), pady=(0, 10))

save_pgn_button = tk.Button(right_frame, text="Salvează PGN", command=save_pgn)
save_pgn_button.pack(padx=(0, 10), pady=(0, 10))

board = chess.Board()
game = chess.pgn.Game()

update_board()

root.mainloop()