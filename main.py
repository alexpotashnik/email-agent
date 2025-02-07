import os
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime

from os import getenv
from dotenv import load_dotenv

from typing import List, Type, Dict

from cli.command import CommandCategoryType, DealsCommand, EnvironmentCommand
from data_access.store import DataStore


def parse_args(argv: List[str], specs: Dict) -> Namespace:
    def get_usage(first, second=None):
        return f'{os.path.basename(__file__)} {first}{f' {second}' if second else ''}'

    if len(argv) == 0 or argv[0] not in specs:
        print('Available commands:')
        for category in specs:
            print('\t' + get_usage(category))
        exit(1)
    category = argv[0]

    if len(argv) == 1 or argv[1] not in specs[category]:
        print('Available commands:')
        for com in specs[category]:
            print('\t' + get_usage(category, com))
        exit(1)
    command = argv[1]

    parser = ArgumentParser()
    parsed = parser.parse_args(argv[2:])
    parsed.command_category = category
    parsed.command = command
    return parsed


def main():
    load_dotenv()

    # TODO: get automatically by reflection, but preserve order
    categories: List[Type[CommandCategoryType]] = [
        EnvironmentCommand, DealsCommand
    ]

    store_path = getenv('STORE_PATH')
    stores = DataStore(f'sqlite+pysqlite:///{store_path}')
    args = parse_args(sys.argv[1:], {c.category: c.arg_specs() for c in categories})
    for command in [c(stores, args) for c in categories]:
        if args.command_category == command.category:
            start = datetime.now()
            if command.handle(args):
                print(f'\n{datetime.now() - start}')
                return
            break

    print(f'Unhandled command: {args.command_category} {args.command}')
    exit(1)


if __name__ == '__main__':
    load_dotenv()
    main()
