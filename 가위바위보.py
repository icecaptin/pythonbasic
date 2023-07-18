import random

class Contestant:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def choose_move(self):
        pass

    def update_score(self, points):
        self.score += points

class Human(Contestant):
    def choose_move(self):
        player = input("Enter name of human:")
        move = input("Enter your move (rock/paper/scissors): ").lower()
        while move not in ['rock', 'paper', 'scissors']:
            print("Invalid move! Please choose rock, paper, or scissors.")
            move = input("Enter your move (rock/paper/scissors): ").lower()
        return move

class Computer(Contestant):
    def choose_move(self):
        return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(player_move, computer_move):
    if player_move == computer_move:
        return "TIE"
    elif (player_move == "rock" and computer_move == "scissors") or \
         (player_move == "paper" and computer_move == "rock") or \
         (player_move == "scissors" and computer_move == "paper"):
        return "Player"
    else:
        return "Computer"

# Main game loop
def play_game():
    player = Human("Player")
    computer = Computer("Computer")
    game_round = 1

    while game_round <= 3:
        print(f"Round {game_round}")
        player_move = player.choose_move()
        computer_move = computer.choose_move()

        print(f"Player chose: {player_move}")
        print(f"Computer chose: {computer_move}")

        winner = determine_winner(player_move, computer_move)
        if winner == "Player":
            player.update_score(1)
            print("Player wins the round!")
        elif winner == "Computer":
            computer.update_score(1)
            print("Computer wins the round!")
        else:
            print("It's a tie!")

        game_round += 1
        print()

    # Display final scores and determine the overall winner
    print("Final Scores:")
    print(f"Player: {player.score}")
    print(f"Computer: {computer.score}")

    if player.score > computer.score:
        print("Player wins the match!")
    elif player.score < computer.score:
        print("Computer wins the match!")
    else:
        print("It's a tie!")

# Start the game
play_game()
