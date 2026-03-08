# TCP-SecureChat (DevSecOps Build)

## Phase 1 - TCP Chatroom (Foundation)

This is the first working iteration of the multi-threaded TCP chatroom. Messages currently travel in cleartext, which will be audited in Phase 2. 

### Overview Screenshot
![All terminals](screenshots/phase1_all_terminals.png)

Status: First iteration stable, all bugs fixed (threading, username encoding, socket reuse).  

Next step: Phase 2 — Build a packet sniffer to intercept TCP messages.