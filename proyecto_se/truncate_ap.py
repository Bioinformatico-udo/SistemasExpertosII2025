# Truncate ap.py to remove lines 1166 onwards (duplicate old class code)
with open('ap.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Keep only lines 0–1164 (1-indexed: lines 1–1165)
keep = lines[:1165]
with open('ap.py', 'w', encoding='utf-8') as f:
    f.writelines(keep)

print(f"Done. File now has {len(keep)} lines.")
