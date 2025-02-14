from argparse import Namespace
from typing import Dict, List

from cli.command import CliCommand
from data_access.models import EventType


class ClientCommand(CliCommand):
    @classmethod
    @property
    def category(cls) -> str:
        return 'client'

    @classmethod
    def arg_specs(cls) -> Dict[str, List]:
        return {
            'list': [],
            'engage': [
                (['-n', '--name'], {'required': 'true'}),
                (['-a', '--email_address'], {'required': 'true'}),
                (['-b', '--bound'], {'required': 'true', 'choices': ['in', 'out']}),
                (['-e', '--email'])
            ]
        }

    def handle(self, args: Namespace):
        match args.command:
            case 'list':
                for c in self._store.list_clients():
                    print(c)

            case 'engage':
                if args.bound == 'in'and not args.email:
                    raise Exception('Email is required for inbound engagements')

                client = self._store.create_client(args.name, args.email_address)
                engagement = self._store.create_engagement(client)
                result = str(engagement)
                if args.bound == 'in':
                    self._store.create_event(engagement,
                                             EventType.CUSTOMER_EMAIL,
                                             {'text': args.email})
                print(result)

            case _:
                return False

        return True
