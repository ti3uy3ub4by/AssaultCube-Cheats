from pymem import Pymem
from pymem.process import module_from_name


class PymemHandler:
    def __init__(self, process_name):
        try:
            self.mem = Pymem(process_name)
            self.module = module_from_name(self.mem.process_handle, process_name).lpBaseOfDll
        except Exception as e:
            print(f"Failed to access the process: {e}")
            exit(1)

    def get_pointer_addr(self, base, offsets):
        try:
            addr = self.mem.read_int(base)
            for offset in offsets:
                if offset != offsets[-1]:
                    addr = self.mem.read_int(addr + offset)
            addr = addr + offsets[-1]
            return addr
        except Exception as e:
            print(f"Error reading memory: {e}")
            return None

    def write_value(self, base_address, offsets, value):
        addr = self.get_pointer_addr(self.module + base_address, offsets)
        if addr is not None:
            self.mem.write_int(addr, value)

    def close(self):
        try:
            self.mem.close_process()
        except:
            pass
