import nbformat
import os

def fix_plot_path(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    modified = False
    for cell in nb.cells:
        if cell.cell_type == 'code':
            source = cell.source
            # Fix the save path to be relative to the notebook location
            # Assuming notebook is in src/eda, 'assets/...' is correct relative path
            # But making it more robust or checking if directory exists
            
            if "save_path = 'assets/interaction_review/playtime_implicit_score_dist.png'" in source:
                new_source = source.replace(
                    "save_path = 'assets/interaction_review/playtime_implicit_score_dist.png'",
                    "save_dir = 'assets/interaction_review'\nif not os.path.exists(save_dir):\n    os.makedirs(save_dir)\nsave_path = os.path.join(save_dir, 'playtime_implicit_score_dist.png')"
                )
                cell.source = new_source
                modified = True
                print("Fixed plot save path logic")

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"Updated {filepath}")
    else:
        print(f"No changes made to {filepath}")

if __name__ == "__main__":
    base_dir = r"c:\Users\rlaqu\Documents\GitHub\AI_Study_Logs\My_RecSys_Project\src\eda"
    fix_plot_path(os.path.join(base_dir, "user_interaction.ipynb"))
