DEMO_BOOK_ID = "demo-book"

DEMO_BOOK_TEXT = """
In the city of Narael, every book kept a memory of the person who last read it.
Mara, a young archivist, discovered that one forbidden volume was answering back.
The book warned her that the Silent Gate would open before dawn, unless the lost
names of the city were spoken aloud.

Eloy, the clockmaker, believed the warning was a trick. He had seen too many
machines mistaken for miracles. But when the tower bells rang without hands,
he followed Mara into the underground archive.

At the Silent Gate, they found Sarin, a guardian made of ink and shadow. Sarin
did not want to harm the city. He had been ordered to protect the names from
those who would turn memory into power.

Mara chose to read the names, not to control the city, but to return them to the
people who had forgotten themselves. The gate closed, the books fell silent, and
Narael remembered.
""".strip()

DEMO_BOOK_SECTIONS = [
    {
        "section_id": "section-1",
        "book_id": DEMO_BOOK_ID,
        "text": (
            "Mara is a young archivist in Narael. She discovers a forbidden volume "
            "that answers back and warns that the Silent Gate will open before dawn."
        ),
        "source": "book_section",
    },
    {
        "section_id": "section-2",
        "book_id": DEMO_BOOK_ID,
        "text": (
            "Eloy is a skeptical clockmaker. He doubts the warning, but follows Mara "
            "after the tower bells ring without hands."
        ),
        "source": "book_section",
    },
    {
        "section_id": "section-3",
        "book_id": DEMO_BOOK_ID,
        "text": (
            "Sarin is a guardian made of ink and shadow. He protects the lost names "
            "so memory cannot be turned into power."
        ),
        "source": "book_section",
    },
    {
        "section_id": "section-4",
        "book_id": DEMO_BOOK_ID,
        "text": (
            "Mara reads the lost names to return them to the people. The Silent Gate "
            "closes and Narael remembers."
        ),
        "source": "book_section",
    },
]
