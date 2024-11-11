Basic Authentication
--------------------

How to use Basic Authentication in a REST API

## What is Basic Authentication?

Basic Authentication is a simple authentication scheme built into the HTTP protocol. The client sends HTTP requests with the Authorization header that contains the word Basic word followed by a space and a base64-encoded string username:password. For example, to authorize as demo / p@55w0rd the client would send the following header:

```
