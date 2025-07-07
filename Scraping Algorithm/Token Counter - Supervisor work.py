import spacy
import os
from pathlib import Path
from spacy import prefer_gpu
from tqdm.auto import tqdm

def clean_instance_text(instance_text: str) -> str:
    """Removes metadata lines from a single text instance."""
    METADATA_PREFIXES = [
        "NOVINA:", "DATUM:", "RUBRIKA:", "NADNASLOV:",
        "NASLOV:", "PODNASLOV:", "STRANA:", "AUTOR(I):"
    ]
    article_lines = []
    lines = instance_text.strip().split('\n')
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if not any(line_stripped.lower().startswith(prefix.lower()) for prefix in METADATA_PREFIXES):
            article_lines.append(line_stripped)
    return " ".join(article_lines)

def main():
    """
    Main function to run the token counting process.
    """
    # --- 1. Load Model ---
    gpu_enabled = prefer_gpu()
    print(f"spaCy GPU enabled: {gpu_enabled}")

    try:
        nlp = spacy.load("hr_core_news_sm", disable=["parser", "ner", "lemmatizer"])
        print("Croatian model loaded successfully.")
    except OSError:
        print("Model 'hr_core_news_sm' not found.")
        print("   Please run 'python -m spacy download hr_core_news_sm' in your terminal.")
        return 

    # --- 2. Define File Paths ---
    script_dir = Path(__file__).parent
    data_dir = script_dir / "Files"

    print(f"\nScanning for .txt files in: {data_dir}")

    if not data_dir.is_dir():
        print(f"\nERROR: The directory '{data_dir}' does not exist.")
        print("   Please make sure your .txt files are in a subfolder named 'Files'.")
        return

    txt_files = list(data_dir.glob('*.txt'))
    
    if not txt_files:
        print("\nNo .txt files found in the 'Files' directory.")
        return

    # --- 3. Main Processing Block ---
    grand_total_tokens = 0
    token_counts_per_file = {}

    print(f"\n--- Found {len(txt_files)} file(s) to process ---\n")
    for file_path in txt_files:
        file_name = file_path.name
        print(f"Reading and cleaning '{file_name}'...")
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            file_content = file.read()

        instances = [inst for inst in file_content.split("<***>") if inst.strip()]
        cleaned_texts = (clean_instance_text(inst) for inst in instances)

        tokens_in_this_file = 0
        print(f"Processing '{file_name}' with nlp.pipe()...")
        
        for doc in tqdm(nlp.pipe(cleaned_texts, batch_size=500), total=len(instances), desc=f"Processing {file_name}"):
            tokens_in_this_file += len(doc)

        token_counts_per_file[file_name] = tokens_in_this_file
        grand_total_tokens += tokens_in_this_file

        print(f"FINISHED: '{file_name}' | Tokens: {tokens_in_this_file:,}\n")
        # ---------------------------

    # --- 4. Final Summary Output ---
    print("="*60)
    print("FINAL AGGREGATED SUMMARY (ALL FILES)")
    print("="*60)
    for file_name, count in sorted(token_counts_per_file.items()):
        print(f"File: {file_name:<50} | Tokens: {count:,}")
    print("-"*60)
    print(f"{'GRAND TOTAL (all files):':<50} | Tokens: {grand_total_tokens:,}")
    print("="*60)

if __name__ == "__main__":
    main()