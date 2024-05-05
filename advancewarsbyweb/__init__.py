from .advancewarsbyweb import AdvanceWarsByWeb

async def setup(bot):
    await bot.add_cog(AdvanceWarsByWeb(bot))