import psutil
import cpuinfo
class CPU():
    def __init__(self):
        self.cpu = cpuinfo.get_cpu_info()
        self.core = psutil.cpu_count()
        self.p_core = psutil.cpu_count(logical=False)
        raw_feq = psutil.cpu_freq()
        self.max_ghz = round(raw_feq.max / 1000, 2)
        self.min_ghz = round(raw_feq.min / 1000, 2)
        self.disk = psutil.disk_usage('/')
        self.ram = psutil.virtual_memory()

cpu = CPU()
print(cpu.cpu['brand_raw'])
print(cpu.core)
print(cpu.p_core)
print(cpu.max_ghz)
print(cpu.min_ghz)
print(cpu.disk)
print(cpu.ram)
