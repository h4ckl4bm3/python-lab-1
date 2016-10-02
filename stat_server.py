#!/usr/local/bin/python
"""Script to test out python functionality."""
import os
import os.path
import sqlite3

from SimpleXMLRPCServer import SimpleXMLRPCServer
from multiprocessing import JoinableQueue as Queue
from multiprocessing import Process
from multiprocessing import Pipe

FILE_LIST = Queue()
STAT_LIST = Queue()
PATH_LIST = Queue()
COMMAND_LIST = Queue()

def stat_files():
    """Worker function."""
    while True:
        try:
            filename = FILE_LIST.get()
            statinfo = os.stat(filename) # When you don't know what to do stat :)
            values = (filename, statinfo[0])
            STAT_LIST.put(values)
            FILE_LIST.task_done()
        except KeyboardInterrupt:
            break

def database(connection):
    """Master function for the database."""
    # Setup database and clean if it exist already
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()
    try:
        cur.execute('''CREATE TABLE files (nr int, name text, info text)''')
    except sqlite3.Error:
        cur.execute('''DELETE FROM files''')
        cur.execute('''VACUUM''')
    conn.commit()

    i = 0
    while True:
        try:
            if not STAT_LIST.empty():
                filename, statinfo = STAT_LIST.get()
                try:
                    val = (i, unicode(filename), statinfo,)
                    cur.execute("INSERT INTO files VALUES (?, ?, ?)", val)
                    conn.commit()
                except sqlite3.Error:
                    pass
                STAT_LIST.task_done()
                i = i + 1
            if not COMMAND_LIST.empty():
                COMMAND_LIST.get()
                cur.execute('''SELECT COUNT(*) FROM files''')
                connection.send(cur.fetchone()[0])
                conn.commit()
                COMMAND_LIST.task_done()
        except KeyboardInterrupt:
            conn.close()

def file_finder():
    """Get path from separate client."""
    while True:
        try:
            path = PATH_LIST.get()
            for root, _, files in os.walk(path):
                for fname in files:
                    path = os.path.join(root, fname)
                    if os.path.isfile(path):
                        FILE_LIST.put(path)
            PATH_LIST.task_done()
        except KeyboardInterrupt:
            break

def add_path(path):
    """Add path to queue for getting stat info."""
    PATH_LIST.put(str(path))
    return "Added " + path

def server_status(command):
    """Retrive status after question from xmlrpc."""
    COMMAND_LIST.put(str(command))
    return  PARENT_CONN.recv()

# Global variables
PARENT_CONN, CHILD_CONN = Pipe()

def main():
    """Main function."""
    # Start stat workers
    i = 0
    while i < 10:
        stat_worker = Process(target=stat_files)
        stat_worker.daemon = True
        stat_worker.start()
        i = i + 1

    # Start database process
    db_worker = Process(target=database, args=(CHILD_CONN,))
    db_worker.daemon = True
    db_worker.start()

    # Start path process
    path_worker = Process(target=file_finder)
    path_worker.daemon = True
    path_worker.start()

    # Start and run an xmlrpc server in main
    server = SimpleXMLRPCServer(("localhost", 8000), logRequests=False)
    server.register_function(add_path, "add_path")
    server.register_function(server_status, "server_status")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
