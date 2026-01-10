
import os
import re

root_dir = r"c:\Users\rlaqu\Documents\GitHub\AI_Study_Logs\agent\Notion_Project"

def to_pascal_case(name):
    # Remove _PROTOCOL
    name = name.replace("_PROTOCOL", "")
    # Remove _DB if preferred, but let's keep it if part of the name unless user implied otherwise.
    # User's example: LECTURE_NOTE_DB_PROTOCOL -> LectureNote.md (Dropped DB)
    # Let's try to be smart. If it ends in _DB, drop it?
    # LECTURE_NOTE_DB -> LectureNote
    if name.endswith("_DB"):
        name = name[:-3]
    
    parts = name.split('_')
    # Capitalize each part
    return "".join(p.capitalize() for p in parts) + ".md"

def rename_protocols():
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith("_PROTOCOL.md"):
                old_path = os.path.join(dirpath, filename)
                name_body = filename[:-3] # remove .md
                new_filename = to_pascal_case(name_body)
                new_path = os.path.join(dirpath, new_filename)
                
                print(f"Renaming: {filename} -> {new_filename}")
                try:
                    os.rename(old_path, new_path)
                except Exception as e:
                    print(f"Error renaming {filename}: {e}")

if __name__ == "__main__":
    rename_protocols()
