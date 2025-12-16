import asyncio
import sys
from bleak import BleakClient

# MAC address passed as command-line argument
if len(sys.argv) < 2:
    raise ValueError("BOT_MAC required as argument: python press.py <MAC_ADDRESS>")

BOT_MAC = sys.argv[1]
CHARACTERISTIC_UUID = "cba20002-224d-11e6-9fb8-0002a5d5c51b"

async def main():
    print("Connecting to SwitchBot...")
    async with BleakClient(BOT_MAC) as client:
        print(f"Connected: {client.is_connected}")
        print("Pressing the button...")
        await client.write_gatt_char(CHARACTERISTIC_UUID, bytes([0x57, 0x01, 0x00]))
        print("Done")

if __name__ == "__main__":
    asyncio.run(main())
