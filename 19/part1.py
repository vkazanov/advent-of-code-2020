from io import StringIO
import pprint
from util import cstr, COLOR, FORMAT
from dataclasses import dataclass

# inp = open("input-test.txt")
inp = open("input.txt")

@dataclass
class Seq:
    value: list
    def __init__(self, value):
        self.value = value

@dataclass
class Alt:
    value: list
    def __init__(self, value):
        self.value = value

rules = {}

def parse(rule_line):
    idx, right = rule_line.split(": ")
    idx = int(idx)
    if " | " not in right:
        rules[idx] = Seq(parse_seq(right))
    else:
        rules[idx] = Alt([Seq(parse_seq(alt)) for alt in right.split(" | ")])

def parse_seq(seq_line):
    res = []
    for c in seq_line.split(" "):
        if c.isnumeric():
            res.append(int(c))
        else:
            res.append(c[1:-1])
    return res

for line in inp:
    line = line.strip()
    if not line: break
    # print("rule: ", line)
    parse(line)

# pprint.pp(rules)

def expand_rule(rule):
    match rule:
        case int(n):
            return expand_rule(rules[rule])
        case str(s):
            return rule
        case Seq(l):
            return Seq(list(expand_rule(r) for r in l))
        case Alt(l):
            return Alt(list(expand_rule(r) for r in l))
        case _:
            assert False
    return rule

rule = expand_rule(rules[0])
# pprint.pp(rule)

def check(line, rule, i=0):
    match rule:
        case str(r):
            return r == line[i], i + 1
        case Seq(rule_seq):
            next_i = i
            for r_i, r in enumerate(rule_seq):
                this_res, next_i = check(line, r, next_i)
                if not this_res:
                    return False, next_i
            return True, next_i
        case Alt(rule_alt):
            for r in rule_alt:
                this_res, next_i = check(line, r, i)
                if this_res:
                    return True, next_i
            return False, i
        case _:
            assert False
    return False, i

# print(check("aaa", Seq(["a", "a", "a"])))
# print(check("aaa", Seq(["a", "a", "b"])))
# print(check("aab", Seq([Seq(["a", "a"]), "b"])))
# print(check("aab", Seq([Seq(["a", "a"]), "a"])))
# print(check("abc", Seq([Alt(["a", "b"]), "b", "c"])))
# print(check("abc", Seq([Alt(["a", "b"]), "b", "d"])))
# print(check("aab", [["a", "a"], "a"]))
# print(check("baa", ["a", "a", "a"]))
# print(check("aaa", ["a", "a"]))
# print(check("aa", ["a", "a", "a"]))
# print(check("baa", [["a", "b"], "a", "a"]))
# print(check("baa", [["b", "a"], "a", "a"]))

# print(check("aba", [[["a"], ["b"]], "a", "a"]))


counter = 0
for line in inp:
    line = line.strip()
    res, l = check(line, rule)
    if res and l == len(line): counter += 1
print(counter)
assert(counter == 162)
