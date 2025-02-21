# Ollamao Chat

#### Ollama + Lmao = Ollamao 🦙

### Chat with large language models on public Ollama instances

This Python script lets you connect to publicly available Ollama instances and chat with large language models (LLMs). Whether you're rocking a potato PC or just can't run giant models (like those 70B chonkers), **Ollamao's got your back**.

**Heads up:** You'll need to find the IP address of a public Ollama instance yourself. But hey, that’s part of the fun, right?

A good place to start is [Shodan](https://www.shodan.io/search?query=port%3A11434+html%3A%22Ollama%22) or [FOFA](https://en.fofa.info/result?qbase64=cG9ydD0iMTE0MzQiICYmIGJvZHk9Ik9sbGFtYSI%3D)




## Features

- **Automatic Model Listing:** Connects to the Ollama instance and displays available models upon startup.
- **Manual IP Input:** Enter the IP of a public Ollama instance you’ve tracked down.
- **Model Selection:** See which models are hanging out on the instance and pick your chat partner.
- **Chat History:** Keeps track of your convo so the LLM doesn’t forget who you are mid-sentence.
- **Streamed Output:** Responses come through one character at a time for that real-time vibe.
- **Exit Option:** Type "exit" to gracefully leave the chat instead of ghosting the LLM.




## Actions

- **Start chatting:**  Initiates a chat session with the selected model. You can converse with the model, ask it questions, and receive responses in real-time.
- **Download a model:**  Downloads a new language model from the Ollama library to the Ollama instance. You'll need to provide the model name from ollama.com/library
- **Delete a model:** Removes a model from the Ollama instance. Be careful with this one!
- **Load a model into memory:** Loads a model, making it ready for use. This might be necessary for some instances before you can chat with a model.
- **Unload a model from memory:** Removes a model from the instance's active memory. This can be useful for freeing up resources on the Ollama instance.




### Getting Started with Ollamao Chat

Follow these steps to get chatting with large language models using **Ollamao**.




## Step 1: Get an IP Address

To connect to an Ollama instance, you'll need its IP address. Here’s how to find one:

1. **Use Shodan:**  
   Visit [Shodan](https://www.shodan.io/search?query=port%3A11434+html%3A%22Ollama%22) and search for public Ollama instances using the query `port:11434 html:"Ollama"`.

2. **Try FOFA:**  
   Access [FOFA](https://en.fofa.info/result?qbase64=cG9ydD0iMTE0MzQiICYmIGJvZHk9Ik9sbGFtYSI%3D) (requires an account) and search for active instances. Use the query `port="11434" && body="Ollama"`.

3. **Check the Public IP List:**  
   A curated list of active Ollama instances is available [here](https://raw.githubusercontent.com/anxkhn/ollamao/refs/heads/main/ip_list.txt). This list is updated regularly with working IPs.
   
   Alternatively, visit [benchmark.md](https://raw.githubusercontent.com/anxkhn/ollamao/refs/heads/main/benchmark.md) for a list of public IPs with their Ollama versions and latency.  
   (Note: This list is updated randomly, so it may not be up to date. It's best to use Shodan or Fofa)

## Step 2: Install Requirements

Ensure you have Python installed (version 3.7 or higher) and the `requests` library. Install it using:

```bash
pip install requests
```




## Step 3: Run the Script

Launch the script with:

```bash
python main.py
```




## Step 4: **Connect to an Ollama Instance**

1. **Enter Server Details:**  
   When prompted, input the IP address and port of the Ollama instance. Default port is `11434`.  
   The script will verify the connection.

2. **Choose an Action:**  
   After connecting, you’ll see these options:
   - Start chatting
   - Download a model
   - Delete a model
   - Load a model into memory
   - Unload a model from memory
   - Exit the application




## Step 5: **Interactive Chat**

### Starting a Chat Session

1. Select **Start chatting**.  
2. The script will display available models hosted on the instance.  
3. Choose a model by number or name and begin chatting.  
4. Type `exit` to end the session.




## Additional Features

### Downloading a Model
1. Select **Download a model**.  
2. Browse the [Ollama Model Library](https://ollama.com/library) for options.  
3. Provide the model name (e.g., `llama2:13b`).  
4. The script downloads the model to the connected instance.

### Deleting a Model
1. Select **Delete a model**.  
2. Pick a model from the available list to remove it from the instance.

### Loading a Model into Memory
1. Select **Load a model into memory**.  
2. Choose a model to preload it for faster access.

### Unloading a Model from Memory
1. Select **Unload a model from memory**.  
2. Remove a running model from active memory to free resources.




## Exiting the Script

Type `exit` at any time to gracefully close the session.  





## Disclaimer

- **Play nice:** Remember, these are public instances. Be respectful, don’t share personal info, and don’t be that person who ruins it for everyone.
- **Availability:** Public instances might come and go, so don't blame us if your favorite one vanishes.
- **Performance:** Response times can vary based on server load, so maybe grab a coffee if things are slow.





## Changelog

**1.2.0 - 7 Dec '24**

- Reverted back to using `requests` library as `httpx.delete` doesn't support message body (as per standard). [Issue Raised](https://github.com/ollama/ollama/issues/7985)

**1.1.0 - 7 Dec '24**

- Switched from `requests` to `httpx` for improved performance and asynchronous support.
- Implemented robust connection handling with retry on failure.
- Added automatic model listing on startup.

**Have fun chatting with Ollamao! 🥳**

API Docs: [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)  
Reddit thread that started this madness: [Here’s why grandma can use your Ollama servers](https://www.reddit.com/r/ollama/comments/1guwg0w/your_ollama_servers_are_so_open_even_my_grandma/)
