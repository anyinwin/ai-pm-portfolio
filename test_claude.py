import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "I need to schedule a routine annual physical. What CPT codes should I expect and what questions should I ask to confirm my costs beforehand?"}
    ]
)

print(message.content[0].text)