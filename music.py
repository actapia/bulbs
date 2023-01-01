import sounddevice as sd
import numpy as np
from IPython import embed
import asyncio
from cycle import color_cycle, parse_args, all_bulbs, switch_brightness
import colorsys
from multiprocessing import Value, Array, Queue, Lock
duration = 1  # seconds
window = 25

avg = Array('d', [0.0 for _ in range(window)])
pos = Value('i', 0)
lock = Lock()



def callback(av, p, l, indata, outdata, frames, time, status):
    if status:
        print(status)
    avg[pos.value] = np.max(np.abs(indata))
    pos.value = (pos.value + 1)%len(avg)
    #print(avg)
    #outdata[:] = indata
            
async def read_sound(t, T, bulbs):
    window2 = 10
    min_arr = [1]*window2
    min_p = 0
    max_arr = [0]*window2
    with sd.Stream(callback=lambda *args: callback(avg, pos, lock, *args)):
        while True:
            sd.sleep(int(t*1000))
            ma = max(avg)
            # min_arr[min_p] = min(avg)
            # max_arr[min_p] = ma
            # print(min_arr, max_arr)
            # min_p = (min_p + 1)%len(min_arr)
            try:
                av = min(int(ma*255), 255)
            except ZeroDivisionError:
                av = 255
            print(av)
            for bulb in bulbs:
                if av < 10:
                    await bulb.turn_off()
                else:
                    await switch_brightness(bulb, av, 0, hard=False)
            
if __name__ == "__main__":
    args, bulbs = parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(read_sound(args.time, args.offset, bulbs))
    #loop.run_until_complete(color_cycle(args.time, args.offset, bulbs, all_bulbs(rgb_cycle)))