from IPython import embed
import argparse
import asyncio
import pywizlight
from tqdm import tqdm
import socket

from ipaddress import IPv4Network

from pywizlight import wizlight, PilotBuilder, discovery

async def get_bulbs(t, ip_range):
    #bulbs = []
    for ip in tqdm(ip_range):
        ip = str(ip)
        if not ip.endswith("255"):
            light = wizlight(ip)
            try:
                await asyncio.wait_for(light.updateState(), t)
                yield light
            except (
                pywizlight.exceptions.WizLightTimeOutError,
                asyncio.exceptions.TimeoutError,
                pywizlight.exceptions.WizLightConnectionError
            ):
                pass
    #return bulbs
    
async def discover(t, ip_range):
    async for bulb in get_bulbs(t, ip_range):
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
    ip = socket.gethostbyname(socket.gethostname())
    parser.add_argument(
        "--ip_range",
        "-i",
        type=IPv4Network,
        help="IP address range to try",
        default=IPv4Network(".".join(ip.split(".")[:-1]) + ".0/24")
    )
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(discover(args.time, args.ip_range))

if __name__ == "__main__":
    main()
    