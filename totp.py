#!/usr/bin/env python
"""Time-based One-time Password Tool

CLI tool that generates rfc6238 TOTPs, using the native system keyring service
to store secret keys for accounts protected by two-factor authentication.

requires:
  https://pypi.org/project/onetimepass/
  https://pypi.org/project/keyring/
  https://pypi.org/project/pyperclip/
"""

from argparse import ArgumentParser
import keyring, pyperclip
import onetimepass as otp

# Use try clause to make a prompt fucntion that works with either python 2 or 3
try: prompt = raw_input
except NameError: prompt = input

# Set up argument parser
parser = ArgumentParser(description='Time-based One-time Password Generator')
parser.add_argument('-a', '--add', action='store_true',
                    help='Add an account rather than generating TOTP.')
parser.add_argument('-p', '--print-only', action='store_true',
                    help='Do not copy TOTP to clipboard.')
parser.add_argument('--service', type=str, default='otp_secret',
                    help='Keyring item name. (Default: otp_secret)')
parser.add_argument('account', type=str, help='Account to generate TOTP for.')
args = parser.parse_args()

# Get shared secret for account
secret = keyring.get_password(args.service, args.account)

# Add an account or print TOTP and copy to clipboard
if args.add:
    # If a secret already exists for the account prompt before overwriting
    add_secret = True
    if secret:
        q = "Account %s already has a shared secret. Overwrite? (Y/N) " % args.account
        a = prompt(q)
        if a and a[0].lower() != 'y': add_secret = False
        else: print("Overwriting shared secret for account %s." % args.account)
    if add_secret:
        secret = prompt("Enter shared secret key (with or without spaces): ")
        keyring.set_password(args.service, args.account, secret)
else:
    # Generate TOTP, copy to clipboard (unless --print-only) and print
    token = otp.get_totp(secret)
    args.print_only or pyperclip.copy(token)
    print("%06d" % token)
