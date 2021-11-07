# Contributing
## Adding Commands:

1. Navigate to `cogs/src/commands` and copy `template.py` to a filename of your choosing in the same directory.
> Note that commands will only be loaded in this directory unless you explicitly state them in `main.py`. This is because `main.py` and `core.py` are dynamically loading/importing all python scripts in `cogs/src/commands` to be loaded cogs and modules. This also means that **you do not have to specify `client.load_extension` for your new script anywhere** as it is loaded automatically on script boot

> If your cog fails to load, a traceback should be printed, but bot execution will continue. We recommend setting the `DEBUG` flag in `cogs/src/common.py` while developing (see below)
2. `template.py` will already be pre-filled with required imports and aid comments. Example workflow will be as such:
> - `Line` [23](https://github.com/savioxavier/repo-finder-bot/blob/d55bfce44dd9061d104ceb9b2d7d6e237ab8fd58/cogs/src/commands/template.py#L23): `Change "template.py" to your script name to categorize accordingly in logs`
> ```py
> logger = logutil.initLogger("issues.py")
> ```
> - `Line` [33-34](https://github.com/savioxavier/repo-finder-bot/blob/d55bfce44dd9061d104ceb9b2d7d6e237ab8fd58/cogs/src/commands/template.py#L33-L34): `Change "command" in these lines to label your desired command name`
> ```py
> ...
>     @commands.command(name="issues")
>     async def issues_command(self, ctx, *, args: str = None):
>       ...
> ```
> - `Line` [5](https://github.com/savioxavier/repo-finder-bot/blob/d55bfce44dd9061d104ceb9b2d7d6e237ab8fd58/cogs/src/commands/template.py#L5-L15): `Import desired libraries. The root of the project is injected to sys.path[0] in "__init__.py" to allow importing parent utility modules`
> - `Line` [35](https://github.com/savioxavier/repo-finder-bot/blob/d55bfce44dd9061d104ceb9b2d7d6e237ab8fd58/cogs/src/commands/template.py#L35): `Code in desired command process`
> ```py
> ...
>   await ctx.send("Hello world!")
> ...
> ```

<hr />

### For developers:
- Debug mode can be enabled in `cogs/src/common.py` by changing `DEBUG=False` to `DEBUG=True`. Currently, this only enables debug logging to console
