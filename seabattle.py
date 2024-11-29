import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Ask for player's name
player_name = input("Enter your name: ")

board = [[" " for _ in range(7)] for _ in range(7)]  
player_board = [[" " for _ in range(7)] for _ in range(7)]  

# Ship sizes and placement
ships = [3, 2, 2, 1, 1, 1, 1] 
for size in ships:
    placed = False
    while not placed:
        x, y = random.randint(0, 6), random.randint(0, 6)
        direction = random.choice(["H", "V"])  
        if direction == "H" and y + size <= 7 and all(board[x][y + i] == " " for i in range(size)):
            for i in range(size):
                board[x][y + i] = "S"
            placed = True
        elif direction == "V" and x + size <= 7 and all(board[x + i][y] == " " for i in range(size)):
            for i in range(size):
                board[x + i][y] = "S"
            placed = True

shots = 0  
all_sunk = False  

# Main game loop
while not all_sunk:
    clear_screen()
    
    print(f"Welcome, {player_name}!")
    print("  A B C D E F G")
    for i, row in enumerate(player_board):
        print(f"{i+1} " + " ".join(row))
    
    coord = input("Enter shot coordinates (e.g., B3): ")
    if len(coord) != 2 or not coord[0].isalpha() or not coord[1].isdigit():
        print("Invalid coordinate format. Try again.")
        continue

    y = ord(coord[0].upper()) - ord("A")  
    x = int(coord[1]) - 1  

    if not (0 <= x < 7 and 0 <= y < 7):
        print("Coordinates are out of bounds. Try again.")
        continue

    if player_board[x][y] != " ":
        print("You already shot here. Try again.")
        continue

    shots += 1  

    if board[x][y] == "S":
        player_board[x][y] = "H" 
        board[x][y] = "H"  
        print("Hit!")
        sunk = True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x, y
            while 0 <= nx < 7 and 0 <= ny < 7 and board[nx][ny] == "H":
                nx, ny = nx + dx, ny + dy
            if 0 <= nx < 7 and 0 <= ny < 7 and board[nx][ny] == "S":
                sunk = False
        if sunk:
            print("Ship sunk!")
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x, y
                while 0 <= nx < 7 and 0 <= ny < 7 and board[nx][ny] == "H":
                    player_board[nx][ny] = "X"  
                    nx, ny = nx + dx, ny + dy
    else:
        player_board[x][y] = "M" 
        print("Miss.")

    all_sunk = all(cell != "S" for row in board for cell in row)

# Final message
clear_screen() 
print(f"Congratulations, {player_name}! You sunk all the ships in {shots} shots.")
