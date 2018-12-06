#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from redisapp.app import App
from redisapp.tester import Tester

def main():

    aplicacion = App()
    tester = Tester(aplicacion)

    print 'prueba para 100 repeticiones de tendencias_v1'

    tester.test_function(50, 'tendencias_v1', marketplace='FR', n='5', fecha_ini=13000, fecha_fin=15000)

if __name__ == "__main__":
    main()
