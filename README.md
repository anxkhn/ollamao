```markdown
# Ollamao Chat

#### Ollama + Lmao = Ollamao 🦙

### Chat with large language models on public Ollama instances

This Python script lets you connect to publicly available Ollama instances and chat with large language models (LLMs). Whether you're rocking a potato PC or just can't run giant models (like those 70B chonkers), **Ollamao's got your back**.

**Heads up:** You'll need to find the IP address of a public Ollama instance yourself. But hey, that’s part of the fun, right?

A good place to start is [Shodan](https://www.shodan.io/search?query=port%3A11434+html%3A%22Ollama%22) or [FOFA](https://en.fofa.info/result?qbase64=cG9ydD0iMTE0MzQiICYmIGJvZHk9Ik9sbGFtYSI%3D)

---

## Features

- **Automatic Model Listing:** Connects to the Ollama instance and displays available models upon startup.
- **Manual IP Input:** Enter the IP of a public Ollama instance you’ve tracked down.
- **Model Selection:** See which models are hanging out on the instance and pick your chat partner.
- **Chat History:** Keeps track of your convo so the LLM doesn’t forget who you are mid-sentence.
- **Streamed Output:** Responses come through one character at a time for that real-time vibe.
- **Exit Option:** Type "exit" to gracefully leave the chat instead of ghosting the LLM.

---

## Actions

- **Start chatting:**  Initiates a chat session with the selected model. You can converse with the model, ask it questions, and receive responses in real-time.
- **Download a model:**  Downloads a new language model from the Ollama library to the Ollama instance. You'll need to provide the model name from ollama.com/library
- **Delete a model:** Removes a model from the Ollama instance. Be careful with this one!
- **Load a model into memory:** Loads a model, making it ready for use. This might be necessary for some instances before you can chat with a model.
- **Unload a model from memory:** Removes a model from the instance's active memory. This can be useful for freeing up resources on the Ollama instance.

---

## Requirements

- Python 3.7 or higher
- `httpx` library

---

## How to Use

1. **Install the `httpx` library:**

   ```bash
   pip install httpx
   ```

2. **Hunt down a public Ollama instance:**  
   Use [Shodan](https://www.shodan.io/search?query=port%3A11434+html%3A%22Ollama%22) / [FOFA](https://en.fofa.info/result?qbase64=cG9ydD0iMTE0MzQiICYmIGJvZHk9Ik9sbGFtYSI%3D) to track down an IP, or grab one from `ip_list.txt`, or use your own private instance if you’re fancy like that.

3. **Run the script:**

   ```bash
   python main.py
   ```

4. **Follow the prompts:**

   - Enter the IP address of the Ollama instance.
   - Pick a model from the list (it’ll show you what’s available).
   - Start chatting! Talk, ask questions, or just see what the LLM has to say.
   - Type "exit" to end the session like a civilized person.

---

## Disclaimer

- **Play nice:** Remember, these are public instances. Be respectful, don’t share personal info, and don’t be that person who ruins it for everyone.
- **Availability:** Public instances might come and go, so don't blame us if your favorite one vanishes.
- **Performance:** Response times can vary based on server load, so maybe grab a coffee if things are slow.

---


## Changelog

**1.1.0 - 7 Dec '24**

- Switched from `requests` to `httpx` for improved performance and asynchronous support.
- Added a 10-second timeout to all API requests.
- Implemented robust connection handling with retry on failure.
- Added automatic model listing on startup.

**Have fun chatting with Ollamao! 🥳**

API Docs: [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)  
Reddit thread that started this madness: [Here’s why grandma can use your Ollama servers](https://www.reddit.com/r/ollama/comments/1guwg0w/your_ollama_servers_are_so_open_even_my_grandma/)