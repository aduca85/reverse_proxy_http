Reverse proxy
==================

This source code implements a layer 3 reverse proxy with a basic understanding of HTTP layer 7 protocol.
It handles only GET requests that are not bigger than 4096 bytes and for connections faster than 60 seconds.
If the request is valid it will be sent to an upstream the selection at this stage being randomly from the list provided in the config.yaml file.

Requirements
------------
Python 3.x.x

Platform
--------
Any Linux distributions available.

Usage
-----
Just run main.py from ```sources``` folder

TO DOs:
 - implement test cases
 - implement different load balancing methods
 - support other type of HTTP requests (e.g. HEAD, POST)

 Author(s)
-------------------
- Author: Andrei Duca
