import socket
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog

class TicTacToeClient:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Caro 3x3 - Client (Player O)")
        
        self.board = [" " for _ in range(9)]
        self.my_turn = False
        self.buttons = []
        
        # Ask for server IP
        self.host = simpledialog.askstring("Connect", "Enter Server IP Address:", initialvalue="127.0.0.1")
        if not self.host:
            self.window.destroy()
            return
            
        self.port = 5555
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.client_socket.connect((self.host, self.port))
            self.create_widgets()
            self.status_label.config(text="Connected! Waiting for Player X...")
            threading.Thread(target=self.receive_data, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"Could not connect: {e}")
            self.window.destroy()

    def create_widgets(self):
        for i in range(9):
            btn = tk.Button(self.window, text=" ", font=('normal', 20), width=5, height=2,
                           command=lambda i=i: self.on_click(i))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)
        
        self.status_label = tk.Label(self.window, text="Opponent's turn", font=('normal', 12))
        self.status_label.grid(row=3, column=0, columnspan=3)

    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                index = int(data)
                self.window.after(0, lambda: self.opponent_move(index))
            except:
                break

    def on_click(self, index):
        if self.my_turn and self.board[index] == " ":
            self.board[index] = "O"
            self.buttons[index].config(text="O")
            self.my_turn = False
            self.status_label.config(text="Opponent's turn")
            self.client_socket.send(str(index).encode())
            self.check_winner()

    def opponent_move(self, index):
        self.board[index] = "X"
        self.buttons[index].config(text="X")
        self.my_turn = True
        self.status_label.config(text="Your turn (O)")
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
        self.my_turn = False
        self.status_label.config(text="Opponent's turn")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    client = TicTacToeClient()
    client.run()
