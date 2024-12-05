import random, os, time

# Function to clear the screen (removes old text)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display the game board
def display_board(board):
    # Print column labels (A-G)
    print("  A B C D E F G")
    for row_num, row in enumerate(board):
        # Print each row with its number and the board cells
        print(f"{row_num + 1} " + " ".join(row))

# Function to place ships on the hidden board
def place_ships(hidden_board, ship_sizes):
    # Helper function to check if a ship can be placed in a valid position
    def is_valid_placement(row, col, size, direction):
        for i in range(size):  # Loop through each part of the ship
            r = row + direction[0] * i  # Calculate the row for the current segment
            c = col + direction[1] * i  # Calculate the column for the current segment

            # Check if the segment is within the board and the cell is empty
            if not (0 <= r < 7 and 0 <= c < 7) or hidden_board[r][c] != " ":
                return False

            # Check surrounding cells to ensure no ships are adjacent
            for dr in range(-1, 2):  # Check rows above, below, and same row
                for dc in range(-1, 2):  # Check columns left, right, and same column
                    nr, nc = r + dr, c + dc  # Calculate the neighboring cell
                    if 0 <= nr < 7 and 0 <= nc < 7 and hidden_board[nr][nc] == "S":
                        return False
        return True  # All checks passed, placement is valid

    for ship_size in ship_sizes:  # Loop through each ship size
        placed = False  # Flag to indicate if the ship is placed
        while not placed:  # Keep trying until the ship is placed
            row = random.randint(0, 6)  # Random starting row
            col = random.randint(0, 6)  # Random starting column
            direction = random.choice([(0, 1), (1, 0)])  # Randomly choose horizontal or vertical
            if is_valid_placement(row, col, ship_size, direction):  # Check placement validity
                for i in range(ship_size):  # Place the ship
                    r = row + direction[0] * i  # Calculate the row
                    c = col + direction[1] * i  # Calculate the column
                    hidden_board[r][c] = "S"  # Mark the cell as part of the ship
                placed = True  # Ship placed successfully

# Function to handle a single player's turn
def take_turn(player_board, hidden_board):
    while True:  # Repeat until a valid move is made
        move = input("Enter a coordinate to shoot (e.g., B3): ").upper()

        # Validate input: must be a letter (A-G) and number (1-7)
        if len(move) != 2 or not move[0].isalpha() or not move[1].isdigit():
            print("Invalid input. Use a letter (A-G) and a number (1-7).")
            time.sleep(1.2)
            continue

        col = ord(move[0]) - ord("A")  # Convert letter to column index
        row = int(move[1]) - 1  # Convert number to row index

        # Check if the move is within the board
        if not (0 <= row < 7 and 0 <= col < 7):
            print("Out of bounds! Try again.")
            time.sleep(1.2)
            continue

        # Check if the cell has already been targeted
        if player_board[row][col] != " ":
            print("You already shot here! Try a different spot.")
            time.sleep(1.2)
            continue

        # If all checks pass, process the shot
        if hidden_board[row][col] == "S":  # Hit a ship
            player_board[row][col] = "H"  # Mark the hit on the player's board
            hidden_board[row][col] = "H"  # Mark the hit on the hidden board
        else:  # Missed
            player_board[row][col] = "M"  # Mark the miss on the player's board

        return all(cell != "S" for row in hidden_board for cell in row)  # Check if all ships are sunk

# Function to play a single game
def play_game(player_name):
    hidden_board = [[" " for _ in range(7)] for _ in range(7)]  # Board with ships
    player_board = [[" " for _ in range(7)] for _ in range(7)]  # Player's view of the board
    ship_sizes = [3, 2, 2, 1, 1, 1, 1]  # Sizes of the ships to place
    place_ships(hidden_board, ship_sizes)  # Place ships on the hidden board

    shots_taken = 0  # Count the number of shots taken
    game_over = False  # Flag to indicate if the game is over

    while not game_over:  # Keep playing until all ships are sunk
        clear_screen()
        display_board(player_board)  # Show the current player's board
        shots_taken += 1
        game_over = take_turn(player_board, hidden_board)  # Player takes a turn

    clear_screen()
    display_board(player_board)  # Show the final board
    print(f"Congratulations, {player_name}! You sunk all the ships in {shots_taken} shots.")
    return shots_taken

# Main function to manage the game and leaderboard
# Main function that handles the flow of the game and the leaderboard
def main():
    leaderboard = []  # This list will store players' scores (name and shots taken)

    while True:  # Infinite loop to keep the game running until the player decides to stop
        clear_screen()  # Clear the screen to make the game look cleaner
        player_name = input("Enter your name: ")  # Ask the player for their name
        shots_taken = play_game(player_name)  # Call the play_game function, pass the player's name, and get the shots taken in the game
        leaderboard.append((player_name, shots_taken))  # Add the player's name and score (shots taken) to the leaderboard

        # Ask if the player wants to play again
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()  # Get the player's choice and clean the input
        if play_again != "yes":  # If the player doesn't want to play again (they enter anything other than "yes")
            # Sort the leaderboard by the number of shots taken (ascending order)
            leaderboard.sort(key=sort_by_shots)
            print("\nLeaderboard:")  # Print a message indicating the leaderboard
            for rank, (name, shots) in enumerate(leaderboard, start=1):  # For each player, print their rank, name, and shots taken
                print(f"{rank}. {name} - {shots} shots")  # Display each player's score
            break  # Break out of the loop, ending the game

# Function to sort the leaderboard by the number of shots taken
def sort_by_shots(player):
    return player[1]  # Return the number of shots taken to use it as the sorting key

# Run the game by calling the main function
main()
