from agent.templates import PromptTemplate
from data_access.store import DataStore


class EmailAgent:
    def __init__(self, agent_name: str, store: DataStore):
        if not agent_name:
            raise Exception('Missing agent name')
        self._agent_name = agent_name
        self._store = store

    def compose(self, engagement_id: int):
        engagement = self._store.find_engagement(engagement_id)
        events = self._store.list_events(engagement)
        if not events:
            return PromptTemplate.REACHOUT.format(agent_name=self._agent_name, client_name=engagement.client.name)

        return None