"""
Solve the puzzle below:
    Five people where eating apples, A finished before B, but behind C.
    D Finished before E but, behind B. What was the finishing order.
"""

from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)


def constraint_behind(variables, values):
    return values[0] > values[1]


def constraint_before(variables, values):
    return values[0] < values[1]


if __name__ == "__main__":
    variables = ("A", "B", "C", "D", "E")
    domains = {i: list(range(len(variables))) for i in variables}

    constraints = [
        (("A", "B"), constraint_before),
        (("A", "C"), constraint_behind),
        (("D", "E"), constraint_before),
        (("D", "B"), constraint_behind),
    ]

    problem = CspProblem(variables, domains, constraints)
    soln = backtrack(problem)
    soln = sorted(list(soln.items()), key=lambda x: x[1])
    soln = "".join([i[0] for i in soln])
    print("\nSolutions:\n\nNormal:", soln)
