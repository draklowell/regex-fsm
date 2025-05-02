"""
A simple regex engine that compiles a regex pattern into a finite state machine (FSM)

Discrete Math 2. Lab 3
Ukrainian Catholic University
Andrii Kryvyi
"""

from abc import ABC, abstractmethod


class Token(ABC):
    """
    An abstract base class representing a token in a regex pattern.
    """

    @abstractmethod
    def check(self, char: str) -> bool:
        """
        Checks if the given character matches the token.

        Parameters:
            char: The character to check.

        Returns:
            True if the character matches the token, otherwise False.
        """

    def __repr__(self):
        return "Unknown"


class AnyToken(Token):
    """
    A class representing a token that matches any character.
    """

    def check(self, char: str) -> bool:
        return True

    def __repr__(self):
        return "Any"


class InToken(Token):
    """
    A class representing a token that matches specific characters.

    Attributes:
        chars: The characters to match.
    """

    chars: set[str]

    def __init__(self, chars: set[str]) -> None:
        self.chars = chars

    def check(self, char: str) -> bool:
        return char in self.chars

    def __repr__(self):
        if len(self.chars) == 1:
            return repr(next(iter(self.chars)))

        return f"In({', '.join(map(repr, self.chars))})"


class RangeToken(Token):
    """
    A class representing a token that matches a range of characters.

    Attributes:
        start: The starting character of the range.
        end: The ending character of the range.
    """

    start: str
    end: str

    def __init__(self, start: str, end: str) -> None:
        if start > end:
            raise ValueError("Invalid range")

        self.start = start
        self.end = end

    def check(self, char: str) -> bool:
        return self.start <= char <= self.end

    def __repr__(self):
        return f"Range({self.start}-{self.end})"


class OrToken(Token):
    """
    A class representing a token that matches a logical OR of other tokens.

    Attributes:
        tokens: The tokens to match.
    """

    tokens: tuple[Token, ...]

    def __init__(self, *tokens: Token) -> None:
        self.tokens = tokens

    def check(self, char: str) -> bool:
        return any(token.check(char) for token in self.tokens)

    def __repr__(self):
        return f"Or({', '.join(map(repr, self.tokens))})"


class NotToken(Token):
    """
    A class representing a token that matches a logical NOT of other token.

    Attributes:
        token: The token to match.
    """

    token: Token

    def __init__(self, token: Token) -> None:
        self.token = token

    def check(self, char: str) -> bool:
        return not self.token.check(char)

    def __repr__(self):
        return f"Not({self.token!r})"
