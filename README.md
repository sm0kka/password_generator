# usage: pg.py [-h] [-c] [-a] [-s SET] [-m] [-v] [-t]

# Password generator

## optional arguments:
  ## -h, --help         show this help message and exit
  -c , --chars       Length of password in characters (default: 14)
  -a , --amount      Amount of passwords (default: 1)
  -s SET, --set SET  Charset for password generation
                     (d: digits, l: lowercase letters, u: uppercase letters, p: punctuation) 
                     (default: dlu)
  -m , --manual      Manual slice set of chars (default: 0)
  -v, --verbose      Show set of chars before generation (default: False)
  -t, --temporary    Generate temporary password. Ignore all other settings
                     except of -a. Example: Zyx51534 (default: False)
