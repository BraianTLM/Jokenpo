import os
import random
from colorama import Fore, init
from time import sleep
from collections import Counter

init(autoreset=True)

# History of player choices for performance analysis
player1_choices = []
computer_choices = []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_screen():
    print(Fore.YELLOW + '=' * 60)
    print(Fore.YELLOW + '                   Vamos jogar Jokenpo               ')
    print(Fore.YELLOW + '=' * 60)

    print(f'''Suas opções
    {Fore.GREEN}[0] {Fore.CYAN}Pedra
    {Fore.GREEN}[1] {Fore.CYAN}Papel
    {Fore.GREEN}[2] {Fore.CYAN}Tesoura
    {Fore.GREEN}[3] {Fore.CYAN}Lagarto
    {Fore.GREEN}[4] {Fore.CYAN}Spock
    ''')

def validate_input(player_input):
    if player_input not in [0, 1, 2, 3, 4]:
        print(Fore.RED + 'Jogada inválida! Por favor, escolha entre 0 e 4.')
        return False
    return True

def easy_mode():
    return random.randint(0,4)

def medium_mode():
    if len(player1_choices) >= 2:
        # The computer tries to predict the next move based on previous choices
        last_choice = player1_choices[-1]
        return (last_choice + 1) % 5  # Choose the next move that would beat the last one
    return random.randint(0, 4)

def hard_mode():
    if len(player1_choices) >= 3:
        # The computer tries to "learn" the player's pattern and exploits his weaknesses
        most_common_choice = Counter(player1_choices).most_common(1)[0][0]
        return (most_common_choice + 1) % 5
    return random.randint(0, 4)

def display_choice(player1, player2, is_computer=False):
    choices = ['Pedra', 'Papel', 'Tesoura', 'Lagarto', 'Spock']
    print(Fore.CYAN + f'Jogador 1 escolheu: {choices[player1]}')
    if is_computer:
        print(Fore.CYAN + f'Computador escolheu: {choices[player2]}')
    else:
        print(Fore.CYAN + f'Jogador 2 escolheu: {choices[player2]}')

def determine_winner(player1, player2):
    # Victory Table Rock(0), Paper(1), Scissors(2), Lizard(3), Spock(4)
    win_scenarios = {
        0: [2, 3],  # Rock beats Scissors and Lizard
        1: [0, 4],  # Paper beats Rock and Spock
        2: [1, 3],  # Scissors beat Paper and Lizard
        3: [1, 4],  # Lizard beats Paper and Spock
        4: [0, 2]   # Spock wins Rock and Scissors
    }

    if player1 == player2:
        print(Fore.CYAN + 'Empate')
        return 0
    elif player2 in win_scenarios[player1]:
        print(Fore.GREEN + 'Jogador 1 venceu')
        return 1
    else:
        print(Fore.GREEN + 'Jogador 2 venceu')
        return 2

def animation():
    print(Fore.YELLOW + 'JO')
    sleep(1)
    print(Fore.YELLOW + 'KEN')
    sleep(1)
    print(Fore.YELLOW + 'PO!')
    sleep(1)

def analyze_performance():
    total_games = len(player1_choices)
    if total_games == 0:
        return

    wins = player1_choices.count(1)
    losses = player1_choices.count(2)
    draws = total_games - wins - losses

    print(Fore.YELLOW + f'''\nAnálise de desempenho
        {Fore.CYAN} Vitórias: {wins / total_games * 100:.2f}%
        {Fore.CYAN} Derrotas: {losses / total_games * 100:.2f}%
        {Fore.CYAN} Empates: {draws / total_games * 100:.2f}%
        ''')

def play_game():
    score_player1 = 0
    score_player2 = 0

    while True:
        main_screen()

        while True:
            try:
                player1 = int(input(Fore.LIGHTRED_EX + 'Escolha uma opção primeiro jogador: '))
                if validate_input(player1):
                    break
            except ValueError:
                print(Fore.RED + 'Entrada inválida! Insira um número!')

        clear_screen()

        # Choose whether the player wants to play against a person or the computer
        mode = input(Fore.YELLOW + 'Você quer jogar contra o computador (c) ou contra pessoa (p)? ').lower()

        # Play against the computer and select the difficulty level
        if mode == 'c':
            difficulty = input(Fore.RESET + f'''Escolha o nível de dificuldade
                    {Fore.GREEN} [f] {Fore.CYAN}Fácil
                    {Fore.GREEN} [m] {Fore.CYAN}Médio
                    {Fore.GREEN} [d] {Fore.CYAN}Difícil
                    ''').lower()

            difficulty_modes = {'f': easy_mode, 'm': medium_mode, 'd': hard_mode}
            player2 = difficulty_modes.get(difficulty, easy_mode)()

            # Adds choices to history for performance analysis
            player1_choices.append(player1)
            computer_choices.append(player2)

        # Play against someone else
        elif mode == 'p':
            main_screen()
            while True:
                try:
                    player2 = int(input(Fore.LIGHTRED_EX + 'Escolha uma opção segundo jogador: '))
                    if validate_input(player2):
                        break
                except ValueError:
                    print(Fore.RED + 'Entrada inválida! Insira um número')

        else:
            print(Fore.RED + 'Opção inválida! Escolha "c" para computador ou "p" para pessoa')
            continue

        clear_screen()

        animation()

        display_choice(player1, player2, is_computer=(mode == 'c'))

        result = determine_winner(player1, player2)
        if result == 1:
            score_player1 += 1
        elif result == 2:
            score_player2 += 1

        print(Fore.YELLOW + f'\nPlacar: Jogador 1: {score_player1} | Jogador 2: {score_player2}')

        # Analyze performance only in computer mode
        if mode == 'c':
            analyze_performance()

        play_again = input(Fore.YELLOW + '\nQuer jogar novamente? (s/n): ').lower()
        if play_again != 's':
            print(Fore.LIGHTBLUE_EX + 'Até logo!')
            sleep(2)
            exit()
        clear_screen()


play_game()
