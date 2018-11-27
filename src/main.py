#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from redisapp.app import App

def main():

    clase = App()

    print 'Hola mundo'
    for i in xrange(len(sys.argv)):
        print sys.argv[i]

if __name__ == "__main__":
    main()

