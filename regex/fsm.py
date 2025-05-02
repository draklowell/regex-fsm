"""
A simple regex engine that compiles a regex pattern into a finite state machine (FSM)

Discrete Math 2. Lab 3
Ukrainian Catholic University
Andrii Kryvyi
"""

from collections import deque

from regex.parser import parse
from regex.state import State


class RegexFSM:
    """
    A class for compiling a regex pattern into a finite state machine (FSM).

    Attributes:
        initial_state: The initial state of the FSM.
    """

    initial_state: State

    def __init__(self, pattern: str) -> None:
        self.initial_state = parse(pattern)

    def check_string(self, string: str) -> bool:
        """
        Checks if the given string matches the regex pattern.

        Parameters:
            string: The string to check.

        Returns:
            True if the string matches the regex pattern, otherwise False.
        """
        states = deque([self.initial_state, None])
        for char in string:
            state = states.popleft()
            while state is not None:
                for next_state in state.next(char):
                    states.append(next_state)

                state = states.popleft()

            states.append(None)

        for state in states:
            if state and state.is_terminal:
                return True

        return False

    def to_graphviz(self) -> str:
        """
        Converts the FSM to a Graphviz dot format string.

        Returns:
            A string representing the FSM in Graphviz dot format.
        """
        graph = "digraph G {\n"
        graph += "rankdir=LR;\n"
        graph += "node [shape=circle];\n"

        visited = set([self.initial_state.idx])
        queue = deque([self.initial_state])

        while queue:
            state = queue.popleft()

            if state.is_terminal:
                graph += f"  S{state.idx} [shape=doublecircle];\n"

            for token, next_state in state.table:
                graph += f'  S{state.idx} -> S{next_state.idx} [label="{token!s}"];\n'

                if next_state.idx not in visited:
                    visited.add(next_state.idx)
                    queue.append(next_state)

        graph += "}\n"
        return graph
