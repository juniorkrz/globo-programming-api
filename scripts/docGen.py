import json

try:
    with open('./data/channels.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except Exception as e:
    print(f"Error loading file: {e}")
    data = {}

# Start creating the markdown content
markdown_content = "# Canais Disponíveis\n\n"

for category, details in data.items():
    markdown_content += f"## {details['name']}\n"

    for channel_key, channel_details in details['channels'].items():
        markdown_content += f"- {channel_details['name']}: ```{channel_key}```\n"

    markdown_content += "\n"

# Write the markdown content to Channels.MD
try:
    with open('./docs/Channels.MD', 'w', encoding='utf-8') as file:
        file.write(markdown_content)
    print("Channels.MD created successfully.")
except Exception as e:
    print(f"Error writing file: {e}")
