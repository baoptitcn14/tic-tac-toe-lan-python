import socket
import threading
import tkinter as tk
from tkinter import messagebox

class TicTacToeServer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Caro 3x3 - Server (Player X)")
        
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.my_turn = True
        self.buttons = []
        
        # Setup Network
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '0.0.0.0' # Listen on all interfaces
        self.port = 5555
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        
        self.conn = None
        self.addr = None
        
        self.create_widgets()
        
        # Start networking thread
        threading.Thread(target=self.wait_for_connection, daemon=True).start()
        
    def create_widgets(self):
        for i in range(9):
            btn = tk.Button(self.window, text=" ", font=('normal', 20), width=5, height=2,
                           command=lambda i=i: self.on_click(i))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)
        
        self.status_label = tk.Label(self.window, text="Waiting for opponent...", font=('normal', 12))
        self.status_label.grid(row=3, column=0, columnspan=3)

    def wait_for_connection(self):
        self.conn, self.addr = self.server_socket.accept()
        self.status_label.config(text=f"Connected to {self.addr[0]}")
        threading.Thread(target=self.receive_data, daemon=True).start()

    def receive_data(self):
        while True:
            try:
                data = self.conn.recv(1024).decode()
                if not data:
                    break
                index = int(data)
                self.window.after(0, lambda: self.opponent_move(index))
            except:
                break

    def on_click(self, index):
        if self.my_turn and self.board[index] == " " and self.conn:
            self.board[index] = "X"
            self.buttons[index].config(text="X")
            self.my_turn = False
            self.status_label.config(text="Opponent's turn")
            self.conn.send(str(index).encode())
            self.check_winner()

    def opponent_move(self, index):
        self.board[index] = "O"
        self.buttons[index].config(text="O")
        self.my_turn = True
        self.status_label.config(text="Your turn (X)")
        self.check_winner()

    def check_winner(self):
        win_coords = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for coord in win_coords:
            if self.board[coord[0]] == self.board[coord[1]] == self.board[coord[2]] != " ":
                messagebox.showinfo("Game Over", f"Player {self.board[coord[0]]} wins!")
                self.reset_game()
                return
        if " " not in self.board:
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_game()

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        for btn in self.buttons:
            btn.config(text=" ")
        self.my_turn = True
        self.status_label.config(text="Your turn (X)")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    server = TicTacToeServer()
    server.run()
