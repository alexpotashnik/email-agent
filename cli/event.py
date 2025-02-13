from argparse import Namespace
from typing import Dict, List

from cli.command import CliCommand
from data_access.models import EventType


class EventCommand(CliCommand):
    @classmethod
    @property
    def category(cls):
        return 'event'

    @classmethod
    def arg_specs(cls) -> Dict[str, List]:
        return {
            'list': [
                (['-eid', '--engagement-id'], {'required': 'true'})
            ],
            'get-email': [
                (['-eid', '--engagement-id'], {'required': 'true'}),
                (['-s', '--source'], {'required': 'true', 'choices': ['client', 'counterparty']}),
                (['-e', '--email'])
            ],
            'timeout': [(['-eid', '--engagement-id'], {'required': 'true'})]
        }

    def handle(self, args: Namespace):
        engagement = self._store.find_engagement(args.engagement_id)
        match args.command:
            case 'list':
                for e in self._store.list_events(engagement):
                    print(e)

            case 'get-email':
                type = EventType.CUSTOMER_EMAIL if args.source == 'client' else EventType.COUNTERPARTY_EMAIL
                self._store.create_event(engagement, type, {'text': args.email})

            case 'timout':
                self._store.create_event(engagement, EventType.OUTREACH_TIMEOUT)

            case _:
                return False

        return True
