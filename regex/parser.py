"""
A simple regex engine that compiles a regex pattern into a finite state machine (FSM)

Discrete Math 2. Lab 3
Ukrainian Catholic University
Andrii Kryvyi
"""

from typing import Generator

from regex.state import State
from regex.tokens import AnyToken, InToken, NotToken, OrToken, RangeToken, Token


class ClassProcessor:
    """
    A class for processing character classes in regex.

    Attributes:
        chars: The character class being processed.
        tokens: The tokens in the class.
        range_: The range of characters in the class.
    """

    chars: list[str]
    tokens: list[Token]
    range_: str | None
    negated: bool = False

    def __init__(self) -> None:
        self.chars = []
        self.tokens = []
        self.range_ = None
        self.negated = False

    def add(self, char: str, escaped: bool = False) -> Token | None:
        """
        Adds a character to the class or range.

        Parameters:
            char: The character to add.
            escaped: A boolean indicating if the character is escaped.

        Returns:
            The character class if the end of the class is reached, otherwise None.
        """
        if not escaped and char == "^":
            if self.chars:
                raise ValueError("Invalid regex pattern")
            if self.range_ is not None:
                raise ValueError("Invalid regex pattern")

            self.negated = True
            return None

        if not escaped and char == "]":
            if self.range_ is not None:
                raise ValueError("Invalid regex pattern")

            tokens = []
            if self.chars:
                tokens.append(InToken(set(self.chars)))
            if self.tokens:
                tokens += self.tokens

            if not tokens:
                raise ValueError("Invalid regex pattern")

            if len(tokens) == 1:
                token = tokens[0]
            else:
                token = OrToken(*tokens)

            if self.negated:
                token = NotToken(token)

            return token

        if not escaped and char == "-":
            if self.range_ is not None or len(self.chars) == 0:
                raise ValueError("Invalid regex pattern")

            self.range_ = self.chars.pop()
            return None

        if self.range_ is not None:
            self.tokens.append(RangeToken(self.range_, char))
            self.range_ = None
        else:
            self.chars.append(char)

        return None


def parse(pattern: str) -> State:
    """
    Parses a regex pattern and builds a finite state machine (FSM).

    Parameters:
        pattern: The regex pattern to parse.

    Returns:
        The initial state of the FSM.
    """
    tokens = tokenize(pattern)
    pairs = group_tokens(tokens)
    return build(pairs)


def build(pairs: Generator[tuple[Token, str | None], None, None]) -> State:
    """
    Builds a finite state machine (FSM) from the given pairs of tokens and modifiers.

    Parameters:
        pairs: A generator of pairs of tokens and modifiers.

    Returns:
        The initial state of the FSM.
    """
    initial_state = State(0)
    jumps = [initial_state]
    counter = 1

    for token, modifier in pairs:
        new_state = State(counter)
        counter += 1
        for jump in jumps:
            jump.add_transition(token, new_state)

        match modifier:
            case None:
                jumps = [new_state]
            case "*":
                jumps.append(new_state)
                new_state.add_transition(token, new_state)
            case "?":
                jumps.append(new_state)

    for jump in jumps:
        jump.is_terminal = True

    return initial_state


def group_tokens(
    tokens: Generator[Token | str, None, None],
) -> Generator[tuple[Token, str | None], None, None]:
    """
    Groups tokens and modifiers into pairs.

    Parameters:
        tokens: A generator of tokens.

    Yields:
        Pairs of tokens and modifiers.
    """
    last_token = None
    for element in tokens:
        if isinstance(element, str):
            if last_token is None:
                raise ValueError("Invalid regex pattern")

            if element == "+":
                yield (last_token, None)
                element = "*"

            yield (last_token, element)
            last_token = None
            continue

        if last_token is not None:
            yield (last_token, None)

        last_token = element

    if last_token is not None:
        yield (last_token, None)


def tokenize(pattern: str) -> Generator[Token | str, None, None]:
    """
    Tokenizes a regex pattern into tokens.

    Parameters:
        pattern: The regex pattern to tokenize.

    Yields:
        Tokens and modifiers.
    """
    class_processor = None
    escaped = False
    for char in pattern:
        if class_processor is not None:
            token = class_processor.add(char, escaped)
            if token is not None:
                class_processor = None
                yield token

            escaped = False
            continue

        if not escaped and char == "[":
            class_processor = ClassProcessor()
            continue

        if not escaped and char in set("+*?"):
            yield char
            continue

        if not escaped and char == ".":
            yield AnyToken()
            continue

        if not escaped and char == "\\":
            escaped = True
            continue

        yield InToken({char})
        escaped = False
