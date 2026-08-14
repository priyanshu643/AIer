# stats/gpu.py
import subprocess

class GPU():
    def __init__(self):
        self.gpu_name = 'NVIDIA'
        # subprocess.getoutput captures the actual text output
        try:
            raw_vram = subprocess.getoutput('nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits')
            # Convert the string (e.g., '8192') into an integer for math later
            self.vram = int(raw_vram.strip())
        except:
            self.vram = 0
gpu = GPU()
print(gpu.vram)