from agent.templates import PromptTemplate
from data_access.models import EventType, Engagement
from data_access.store import DataStore
from openai import OpenAI


class EmailAgent:
    def __init__(self,
                 agent_name: str,
                 store: DataStore,
                 openai: OpenAI,
                 openai_model: str,
                 openai_temperature: float):
        if not agent_name:
            raise Exception('Missing agent name')
        self._agent_name = agent_name
        self._store = store
        self._openai = openai
        self._openai_model = openai_model
        self._openai_temperature = openai_temperature

    def _compose(self, engagement: Engagement):
        last_event = self._store.find_last_event(engagement)
        names = {
            'agent_name': self._agent_name,
            'client_name': engagement.client.name
        }
        if not last_event:
            return PromptTemplate.REACHOUT.format(**names)

        match last_event.type:
            case EventType.COUNTERPARTY_EMAIL:
                return PromptTemplate.RESPOND_TO_COUNTERPARTY.format(**{
                    **names,
                    **{
                        'counterparty': engagement.counterparty_name,
                        'text': last_event.attributes['text']
                    }
                })
            case EventType.CUSTOMER_EMAIL:
                return PromptTemplate.RESPOND_TO_CUSTOMER.format(**{
                    **names,
                    **{'text': last_event.attributes['text']}
                })
            case EventType.OUTBOUND_EMAIL:
                return None
            case EventType.OUTREACH_TIMEOUT:
                timed_out_event = self._store.get_event(last_event.attributes['target_event_id'])
                return PromptTemplate.FOLLOWUP.format(**{
                    **names,
                    **{
                        'text': timed_out_event.attributes['text'],
                        'timeout': '1 week' # Hard coded FOR TESTING PURPOSES ONLY. Should be calculated from timestamps
                    }
                })
            case _:
                raise Exception(f'Unexpected event type: {last_event.type}')


    def compose(self, engagement_id: int, dry_run: bool = True):
        engagement = self._store.find_engagement(engagement_id)
        prompt = self._compose(engagement)
        if dry_run or not prompt:
            return prompt

        response = self._openai.chat.completions.create(
            model=self._openai_model,
            messages=[{'role': 'user', 'content': prompt}],
            temperature=self._openai_temperature
        )
        email = response.choices[0].message.content
        self._store.create_event(engagement, EventType.OUTBOUND_EMAIL, {'text': email})
        return email

