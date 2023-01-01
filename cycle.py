import argparse
import asyncio

from pywizlight import wizlight, PilotBuilder, discovery

async def switch_color(bulb, rgb, T, hard=True):
    #print(hard)
    if hard:
        await bulb.turn_off()
    await bulb.turn_on(PilotBuilder(rgb=rgb))
    if T:
        await asyncio.sleep(T)
        
async def switch_brightness(bulb, brightness, T, hard=True):
    if hard:
        await bulb.turn_off()
    await bulb.turn_on(PilotBuilder(brightness=brightness))
    if T:
        await asyncio.sleep(T)
        
def basic_cycle(f):
    async def cycler(bulbs, param_list, t, T, **kwargs):
        for bulb, params in zip(bulbs, param_list):
            await f(bulb, params, T, **kwargs)
        await asyncio.sleep(t)
    return cycler
    
async def do_cycle(t, T, bulbs, cycle, f, **kwargs):
    for params_list in cycle(bulbs):
        await f(bulbs, params_list, t, T, **kwargs)
       
async def color_cycle(t, T, bulbs, cycle, **kwargs):
    await do_cycle(t, T, bulbs, cycle, basic_cycle(switch_color), **kwargs)
        
def all_bulbs(cycle):
    def new_cycle(bulbs):
        for rgb in cycle():
            yield [rgb]*len(bulbs)
    return new_cycle
        
def parse_args(default_t=1, default_T=0):
    parser = argparse.ArgumentParser()
    parser.add_argument("--time", "-t", type=float, default=default_t)
    parser.add_argument("--offset", "-T", type=float, default=default_T)
    parser.add_argument("--bulbs", "-b", nargs="+", default=["192.168.1.184"])
    parser.add_argument("--bulbs-file", "-B")
    args = parser.parse_args()
    if args.bulbs_file:
        with open(args.bulbs_file, "r") as bulbs_file:
            args.bulbs = list(l.strip() for l in bulbs_file)
    return args, [wizlight(bulb) for bulb in args.bulbs]