#!/usr/bin/env python3

# Versatile password generator by Jákup Lützen

import secrets
import string
import argparse
import gc
import pyperclip # remember to pip3 install pyperclip

def main():
    default_length = 16
    # Defining command line arguments
    parser = argparse.ArgumentParser(description="Generate a password")
    parser.add_argument('-l', action='store_true', help="use lowercase")
    parser.add_argument('-u', action='store_true', help="use uppercase")
    parser.add_argument('-d', action='store_true', help="use digits")
    parser.add_argument('-s', action='store_true', help="use symbols")
    parser.add_argument('-c', action='store_true', help="copy password to clipboard")
    parser.add_argument('-f', action='store_true', help="Require password to include every specified type of characters")
    parser.add_argument('-n', default=default_length, type=int, help=f"password length (default {default_length})")
    parser.add_argument('--include', default="", type=str,help=" characters to include 'in singlequotes'")
    parser.add_argument('--exclude', default="", type=str, help="characters to exclude 'in singlequotes' (supersedes --include flag)")
    parser.add_argument('-r', default=1, type=int, help="'repeats', amount of passwords to be generated. (default 1)")
    
    args = parser.parse_args()

    # Checking how many sets of characters are to be used
    elements = count_arguments(args)

    # If none given, default to all
    if elements == 0:
        args.l = args.u = args.d = args.s = True
    elements = count_arguments(args)
    
    # Flags and key pairings, makes stuff loopable:
    pairs = [(args.l, string.ascii_lowercase), (args.u, string.ascii_uppercase), (args.d, string.digits), (args.s, string.punctuation), (bool(args.include), args.include)]

    # Add sets to superset (but they are lists)
    chars: list = superset(pairs)

    # Remove excluded characters
    if args.exclude:
        for c in args.exclude:
            if c in chars:
                chars.remove(c)


    # Build and print actual password / passwords
    passwords: list = []
    for _ in range(args.r):
        while True: 
            password: str = ''.join(secrets.choice(chars) for i in range(args.n))
            if not args.f:
                # -f flag not set. We can exit break out already here
                break
            if args.n < elements:
                raise SyntaxError(f"password length can not be lower than amount of character types, when -f flag is specified. You need atleast {elements} characters")
            # -f is set. Check that all types are present.
            if checktypes(pairs, password, elements):
                # We have all we need. Break out of while loop
                break
        passwords.append(password)
    

    password = "\n".join(passwords)
    if args.c:
        pyperclip.copy(password)
        print("Password copied to clipboard!")
    else:
        print(password)

    # All done. Time to clean up sensitive data
    del(passwords)
    del(password)
    del(chars)
    gc.collect()

def count_arguments(args) -> int:
    """ Counts valid command line arguments except -n"""
    n: int = 0
    for arg in vars(args):
        if arg in ["u", "l", "d", "s", "include"]:
            n += bool(getattr(args, arg))
    return n


def superset(pairs) -> list:
    """ Build list of specified character sets, and return deduplicated list """
    chars = []
    for pair in pairs:
        if pair[0]:
            chars += list(pair[1])
    # Finally, deduplicate characters before returning
    return list(set(chars))


def checktypes(pairs, this_passw, elements) -> bool:
    """ Check if all specified character types in list of tuplets are present in password"""
    matches = 0
    for pair in pairs:
        if pair[0] == True:
            for c in pair[1]:
                if c in this_passw:
                    # Increment and break in order to only register one success per character type
                    matches += 1
                    break
    if matches == elements:
        # We have all we need. Break out of while loop
        del(this_passw)
        return True
    else:
        return False


if __name__ == "__main__":
    main()
