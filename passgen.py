#!/usr/bin/env python3
import secrets
import string
import argparse


def main():
    # Defining command line arguments
    parser = argparse.ArgumentParser(description="Generate a password")
    parser.add_argument('-l', action='store_true', help="use lowercase")
    parser.add_argument('-u', action='store_true', help="use uppercase")
    parser.add_argument('-d', action='store_true', help="use numbers")
    parser.add_argument('-s', action='store_true', help="use symbols")
    parser.add_argument('-n', default=12, type=int, help="password length (default 12)")
    parser.add_argument('--charset', default="", help="custom character set \"in quotes\"")
    args = parser.parse_args()

    # Checking how many sets of characters are to be used
    elements = count_arguments(args)
    # If none given, default to all
    if elements == 0:
        args.l = args.u = args.d = args.s = True
    elements = count_arguments(args)

    # Add sets to superset
    chars = ""
    if args.l:    chars += string.ascii_lowercase
    if args.u:
        chars += string.ascii_uppercase
    if args.d:
        chars += string.digits
    if args.s:
        chars += string.punctuation
    if args.charset:
        chars += args.charset

    # Deduplicate in case custom characters are entered, that already exist in superset
    chars = unique(chars)

    # Build and print actual password
    password = ''.join(secrets.choice(chars) for i in range(args.n))
    print(password)

def count_arguments(args) -> int:
    """ Counts valid command line arguments except -n"""
    n: int = 0
    for arg in vars(args):
        if not arg == "n":
            n += bool(getattr(args, arg))
    return n



def unique(s) -> str:
    """ Just a silly function to deduplicate symbols in a string """
    st: str = ""
    length: int = len(s)
 
    # loop to traverse the string and
    # check for repeating chars using
    # IndexOf() method in Java
    for i in range(length):
 
        # character at i'th index of s
        c: str = s[i]
 
        # if c is present in str, it returns
        # the index of c, else it returns - 1
        # print(st.index(c))
        if c not in st:
            # adding c to str if -1 is returned
            st += c
 
    return st

if __name__ == "__main__":
    main()
