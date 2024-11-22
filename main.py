import requests
import json


def main():
    """
    An interactive chatbot that connects to the Ollama API,
    allows you to choose a model, maintains chat history, streams
    the output to the terminal, and allows you to exit by typing 'exit'.
    """

    ip_address = input("Enter the IP address of the Ollama server: ")
    port = input("Enter the port (press Enter for default 11434): ")
    port = port if port else "11434"
    base_url = f"http://{ip_address}:{port}/api"

    # 1. Get available models
    response = requests.get(f"{base_url}/tags")
    response.raise_for_status()
    models = response.json()["models"]

    print("\nAvailable models:")
    for i, model in enumerate(models):
        print(f"{i+1}. {model['name']}")

    # 2. Choose a model
    while True:
        try:
            choice = int(input("\nChoose a model number: "))
            selected_model = models[choice - 1]["name"]
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")

    # 3. Start chatting
    messages = []
    while True:
        user_message = input("\nYou: ")
        if user_message.lower() == "exit":
            break  # Exit the chat loop

        messages.append({"role": "user", "content": user_message})

        response = requests.post(
            f"{base_url}/chat",
            json={"model": selected_model, "messages": messages, "stream": True},
            stream=True,
        )
        response.raise_for_status()

        print("Assistant: ", end="", flush=True)
        assistant_message = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                try:
                    json_data = json.loads(decoded_line)
                    assistant_message += json_data["message"]["content"]
                    print(json_data["message"]["content"], end="", flush=True)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    print(f"Raw response line: {decoded_line}")

        print()
        messages.append({"role": "assistant", "content": assistant_message})


if __name__ == "__main__":
    main()
