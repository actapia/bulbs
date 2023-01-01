from IPython import embed
import asyncio
from cycle import color_cycle, parse_args, all_bulbs

def rgb_cycle():
    while True:
        for i in range(3):
            rgb = [0]*3
            rgb[i] = 255
            yield rgb
            
if __name__ == "__main__":
    args, bulbs = parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(color_cycle(args.time, args.offset, bulbs, all_bulbs(rgb_cycle)))