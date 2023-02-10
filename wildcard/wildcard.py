#!/usr/bin/env python3

# A function which does wildcard matching with ? and *
# on a string.

# Checks whether a pattern string is empty or all stars.
def all_stars_or_empty(s):
    if s == "":
        return True

    if s[0] == "*":
        return all_stars_or_empty(s[1:])

    return False


# Performs a wildcard match.
def match(pattern, s, debug=False):
    if debug:
        print(f"MATCH pattern: {pattern} string: {s}")

    while s and pattern:
        # We always consume a character from the pattern.
        pat_char = pattern[0]
        pattern = pattern[1:]
        if pat_char == "?" or pat_char == s[0]:
            if debug:
                print(f"ONE {pat_char} ~= {s[0]}")

            # Either the pattern is a "match any" (?) or the
            # pattern character matches the string character.
            # If this is the case we consume a character from
            # the string.
            s = s[1:]
        elif pat_char == "*":
            # Star wild card.
            # If pattern is empty then the last character in the pattern
            # was a star and we have a match.
            if pattern == "":
                return True

            # Otherwise we are going to continue to consume characters
            # from the string and then see if we can make the rest
            # match.
            t = s

            while t:
                if match(pattern, t, debug):
                    return True
                t = t[1:]

            # If we get here there is no way we can make the rest of
            # the string match, and we can confidently declare a
            # failure.
            return False
        else:
            # pattern[0] != s[0]: No match.
            return False

    if debug:
        print(f"END WHILE pattern: {pattern} string: {s}")

    # Pattern exhausted but string not exhausted: No match.
    if pattern == "":
        return s == ""

    # String exhausted and maybe pattern exhausted.
    # If the pattern left is a star, we are good.
    # If the pattern is not exhausted, we do not have a match.
    return all_stars_or_empty(pattern)


def tester(pattern, s, expect, debug=False):
    m = match(pattern, s, debug)
    r = "OK" if expect == m else "FAIL"
    print(f"{r} pattern: {pattern} string: {s} match: {m} expect: {expect}")


def main():
    tester("aap", "aap", True)
    tester("aap", "banana", False)
    tester("?ap", "aap", True)
    tester("?a?", "aap", True)
    tester("???", "aap", True)
    tester("????", "aap", False)
    tester("aap*", "aap", True)
    tester("*aap", "aap", True)
    tester("*aap*", "aap", True)
    tester("a?", "aap", False)
    tester("a??", "aap", True)
    tester("a*", "aap", True)
    tester("a**", "aap", True)
    tester("a***", "aap", True)
    tester("a*", "bap", False)
    tester("a*p", "aap", True)
    tester("a**p", "aap", True)
    tester("a*m?o*z", "abcdefghijklmnopqrstuvwxyz", True)
    tester("a*****?*****z", "abcdefghijklmnopqrstuvwxyz", True)


if __name__ == '__main__':
    main()
