from enum import StrEnum


class PromptTemplate(StrEnum):
    REACHOUT = ('Generate an email to a prospective client for a real estate agent. '
                'Agent\'s name is {agent_name}. Client\'s name is {client_name}. '
                'Emphasize long track record of success getting home buyers into the home of their dreams.'
                'Suggest a friendly coffee meeting to discuss I can help.')

    FOLLOWUP = ('Write a follow up email from a real estate agent to a client. '
                'Agent\'s name is {agent_name}. Client\'s name is {client_name}. '
                'Last email was written {timeout} ago and the text was {text}')
