import json

import httpx


def main():
    """
    An interactive chatbot that connects to the Ollama API,
    allows you to choose a model, maintains chat history, streams
    the output to the terminal, and allows you to exit by typing 'exit'.
    """

    base_url = get_base_url()
    if not base_url:
        return

    while True:
        print("\nChoose an action:")
        print("1. Start chatting")
        print("2. Download a model")
        print("3. Delete a model")
        print("4. Load a model into memory")
        print("5. Unload a model from memory")
        print("6. Exit")

        choice = input("\nEnter the number of your choice: ")

        if choice == "1":
            start_chat(base_url)
        elif choice == "2":
            download_model(base_url)
        elif choice == "3":
            delete_model(base_url)
        elif choice == "4":
            load_model(base_url)
        elif choice == "5":
            unload_model(base_url)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please enter a valid number.")


def get_base_url():
    """Gets the base URL from the user, with retries on connection failure."""
    while True:
        ip_address = input("Enter the IP address of the Ollama server: ")
        port = input("Enter the port (press Enter for default 11434): ")
        port = port if port else "11434"
        base_url = f"http://{ip_address}:{port}/api"

        try:
            response = httpx.get(f"{base_url}/tags", timeout=10.0)
            response.raise_for_status()
            print("\nAvailable models:")
            for model in response.json()["models"]:
                print(f"- {model['name']}")
            return base_url
        except httpx.HTTPError as exc:
            print(f"Error connecting to Ollama server: {exc}")
            if input("Try a different IP address? (y/n): ").lower() != "y":
                return None


def start_chat(base_url):
    """Starts an interactive chat session with a chosen model."""

    # 1. Get available models
    try:
        response = httpx.get(f"{base_url}/tags", timeout=10.0)
        response.raise_for_status()
        models = response.json()["models"]
    except httpx.HTTPError as exc:
        print(f"HTTP error occurred: {exc}")
        return

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

        try:
            response = httpx.post(
                f"{base_url}/chat",
                json={
                    "model": selected_model,
                    "messages": messages,
                    "stream": True,
                },
                stream=True,
                timeout=10.0,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            print(f"HTTP error occurred: {exc}")
            return

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


def download_model(base_url):
    """Downloads a model from the Ollama library."""
    print("\nYou can browse available models at: ollama.com/library")
    print(
        "Hint: Specify the model size using the format: model:size e.g. llama3.2:3b"
    )
    model_name = input("Enter the name of the model to download: ")
    try:
        response = httpx.post(
            f"{base_url}/pull",
            json={"model": model_name},
            stream=True,
            timeout=10.0,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"HTTP error occurred: {exc}")
        return

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")
            try:
                json_data = json.loads(decoded_line)
                print(json_data["status"])
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                print(f"Raw response line: {decoded_line}")


def delete_model(base_url):
    """Deletes a model."""
    model_name = input("Enter the name of the model to delete: ")
    try:
        response = httpx.delete(
            f"{base_url}/delete", json={"model": model_name}, timeout=10.0
        )
        response.raise_for_status()
        print(f"Model '{model_name}' deleted successfully.")
    except httpx.HTTPError as exc:
        print(f"HTTP error occurred: {exc}")


def load_model(base_url):
    """Loads a model into memory."""
    model_name = input("Enter the name of the model to load: ")
    try:
        response = httpx.post(
            f"{base_url}/generate", json={"model": model_name}, timeout=10.0
        )
        response.raise_for_status()
        print(f"Model '{model_name}' loaded successfully.")
    except httpx.HTTPError as exc:
        print(f"HTTP error occurred: {exc}")


def unload_model(base_url):
    """Unloads a model from memory."""

    # 1. Get running models
    try:
        response = httpx.get(f"{base_url}/ps", timeout=10.0)
        response.raise_for_status()
        models = response.json()["models"]
    except httpx.HTTPError as exc:
        print(f"HTTP error occurred: {exc}")
        return

    if not models:
        print("No models are currently loaded in memory.")
        return

    print("\nLoaded models:")
    for i, model in enumerate(models):
        print(f"{i+1}. {model['name']}")

    # 2. Choose a model to unload
    while True:
        try:
            choice = int(input("\nChoose a model number to unload: "))
            selected_model = models[choice - 1]["name"]
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")

    try:
        response = httpx.post(
            f"{base_url}/generate",
            json={"model": selected_model, "keep_alive": 0},
            timeout=10.0,
        )
        response.raise_for_status()
        print(f"Model '{selected_model}' unloaded successfully.")
    except httpx.HTTPError as exc:
        print(f"HTTP error occurred: {exc}")


if __name__ == "__main__":
    main()
