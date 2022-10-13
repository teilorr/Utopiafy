from discord.ext import commands
import re

class convertToSeconds(commands.Converter):
    async def convert(self, ctx, argument):
        time_regex = re.compile(r"(\d{1,5}(?:[.,]?\d{1,5})?)([smhd])")
        time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}

        matches = time_regex.findall(argument.lower())
        time = 0

        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument(' :x: │ {} é medida de tempo na casa da sua mãe! h/m/s/d são formatos válidos.'.format(k))
            except ValueError:
                raise commands.BadArgument(' :x: │ {} não é um número!'.format(v))
        return int(time)