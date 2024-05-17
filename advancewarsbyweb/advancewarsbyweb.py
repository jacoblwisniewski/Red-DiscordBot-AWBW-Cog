from typing import Dict, Union
from redbot.core import commands
import discord

from advancewarsbyweb.web_helper import (
    get_current_turn_player_id,
    get_game_html,
    get_player_info,
    get_username_from_player_id,
    get_usernames_from_game,
    is_game_ended,
    is_valid_game,
)


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
        await ctx.send(
            f"{current_turn_awbw_username} it is your turn for AWBW game {game_id}."
        )

    @awbw.command(
        name="turntracker", usage="<game_id> <awbw_to_discord_username_mappings>"
    )
    async def turn_tracker(
        self,
        ctx: commands.Context,
        game_id: str,
        awbw_to_discord_username_mappings: str,
    ):
        """Initialize Discord turn tracker notifications for an active AWBW game."

        Example:
        - `[p]awbw turntracker 123456789 awbw_username3:discord_username9,awbw_username76:discord_username934,awbw_username2343:discord_username5799`

        **Arguments**

        - `<game_id>` The game id of the game to track. For https://awbw.amarriner.com/game.php?games_id=123456789 this would be 123456789.
        - `<awbw_to_discord_username_mappings>` A mapping of AWBW player usernames to their discord usernames.
        A comma separated list in format of awbw_username:discord_username pairs.
        """
        game_html = get_game_html(game_id)

        if not is_valid_game(game_html, game_id):
            await ctx.send(f"{game_id} is an invalid game ID.")
            return

        if is_game_ended(game_html):
            await ctx.send(f"Game {game_id} has already ended.")
            return

        try:
            awbw_to_discord_username_dict = (
                self.parse_awbw_to_discord_username_mappings(
                    game_html, awbw_to_discord_username_mappings
                )
            )
        except ValueError as e:
            await ctx.send(
                f"Invalid awbw to discord username mapping provided. Error: {e}"
            )
            return

        current_turn_awbw_username = self.get_current_turn_awbw_username(game_html)
        current_turn_discord_username = awbw_to_discord_username_dict[
            current_turn_awbw_username
        ]

        discord_member_current_turn = discord.utils.get(
            ctx.guild.members, name=current_turn_discord_username
        )

        if discord_member_current_turn is None:
            await ctx.send(
                f"Could not find a discord server member with the username: {current_turn_discord_username}"
            )
        else:
            await ctx.send(
                f"{discord_member_current_turn.mention} it is your turn for AWBW game {game_id}."
            )

    def get_current_turn_awbw_username(self, game_html: str):
        current_turn_player_id = get_current_turn_player_id(game_html)
        player_info_json = get_player_info(game_html)
        return get_username_from_player_id(current_turn_player_id, player_info_json)

    def parse_awbw_to_discord_username_mappings(
        self, game_html: str, awbw_to_discord_username_mappings: str
    ) -> Dict:
        # Check if input is empty
        if not awbw_to_discord_username_mappings:
            raise ValueError("Mapping is empty.")

        # Strip whitespace and split by commas
        mappings_list = awbw_to_discord_username_mappings.strip().split(",")

        awbw_to_discord_username_dict = {}

        # Iterate over each pair in the mappings list and add to dictionary
        for mapping in mappings_list:
            # Check if the mapping has the correct format
            if ":" not in mapping:
                raise ValueError(
                    f"Invalid mapping format: {mapping}. Expected format: 'awbw_username:discord_username'."
                )

            # Split the mapping into awbw_username and discord_username
            awbw_username, discord_username = mapping.split(":")

            # Check if both awbw_username and discord_username are provided
            if not awbw_username:
                raise ValueError(f"Invalid mapping: {mapping}. Missing awbw username.")

            if not discord_username:
                raise ValueError(
                    f"Invalid mapping: {mapping}. Missing discord username."
                )

            awbw_to_discord_username_dict[awbw_username] = discord_username

        # Check if provided awbw usernames exist in the game
        result = self.do_all_parsed_awbw_usernames_exist(
            game_html, awbw_to_discord_username_dict
        )
        awbw_usernames_list = get_usernames_from_game(game_html)

        if isinstance(result, str):
            raise ValueError(
                f"Invalid mapping: {mapping}. {result} is not a valid awbw username in provided game. List of all valid awbw usernames: {awbw_usernames_list}"
            )

        return awbw_to_discord_username_dict

    def do_all_parsed_awbw_usernames_exist(
        self, game_html: str, awbw_to_discord_username_dict: Dict
    ) -> Union[str, bool]:
        awbw_usernames_list = get_usernames_from_game(game_html)

        # Iterate over the awbw to discord username dictionary
        for awbw_username in awbw_to_discord_username_dict.keys():
            # Validate that each awbw username exists in the parsed list provided as input
            if awbw_username not in awbw_usernames_list:
                # Return the username that does not exist.
                return awbw_username
        # If all usernames exist then return True
        return True
