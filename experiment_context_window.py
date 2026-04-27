import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# We're going to stuff the context window by repeating
# a large block of text until we hit the limit
# Claude Haiku has a 200k token context window
# so we'll use a smaller max_tokens to trigger the issue faster

chunk = """
CPT Code 99395 - Preventive visit ages 18-39. 
Comprehensive physical exam for established patient. 
Typical cost $150-250. Usually covered 100% under 
ACA plans as preventive care. Common add-ons include
blood panel 80050, Pap smear 88141, STI screening 87491.
Insurance verification recommended before appointment.
Always confirm network status with both insurance and provider.
""" * 1000  # repeat 1000 times to create a massive prompt

print("Chunk size created.")
print(f"Approximate length: {len(chunk.split())} words")
print("Attempting to count tokens first...")

try:
    token_response = client.messages.count_tokens(
        model="claude-haiku-4-5-20251001",
        messages=[{"role": "user", "content": chunk}]
    )
    print(f"Token count: {token_response.input_tokens}")
    print("Now attempting to send to Claude...")
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": chunk}]
    )
    print(response.content[0].text)

except anthropic.BadRequestError as e:
    print(f"\nBAD REQUEST ERROR: {e}")
    
except anthropic.APIStatusError as e:
    print(f"\nAPI STATUS ERROR: {e.status_code}")
    print(f"Message: {e.message}")

except Exception as e:
    print(f"\nERROR TYPE: {type(e).__name__}")
    print(f"ERROR: {e}")
