"""
A simple regex engine that compiles a regex pattern into a finite state machine (FSM)

Discrete Math 2. Lab 3
Ukrainian Catholic University
Andrii Kryvyi
"""

from typing import Generator

from regex.tokens import Token


class State:
    """
    A class representing a state in a finite state machine (FSM) for regex matching.

    Attributes:
        idx: The index of the state.
        table: A list of tuples representing the transition table, where each
               tuple contains a token and the next state.
        is_terminal: A boolean indicating if the state is a terminal state.
    """

    idx: int
    table: list[tuple[Token, "State"]]
    is_terminal: bool

    def __init__(self, idx: int, is_terminal: bool = False) -> None:
        self.idx = idx
        self.table = []
        self.is_terminal = is_terminal

    def add_transition(self, token: Token, state: "State") -> None:
        """
        Adds a transition to the state for the given character.

        Parameters:
            token: The token to transition on.
            state: The state to transition to.
        """
        self.table.append((token, state))

    def next(self, char: str) -> "Generator[State, None, None]":
        """
        Returns the next state for the given character.

        Parameters:
            char: The character to check.

        Returns:
            The next state if the character is in the transition table, otherwise None.
        """
        for token, state in self.table:
            if token.check(char):
                yield state

    def __repr__(self):
        if self.is_terminal:
            return f"S{self.idx}(T)"
        return f"S{self.idx}"
