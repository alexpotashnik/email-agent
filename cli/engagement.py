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
            'compose': [
                (['-id', '--engagement-id'], {'required': 'true'}),
                (['--dry-run'], {
                    'action': 'store_true',
                    'default': False,
                    'help': 'The call to OpenAI is not be made, only the prompt is displayed, and the system will not '
                            'consider the email as having been sent.'
                })
            ],
            'counterparty': [
                (['-id', '--engagement-id'], {'required': 'true'}),
                (['-n', '--name'], {'required': 'true'}),
                (['-e', '--email'], {'required': 'true'}),
                (['-a', '--address'], {'required': 'true'}),
            ]
        }

    def handle(self, args: Namespace):
        match args.command:
            case 'list':
                for e in self._store.list_engagements():
                    print(e)

            case 'compose':
                if response := self._email_agent.compose(args.engagement_id, args.dry_run):
                    print(response)
                else:
                    print('No communication recommended at this time.')

            case 'counterparty':
                print(self._store.update_engagement(args.engagement_id, args.name, args.email, args.address))

            case _:
                return False

        return True
