import os
import json
import shutil
from pathlib import Path

# Constants
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "steam_data" / "new_steam"
CRAWLED_DATA_DIR = DATA_DIR / "crawled_data"

def clean_file(file_path):
    print(f"Processing {file_path.name}...")
    
    kept_lines = []
    removed_count = 0
    total_count = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                data = json.loads(line)
                total_count += 1
                
                game_count = data.get('game_count', 0)
                timecreated = data.get('timecreated')
                loccountrycode = data.get('loccountrycode')
                
                # Logic to KEEP:
                # 1. game_count > 0 OR
                # 2. timecreated is not None (profile loaded, valid user) OR
                # 3. loccountrycode is not None (profile loaded, valid user)
                
                if game_count > 0 or timecreated is not None or loccountrycode is not None:
                    kept_lines.append(line)
                else:
                    # Discard if everything is empty/zero (likely API error or completely empty private profile which we might want to retry anyway to be sure)
                    removed_count += 1
                    
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line in {file_path.name}")
                continue

    if removed_count > 0:
        # Create backup
        backup_path = file_path.with_suffix('.jsonl.bak')
        shutil.copy2(file_path, backup_path)
        print(f"  Backup created at {backup_path.name}")
        
        # Overwrite file
        with open(file_path, 'w', encoding='utf-8') as f:
            for line in kept_lines:
                f.write(line + "\n")
        print(f"  Removed {removed_count}/{total_count} lines. Saved clean file.")
    else:
        print(f"  No lines removed. File is clean.")

def main():
    if not CRAWLED_DATA_DIR.exists():
        print(f"Data directory {CRAWLED_DATA_DIR} does not exist.")
        return

    jsonl_files = sorted(list(CRAWLED_DATA_DIR.glob("crawled_users_*.jsonl")))
    
    if not jsonl_files:
        print("No crawled_users_*.jsonl files found.")
        return
        
    print(f"Found {len(jsonl_files)} files to check.")
    
    for file_path in jsonl_files:
        clean_file(file_path)

    print("\nCleaning complete. You can now run the crawler again to retry the removed users.")

if __name__ == "__main__":
    main()
