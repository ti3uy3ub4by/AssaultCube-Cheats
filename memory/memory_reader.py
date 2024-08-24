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
        if not isinstance(offsets, (list, tuple)):
            offsets = [offsets]  # Đảm bảo rằng offsets là một danh sách hoặc tuple
        try:
            addr = self.mem.read_int(base)
            for offset in offsets[:-1]:
                addr = self.mem.read_int(addr + offset)
            return addr + offsets[-1]
        except Exception as e:
            return None

    def write_value(self, base_address, offsets, value):
        addr = self.get_pointer_addr(self.module + base_address, offsets)
        if addr is not None:
            try:
                self.mem.write_int(addr, value)
            except Exception as e:
                print(f"Error writing value at address {addr}: {e}")

    def read_value(self, base_address, offsets):
        addr = self.get_pointer_addr(self.module + base_address, offsets)
        if addr is not None:
            try:
                return self.mem.read_int(addr)
            except Exception as e:
                print(f"Error reading value at address {addr}: {e}")
                return None
        return None

    def close(self):
        try:
            self.mem.close_process()
        except Exception as e:
            print(f"Failed to close process: {e}")
