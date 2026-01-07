from io import StringIO
import pprint
from util import cstr, COLOR, FORMAT
from dataclasses import dataclass

# inp = open("input-test-2.txt")
inp = open("input-2.txt")

@dataclass
class Rule:
    value: int
    def __init__(self, value):
        self.value = value

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

all_rules = {}

def parse(rule_line):
    idx, right = rule_line.split(": ")
    idx = int(idx)
    if " | " not in right:
        all_rules[idx] = Seq(parse_seq(right))
    else:
        all_rules[idx] = Alt([Seq(parse_seq(alt)) for alt in right.split(" | ")])

def parse_seq(seq_line):
    res = []
    for c in seq_line.split(" "):
        if c.isnumeric():
            res.append(Rule(int(c)))
        else:
            res.append(c[1:-1])
    return res

for line in inp:
    line = line.strip()
    if not line: break
    parse(line)

def check(line, rule, i, rules):
    match rule:
        case str(r):
            if i < len(line) and r == line[i]:
                return True, [i + 1]
            else:
                return False, [i]

        case Seq(rule_seq):
            iss = [i]
            for r in rule_seq:
                if not iss:
                    return False, [i]
                next_iss = []
                for next_i in iss:
                    this_res, this_iss = check(line, r, next_i, rules)
                    if this_res:
                        next_iss.extend(this_iss)
                iss = next_iss
            return True, next_iss

        case Alt(rule_alt):
            res_iss = []
            for r in rule_alt:
                this_res, next_iss = check(line, r, i, rules)
                if this_res:
                    res_iss.extend(next_iss)
            if res_iss:
                return True, res_iss
            else:
                return False, [i]

        case Rule(rule_i):
            this_res, next_iss = check(line, rules[rule_i], i, rules)
            if this_res:
                return True, next_iss
            return False, [i]

        case _:
            print("invalid: ", rule)
            assert False

counter = 0
for line in inp:
    line = line.strip()
    res, iss = check(line, all_rules[0], 0, all_rules)
    if res and any(i == len(line) for i in iss):
        counter += 1

print(counter)
assert(counter == 267)
