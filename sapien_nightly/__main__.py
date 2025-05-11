import argparse

from sapien_nightly.install import install


def main():
    parser = argparse.ArgumentParser(
        prog="sapien-nightly", description="SAPIEN Nightly Release Installer"
    )
    subparsers = parser.add_subparsers()
    parser_install = subparsers.add_parser(
        "install", help="Install SAPIEN Nightly Release"
    )
    parser_install.set_defaults(func=install)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
