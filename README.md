# email-assistant

## Simplifying Assumptions
* Client is only engaged as a buyer (therefore representing one side of the deal)
* 1 deal per conversation

## Commands
* `client`
  * `engage`
  * `list`
* `engagement`
  * `list`
  * `advance [--preview-only]`
* `deal`
  * `explore`
  * `negotiate`
  * `close`

## Diagrams
### Persistence
```mermaid
classDiagram
    class Client {
        -name: string
        +engage()
    }
        
    class Conversation {
        -attributes: json
        -timestamp: datetime
        +follow_up()
    }
    
    class Deal {
        -address: varchar
        -status: varchar
        +initiate()
        +negotiate()
        +close()
    }
    
    class Engagement {
        -buyer_id: integer
        -counterparty: varchar
        +<<static>> list(status)
        +advance(preview_only: bool)
    }
    
    class Event {
        -deal_id: integer
        -attributes: json
        -timestamp: datetime
    }
    
    class PromptTemplate {
        -text: varchar
    }

    Client "1" -- "0..*" Conversation
    Engagement "1" -- "1" Client : "buyer"
    Engagement "1" -- "0..*" Deal
    Deal "1" -- "0..*" Event 
```

### No Action Required
```mermaid
sequenceDiagram
  participant User
  participant CLI
  participant EmailAgent
  participant DataStore
  participant GPT

  User->>CLI: "advance engagement"
  CLI->>EmailAgent: "query next step"
  EmailAgent->>DataStore: "query"
  DataStore->>EmailAgent: "events, conversation"
  EmailAgent->>CLI: "blocked or wait"
  CLI->>User: "no action required      
  
```

### Send Email
```mermaid
sequenceDiagram 
  participant User
  participant CLI
  participant EmailAgent
  participant DataStore
  participant GPT

  User->>CLI: "advance engagement"
  CLI->>EmailAgent: "query next step"
  EmailAgent->>DataStore: "query"
  DataStore->>EmailAgent: "events, conversation"
  EmailAgent->>GPT: "prompt"
  EmailAgent->>CLI: "email"
  CLI->>User: "email"

```

## Sample conversations
* "Deal-less"
  * Provide market analysis (general)
  * Reply to an engagement request (inbound)
  * Reach out to prospect (outbound)
  * First meeting (introduce set of potential deals)
* Explore a potential deal
  * Local market analysis
  * More information about the property
  * Sway toward purchase
* Negotiation
  * Price-based
  * Property history
  * Requests to fix
  * Bidding war
* Closing
  * Facilitating funds transfer
  * Taking possession
  * Celebration