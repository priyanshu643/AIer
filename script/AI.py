import os
from huggingface_hub import hf_hub_download
from llama_cpp import Llama


class AIerEngine:
    def __init__(self):
        # We define exactly which model we want to power our CLI
        self.repo_id = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
        self.filename = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
        self.models_dir = os.path.join(os.getcwd(), "models")
        self.llm = None

    def install_and_load(self):
        print("Checking for AIer core engine...")

        # 1. Download the model (or instantly return the path if it already exists)
        # It safely stores the file in your AIer/models folder
        model_path = hf_hub_download(
            repo_id=self.repo_id,
            filename=self.filename,
            local_dir=self.models_dir
        )
        print("Engine installed and ready!")

        # 2. Load the model into memory
        # verbose=False keeps the terminal clean from C++ debug logs
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,  # Gives the AI room to read hardware stats and reply
            verbose=False
        )

    def generate_advice(self, user_prompt):
        if not self.llm:
            return "Error: Model not loaded."
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system",
                 "content": "You are a senior AI hardware engineer. Format your responses using Markdown, bullet points, and bold text for readability."},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=400,  # Increased so it has room to write a good response
            stop=["<|im_end|>"]  # Qwen's actual stop token
        )

        return response['choices'][0]['message']['content'].strip()

        # Extract just the text from the response dictionary
        text = response['choices'][0]['text'].strip()
        return text


# --- Test it out ---
if __name__ == "__main__":
    engine = AIerEngine()
    engine.install_and_load()

    # Let's ask it a test question
    answer = engine.generate_advice("What is a good graphics card for AI?")
    print(f"\nAIer: {answer}")