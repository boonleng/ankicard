import os
import csv
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


if __name__ == "__main__":
    my_model = genanki.Model(
        251960520,
        "Enuk Model",
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
                en_word, uk_word, gender = row[0], row[1], "-"
            else:
                en_word, uk_word, gender = row[0], row[1], row[2]
            audio_file = f"audio/{uk_word}.mp3"
            if not os.path.exists(audio_file):
                print(f"Generating audio for {audio_file} ...")
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
