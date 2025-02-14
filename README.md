# email-assistant

## Simplifying Assumptions
* Client is only engaged as a buyer (therefore representing one side of the deal)
* 1 deal per conversation

## Commands
* `environment`
  * `reset`
* `client`
  * `list`
  * `engage`
* `engagement`
  * `list`
  * `compose [--dry-run]`
  * `counterparty`
* `event`
  * `list`
  * `receive-email`
  * `timeout`

## Diagrams
### Persistence
```mermaid
classDiagram
    class Client {
        -name: string
        -email: string
    }
        
    class Engagement {
        -client_id: integer
        -counterparty_name: varchar?
        -counterparty_email: varchar?
        -property_address: varchar?
    }
    
    class EventType {
        <<enumeration>>
        OUTBOUND_EMAIL
        CUSTOMER_EMAIL
        COUNTERPARTY_EMAIL
        OUTREACH_TIMEOUT
    }
    
    class Event {
        -engagment_id: integer
        -attributes: json
        -type: EventType
        -timestamp: datetime
    }

    Engagement "1" -- "1" Client : "buyer"
    Engagement "1" -- "0..*" Event 
    EventType -- Event
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

## Samples of exchanges that inspired the design
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