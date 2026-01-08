import pprint
from functools import lru_cache
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
    for c in seq_line.split():
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

def check(line, rules):

    def match_node(node, i):
        match node:
            case str(c):
                return frozenset((i + 1,)) if i < len(line) and c == line[i] else frozenset()

            case Seq(rule_seq):
                positions = {i}
                for r in rule_seq:
                    positions = {p2 for p in positions for p2 in match_node(r, p)}
                    if not positions:
                        break
                return frozenset(positions)

            case Alt(options):
                return frozenset(p2 for opt in options for p2 in match_node(opt, i))

            case Ref(rule_i):
                return match_rule(rule_i, i)

            case _:
                raise TypeError(f"Invalid rule: {node!r}")

    @lru_cache(maxsize=None)
    def match_rule(rule_i, i):
        return match_node(rules[rule_i], i)

    return len(line) in match_rule(0, 0)

counter = sum(check(line.strip(), all_rules) for line in inp)

print(counter)
assert(counter == 267)
