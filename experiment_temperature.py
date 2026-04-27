import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

question = "I need to schedule a routine annual physical. What CPT codes should I expect and what questions should I ask to confirm my costs beforehand?"

print("=" * 60)
print("TEMPERATURE 0 - Running 3 times")
print("=" * 60)

for i in range(3):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        temperature=0,
        messages=[{"role": "user", "content": question}]
    )
    print(f"\nRun {i+1}:")
    print(response.content[0].text)
    print("-" * 40)

print("\n")
print("=" * 60)
print("TEMPERATURE 1 - Running 3 times")
print("=" * 60)

for i in range(3):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        temperature=1,
        messages=[{"role": "user", "content": question}]
    )
    print(f"\nRun {i+1}:")
    print(response.content[0].text)
    print("-" * 40)