from selenium import webdriver
from time import sleep
import json

import scrapping_bga

game_status_path = '../io/game_status.json'
player_action_folder = '../io/'

browser = webdriver.Chrome(executable_path='./chromedriver.exe')

browser.get('https://boardgamearena.com/')

num_players = int(input('Number of players: '))

progress = -1

try:
    while True:
        input('Entre em uma partida e pressione Enter')

        while progress < 100:
            # Espera comecar uma nova rodada
            while progress == int(browser.find_element_by_id('pr_gameprogression').text):
                sleep(1)
            progress = int(browser.find_element_by_id('pr_gameprogression').text)
            
            sleep(2)
            scrapping_bga.create_game_status(browser.page_source, num_players, game_status_path)

            # Espera tempo suficiente do bot computar e escrever a jogada no arquivo
            sleep(3)

            # Descobre a carta a ser jogada...
            with open(player_action_folder + '/player_1.json') as move_json:
                move = json.load(move_json)
                action = move['command']['subcommand']
                card = move['command']['argument']

                print('[{0}%] {1} >> {2}'.format(progress, action, card))

except Exception as e:
    print('Erro: ' + str(e))

finally:
    browser.quit()
