from ollama import chat

MODEL_NAME = "qwen3:1.7b"

def generate_response(system_prompt: str, user_prompt: str) -> str:
    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
    )

    return response["message"]["content"]