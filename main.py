#!/usr/bin/env python3

import math
import random
import sys
import time


def main(program_name, *args):
    min_int = 0
    max_int = 255
    reprs = []
    bases = []

    # Parse arguments
    for arg in args:
        if arg == "-h" or arg == "--help":
            print("\n".join([
                f"{program_name} <min>-<max> <ident1>:<base> <ident2>:<base2> ...",
                "",
                "   Quiz student on numeric representation conversions",
                "   between <base1> and <base2>, etc., identified by the ",
                "   identifiers <ident1> <ident2>, etc., for numbers ranging",
                "   from <min> to <max>, where '<min>-<max>' is optional."
                "",
                "   Requires at least 2 bases.",
                "",
                "   Default:",
                f"       {program_name} 0-255 dig:10 hex:16 bin:2",
                "",
                f"{program_name} -h|--help",
                "",
                "   Display this help message."]))
            return
        invalid_arg_error = \
            ValueError(
                f"Invalid argument '{arg}'! Expected '<ident>:<base>' or '<min>-<max>'"
                "where <base>, <min> and <max> are integers.")
        if ":" in arg:
            repr, base_string = arg.split(':', maxsplit=1)
            try:
                base = int(base_string)
            except ValueError as e:
                raise invalid_arg_error from e
            reprs.append(repr)
            bases.append(base)
        elif "-" in arg:
            min_int_str, max_int_str = arg.split('-', maxsplit=1)
            try:
                min_int = int(min_int_str)
                max_int = int(max_int_str)
            except ValueError as e:
                raise invalid_arg_error from e
        else:
            raise invalid_arg_error

    if not reprs:
        reprs = ["dig", "hex", "bin"]
        bases = [  10 ,   16 ,    2 ]

    col_widths = [
        max(math.ceil(math.log(max_int, base)), len(repr))
        for repr, base in zip(reprs, bases)]

    rounds = 0
    correct = 0
    incorrect = 0
    avg_round_secs = 0

    # Print commands with default args shown
    print(f"{program_name} {min_int}-{max_int} "
        f"{' '.join(f'{repr}:{base}' for repr, base in zip(reprs, bases))}")
    print()
    print("Fill in the blanks!")
    while True:
        try:
            num = random.randint(min_int, max_int)
            filled = reprs[random.randint(0, len(reprs) - 1)]
            answers = []

            headers_line = ""
            values_line = ""
            for repr, base, col_width in zip(reprs, bases, col_widths):
                headers_line += repr.rjust(col_width) + " "

                # Create the answer string
                answer = ""
                x = num
                while x > 0:
                    x, digit = divmod(x, base)
                    answer = "0123456789ABCDEF"[digit] + answer
                answers.append(answer)

                # Fill the answer if randomly chosen to be filled;
                # otherwise leave blank
                if repr == filled:
                    values_line += answer.rjust(col_width) + " "
                else:
                    values_line += " "*(col_width - 1) + "- "

            print(headers_line)
            print(values_line)

            t0 = time.time()
            for repr, answer in zip(reprs, answers):
                if repr != filled:
                    prompt = f"{repr}> "
                    while input(prompt).strip().lstrip('0').upper() != answer:
                        print(len(prompt)*" " + "Incorrect :(")
                        incorrect += 1
                        rounds += 1
                    print(len(prompt)*" " + "Correct   :)")
                    correct += 1
                    rounds += 1
            avg_round_secs = \
                (avg_round_secs*(rounds - 1) + (time.time() - t0))/rounds
            print()
            print(f"Correct: {100*correct/(correct + incorrect):>3.2f}%"
                  f"\tAvg. Round Time: {round(avg_round_secs)}s")
            print()

        except KeyboardInterrupt:
            exit(0)


if __name__ == "__main__":
    main(*sys.argv)

