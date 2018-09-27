from pyhector import units
from tabulate import tabulate
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("output", type=str)
args = parser.parse_args()

with open(args.output, "w") as f:
    f.write(
        tabulate(
            map(lambda item: ("``%s``" % item[0], "``%s``" % item[1]), sorted(units.items())),
            ["emissions", "unit"],
            tablefmt="grid",
        )
    )
