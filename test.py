"""
A simple regex engine that compiles a regex pattern into a finite state machine (FSM)

Discrete Math 2. Lab 3
Ukrainian Catholic University
Andrii Kryvyi
"""

from regex.fsm import RegexFSM

# Test 2
regex_compiled2 = RegexFSM("a[bc]d")
assert regex_compiled2.check_string("abd")
assert regex_compiled2.check_string("acd")
assert not regex_compiled2.check_string("ad")
assert not regex_compiled2.check_string("a[bc]d")

# Test 3
regex_compiled3 = RegexFSM("a[bc]d*")
assert regex_compiled3.check_string("abd")
assert regex_compiled3.check_string("ab")
assert regex_compiled3.check_string("acd")
assert not regex_compiled3.check_string("ad")
assert not regex_compiled3.check_string("a")
assert not regex_compiled3.check_string("a[bc]d")

# Test 4
regex_compiled4 = RegexFSM("a[^bc]d*e")
assert not regex_compiled4.check_string("abd")
assert not regex_compiled4.check_string("acd")
assert not regex_compiled4.check_string("ad")
assert not regex_compiled4.check_string("a")
assert not regex_compiled4.check_string("afd")
assert regex_compiled4.check_string("afde")
assert not regex_compiled4.check_string("afd")
assert regex_compiled4.check_string("afddde")
assert regex_compiled4.check_string("afddddde")

# Test 5
regex_compiled5 = RegexFSM("a[bc]?d*e")
assert regex_compiled5.check_string("abe")
assert regex_compiled5.check_string("acde")
assert not regex_compiled5.check_string("ad")
assert not regex_compiled5.check_string("a")
assert not regex_compiled5.check_string("afd")
assert regex_compiled5.check_string("ae")

# Test 6
regex_compiled6 = RegexFSM("a[a-z]?d*e+")
assert regex_compiled6.check_string("abdde")
assert not regex_compiled6.check_string("a4de")
assert not regex_compiled6.check_string("a4deee")
