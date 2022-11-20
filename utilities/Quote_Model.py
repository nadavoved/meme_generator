"""Contain the QuoteModel class, which encapsulates quotes as objects.

Those are used within a text - picture generator.
"""


class QuoteModel:
    """Encapsulate quote components."""

    def __init__(self, body, author):
        """Construct a new QuoteModel object."""
        self.body = body
        self.author = author

    def __str__(self):
        """Return a human-readable string representation."""
        return f'{self.body} - {self.author}'

    def __repr__(self):
        """Return a repr of the object."""
        return f'QuoteModel({self.body!r}, {self.author!r})'
