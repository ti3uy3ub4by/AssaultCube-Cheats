import sys
import pyMeow as pm

# Debug print
print("Script started")

# Initialize process and base
try:
    proc = pm.open_process("ac_client.exe")
    base = pm.get_module(proc, "ac_client.exe")["base"]
    print("Process and base initialized")
except Exception as e:
    print(f"Error initializing process and base: {e}")
    sys.exit(e)

# Define pointers and offsets
class Pointer:
    local_player = 0x0017E0A8

class Offsets:
    assault_rifle_ammo = 0x140
    submachine_gun_ammo = 0x138
    sniper_ammo = 0x13C
    shotgun_ammo = 0x134
    pistol_ammo = 0x12C
    grenade_ammo = 0x144

# Define cheat functions
def set_infinite_ammo():
    try:
        local_player = pm.r_int(proc, base + Pointer.local_player)
        ammo_offsets = [
            Offsets.assault_rifle_ammo, Offsets.submachine_gun_ammo,
            Offsets.sniper_ammo, Offsets.shotgun_ammo,
            Offsets.pistol_ammo, Offsets.grenade_ammo
        ]
        for offset in ammo_offsets:
            pm.w_int(proc, local_player + offset, 99)
    except Exception as e:
        print(f"Error setting ammo: {e}")

# Usage example (if you want to execute set_infinite_ammo directly)
if __name__ == "__main__":
    set_infinite_ammo()