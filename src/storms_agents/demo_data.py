DEMO_BOOK_ID = "don-quijote"
DEMO_BOOK_TITLE = "Don Quijote de la Mancha"
DEMO_BOOK_AUTHOR = "Miguel de Cervantes Saavedra"

DEMO_BOOK_TEXT = """
Alonso Quijano, hidalgo de la Mancha, lee tantos libros de caballerias que decide
convertirse en caballero andante. Toma el nombre de Don Quijote, prepara sus armas,
elige a Rocinante como caballo y convierte a Aldonza Lorenzo en Dulcinea del Toboso,
senora ideal de sus pensamientos.

Sancho Panza, labrador practico y lleno de refranes, acepta acompanarlo como escudero
porque Don Quijote le promete el gobierno de una insula. Sancho ve el mundo con los
pies en la tierra, mientras su amo interpreta ventas como castillos y peligros comunes
como aventuras de caballeria.

En el famoso episodio de los molinos, Don Quijote cree ver gigantes desaforados donde
Sancho solo ve molinos de viento. Sancho le advierte que aquello no son gigantes, pero
Don Quijote carga con la lanza convencido de que cumple su destino caballeresco.

Tras caer vencido por las aspas, Don Quijote explica la derrota como obra de encantadores
que transformaron los gigantes en molinos. Esa tension entre ideal, locura, imaginacion
y realidad hace que Sancho siga discutiendo con su amo, entre la lealtad y el sentido comun.
""".strip()

DEMO_BOOK_SECTIONS = [
    {
        "section_id": "quijote-section-1",
        "book_id": DEMO_BOOK_ID,
        "text": (
            "Alonso Quijano reads so many books of chivalry that he decides to become "
            "Don Quijote de la Mancha, a knight-errant who will defend honor and seek "
            "adventures according to the ideals he has absorbed from books."
        ),
        "source": "book_section",
    },
    {
        "section_id": "quijote-section-2",
        "book_id": DEMO_BOOK_ID,
        "text": (
            "Don Quijote names Rocinante as his horse and imagines Dulcinea del Toboso "
            "as the noble lady who gives meaning to his deeds, even though she begins "
            "as Aldonza Lorenzo in ordinary village life."
        ),
        "source": "book_section",
    },
    {
        "section_id": "quijote-section-3",
        "book_id": DEMO_BOOK_ID,
        "text": (
            "Sancho Panza joins Don Quijote as a practical squire. He is loyal and "
            "curious, but he often questions his master's visions with earthy common "
            "sense and proverbial speech."
        ),
        "source": "book_section",
    },
    {
        "section_id": "quijote-section-4",
        "book_id": DEMO_BOOK_ID,
        "text": (
            "In the windmill scene, Don Quijote believes the windmills are giants. "
            "Sancho warns him that they are only windmills, but Don Quijote charges "
            "and is knocked down by the turning sails."
        ),
        "source": "book_section",
    },
    {
        "section_id": "quijote-section-5",
        "book_id": DEMO_BOOK_ID,
        "text": (
            "After the fall, Don Quijote explains that an enchanter changed the giants "
            "into windmills to rob him of glory. The scene reveals the conflict between "
            "his chivalric imagination and Sancho's practical reality."
        ),
        "source": "book_section",
    },
]
