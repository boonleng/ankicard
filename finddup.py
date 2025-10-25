import csv
import glob

FILE = "словничок.csv"

# Find duplicate 2nd column entries
seen = set()
duplicates = set()

with open(FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) > 1:
            uk_word = row[0]
            if uk_word in seen:
                duplicates.add(uk_word)
            seen.add(uk_word)

print("Duplicate entries found:")
for dup in duplicates:
    print(dup)

for audio in glob.glob("audio/*.mp3"):
    if audio.split("/")[-1].replace(".mp3", "") not in seen:
        print(f"Missing: {audio}")

# with open("bulia.txt", "r", encoding="utf-8") as f:
#     lines = f.readlines()
#     for line in lines:
#         word = line.split("\t")[0].strip().lower()
#         if word not in seen:
#             print(f"Missing entry for word in bulia.txt: {word}")
