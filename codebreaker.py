## Simple Python Code Breaker Game
import random

colors = ["black", "blue", "green", "red", "yellow", "white"]

def set_master_code():
    return [get_random_color() for i in range(0,4)]

def get_random_color():
    return colors[random.randint(0, 5)]

def code_breaker_play(master_code, player_code):
    play_feedback = []
    for i in range(0,4):
        if master_code[i] == player_code[i]:
            play_feedback.append("X")
        elif player_code[i] in master_code:
            play_feedback.append("0")
    random.shuffle(play_feedback)
    return play_feedback

def print_player_plays(all_player_plays, all_code_maker_feedback):
    format_row = "{:<32} {:<32}"
    print(format_row.format("\n--Player Play--", "--Code Maker Feedback--"))
    for i in range(0, len(all_player_plays)):
        print(format_row.format(', '.join(map(str, all_player_plays[i])), ', '.join(map(str, all_code_maker_feedback[i]))))

def get_user_input(message):
    user_input = ""
    player_code_ints = []
    while len(user_input) < 4 or any(y > 6 for y in player_code_ints):
        user_input = input(message)
        player_code_ints = [int(x) for x in user_input.split(',')]
    return player_code_ints

def play_game():
    print("Welcome to Mastermind: --- Setting Master Code ---")
    print("Select Options: 1:black, 2:blue, 3:green, 4:red, 5:yellow, 6:white")
    print("X = Right Position & Color.  0 = Right Color Wrong Position. \n")
    master_code = set_master_code()

    player_code_ints = []
    all_player_plays = []
    all_code_maker_feedback = []
    for i in range(0, 10):
        player_code_ints = get_user_input("\nEnter 4 comma separated numbers:")
        player_code = [colors[x-1] for x in player_code_ints]
        all_player_plays.append(player_code)
        play_result = code_breaker_play(master_code, player_code)
        all_code_maker_feedback.append(play_result)
        print_player_plays(all_player_plays, all_code_maker_feedback)

        if(len(play_result) == 4 and all(x == "X" for x in play_result)):
            print("You Won")
            return

    print("Sorry Try Again :( ")
    print("The code was: " + ', '.join(map(str,master_code)))

def main():
    play_game()

main()