1.first we have create google cloud platform new project to create api credentials 
2.And then Enable Gmail Api in the library
3. go  to credentials click create add oAuth client if you created download the file oAuth client
3. create service Account to give gmail account 
4. create app in oAuth consent screen and publish 
5. run the code u get token.json file 





# Gmail_api
A standalone Python script that integrates with Gmail API and performs some rule based operations on emails.

#### Task Details & Breakdown:
- This project is meant to be a standalone Python script, not a web server project. Use any 3rd party libraries you need for the assignment
- Authenticate to Google’s Gmail API using OAuth (use Google’s official Python client) and fetch a list of emails from your Inbox.
- Come up a database table representation and store these emails there. Use any relational database for this (Postgres / MySQL / SQLite3).
- Now that you can fetch emails, write another script that can process emails based on some rules and take some actions on them.
- These rules can be stored in a JSON file. The file should have a list of rules. Each rule has a set of conditions with an overall predicate and a set of actions.

#### Requirements for Rules:

###### Each rule has 3 properties:
- Field name (From / To / Subject / Date Received / etc)
- Predicate ( contains / not equals / less than )
- Value
A collection of Rules has one of 2 predicates - “All” or “Any”
- “All” indicates that all the given conditions must match in order to run the actions.
- “Any” indicates that at least one of the conditions must match in order to run the
conditions. Implement the following set:
Fields: From, To, Subject, Message, Received Date/Time Predicate:
- For string type fields - Contains, Does not Contain, Equals, Does not equal
- For date type field (Received) - Less than / Greater than for days / months. Actions:
- Mark as read / mark as unread
- Archive message
- Add label
