#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis

class App(object):
    r""" Clase que implementa la lógica de la aplicación.

    Args:
        r (Redis, optional): Objeto para conectarse a la base de datos, si
            no se brinda se conecta a localhost en el puerto 6379.
    """

    def __init__(self, r=None):

        if r is None:
            r = redis.Redis(host='localhost', port=6379)

        self.redis = r

    def tendencias_v1(self, marketplace, n, fecha_ini, fecha_fin=None):
        r""" Consulta productos con mejores ventas.
        Consulta los n productos con mejor ventas y reviews en una localidad
        específica durante un intervalo de tiempo dado.

        Args:
            marketplace (string): Código de país para la tienda.
            fecha_ini (string): Timestamp fecha inicial a partir de la cual
                contar las ventas.
            fechan_fin (string, optional): Timestamp fecha final para contar las
                ventas. Por defecto se usa la fecha del servidor.
            n (int): Cantidad de productos a incluir en la lista.
        """
        pass
