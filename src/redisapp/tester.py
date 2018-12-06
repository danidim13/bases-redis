#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import random
import time
import exceptions
import csv
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
        return avg

    def test_tendencias_rango(self, n_total, start_size, step):
        r"""Probar consulta de tendencias para rangos de diferente tamaño
        """

        repeat = 50

        arr = np.zeros((n_total, 2))

        market = 'UK'
        key = 'reviews:marketplace:' + market

        filename = 'prueba_tend_2.csv'

        total_elem = self.app.redis.zcard(key)

        for n in xrange(n_total):
            start_elem = random.randint(0, total_elem/4)
            start_date = self.app.redis.zrange(key, start_elem, start_elem, withscores=True)[0][1]

            end_elem = start_elem + n*step + start_size

            if end_elem >= total_elem:
                print "No hay suficientes elementos!"
                print start_elem, end_elem
                raise Exception

            end_date = self.app.redis.zrange(key, end_elem, end_elem, withscores=True)[0][1]

            size = self.app.redis.zcount(key, start_date, end_date)
            time = self.test_function(repeat, 'tendencias_v1', marketplace=market, n='5', fecha_ini=start_date, fecha_fin=end_date)

            arr[n, 0] = size
            arr[n, 1] = time

        print "Pruebas terminadas para n = " + str(n_total)

        with open(filename, 'w') as csv_file:

            writer = csv.writer(csv_file)
            writer.writerow(['tamaño', 'tiempo (s)'])
            for n in xrange(n_total):
                writer.writerow(arr[n, :].tolist())

        print "Prueba finalizada!"
