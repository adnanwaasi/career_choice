import ollama

def get_response(string1):
    response = ollama.chat(
        model="career",messages=[
            {"role": "user", "content": string1}
        ]
    )   
    return response["message"]["content"]

# Optional: Add data storage if needed

def store_data(id: str, prompt: str, response: str):
    filename = id + ".txt"
    with open(filename, "w") as f:
        f.write(f"{id}\t{prompt}\t{response}\n")
