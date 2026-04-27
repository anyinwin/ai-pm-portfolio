import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Three prompts of different complexity
prompts = [
    "What CPT codes for annual exam?",
    
    "I need to schedule a routine annual physical. I have Blue Cross PPO insurance in zip code 10001. What CPT codes should I expect and what specific questions should I ask to confirm my costs beforehand?",
    
    "I am a 32 year old woman with Blue Cross PPO insurance in zip code 10001. I need to schedule a routine annual physical with a new primary care physician. I have met $500 of my $1000 deductible this year. What CPT codes should I expect for this visit, what additional codes might be added without my knowledge, what questions should I ask the provider before my appointment to confirm costs, and what should I say when I call my insurance company to verify coverage?"
]

for i, prompt in enumerate(prompts):
    response = client.messages.count_tokens(
        model="claude-opus-4-6",
        messages=[{"role": "user", "content": prompt}]
    )
    
    word_count = len(prompt.split())
    token_count = response.input_tokens
    
    print(f"\nPrompt {i+1}:")
    print(f"Text: {prompt[:80]}...")
    print(f"Word count: {word_count}")
    print(f"Token count: {token_count}")
    print(f"Tokens per word ratio: {token_count/word_count:.2f}")