# 🤖 AIer: AI Hardware Scanner & Recommender

AIer is an intelligent Python CLI tool that scans your local hardware (CPU, RAM, and GPU VRAM) to recommend the perfect open-source AI models for your system. 

Instead of relying on basic `if/else` logic, AIer uses **Retrieval-Augmented Generation (RAG)**. It fetches real-time trending GGUF models from the Hugging Face API, calculates VRAM requirements, and passes the data to an embedded AI engine (Qwen 1.5B) to write a custom, human-readable recommendation that accounts for Context Windows (KV Cache).

---

## ✨ Features
* **Deep Hardware Scanning:** Detects CPU details, system RAM, and reads NVIDIA/AMD VRAM dynamically using native subprocess calls.
* **Live API Integration:** Fetches the most downloaded GGUF models directly from Hugging Face.
* **Embedded AI Engine:** Uses `llama-cpp-python` to run a local 1.5B parameter model that acts as your hardware advisor.
* **KV Cache Awareness:** Ensures recommendations leave enough VRAM breathing room for user prompts and generation space.

---

## 🚀 Installation

**1. Clone the repository**
```bash
git clone https://github.com/priyanshu643/AIer.git
cd AIer
```

**2. Create a virtual environment (Recommended)**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

**3. Install required dependencies**
```bash
pip install psutil py-cpuinfo requests huggingface_hub llama-cpp-python
```
*(Note: If you have a supported GPU and want the embedded AI to run faster, you can install `llama-cpp-python` with specific hardware acceleration flags [found in their documentation](https://github.com/abetlen/llama-cpp-python#installation-with-hardware-acceleration)).*

---

## 🛠️ Usage

To start the hardware scan and generate your recommendation, run:

```bash
python script/script.py
```

### What happens when you run it?
1. **Hardware Scan:** AIer instantly checks your RAM and VRAM.
2. **Fetch & Filter:** It contacts Hugging Face, downloads the trending list, and filters out models that would exceed your system limits.
3. **Engine Boot:** *(First run only)* It downloads a ~1.1GB Qwen model into a local `models/` directory.
4. **Recommendation:** The embedded AI reads your specs and outputs a formatted Markdown recommendation explaining exactly which model you should install and why.

---

## 📁 Project Structure

```text
AIer/
├── script/
│   ├── AI.py          # Manages downloading and running the embedded AI model
│   └── script.py      # Main execution file connecting hardware scanning & recommendation
├── stats/
│   ├── cpu.py         # Handles CPU and System RAM detection
│   └── gpu.py         # Handles GPU and VRAM detection
├── .gitignore         # Ignores downloaded models, IDE settings, and cache
└── README.md          # Project documentation
```
