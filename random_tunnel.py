from IPython import embed
import asyncio
from cycle import color_cycle, do_cycle, parse_args, all_bulbs
import random
import colorsys

from pywizlight import wizlight, PilotBuilder, discovery

def random_cycle(bulbs):
    while True:
        yield [[int(255 * color) for color in colorsys.hsv_to_rgb(random.random(), 1, 1)] for _ in bulbs]
        
async def delay(t, f):
    if t > 0:
        await asyncio.sleep(t)
    await f
        
async def tunnel(bulbs, param_list, t, T):
    for i in range(len(bulbs)):
        task1 = asyncio.create_task(delay(-t, bulbs[i-1].turn_off()))
        task2 = asyncio.create_task(delay(t, bulbs[i].turn_on(PilotBuilder(rgb=param_list[i]))))
        await task1
        await task2
        await asyncio.sleep(T)
            
if __name__ == "__main__":
    args, bulbs = parse_args(default_t=0, default_T=3)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_cycle(args.time, args.offset, bulbs, random_cycle, tunnel))