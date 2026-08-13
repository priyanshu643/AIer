from stats.cpu import CPU
import requests
cpu = CPU()

url = "https://huggingface.co/api/models?search=gguf&sort=downloads&direction=-1"
response = requests.get(url)
models = response.json()
print(models)
