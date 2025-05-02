"""
A simple regex engine that compiles a regex pattern into a finite state machine (FSM)

Discrete Math 2. Lab 3
Ukrainian Catholic University
Andrii Kryvyi
"""

from regex.fsm import RegexFSM

pattern0 = "a*4.+hi"
fsm0 = RegexFSM(pattern0)
with open("examples/pattern0.dot", "w", encoding="utf8") as file:
    file.write(fsm0.to_graphviz())
assert fsm0.check_string("aaaaaa4uhi")
assert fsm0.check_string("4uhi")
assert fsm0.check_string("a4.hi")
assert fsm0.check_string("444hi")
assert not fsm0.check_string("meow")
assert not fsm0.check_string("4hi")


pattern1 = "[a-c]+[d-f]+[g-i]*"
fsm1 = RegexFSM(pattern1)
with open("examples/pattern1.dot", "w", encoding="utf8") as file:
    file.write(fsm1.to_graphviz())
assert fsm1.check_string("abcddggg")
assert fsm1.check_string("aaadef")
assert fsm1.check_string("bcdfi")
assert fsm1.check_string("ccdd")
assert fsm1.check_string("abcd")
assert not fsm1.check_string("xyz")

pattern2 = "[a-zsh]*[^a-z]+"
fsm2 = RegexFSM(pattern2)
with open("examples/pattern2.dot", "w", encoding="utf8") as file:
    file.write(fsm2.to_graphviz())
assert fsm2.check_string("shs123")
assert fsm2.check_string("abcm@#")
assert fsm2.check_string("shtT")
assert not fsm2.check_string("shshabc")
assert not fsm2.check_string("")

pattern3 = "[^a-z]+[A-Z]*"
fsm3 = RegexFSM(pattern3)
with open("examples/pattern3.dot", "w", encoding="utf8") as file:
    file.write(fsm3.to_graphviz())
assert fsm3.check_string("123ABC")
assert fsm3.check_string("@@Z")
assert fsm3.check_string("TTT")
assert fsm3.check_string("##")
assert not fsm3.check_string("abc")
assert not fsm3.check_string("aZ")

pattern4 = "a?b*c+"
fsm4 = RegexFSM(pattern4)
with open("examples/pattern4.dot", "w", encoding="utf8") as file:
    file.write(fsm4.to_graphviz())
assert fsm4.check_string("c")
assert fsm4.check_string("accc")
assert fsm4.check_string("abbbc")
assert fsm4.check_string("bcc")
assert not fsm4.check_string("a")
assert not fsm4.check_string("")
assert not fsm4.check_string("bbbaaa")
