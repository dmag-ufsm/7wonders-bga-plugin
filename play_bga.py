from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import json

import scrapping_bga

player_action_folder = './io'
game_status_path = player_action_folder + '/game_status.json'

options = Options()
options.add_argument("--user-data-dir=cookies")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome('/home/bettker/Desktop/Testes/git/7wonders-bga-plugin/chromedriver', options=options)

browser.get('https://boardgamearena.com/')

num_players = int(input('Number of players: '))

while True:
    input('Entre em uma partida, escolha o tabuleiro, e pressione Enter para começar')

    progress = -1
    while progress < 92:
        # Espera comecar uma nova rodada
        while progress == int(browser.find_element_by_id('pr_gameprogression').text):
            sleep(1)
        progress = int(browser.find_element_by_id('pr_gameprogression').text)
        sleep(2)

        # Se ta acabando o turno, sleep adicional para esperar batalha
        if (26 <= progress <= 36) or (59 <= progress <= 69):
            sleep(5)

        scrapping_bga.create_game_status(browser.page_source, num_players, game_status_path)

        # Espera tempo suficiente do bot computar e escrever a jogada no arquivo
        sleep(3)

        # Descobre a carta a ser jogada...
        with open(player_action_folder + '/player_1.json') as move_json:
            move = json.load(move_json)
            action = move['command']['subcommand']
            card = move['command']['argument']

            print('[{0}%] {1} >> {2}'.format(progress, action, card))

    print('Fim de jogo.\n')
    scrapping_bga.reset_variables()

browser.quit()
