# python-lab

This repository is for lab and testing of python code. You should definitely not use any code from here in production environments. The only reason I have it up on Github is when I would like to build on an old example on a different computer.

## stat-server.py and stat-client.py

I wanted to try to use threads in Python. After a while I found that I probably wanted to test multiprocessing so I converted the code. The stat-server does absolutely nothing useful :)

Links to some of the modules used in this code:

* [threading][1] - used in the first version
* [Queue][2] - first queue
* [sqlite3][3] - used for storage
* [SimpleXMLRPCServer][4] - rpc service used on localhost to send commands and retrieve results
* [multiprocessing][5] - switched to use multiprocessing to test [Pipe][6] and to be able to look at more functionality later

On the to do list after this project is to look more thoroughly on the multiprocessing module.

 [1]: https://docs.python.org/2/library/threading.html
 [2]: https://docs.python.org/2/library/queue.html
 [3]: https://docs.python.org/2/library/sqlite3.html
 [4]: https://docs.python.org/2/library/simplexmlrpcserver.html
 [5]: https://docs.python.org/2/library/multiprocessing.html
 [6]: https://docs.python.org/2/library/multiprocessing.html#pipes-and-queues

