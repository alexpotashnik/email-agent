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
            'receive-email': [
                (['-eid', '--engagement-id'], {'required': 'true'}),
                (['-s', '--source'], {'required': 'true', 'choices': ['client', 'counterparty']}),
                (['-e', '--email'])
            ],
            'timeout': [(['-t', '--target_event-id'], {'required': 'true'})]
        }

    def handle(self, args: Namespace):
        match args.command:
            case 'list':
                engagement = self._store.find_engagement(args.engagement_id)
                for e in self._store.list_events(engagement):
                    print(f'{e}\n')

            case 'receive-email':
                engagement = self._store.find_engagement(args.engagement_id)
                type = EventType.CUSTOMER_EMAIL if args.source == 'client' else EventType.COUNTERPARTY_EMAIL
                self._store.create_event(engagement, type, {'text': args.email})

            case 'timeout':
                event = self._store.get_event(args.target_event_id)
                self._store.create_event(event.engagement,
                                         EventType.OUTREACH_TIMEOUT,
                                         {'target_event_id': args.target_event_id})

            case _:
                return False

        return True
