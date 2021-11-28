import argparse
import simpleai.search as ss
import string
import math


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Creates the input string using the greedy algorithm"
    )
    parser.add_argument(
        "--input-string", dest="input_string", required=True, help="Input string"
    )
    parser.add_argument(
        "--initial-state",
        dest="initial_state",
        required=False,
        default="",
        help="Starting point for the search",
    )
    return parser


class Problem(ss.SearchProblem):
    def set_target(self, target_string):
        self.target_string = target_string

    def actions(self, cur_state):
        if len(cur_state) < len(self.target_string):
            x = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
            return list(x) + ["-" + i for i in x]
        else:
            return []

    def result(self, cur_state, action):
        if "-" in action:
            try:
                b = list(cur_state)
                b.remove(action[1])
                return "".join(b)
            except Exception as e:
                return cur_state
        return cur_state + action

    def is_goal(self, cur_state):
        return cur_state == self.target_string

    def heuristic(self, cur_state):
        # Favour states that have the same beginning as self.target_string
        r = self.target_string.find(cur_state)
        g = 0
        if r == -1:
            r = len(self.target_string) + 1
        if r > 0:
            # For states that are contained in target_string favour those with shorter lengths
            g = int(10 * (1 - math.log(1 / len(cur_state))))

        # Compute how well do the strings match character for character
        dist = sum(
            [
                1 if cur_state[i] != self.target_string[i] else 0
                for i in range(len(cur_state))
            ]
        )

        # Prefer matches when target_string is equal to cur_state in length
        diff = len(self.target_string) - len(cur_state)
        return r + diff + dist + g


if __name__ == "__main__":
    args = build_arg_parser().parse_args()

    prob = Problem()
    prob.initial_state = args.initial_state
    prob.set_target(args.input_string)

    output = ss.greedy(prob)
    print("\nTarget string:", args.input_string)
    print("\nPath to the solution:")
    for item in output.path():
        try:
            b = item[0].replace("-", "remove ")
            if not b.startswith("remove"):
                b = "add " + item[0]
            print((b, item[1]))
        except:
            print(item)
