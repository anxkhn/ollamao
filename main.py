import json
import webbrowser

import requests


def main():
    """
    An interactive chatbot that connects to the Ollama API,
    allows you to choose a model, maintains chat history, streams
    the output to the terminal, and allows you to exit by typing 'exit'.
    """

    while True:
        ip_address = input("Enter the IP address of the Ollama server: ")
        port = input("Enter the port (press Enter for default 11434): ")
        port = port if port else "11434"
        test_url = f"http://{ip_address}:{port}"
        base_url = f"http://{ip_address}:{port}/api"

        # Check if the Ollama server is running
        try:
            response = requests.get(test_url)
            response.raise_for_status()
            if "Ollama is running" in response.text:
                print("Connected to Ollama server successfully!")
                break
            else:
                print(
                    "Could not connect to Ollama server. Please check the IP address and port."
                )
        except requests.exceptions.RequestException as e:
            print(f"Could not connect to Ollama server: {e}")

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


def start_chat(base_url):
    """Starts an interactive chat session with a chosen model."""

    # 1. Get available models
    response = requests.get(f"{base_url}/tags")
    response.raise_for_status()
    models = response.json()["models"]

    print("\nAvailable models:")
    for i, model in enumerate(models):
        print(f"{i+1}. {model['name']}")

    # 2. Choose a model (by number, name, or 0/exit to go back)
    while True:
        try:
            choice = input(
                "\nChoose a model number or name (or 0/exit to go back): "
            )
            if choice == "0" or choice.lower() == "exit":
                return
            try:
                choice = int(choice)
                selected_model = models[choice - 1]["name"]
            except ValueError:
                selected_model = choice
                if not any(
                    model["name"] == selected_model for model in models
                ):
                    raise ValueError("Invalid model name.")
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number or model name.")

    # 3. Start chatting
    messages = [
        {
            "role": "system",
            "content": "You are an Ollama chatbot built by Anas Khan. You have to serve user query be as helpful as possible.",
        },
    ]
    while True:
        user_message = input("\nYou: ")
        if user_message.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_message})

        response = requests.post(
            f"{base_url}/chat",
            json={
                "model": selected_model,
                "messages": messages,
                "stream": True,
            },
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


def download_model(base_url):
    """Downloads a model from the Ollama library."""
    print("\nYou can browse available models at: ollama.com/library")
    print(
        "Hint: Specify the model size using the format: model:size e.g. llama3.2:3b"
    )
    explore = input(
        "Would you like to explore models in your browser? (y/n): "
    )
    if explore.lower() == "y":
        webbrowser.open("https://ollama.com/library")

    model_name = input(
        "Enter the name of the model to download (or 0/exit to go back): "
    )
    if model_name == "0" or model_name.lower() == "exit":
        return

    response = requests.post(
        f"{base_url}/pull", json={"model": model_name}, stream=True
    )
    response.raise_for_status()

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

    # 1. Get available models
    response = requests.get(f"{base_url}/tags")
    response.raise_for_status()
    models = response.json()["models"]

    print("\nAvailable models:")
    for i, model in enumerate(models):
        print(f"{i+1}. {model['name']}")

    # 2. Choose a model (by number, name, or 0/exit to go back)
    while True:
        try:
            choice = input(
                "\nChoose a model number or name to delete (or 0/exit to go back): "
            )
            if choice == "0" or choice.lower() == "exit":
                return
            try:
                choice = int(choice)
                selected_model = models[choice - 1]["name"]
            except ValueError:
                selected_model = choice
                if not any(
                    model["name"] == selected_model for model in models
                ):
                    raise ValueError("Invalid model name.")
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number or model name.")

    response = requests.delete(
        f"{base_url}/delete", json={"model": selected_model}
    )
    response.raise_for_status()
    print(f"Model '{selected_model}' deleted successfully.")


def load_model(base_url):
    """Loads a model into memory."""

    # 1. Get available models
    response = requests.get(f"{base_url}/tags")
    response.raise_for_status()
    models = response.json()["models"]

    print("\nAvailable models:")
    for i, model in enumerate(models):
        print(f"{i+1}. {model['name']}")

    # 2. Choose a model (by number, name, or 0/exit to go back)
    while True:
        try:
            choice = input(
                "\nChoose a model number or name to load (or 0/exit to go back): "
            )
            if choice == "0" or choice.lower() == "exit":
                return
            try:
                choice = int(choice)
                selected_model = models[choice - 1]["name"]
            except ValueError:
                selected_model = choice
                if not any(
                    model["name"] == selected_model for model in models
                ):
                    raise ValueError("Invalid model name.")
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number or model name.")

    response = requests.post(
        f"{base_url}/generate", json={"model": selected_model}
    )
    response.raise_for_status()
    print(f"Model '{selected_model}' loaded successfully.")


def unload_model(base_url):
    """Unloads a model from memory."""

    # 1. Get running models
    response = requests.get(f"{base_url}/ps")
    response.raise_for_status()
    models = response.json()["models"]

    if not models:
        print("No models are currently loaded in memory.")
        return

    print("\nLoaded models:")
    for i, model in enumerate(models):
        print(f"{i+1}. {model['name']}")

    # 2. Choose a model to unload (by number, name, or 0/exit to go back)
    while True:
        try:
            choice = input(
                "\nChoose a model number or name to unload (or 0/exit to go back): "
            )
            if choice == "0" or choice.lower() == "exit":
                return
            try:
                choice = int(choice)
                selected_model = models[choice - 1]["name"]
            except ValueError:
                selected_model = choice
                if not any(
                    model["name"] == selected_model for model in models
                ):
                    raise ValueError("Invalid model name.")
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number or model name.")

    response = requests.post(
        f"{base_url}/generate",
        json={"model": selected_model, "keep_alive": 0},
    )
    response.raise_for_status()
    print(f"Model '{selected_model}' unloaded successfully.")


if __name__ == "__main__":
    main()
