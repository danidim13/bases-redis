#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import random
import time
import exceptions
from app import App
import numpy as np

class Tester(object):
    r"""Clase para probar los tiempos de la apliación.

    Recibe como parámetro una instancia de App()

    Args:
        app (App, optional): Instancia de la aplicación, si no se proporciona
            crea una con valores default.
    """

    def __init__(self, app=None):
        if app is None:
            self.app = App()
        else:
            self.app = app

    def test_function(self, repetitions, func_name, *args, **kwargs):
        r"""Funcion de utilidad para correr pruebas sobre una función.

        Las pruebas se corren sobre self.app.<func_name>

        Args:
            repetitions (int): Cantidad de repeticiones para la prueba.
            func_name (string): Nombre de la función que se va a probar.

        Returns:
            np.array: Retorna un arreglo con el tiempo que tomó cada repetición.

        Example:
            >>> probador = Tester()
            >>> resultado = probador.tests_function(100, 'tendencias_v1', marketplace='FR', n=5, fecha_ini=13000, fecha_fin=14000)
        """

        func = None
        try:
            func = getattr(self.app, func_name)
        except Exception as e:
            print "No existe el método " + func_name
            raise e


        loop_iter = 1
        loop_time = None
        while True:
            start = time.clock()
            for i in xrange(loop_iter): func(*args, **kwargs)
            end = time.clock()

            loop_time = end-start
            if loop_time < 0.2:
                loop_iter = loop_iter*5
            else:
                break;

        print "Using {:d} loop_iter".format(loop_iter)

        # imprimir un mensaje informativo cada 15 segundos
        update_freq = 15.0
        approx_loops_mod = int( update_freq * loop_iter / loop_time)

        results = np.zeros(repetitions)
        for j in xrange(repetitions):

            start = time.clock()
            for i in xrange(loop_iter): self.app.tendencias_v1(*args, **kwargs)
            end = time.clock()
            total = (end - start)/loop_iter

            results[j] = total

            if j%approx_loops_mod == 0:
                print 'Repeticion {:d}...'.format(j)

        min = np.min(results)
        avg = np.mean(results)
        max = np.max(results)
        print 'Mínimo: {:f}, promedio: {:f}, máximo: {:f}'.format(min, avg, max)
        return results
