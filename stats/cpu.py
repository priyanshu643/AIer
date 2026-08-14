import psutil
import cpuinfo


class CPU():
    def __init__(self):
        info = cpuinfo.get_cpu_info()
        self.cpu = info.get('brand_raw', info.get('arch', 'Unknown CPU'))
        self.core = psutil.cpu_count()
        self.p_core = psutil.cpu_count(logical=False)
        raw_feq = psutil.cpu_freq()
        self.max_ghz = round(raw_feq.max / 1000, 2) if raw_feq and raw_feq.max else 0
        self.min_ghz = round(raw_feq.min / 1000, 2) if raw_feq and raw_feq.min else 0
        self.disk = psutil.disk_usage('/')
        self.ram = psutil.virtual_memory()

# cpu = CPU()
# print(cpu.cpu)
# print(cpu.core)
# print(cpu.p_core)
# print(cpu.max_ghz)
# print(cpu.min_ghz)
# print(cpu.disk)
# print(cpu.ram)
