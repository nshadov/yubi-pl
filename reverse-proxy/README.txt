========[ GENERAL DESCRIPTION ]========

Simple HTTP proxy:

  * Receives request at LPORT tcp port
  * Sends request to RHOST:RPORT and receives response
  * Forwards response to active connection at LPORT


========[ HOW TO ]========

  * Start proxy:

    ./proxy.py

  * Open web browser and visit URL:

    http://localhost:8080
