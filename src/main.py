#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from redisapp.app import App
from redisapp.tester import Tester

def main():

    aplicacion = App()
    tester = Tester(aplicacion)

    print 'prueba para 100 repeticiones de tendencias_v1'

    tester.test_tendencias_rango(60, 200, 50)

if __name__ == "__main__":
    main()
