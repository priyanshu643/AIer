# stats/gpu.py
import subprocess


class GPU():
    def __init__(self):
        self.gpu_name = 'Unknown GPU'
        self.vram = 0
        try:
            raw_output = subprocess.getoutput('nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits')
            lines = [line.strip() for line in raw_output.splitlines() if line.strip()]
            if lines and not lines[0].startswith("nvidia-smi:"):
                parts = lines[0].split(',')
                if len(parts) >= 2:
                    self.gpu_name = parts[0].strip()
                    self.vram = int(parts[1].strip())
                elif len(parts) == 1:
                    self.vram = int(parts[0].strip())
                    self.gpu_name = 'NVIDIA GPU'
        except Exception:
            self.gpu_name = 'N/A'
            self.vram = 0


if __name__ == "__main__":
    gpu = GPU()
    print(f"GPU: {gpu.gpu_name}, VRAM: {gpu.vram} MB")