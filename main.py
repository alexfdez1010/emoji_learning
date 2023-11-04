from random import randint, shuffle
import emoji

from genanki import Deck, Model, Note, Package

import streamlit as st

import os

CSS = """
.card {
    font-family: helvetica;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}
#emoji{
    font-size: 100px;
}
"""

EMOJIS = {
    emoji: data
    for emoji, data in emoji.EMOJI_DATA.items() if len(emoji) == 1 # Only single emojis
}

MODEL = Model(
    1224149397,
    'Emoji language learning',
    fields=[
        {'name': 'Emoji'},
        {'name': 'Answer'}
    ],
    templates=[
        {
            'name': 'Emoji card',
            'qfmt': '<div id="emoji">{{Emoji}}</div>',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}'
        },
    ],
    css=CSS
)

LANGUAGES = {
    "Spanish": "es",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh",
    "Persian": "fa",
    "Indonesian": "id"
}

def process_description(description: str) -> str:
    """
    Process the description of the deck to eliminate underscores and two points

    Args:
        description (str): Description of the deck

    Returns:
        str: Processed description
    """
    return description.replace("_", " ").replace(":", "")

def capitalize_first_letter(phrase: str) -> str:
    """
    Capitalize the first letter of a phrase

    Args:
        phrase (str): Phrase to capitalize

    Returns:
        str: Capitalized phrase
    """
    return phrase[0].upper() + phrase[1:]

def generate_deck(language: str) -> str:
    deck = Deck(randint(1 << 31, 1 << 32), f"Emoji {language} deck")

    language_code = LANGUAGES[language]

    emojis = list(EMOJIS.items())
    shuffle(emojis)

    for emoji, data in emojis:
        
        if language_code in data:
            answer = process_description(data[language_code])

            if language in ("Spanish", "Portuguese", "French", "Italian", "Indonesian", "English", "German"):
                answer = capitalize_first_letter(answer)

            note = Note(
                model=MODEL,
                fields= [emoji, answer],
                sort_field=0
            )

            deck.add_note(note)
    
    package = Package(deck)
    package_name = f"emojis_{language_code}.apkg"

    package.write_to_file(package_name)

    return package_name

def main():
    
    st.set_page_config(
        page_title="Emoji language learning",
        page_icon=":books:"
    )

    st.title("📚 Emoji language learning")
    
    st.markdown(
        """
        Learning a new language can be quite challenging, as it often requires leveraging 
        the foundations of languages you already know. To address this challenge and capitalize 
        on a universally understood form of communication, this project harnesses the power of 
        emojis to facilitate language learning for individuals from any cultural background. 
        By integrating the universal appeal of emojis with the proven method of spaced repetition 
        learning, this project creates a dynamic deck of cards featuring emojis alongside their 
        descriptions in the language you aspire to learn. These decks are compatible with Anki, 
        the leading spaced-repetition application and also open source, allowing for a seamless 
        import into your Anki app to kickstart your learning journey.

        You can download Anki for free [here](https://apps.ankiweb.net/).
        """
    ) 

    language = st.selectbox("Select language", list(LANGUAGES.keys()))

    button = st.button("Generate deck")

    if button and language:
        package_name = generate_deck(language)

        package_content = open(package_name, "rb").read()
        
        st.success("Deck generated successfully! Download it below")

        st.download_button(
            "Download deck",
            data=package_content,
            file_name=package_name,
            args=(language,),
            help="Download the deck to import into Anki"
        )

        os.remove(package_name)


if __name__ == "__main__":
    main()