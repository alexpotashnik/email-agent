import os
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime

from os import getenv
from dotenv import load_dotenv

from typing import List, Type, Dict, Tuple

from agent.email_agent import EmailAgent
from cli.command import CommandCategoryType
from cli.client import ClientCommand
from cli.engagement import EngagementCommand
from cli.environment import EnvironmentCommand
from cli.event import EventCommand
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

    args_parser = ArgumentParser(prog=get_usage(category, command))

    def create_arg(target, spec):
        target.add_argument(
            *(spec[0] if isinstance(spec, Tuple) else spec),
            **(spec[1] if isinstance(spec, Tuple) and len(spec) > 1 else {}))

    for arg_spec in specs[category][command]:
        if len(arg_spec) > 1 and all([isinstance(item, Tuple) for item in arg_spec]):
            group = args_parser.add_mutually_exclusive_group(required=True)
            for group_member_spec in arg_spec:
                create_arg(group, group_member_spec)
        else:
            create_arg(args_parser, arg_spec)

    parsed = args_parser.parse_args(argv[2:])
    parsed.command_category = category
    parsed.command = command
    return parsed


def main():
    load_dotenv()

    # TODO: get automatically by reflection, but preserve order
    categories: List[Type[CommandCategoryType]] = [
        ClientCommand, EngagementCommand, EnvironmentCommand, EventCommand
    ]

    store_path = getenv('STORE_PATH')
    agent_name = getenv('AGENT_NAME')
    with DataStore.get(f'sqlite+pysqlite:///{store_path}') as store:
        email_agent = EmailAgent(agent_name, store)
        args = parse_args(sys.argv[1:], {c.category: c.arg_specs() for c in categories})
        for command in [c(store, email_agent, args) for c in categories]:
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
