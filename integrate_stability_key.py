import sys

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python integrate_stability_key.py <key_value>")
    sys.exit(1)

# Get the key_value from the command-line argument
key_value = sys.argv[1]

# Generate the content of the key.py file
content = f"stability_key = {repr(key_value)}\n"

# Write the content to key.py
with open("stability_key.py", "w") as f:
    f.write(content)

print(f"stability_key.py file has been integrated with stability_key = {key_value}")

