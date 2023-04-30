from IPython import embed
import argparse
import asyncio
import pywizlight
from tqdm import tqdm
import socket

from ipaddress import IPv4Network

from pywizlight import wizlight, PilotBuilder, discovery

async def is_bulb(ip, t):
    light = wizlight(ip)
    try:
        await asyncio.wait_for(light.updateState(), t)
        return True
    except (
            pywizlight.exceptions.WizLightTimeOutError,
            asyncio.exceptions.TimeoutError,
            pywizlight.exceptions.WizLightConnectionError
    ):
         #print("{} is not a light".format(ip))
         return False

async def get_bulbs(t, ip_ranges):
    #bulbs = []
    ips = [
        s for s in (str(ip) for ip_range in ip_ranges for ip in ip_range)
        if not s.endswith("255")
    ]
    futures = [is_bulb(s, t) for s in ips]
    for ip, res in zip(ips, await asyncio.gather(*futures, return_exceptions=True)):
        if res:
            yield wizlight(ip)
    
async def discover(t, ip_ranges):
    async for bulb in get_bulbs(t, ip_ranges):
        print(bulb.ip)

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--time",
        "-t",
        type=float,
        default=1,
        help="time to wait for responses in seconds"
    )
    #ip = socket.gethostbyname(socket.gethostname())
    parser.add_argument(
        "--ip_ranges",
        "-i",
        type=IPv4Network,
        nargs="+",
        help="IP address ranges to try",
        default=[
            IPv4Network(".".join(ip.split(".")[:-1]) + ".0/24")
            for ip in socket.gethostbyname_ex(socket.gethostname())[-1]
        ]
    )
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(discover(args.time, args.ip_ranges))

if __name__ == "__main__":
    main()
    