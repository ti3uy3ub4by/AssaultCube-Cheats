import pyMeow as pm
from configs.offsets import Pointer, AmmoOffsets

try:
    proc = pm.open_process("ac_client.exe")
    base = pm.get_module(proc, "ac_client.exe")["base"]
except Exception as e:
    print(f"Failed to open process or get base module: {e}")

# Check proc và base
if not proc or not base:
    print("Process or base module is invalid. Exiting...")
    exit(1)


def set_ammo():
    try:
        local_player = pm.r_int(proc, base + Pointer.local_player)
        ammo_offsets = [
            AmmoOffsets.assault_rifle, AmmoOffsets.submachine_gun,
            AmmoOffsets.sniper, AmmoOffsets.shotgun,
            AmmoOffsets.pistol, AmmoOffsets.grenade
        ]
        for offset in ammo_offsets:
            pm.w_int(proc, local_player + offset, 99)
    except Exception as e:
        print(f"Error setting ammo: {e}")

if __name__ == "__main__":
    set_ammo()

