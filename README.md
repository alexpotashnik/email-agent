# email-assistant

## Commands
* `client`
  * `engage`
  * `list`
* `engagment`
  * `list`
  * `advance [--preview-only]`
* `deal`
  * `explore`
  * `negotiate`
  * `close`

## Diagrams
### No Action Required
```mermaid
sequenceDiagram
  participant User
  participant CLI
  participant EngagementEngine
  participant DataStore
  participant GPT

  User->>CLI: "advance engagement"
  CLI->>EngagementEngine: "query next step"
  EngagementEngine->>DataStore: "query"
  DataStore->>EngagementEngine: "events, conversation"
  EngagementEngine->>CLI: "blocked or wait"
  CLI->>User: "no action required      
  
```

### Send Email
```mermaid
sequenceDiagram 
  participant User
  participant CLI
  participant EngagementEngine
  participant DataStore
  participant GPT

  User->>CLI: "advance engagement"
  CLI->>EngagementEngine: "query next step"
  EngagementEngine->>DataStore: "query"
  DataStore->>EngagementEngine: "events, conversation"
  EngagementEngine->>GPT: "prompt"
  EngagementEngine->>CLI: "email"
  CLI->>User: "email"

```

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

## Simplifying Assumptions
* Client is only engaged as a buyer (therefore representing one side of the deal)
* 1 deal per conversation