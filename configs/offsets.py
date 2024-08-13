class Pointer:
    local_player = 0x0017E0A8
    entity_list = 0x18AC04
    fov = 0x18A7CC
    player_count = 0x18AC0C
    view_matrix = 0x17DFD0


class Offsets:
    pos = 0x4
    fpos = 0x28
    team = 0x30C
    name = 0x205
    health = 0xEC
    armor = 0xF0
    knife_speed = 0x14C


class AmmoOffsets:
    assault_rifle = 0x140
    submachine_gun = 0x138
    sniper = 0x13C
    shotgun = 0x134
    pistol = 0x12C
    grenade = 0x144


class FastFireOffsets:
    assault_rifle = 0x164
    sniper = 0x160
    shotgun = 0x158

    auto_shoot = 0x204


class PositionOffsets:
    pos_x = 0x2C
    pos_y = 0x30
    pos_z = 0x28

    head_pos_x = 0x4
    head_pos_y = 0xC
    head_pos_z = 0x8

    camera_x = 0x34
    camera_y = 0x38
