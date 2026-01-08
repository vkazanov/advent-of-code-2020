import pprint
from dataclasses import dataclass

# inp = open("input-test-2.txt")
inp = open("input-2.txt")

@dataclass
class Ref:
    i: int

@dataclass
class Seq:
    parts: tuple

@dataclass
class Alt:
    options: tuple

def parse_rule(rules, rule_line):
    idx, right = rule_line.split(": ")
    idx = int(idx)
    if " | " not in right:
        rules[idx] = parse_seq(right)
    else:
        rules[idx] = Alt(tuple(parse_seq(option) for option in right.split(" | ")))

def parse_seq(seq_line):
    parts = []
    for c in seq_line.split(" "):
        if c.isdigit():
            parts.append(Ref(int(c)))
        else:
            parts.append(c.strip('"'))
    return Seq(tuple(parts))

all_rules = {}
for line in inp:
    line = line.strip()
    if not line: break
    parse_rule(all_rules, line)

def check(line, rule, i, rules):
    match rule:
        case str(r):
            if i < len(line) and r == line[i]:
                return [i + 1]
            return []

        case Seq(rule_seq):
            positions = [i]
            for r in rule_seq:
                next_positions = []
                for next_i in positions:
                    next_positions.extend(check(line, r, next_i, rules))
                positions = next_positions
                if not positions:
                    break
            return next_positions

        case Alt(options):
            res_positions = []
            for r in options:
                next_positions = check(line, r, i, rules)
                res_positions.extend(next_positions)
            return res_positions

        case Ref(rule_i):
            return check(line, rules[rule_i], i, rules)

        case _:
            print("invalid: ", rule)
            assert False

counter = 0
for line in inp:
    line = line.strip()
    if any(i == len(line) for i in check(line, all_rules[0], 0, all_rules)):
        counter += 1

print(counter)
assert(counter == 267)
