from enum import StrEnum


class PromptTemplate(StrEnum):
    REACHOUT = ('Write an email to a prospective client for a real estate agent. '
                'Agent\'s name is {agent_name}. Client\'s name is {client_name}. '
                'Emphasize long track record of success getting home buyers into the home of their dreams. '
                'Suggest a friendly coffee meeting to discuss I can help.')

    FOLLOWUP = ('Write a follow up email from a real estate agent to a client. '
                'Agent\'s name is {agent_name}. Client\'s name is {client_name}. '
                'Last email was written {timeout} ago and the text was {text}')

    RESPOND_TO_COUNTERPARTY = ('Write an email from a real estate agent to a client interested in buying a particular '
                               'property after receiving communication from a seller. '
                               'Agent\'s name is {agent_name}. Client\'s name is {client_name}. '
                               'Seller\'s name is {counterparty} who wrote {text}')

    RESPOND_TO_CUSTOMER = ('Write an email for a real estate agent in response to a client who wrote: {text}. '
                           'Agent\'s name is {agent_name}. Client\'s name is {client_name}.')
