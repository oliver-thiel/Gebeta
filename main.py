#Gebeta game implementation

def main():
    print("Do you want to play or analyze the Gebeta game?")
    print("Type 0 to play, or an integer n > 0 to analyze the game tree up to depth n.")

    while True:  # Repeat until a valid input is given
        print("Enter your choice: ")
        user_input = input()
        if user_input.isdigit():  # Only numbers are accepted
            choice : int = int(user_input)  # Convert the input to an integer
            if choice >= 0:  # Only non-negative integers are valid
                break
            else:
                print("Invalid input. Please enter a valid integer.")

    if choice == 0:
        import Gebeta_MCTS
        Gebeta_MCTS.play_game()
    else:
        import Gebeta_analysis
        Gebeta_analysis.analyse_game_tree(choice)


if __name__ == "__main__":
    main()