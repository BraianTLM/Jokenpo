import os
import random
from colorama import Fore, init
from time import sleep
from collections import Counter

init(autoreset=True)

# Histórico das escolhas do jogador para análise de desmpenho
player1_choices = []
computer_choices = []

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def tela_principal():
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

def validar_entrada(player_input):
    if player_input not in [0, 1, 2, 3, 4]:
        print(Fore.RED + 'Jogada inválida! Por favor, escolha entre 0 e 4.')
        return False
    return True

def modo_facil():
    return random.randint(0,4)

def modo_medio():
    if len(player1_choices) >= 2:
        # O computador tenta prever a próxima jogada com base nas escolhas anteriores
        last_choice = player1_choices[-1]
        return (last_choice + 1) % 5  # Escolhe a próxima jogada que venceria a ultima
    return random.randint(0, 4)

def modo_dificil():
    if len(player1_choices) >= 3:
        # O computador tenta "aprender" o padrão do jogador e explora suas fraquezas
        most_common_choice = Counter(player1_choices).most_common(1)[0][0]
        return (most_common_choice + 1) % 5
    return random.randint(0, 4)

def exibir_escolhas(player1, player2, is_computer=False):
    choices = ['Pedra', 'Papel', 'Tesoura', 'Lagarto', 'Spock']
    print(Fore.CYAN + f'Jogador 1 escolheu: {choices[player1]}')
    if is_computer:
        print(Fore.CYAN + f'Computador escolheu: {choices[player2]}')
    else:
        print(Fore.CYAN + f'Jogador 2 escolheu: {choices[player2]}')

def determinar_vencedor(player1, player2):
    # Tabela de vitória Pedra(0), Papel(1), Tesoura(2), Lagarto(3), Spock(4)
    win_scenarios = {
        0: [2, 3],  # Pedra vence Tesoura e Lagarto
        1: [0, 4],  # Papel vence Pedra e Spock
        2: [1, 3],  # Tesoura vence Papel e Lagarto
        3: [1, 4],  # Lagarto vence Papel e Spock
        4: [0, 2]   # Spock vence Pedra e Tesoura
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

def animacao():
    print(Fore.YELLOW + 'JO')
    sleep(1)
    print(Fore.YELLOW + 'KEN')
    sleep(1)
    print(Fore.YELLOW + 'PO!')
    sleep(1)

def analisar_performance():
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

def jogar_jogo():
    score_player1 = 0
    score_player2 = 0

    while True:
        tela_principal()

        while True:
            try:
                player1 = int(input(Fore.LIGHTRED_EX + 'Escolha uma opção primeiro jogador: '))
                if validar_entrada(player1):
                    break
            except ValueError:
                print(Fore.RED + 'Entrada inválida! Insira um número!')

        limpar_tela()

        # Escolher se o jogador quer jogar contra pessoa ou o computador
        mode = input(Fore.YELLOW + 'Você quer jogar contra o computador (c) ou contra pessoa (p)? ').lower()

        # Jogar contra o computador e selecionar o nível de dificuldade
        if mode == 'c':
            difficulty = input(Fore.RESET + f'''Escolha o nível de dificuldade
                    {Fore.GREEN} [f] {Fore.CYAN}Fácil
                    {Fore.GREEN} [m] {Fore.CYAN}Médio
                    {Fore.GREEN} [d] {Fore.CYAN}Difícil
                    ''').lower()

            difficulty_modes = {'f': modo_facil, 'm': modo_medio, 'd': modo_dificil}
            player2 = difficulty_modes.get(difficulty, modo_facil)()

            # Adiciona as escolhas ao histórico para análise de desempenho
            player1_choices.append(player1)
            computer_choices.append(player2)

        # Jogar contra outra pessoa
        elif mode == 'p':
            tela_principal()
            while True:
                try:
                    player2 = int(input(Fore.LIGHTRED_EX + 'Escolha uma opção segundo jogador: '))
                    if validar_entrada(player2):
                        break
                except ValueError:
                    print(Fore.RED + 'Entrada inválida! Insira um número')

        else:
            print(Fore.RED + 'Opção inválida! Escolha "c" para computador ou "p" para pessoa')
            continue

        limpar_tela()

        animacao()

        exibir_escolhas(player1, player2, is_computer=(mode == 'c'))

        result = determinar_vencedor(player1, player2)
        if result == 1:
            score_player1 += 1
        elif result == 2:
            score_player2 += 1

        print(Fore.YELLOW + f'\nPlacar: Jogador 1: {score_player1} | Jogador 2: {score_player2}')

        # Analisar desempenho apenas no modo contra o computador
        if mode == 'c':
            analisar_performance()

        play_again = input(Fore.YELLOW + '\nQuer jogar novamente? (s/n): ').lower()
        if play_again != 's':
            print(Fore.LIGHTBLUE_EX + 'Até logo!')
            sleep(2)
            exit()
        limpar_tela()

jogar_jogo()
