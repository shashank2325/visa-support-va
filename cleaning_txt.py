import os


input_dir = "./scraped_data/"
output_dir = "./cleaned_data/"


unwanted_phrases = [
    "Official websites use .gov", 
    "Share sensitive information only on official", 
    "ALERT:",
    "Secure .gov websites use HTTPS",
    "Last updated on",
]

def clean_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    cleaned_lines = []
    for line in lines:
        if not any(phrase in line for phrase in unwanted_phrases):
            cleaned_lines.append(line.strip())

    
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(cleaned_lines))


if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        clean_file(input_path, output_path)
        print(f"Cleaned: {filename} -> {output_path}")
