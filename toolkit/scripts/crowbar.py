#!/usr/bin/env python3

try:
    import sys

    from crowbar.lib.main import main

except Exception as err:
    print(err, file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    main()
