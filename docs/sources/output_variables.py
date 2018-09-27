from pyhector import output
from tabulate import tabulate
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("output", type=str)
args = parser.parse_args()

sorted_output = sorted(output.items(), key=output.get("component"))

with open(args.output, "w") as f:
    f.write(
        tabulate(
            map(
                lambda item: (
                    "``%s``" % item[1]["component"],
                    "``%s``" % item[1]["variable"],
                    item[1]["description"],
                    "``%s``" % item[1]["unit"],
                ),
                sorted_output,
            ),
            ["component", "variable", "description", "unit"],
            tablefmt="grid",
        )
    )
