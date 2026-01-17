import tkinter as tk
import random
import time

ROWS = 6
COLUMNS = 7
PLAYER = 1
AI = 2
EMPTY = 0

# ---------- GAME LOGIC ----------
def create_board():
    return [[0]*COLUMNS for _ in range(ROWS)]

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == EMPTY:
            return r

def winning_move(board, piece):
    for r in range(ROWS):
        for c in range(COLUMNS-3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def get_valid_locations(board):
    return [c for c in range(COLUMNS) if is_valid_location(board, c)]

# ---------- EASY AI (FAST) ----------
def ai_move_easy(board):
    valid_cols = get_valid_locations(board)

    # 1️⃣ Try to win
    for col in valid_cols:
        row = get_next_open_row(board, col)
        board[row][col] = AI
        if winning_move(board, AI):
            board[row][col] = EMPTY
            return col
        board[row][col] = EMPTY

    # 2️⃣ Try to block player
    for col in valid_cols:
        row = get_next_open_row(board, col)
        board[row][col] = PLAYER
        if winning_move(board, PLAYER):
            board[row][col] = EMPTY
            return col
        board[row][col] = EMPTY

    # 3️⃣ Otherwise random (mistakes allowed)
    return random.choice(valid_cols)

# ---------- GUI ----------
class Connect4GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Connect 4 (Easy AI)")
        self.canvas = tk.Canvas(self.window, width=700, height=600, bg="blue")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.player_click)
        self.reset_game()

    def reset_game(self):
        self.board = create_board()
        self.game_over = False
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLUMNS):
                color = "white"
                if self.board[r][c] == PLAYER:
                    color = "red"
                elif self.board[r][c] == AI:
                    color = "yellow"

                self.canvas.create_oval(
                    c*100+10, r*100+10,
                    c*100+90, r*100+90,
                    fill=color
                )

    def show_message(self, text):
        self.canvas.create_text(350, 300, text=text, font=("Arial", 36), fill="white")
        self.window.update()
        time.sleep(1.5)
        self.reset_game()

    def player_click(self, event):
        if self.game_over:
            return

        col = event.x // 100
        if is_valid_location(self.board, col):
            row = get_next_open_row(self.board, col)
            drop_piece(self.board, row, col, PLAYER)
            self.draw_board()

            if winning_move(self.board, PLAYER):
                self.game_over = True
                self.show_message("YOU WIN!")
                return

            self.ai_turn()

    def ai_turn(self):
        col = ai_move_easy(self.board)
        row = get_next_open_row(self.board, col)
        drop_piece(self.board, row, col, AI)
        self.draw_board()

        if winning_move(self.board, AI):
            self.game_over = True
            self.show_message("AI WINS!")

    def run(self):
        self.window.mainloop()

# ---------- RUN ----------
if __name__ == "__main__":
    Connect4GUI().run()
