import json
import re
import sys
import requests
from bs4 import BeautifulSoup

AWBW_URL = "https://awbw.amarriner.com/"

def get_game_session_url(game_id: str):
    return AWBW_URL + "game.php?games_id=" + game_id

def getHTMLDocument(url: str):
    # request for HTML document of given url 
    response = requests.get(url) 
      
    # response will be provided in JSON format 
    return response.text 

def get_game_session(game_id: str):
    return getHTMLDocument(get_game_session_url(game_id))

def get_current_turn_player_id(game_session_html: str) -> str:
    return re.findall(r'let\s+currentTurn\s*=\s*(\d+);', game_session_html)[0]

def get_player_info(game_session_html: str):
    return json.loads(re.findall(r'let\s+playersInfo\s*=\s*({.*?});', game_session_html)[0])

def get_username_from_player_id(player_id: str, player_info_json: str) -> str:
    return player_info_json[player_id]["users_username"]

def main():
    game_session_html = get_game_session("1160554")
    current_turn_player_id = get_current_turn_player_id(game_session_html)
    player_info_json = get_player_info(game_session_html)
    print(player_info_json)
    print(get_username_from_player_id(current_turn_player_id, player_info_json))
    
if __name__ == '__main__':
    main()