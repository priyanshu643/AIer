import os
import sys
from pathlib import Path

# Add project root and script dir to sys.path so it works when run from any directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(1, str(SCRIPT_DIR))

import requests
import re
from stats.cpu import CPU
from stats.gpu import GPU
try:
    from script.AI import AIerEngine
except ImportError:
    from AI import AIerEngine


def calculate_vram_needs(model_id):
    """Programmatic math to find required VRAM based on parameter count."""
    match = re.search(r'(\d+(?:\.\d+)?)B', model_id, re.IGNORECASE)
    if match:
        params_billion = float(match.group(1))
        # 0.6 GB per billion params (for Q4) + 1.5GB overhead
        return round((params_billion * 0.6) + 1.5, 2)
    return None


def fetch_and_filter_models(user_vram_gb):
    """Fetches real Hugging Face data and filters it down to what actually fits."""
    print("[SYSTEM] Fetching trending GGUF models from Hugging Face...")

    # Notice we removed the arbitrary limit. We are pulling the main trending feed.
    url = "https://huggingface.co/api/models?search=gguf&sort=downloads&direction=-1"
    response = requests.get(url)

    if response.status_code != 200:
        print("[ERROR] Could not connect to Hugging Face.")
        return []

    all_models = response.json()
    viable_models = []

    for model in all_models:
        model_id = model.get('id')
        req_vram = calculate_vram_needs(model_id)

        # We only keep the model if it safely fits in the user's VRAM
        if req_vram and req_vram <= user_vram_gb:
            viable_models.append(f"{model_id} (Needs ~{req_vram} GB VRAM)")

        # We cap the list at the top 10 compatible models so we don't blow up
        # the local LLM's context window during the final generation phase.
        if len(viable_models) >= 10:
            break

    return viable_models


def main():
    print("=== AIer: Local Hardware Scanner & Recommender ===\n")

    # 1. Scan Hardware
    print("[SYSTEM] Scanning hardware...")
    cpu = CPU()
    gpu = GPU()

    user_vram_gb = gpu.vram / 1024
    user_ram_gb = cpu.ram.total / (1024 ** 3)

    print(f"-> CPU: {cpu.cpu} | RAM: {round(user_ram_gb, 1)} GB")
    print(f"-> GPU: {gpu.gpu_name} | VRAM: {round(user_vram_gb, 1)} GB\n")

    # 2. Get Compatible Models from Hugging Face
    compatible_models = fetch_and_filter_models(user_vram_gb)

    if not compatible_models:
        print("[SYSTEM] Your system does not have enough VRAM to run trending local models.")
        return

    # 3. Format the data for the Local LLM
    models_text = "\n".join(compatible_models)

    prompt = f"""You are AIer, a local AI hardware expert. 
    USER SYSTEM: {gpu.gpu_name} GPU with {round(user_vram_gb, 1)} GB VRAM.
    MODELS THAT TECHNICALLY FIT:
    {models_text}

    TASK: 
    Do NOT just recommend the largest model. You must account for the Context Window (KV Cache) which stores the user's prompts and generated tokens. 
    1. Pick the best model that leaves enough VRAM breathing room for a large prompt context.
    2. Explain WHY you picked it over the larger models.
    3. Warn the user about what will happen if they max out their VRAM.

    Format your answer cleanly with Markdown headers and bullet points."""

    # 4. Boot up the Local LLM to write the response
    print("[SYSTEM] Booting up local AI engine to analyze results...")
    engine = AIerEngine()
    engine.install_and_load()  # This handles downloading/loading Qwen 1.5B via huggingface_hub and llama-cpp-python

    print("\n" + "=" * 40)
    print("AIer Recommendation:")
    print("=" * 40)

    # The local AI generates the final text!
    recommendation = engine.generate_advice(prompt)
    print(recommendation)
    print("=" * 40)


if __name__ == "__main__":
    main()