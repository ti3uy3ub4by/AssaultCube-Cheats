BASE_ADDRESS_HEALTH = 0x0017E0A8
BASE_ADDRESS_ARMOR = 0x0017E0A8

OFFSETS_HEALTH = [0xEC]
OFFSETS_ARMOR = [0xF0]

class Pointer:
    local_player = 0x0017E0A8
    entity_list = 0x18AC04
    fov = 0x18A7CC
    player_count = 0x18AC0C

"""class Offsets:
    pos_x = 0x2C
    pos_y = 0x30
    pos_z = 0x28

    head_pos_x = 0x4
    head_pos_y = 0xC
    head_pos_z = 0x8

    camera_x = 0x34
    camera_y = 0x38

    assault_rifle_ammo = 0x140
    submachine_gun_ammo = 0x138
    sniper_ammo = 0x13C
    shotgun_ammo = 0x134
    pistol_ammo = 0x12C
    grenade_ammo = 0x144

    fast_fire_assault_rifle = 0x164
    fast_fire_sniper = 0x160
    fast_fire_shotgun = 0x158

    auto_shoot = 0x204
"""
