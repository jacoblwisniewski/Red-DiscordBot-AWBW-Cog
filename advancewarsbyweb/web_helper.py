import json
import re
import requests

AWBW_URL = "https://awbw.amarriner.com/"

def get_game_session_url(game_id: str):
    return AWBW_URL + "game.php?games_id=" + game_id

def getHTMLDocument(url: str):
    # request for HTML document of given url 
    response = requests.get(url) 
      
    # response will be provided in JSON format 
    return response.text 

def get_game_html(game_id: str):
    return getHTMLDocument(get_game_session_url(game_id))

def get_current_turn_player_id(game_html: str) -> str:
    return re.findall(r'let\s+currentTurn\s*=\s*(\d+);', game_html)[0]

def get_player_info(game_html: str):
    return json.loads(re.findall(r'let\s+playersInfo\s*=\s*({.*?});', game_html)[0])

def get_username_from_player_id(player_id: str, player_info_json: str) -> str:
    return player_info_json[player_id]["users_username"]

def is_game_ended(game_html: str):
    # If endData is null that means the game has not ended yet.
    match = re.search(r'const\s+endData\s*=\s*(null);', game_html)
    if match:
        return False
    return True

def is_valid_game(game_html: str, game_id: str):
    # If gameId is set then the provided ID was valid.
    match = re.search(r'const\s+gameId\s*=\s*(\d+);', game_html)
    if match:
        # As an extra sanitization check. Make sure the provided input matches the game id.
        return str(match.group(1)) == game_id
    return False   

def main():
    game_session_html = get_game_html("1164260")
    print(is_valid_game(game_session_html, "1164260"))
    print(is_game_ended(game_session_html))
    #print(game_session_html)
    #game_session_html = get_game_html("1160554")
    current_turn_player_id = get_current_turn_player_id(game_session_html)
    player_info_json = get_player_info(game_session_html)
    print(player_info_json)
    print(get_username_from_player_id(current_turn_player_id, player_info_json))
    
if __name__ == '__main__':
    main()