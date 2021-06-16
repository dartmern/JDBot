from discord.ext import commands, menus
import discord, os, itertools, re, functools, typing, random, collections, io
import utils
from discord.ext.commands.cooldowns import BucketType

testers_list =  [524916724223705108,168422909482762240,742214686144987150,813445268624244778,700210850513944576,717822288375971900,218481166142013450,703674286711373914, 732278462571610173, 459185417678487552, 766343727743631361, 540142383270985738]

class Test(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def ticket_make(self,ctx):
    await ctx.send("WIP, will make ticket soon..")

  @commands.command(brief="this command will error by sending no content")
  async def te(self, ctx):
    await ctx.send("this command will likely error...")
    await ctx.send("")

  async def cog_check(self, ctx):
    return ctx.author.id in testers_list

  async def cog_command_error(self, ctx, error):
    if ctx.command and not ctx.command.has_error_handler():
      await ctx.send(error)
      
    #I need to fix all cog_command_error
  
  @commands.command(brief="a command to email you(work in progress)",help="This command will email your email, it will automatically delete in guilds, but not in DMs(as it's not necessary")
  async def email(self, ctx, *args):
    print(args)
    await ctx.send("WIP")

  @commands.cooldown(1,40,BucketType.user)
  @commands.command(brief="a command that can scan urls(work in progress), and files",help="please don't upload anything secret or send any secret url thank you :D")
  async def scan(self, ctx, *, args = None):
    await ctx.send("WIP")
    import vt
    vt_client = vt.Client(os.environ["virustotal_key"])
    used = None
    if args:
      used = True
      urls=re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",args)
      for u in urls:
        response = await vt_client.scan_url_async(u, wait_for_completion = True)
        print(response)

    if len(ctx.message.attachments) > 0:
      await ctx.send("If this takes a while, it probably means it was never on Virustotal before")
      used = True
    for f in ctx.message.attachments:
      analysis = await vt_client.scan_file_async(await f.read(),wait_for_completion=True)
      print(analysis)
      object_info = await vt_client.get_object_async("/analyses/{}", analysis.id)
    
    if used:
      await ctx.send(content="Scan completed")
    await vt_client.close_async()
    
  @commands.command(brief="work in progress")
  async def invert(self,ctx):
    y = 0

    if len(ctx.message.attachments) > 0:
      for x in ctx.message.attachments:
        try:
          discord.utils._get_mime_type_for_image(await x.read())
          passes = True
        except commands.errors.CommandInvokeError:
          passes = False
        if passes is True:
          y += 1
          invert_time=functools.partial(utils.invert_func,await x.read())
          file = await self.bot.loop.run_in_executor(None, invert_time)
          await ctx.send(file=file)
        if passes is False:
          pass

    if len(ctx.message.attachments) == 0 or y == 0:
      url = ctx.author.avatar_url_as(format="png")
      invert_time=functools.partial(utils.invert_func,await url.read() )

      file = await self.bot.loop.run_in_executor(None, invert_time)
      await ctx.send(file=file)

  @invert.error
  async def invert_error(self,ctx,error):
    await ctx.send(error)

  @commands.command(brief="make a unique prefix for this guild(other prefixes still work)")
  async def setprefix(self, ctx, *, arg=None):
    await ctx.send("WIP")

def setup(client):
  client.add_cog(Test(client))