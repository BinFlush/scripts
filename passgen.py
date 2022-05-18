#!/usr/bin/env python3
import secrets
import string
import argparse
import gc
import pyperclip # remember to pip3 install pyperclip

def main():
    # Defining command line arguments
    ### TO-DO: Add option to make sure password includes every character type
    parser = argparse.ArgumentParser(description="Generate a password")
    parser.add_argument('-l', action='store_true', help="use lowercase")
    parser.add_argument('-u', action='store_true', help="use uppercase")
    parser.add_argument('-d', action='store_true', help="use numbers")
    parser.add_argument('-s', action='store_true', help="use symbols")
    parser.add_argument('-c', action='store_true', help="copy password to clipboard")
    parser.add_argument('-f', action='store_true', help="Require password to include every specified type of characters")
    parser.add_argument('-n', default=12, type=int, help="password length (default 12)")
    parser.add_argument('--charset', default="", help="custom character set 'in singlequotes'")
    args = parser.parse_args()

    # Checking how many sets of characters are to be used
    elements = count_arguments(args)
    # If none given, default to all
    if elements == 0:
        args.l = args.u = args.d = args.s = True
    elements = count_arguments(args)
    
    # Flags and key pairings, makes stuff loopable:
    pairs = [(args.l, string.ascii_lowercase), (args.u, string.ascii_uppercase), (args.d, string.digits), (args.s, string.punctuation), (bool(args.charset), args.charset)]

    # Add sets to superset
    chars = ""
    for pair in pairs:
        if pair[0]:
            chars += pair[1]

    # Deduplicate in case custom characters are entered, that already exist in superset
    chars = unique(chars)

    # Build and print actual password
    while True: 
        matches = 0
        password = ''.join(secrets.choice(chars) for i in range(args.n))
        if not args.f:
            # -f flag not set. We can exit break out already here
            break
        if args.n < elements:
            raise SyntaxError(f"password length can not be lower than amount of character types, when -f flag is specified. You need atleast {elements} characters")
        # -f flag is set. Check if all specified character types present
        for pair in pairs:
            if pair[0] == True:
                for c in pair[1]:
                    if c in password:
                        matches += 1
                        # Break in order to only register one success per character type
                        break
        if matches == elements:
            # We have all we need. Break out of while loop
            break



    if args.c:
        pyperclip.copy(password)
    else:
        print(password)

    
    # Clean up sensitive data
    del(password)
    del(chars)
    gc.collect()

def count_arguments(args) -> int:
    """ Counts valid command line arguments except -n"""
    n: int = 0
    for arg in vars(args):
        if arg in ["u", "l", "d", "s", "charset"]:
            n += bool(getattr(args, arg))
    return n


def unique(s) -> str:
    """ Just a silly function to deduplicate symbols in a string """
    st: str = ""
    length: int = len(s)
 
    for i in range(length):
        c: str = s[i]
        if c not in st:
            st += c
    return st

if __name__ == "__main__":
    main()
