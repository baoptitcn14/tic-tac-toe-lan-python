# LAN Tic-Tac-Toe (Caro 3x3)

A simple Player vs Player Tic-Tac-Toe game that works over a Local Area Network (LAN) using Python, Sockets, and Tkinter.

## Features
- 3x3 Grid
- Real-time multiplayer over LAN
- Simple GUI using Tkinter
- Clear and easy to understand code

## Requirements
- Python 3.x

## How to play
1. **Run the Server**: On one computer, run `python server.py`. This player will be 'X'.
2. **Find the IP**: Find the IP address of the server computer (e.g., using `ipconfig` on Windows).
3. **Run the Client**: On the second computer, run `python client.py`.
4. **Connect**: When prompted, enter the Server's IP address. This player will be 'O'.
5. **Start Playing**: Server player ('X') goes first.

## Files
- `server.py`: The game host and Player X.
- `client.py`: The player joining the game and Player O.
