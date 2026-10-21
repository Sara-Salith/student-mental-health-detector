import ast
import base64
from pathlib import Path

# Original chatbot file
chatbot_file = Path("mind_aura_chatbot.py")

# Destination for the animation
assets_folder = Path("assets")
gif_file = assets_folder / "mind_aura.gif"

# Create assets folder if it doesn't exist
assets_folder.mkdir(exist_ok=True)

# Read the original chatbot
source = chatbot_file.read_text(encoding="utf-8")

# Parse the Python source without executing it
tree = ast.parse(source)

gif_data = None

# Find the MIND_AURA_GIF variable
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if (
                isinstance(target, ast.Name)
                and target.id == "MIND_AURA_GIF"
            ):
                gif_data = ast.literal_eval(node.value)
                break

    if gif_data is not None:
        break

if gif_data is None:
    raise ValueError(
        "Could not find MIND_AURA_GIF in mind_aura_chatbot.py"
    )

# Decode and save the GIF
gif_bytes = base64.b64decode(gif_data)

gif_file.write_bytes(gif_bytes)

print(f"GIF extracted successfully: {gif_file.resolve()}")
print(f"File size: {len(gif_bytes):,} bytes")