import psutil

class CPU():
    def __init__(self):
        self.core = psutil.cpu_count()
        self.p_core = psutil.cpu_count(logical=False)
        self.feq_cpu = psutil.cpu_freq()
        self.disk = psutil.disk_usage('/')
        self.ram = psutil.virtual_memory()

# cpu = CPU()
# print(cpu.core)
# print(cpu.p_core)
# print(cpu.feq_cpu)
# print(cpu.disk)
# print(cpu.ram)