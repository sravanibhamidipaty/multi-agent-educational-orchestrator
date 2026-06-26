import time
from groq import Groq
from groq.types.chat import ChatCompletion
from config import GROQ_API_KEY

client: Groq = Groq(api_key=GROQ_API_KEY)

start_time: float = time.time() # to count the latency

response: ChatCompletion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"user", "content": "What is a node in a network?"}]
)

end_time: float = time.time()

print(f"Response: {response.choices[0].message.content}")
print(f"Latency: {end_time-start_time}s")
print(f"Input tokens: {response.usage.prompt_tokens}")
print(f"Output tokens: {response.usage.completion_tokens}")