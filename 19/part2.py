import pprint
from functools import lru_cache
from dataclasses import dataclass

# inp = open("input-test-2.txt")
inp = open("input-2.txt")

@dataclass(frozen=True)
class Ref:
    i: int

@dataclass(frozen=True)
class Seq:
    parts: tuple

@dataclass(frozen=True)
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

def check(line, rules):

    @lru_cache(maxsize=None)
    def run(rule, i):
        match rule:
            case str(r):
                if i < len(line) and r == line[i]:
                    return frozenset((i + 1,))
                return frozenset()

            case Seq(rule_seq):
                positions = set((i,))
                for r in rule_seq:
                    next_positions = set()
                    for next_i in positions:
                        next_positions.update(run(r, next_i))
                    positions = next_positions
                    if not positions:
                        break
                return frozenset(next_positions)

            case Alt(options):
                res_positions = set()
                for r in options:
                    next_positions = run(r, i)
                    res_positions.update(next_positions)
                return frozenset(res_positions)

            case Ref(rule_i):
                return run(rules[rule_i], i)

            case _:
                print("invalid: ", rule)
                assert False

    return len(line) in run(rules[0], 0)

counter = sum(check(line.strip(), all_rules) for line in inp)

print(counter)
assert(counter == 267)
