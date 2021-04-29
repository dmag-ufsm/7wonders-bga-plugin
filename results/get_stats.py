# get_stats.py
# Obtem as estatisticas de todas partidas presentes em um arquivo de resultados

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import sys

if len(sys.argv) != 2:
    print('$ ' + sys.argv[0] + ' <filename>')
    exit()

username = 'Mineradores'
    
filename = sys.argv[1]
f = open(filename, 'r')
lines = f.readlines()

matches = []
for line in lines[1:]:
    if line[0] != '\n':
        matches.append(line.split(',')[0])

# Browser...
options = Options()
options.add_argument("--user-data-dir=cookies")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome('/home/bettker/Documents/DMAG/7wonders-bga-plugin/chromedriver', options=options)

browser.get('https://boardgamearena.com/account')
if 'account' in browser.current_url:
    input('Log in...')

player_stats = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
for i, match in enumerate(matches):
    browser.get('https://boardgamearena.com/table?table=' + match)
    print('[{0}/{1}] {2}... '.format(i+1, len(matches), match), end='')
    
    sleep(2)
    
    # Pega tabela de estatisticas
    stats_table = browser.find_element_by_id('player_stats_table')
    stats_text = stats_table.text.split('\n')

    # Obtem a posicao do jogador na partida
    score_entries = browser.find_element_by_class_name('game_result').find_elements_by_class_name('score-entry')
    for i, elem in enumerate(score_entries):
    	if username in elem.text:
    	    player_id = i
    
    # Remove linhas irrelevantes
    stats_text.remove(stats_text[26]) # All stats
    stats_text.remove(stats_text[17]) # Wonder side A
    stats_text.remove(stats_text[2]) # Thinking time
    stats_text.remove(stats_text[0]) # Player names
    
    # Soma stats da partida no vetor
    player_stats[0].append(int(stats_text[0].split('(')[player_id + 1].split(')')[0]))
    for i in range(1, len(stats_text)):
        stats_splited = stats_text[i].split(' ')
        player_stats[i].append(int(stats_splited[-3:][player_id]))
        
    print('OK')

# Calcula media dos valores
player_stats_avg = []
for ps in player_stats:
    player_stats_avg.append(sum(ps)/len(ps))

# Imprime
#print(player_stats)
#print(player_stats_avg)
print()

labels = ['Game result', 'VP from Military Conflicts (Victory)', 'VP from Military Conflicts (Defeat)', 'VP from Treasury Contents', 'VP from Wonder', 'VP from Civilian Structures', 'VP from Scientific Structures', 'VP from Commercial Structures', 'VP from Guilds', 'Constructed stages of the Wonder', 'Cards discarded', 'Chained constructions', 'Coins spent on commerce', 'Coins gained through commerce', 'Shields', 'Wonder ID', 'Civilian Structures', 'Scientific Structures', 'Guilds', 'Military Structures', 'Commercial Structures', 'Raw Materials', 'Manufactured Goods']

for i in range(len(labels)):
    print(labels[i] + ': ' + str(player_stats_avg[i]))
print('Total matches: ' + str(len(player_stats[0])) )

browser.quit()

