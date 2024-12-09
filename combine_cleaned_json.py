import json
import os

input_dir = "./cleaned_data/"
output_file = "combined_corpus.json"

def combine_files_to_json(input_dir, output_file):
    corpus = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as file:
                text = file.read()
                
                document = {
                    "source": filename,
                    "content": text,
                }
                corpus.append(document)

    
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(corpus, file, indent=4, ensure_ascii=False)

    print(f"Combined corpus saved to {output_file}")

combine_files_to_json(input_dir, output_file)
