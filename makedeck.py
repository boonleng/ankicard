import os
import csv
import glob
import genanki

from gtts import gTTS

FILE = "словничок.csv"

CSS = """
.card {
    font-family: Arial;
    font-size: 24px;
    line-height: 1.6;
    text-align: center;
}
.uk {
    color: #3296ff;
}
.nightMode .uk {
    color: #ffff00;
}
"""


# Hash GUID using the Ukranian word only
class MyNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


def find_duplicates(remove=False):
    # Find duplicate 2nd column entries
    seen = set()
    duplicates = set()

    with open(FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 1:
                uk_word = row[0].lower().strip()
                if uk_word in seen:
                    duplicates.add(uk_word)
                seen.add(uk_word)

    if duplicates:
        print("Duplicate entries found:")
        for dup in duplicates:
            print(dup)

    for audio in glob.glob("audio/*.mp3"):
        if audio.split("/")[-1].lower().strip().replace(".mp3", "") not in seen:
            if remove:
                os.remove(audio)
                print(f"Audio without an entry: {audio} removed.")
            else:
                print(f"Audio without an entry: {audio}")


def add_entries():
    my_model = genanki.Model(
        251960520,
        "En-Uk Model",
        fields=[
            {"name": "Ukrainian"},
            {"name": "English"},
            {"name": "Gender"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{English}}",
                "afmt": '{{FrontSide}}<hr id="answer"><span class="uk">{{Ukrainian}}</span><br>({{Gender}})<br>{{Audio}}',
            },
            {
                "name": "Card 2",
                "qfmt": '<span class="uk">{{Ukrainian}}</span><br>{{Audio}}',
                "afmt": '{{FrontSide}}<hr id="answer">{{English}}<br>({{Gender}})',
            },
        ],
        css=CSS,
    )

    media_files = []
    deck = genanki.Deck(
        2519970926,
        "Буля словничок",
    )

    if not os.path.exists("audio"):
        os.makedirs("audio")

    with open(FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                print(f"Skipping row with insufficient data: {row}")
                continue
            if len(row) < 3:
                uk_word, en_word, gender = row[0], row[1], "-"
            else:
                uk_word, en_word, gender = row[0], row[1], row[2]
            uk_word = uk_word.lower().strip()
            en_word = en_word.lower().strip()
            audio_file = f"audio/{uk_word}.mp3"
            if not os.path.exists(audio_file):
                print(f"Generating {audio_file} ...")
                audio_converter = gTTS(text=uk_word, lang="uk", slow=False)
                audio_converter.save(audio_file)
            # Google Translate link:
            # link = f"https://translate.google.com/?sl=uk&tl=en&text={uk_word}&op=translate"
            # uk_word_with_link = f'<a href="{link}" target="uken">{uk_word}</a>'
            deck.add_note(
                MyNote(
                    model=my_model,
                    fields=[uk_word, en_word, gender, f"[sound:{uk_word}.mp3]"],
                )
            )
            media_files.append(audio_file)

    package = genanki.Package(deck)
    package.media_files = media_files
    output_file = os.path.expanduser("~/Downloads/enuk.apkg")
    package.write_to_file(output_file)
    print(f"Anki package created: {output_file}")


if __name__ == "__main__":
    args = os.sys.argv[1:]
    find_duplicates(remove="remove" in args)
    add_entries()
