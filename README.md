# Ollamao Chat

#### Ollama + Lmao = Ollamao 🦙

### Chat with large language models on public Ollama instances

This Python script lets you connect to publicly available Ollama instances and chat with large language models (LLMs). Whether you're rocking a potato PC or just can't run giant models (like those 70B chonkers), **Ollamao's got your back**.

**Heads up:** You'll need to find the IP address of a public Ollama instance yourself. But hey, that’s part of the fun, right?

A good place to start is [Shodan.](https://www.shodan.io/search?query=port%3A11434+html%3A%22Ollama%22)

---

## Features

- **Manual IP Input:** Enter the IP of a public Ollama instance you’ve tracked down.
- **Model Selection:** See which models are hanging out on the instance and pick your chat partner.
- **Chat History:** Keeps track of your convo so the LLM doesn’t forget who you are mid-sentence.
- **Streamed Output:** Responses come through one character at a time for that real-time vibe.
- **Exit Option:** Type "exit" to gracefully leave the chat instead of ghosting the LLM.

---

## Requirements

- Python 3.7 or higher
- `requests` library

---

## How to Use

1. **Install the `requests` library:**

   ```bash
   pip install requests
   ```

2. **Hunt down a public Ollama instance:**  
   Use [Shodan](https://www.shodan.io/search?query=port%3A11434+html%3A%22Ollama%22) to track down an IP, grab one from `ip_list.txt`, or use your own private instance if you’re fancy like that.

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

**Have fun chatting with Ollamao! 🥳**

API Docs: [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)  
Reddit thread that started this madness: [Here’s why grandma can use your Ollama servers](https://www.reddit.com/r/ollama/comments/1guwg0w/your_ollama_servers_are_so_open_even_my_grandma/)

---

Enjoy!
