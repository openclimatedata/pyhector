from pyhector import emissions
from tabulate import tabulate
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("output", type=str)
args = parser.parse_args()

with open(args.output, "w") as f:
    f.write(
        tabulate(
            map(
                lambda item: ("``%s``" % item[0], ", ".join(map(lambda i: "``%s``" % i, item[1]))),
                sorted(emissions.items()),
            ),
            ["component", "emissions"],
            tablefmt="grid",
        )
    )
