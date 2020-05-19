# License
*This is Project 3 of CNI course in Department of Software Engineering, School of Infomatics, Xiamen University.*  
## Protocol
### Client
```
PURC:[username]:[password]:[userNum] # Purchase license
HELO:[license]                       # Say hello
CKAL:								 # Check alive
RELS:[license]:[ticket]              # Release ticket
```
### Server
```
PERM:[license]                       # Permit license request
FAIL:[info]                          # Fail to give a license
WELC:[ticket]                        # Give a ticket
RFUS:[info]                          # Refuse to give a ticket
UKNW:[info]                          # Cannot recognize the request
GOOD:								 # Permit the alive check
WARN:[info]                          # Receive an unused ticket from client
GBYE:[info]                          # Say goodbye to client
```
