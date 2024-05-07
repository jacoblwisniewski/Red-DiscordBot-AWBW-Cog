from redbot.core import commands

from advancewarsbyweb.web_helper import get_current_turn_player_id, get_game_html, get_player_info, get_username_from_player_id, is_game_ended, is_valid_game

class AdvanceWarsByWeb(commands.Cog):
    """Interact with Advance Wars By Web"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def awbw(self, ctx: commands.Context) -> None:
        """Base command for Advance Wars By Web commands."""
        pass
    
    @awbw.command(name="currentturn", usage="<game_id>")
    async def current_turn_username(self, ctx: commands.Context, game_id: str):
        """Get the AWBW username whose turn it currently is for an active game."

        Example:
        - `[p]awbw currentturn 123456789`

        **Arguments**

        - `<game_id>` The game id of an active AWBW game. For https://awbw.amarriner.com/game.php?games_id=123456789 this would be 123456789.
        """
        
        game_html = get_game_html(game_id)
        
        if not is_valid_game(game_html, game_id):
            await ctx.send(f"{game_id} is an invalid game ID.")
            return
        
        if is_game_ended(game_html):
            await ctx.send(f"Game {game_id} has already ended.")
            return
        
        current_turn_awbw_username = self.get_current_turn_awbw_username(game_html)
        # Your code will go here
        await ctx.send(f"{current_turn_awbw_username} it is your turn for AWBW game {game_id}.")
        #await ctx.send("Not Implemented Yet!!!")

    @awbw.command(name="turntracker", usage="<game_id> <awbw_to_discord_username_mappings>")
    async def turn_tracker(self, ctx: commands.Context):
        """Initialize Discord turn tracker notifications for an active AWBW game."

        Example:
        - `[p]awbw turntracker 123456789 [{"awbw_username": "bob12", "discord_username": "bob28"}, {"awbw_username": "fred12", "discord_username": "fred28"}]`

        **Arguments**

        - `<game_id>` The game id of the game to track. For https://awbw.amarriner.com/game.php?games_id=123456789 this would be 123456789.
        - `<awbw_to_discord_username_mappings>` A mapping of AWBW player usernames to their discord usernames.
        """
        # Your code will go here
        await ctx.send("Not Implemented Yet!!!")

    def get_current_turn_awbw_username(self, game_html: str):
        current_turn_player_id = get_current_turn_player_id(game_html)
        player_info_json = get_player_info(game_html)
        return get_username_from_player_id(current_turn_player_id, player_info_json)