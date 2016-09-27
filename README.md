# Working Title

## Basics

Pass Request and Response objects up the chain until it hits the controller and
then only alter the Response, then pass back down through the middleware chain.

Plugable Routers, comes with default rails-like REST router.


## Primary Classes

### Request

Deals with basic request parsing from WSGI obj.

### Response

Deals with basic response stuff. Holds a `context` var rather than string of
content. Allowing for slightly easier parsing to response types; so output
requires parsers; anticipating basic of: JSON, HTML (via a template parsers
like Jinja) maybe through xml/msgpack for kicks.

### Router

Plugable routers, requires a lot more work than is currently in there.
An interface with the methods: `add` & `get_route`. From there, do what you
like.

Really the url parsing needs to be better than it is.


## Other Stuff

### Middleware

### Context Parsers

### Handlers
