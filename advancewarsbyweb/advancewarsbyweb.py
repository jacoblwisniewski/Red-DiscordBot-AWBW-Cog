from redbot.core import commands

class AdvanceWarsByWeb(commands.Cog):
    """Interact with Advance Wars By Web"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")