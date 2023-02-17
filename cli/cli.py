#!/usr/local/bin/python

import typer
from pathlib import Path


def main(name: str):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)