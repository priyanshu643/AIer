from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlShutdown


class Nvidia():
    def __init__(self):
        try:
            nvmlInit()
            # Get the first GPU (Index 0)
            handle = nvmlDeviceGetHandleByIndex(0)
            # Get memory info
            info = nvmlDeviceGetMemoryInfo(handle)

            # Convert from bytes to Gigabytes
            self.total_vram_gb = info.total / (1024 ** 3)
            nvmlShutdown()
        except Exception as e:
            # Fails safely if no NVIDIA GPU is found or drivers are missing
            return None
nvidia = Nvidia()
print(nvidia.total_vram_gb)