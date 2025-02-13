from argparse import Namespace
from typing import Dict, List

from cli.command import CliCommand


class EngagementCommand(CliCommand):
    @classmethod
    @property
    def category(cls):
        return 'engagement'

    @classmethod
    def arg_specs(cls) -> Dict[str, List]:
        return {
            'list': [],
            'advance': [],
            'counterparty': [
                (['-id', '--engagement-id'], {'required': 'true'}),
                (['-n', '--name'], {'required': 'true'}),
                (['-e', '--email'], {'required': 'true'}),
                (['-a', '--address'], {'required': 'true'}),
            ],
            'close': []
        }

    def handle(self, args: Namespace):
        match args.command:
            case 'list':
                for e in self._store.list_engagements():
                    print(e)

            case 'advance':
                raise Exception

            case 'counterparty':
                print(self._store.update_engagement(args.engagement_id, args.name, args.email, args.address))

            case 'close':
                raise Exception

            case _:
                return False

        return True
