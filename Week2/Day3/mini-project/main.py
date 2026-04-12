def create_board():
	return [[" " for _ in range(3)] for _ in range(3)]


def display_board(board):
	print("\n  1   2   3")
	for row_index, row in enumerate(board, start=1):
		print(f"{row_index} {row[0]} | {row[1]} | {row[2]}")
		if row_index < 3:
			print(" ---+---+---")
	print()


def player_input(player, board):
	while True:
		raw = input(f"Player {player}, enter row and column (e.g. 1 3): ").strip()
		parts = raw.replace(",", " ").split()

		if len(parts) != 2:
			print("Please enter exactly two numbers.")
			continue

		if not (parts[0].isdigit() and parts[1].isdigit()):
			print("Invalid input. Use numbers from 1 to 3.")
			continue

		row = int(parts[0]) - 1
		col = int(parts[1]) - 1

		if row not in range(3) or col not in range(3):
			print("Out of range. Row and column must be between 1 and 3.")
			continue

		if board[row][col] != " ":
			print("That position is already taken. Choose another one.")
			continue

		return row, col


def check_win(board, player):
	for row in board:
		if all(cell == player for cell in row):
			return True

	for col in range(3):
		if all(board[row][col] == player for row in range(3)):
			return True

	if all(board[i][i] == player for i in range(3)):
		return True

	if all(board[i][2 - i] == player for i in range(3)):
		return True

	return False


def check_tie(board):
	return all(cell != " " for row in board for cell in row)


def play():
	board = create_board()
	current_player = "X"

	print("Welcome to Tic Tac Toe!")
	print("Player X goes first.")

	while True:
		display_board(board)
		row, col = player_input(current_player, board)
		board[row][col] = current_player

		if check_win(board, current_player):
			display_board(board)
			print(f"Player {current_player} wins!")
			break

		if check_tie(board):
			display_board(board)
			print("It's a tie!")
			break

		current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
	play()
