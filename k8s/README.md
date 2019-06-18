Reverse proxy k8s deployment
==================

This k8s chart deploys the reverse proxy and two upstreams (customized nginx servers) for testing purposes.
The connection to the upstreams is done via environment variables that reference cluster ip objects for each ustream

Requirements
------------
Helm
Docker

Platform
--------
Any Linux distributions

Usage
-----
Download the source code and run:
```
 - helm lint reverse-proxy
 - helm package reverse-proxy
 - helm install reverse-proxy
```

 Author(s)
-------------------
- Author: Andrei Duca