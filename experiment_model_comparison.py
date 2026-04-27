import anthropic
import os
import time

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

question = """I need to schedule a routine annual physical. 
I have Blue Cross PPO insurance in zip code 10001. 
What CPT codes should I expect and what specific 
questions should I ask to confirm my costs beforehand?"""

models = [
    "claude-opus-4-6",
    "claude-haiku-4-5-20251001"
]

for model in models:
    print(f"\n{'='*60}")
    print(f"MODEL: {model}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    response = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": question}]
    )
    
    end_time = time.time()
    latency = end_time - start_time
    
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    total_tokens = input_tokens + output_tokens
    
    print(f"Response:\n{response.content[0].text}")
    print(f"\nLatency: {latency:.2f} seconds")
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Total tokens: {total_tokens}")