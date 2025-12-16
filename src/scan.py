import asyncio
from bleak import BleakScanner

# SwitchBot Bot specific identifiers
SWITCHBOT_BOT_UUID = "0000fd3d-0000-1000-8000-00805f9b34fb"
SWITCHBOT_BOT_MANUFACTURER_ID = 0x0969  # SwitchBot manufacturer ID (2409)


def _extract_uuids(adv_data):
    """Extract UUIDs from advertisement data"""
    uuids = []
    try:
        if hasattr(adv_data, 'service_uuids'):
            uuids = list(adv_data.service_uuids)
    except:
        pass
    return uuids


def _is_switchbot(adv_data):
    """Check if device is a SwitchBot Bot using manufacturer ID"""
    try:
        # Check manufacturer data (manufacturer ID 0x0969 is unique to SwitchBot Bots)
        if hasattr(adv_data, 'manufacturer_data'):
            for mfg_id, mfg_data in adv_data.manufacturer_data.items():
                if mfg_id == SWITCHBOT_BOT_MANUFACTURER_ID:
                    return True
    except:
        pass
    return False


async def scan_switchbots(timeout=5.0):
    """
    Scan for SwitchBot devices specifically using the SwitchBot UUID.
    
    Args:
        timeout: Scan duration in seconds (default: 5)
    
    Returns:
        List of discovered SwitchBot devices
    """
    scanner = BleakScanner()
    devices = await scanner.discover(timeout=timeout, return_adv=True)
    
    switchbots = []
    for device, adv_data in devices.values():
        if adv_data and _is_switchbot(adv_data):
            uuids = _extract_uuids(adv_data) if adv_data else []
            switchbots.append({
                "mac": device.address,
                "name": device.name or "(SwitchBot)",
                "uuids": [str(u) for u in uuids]
            })
    
    return switchbots


if __name__ == "__main__":
    print("Scanning for SwitchBot devices...")
    switchbots = asyncio.run(scan_switchbots(timeout=5.0))
    
    if switchbots:
        print(f"\nFound {len(switchbots)} SwitchBot device(s):\n")
        for bot in switchbots:
            print(f"  MAC: {bot['mac']}")
            if bot['name']:
                print(f"  Name: {bot['name']}")
            print()
    else:
        print("\nNo SwitchBot devices found.")
