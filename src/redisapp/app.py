#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import string
import random

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

        # Primero se obtienen las
        zset_key = 'reviews:marketplace:{:s}'.format(marketplace)
        rids = self.redis.zrangebyscore(zset_key, fecha_ini, fecha_fin)
        # O(log(n) + m) :- n tamaño de zset y m cantidad de elementos retornados, con f <= n

        # Filtrar los rids que sean compras verificadas
        verified = [id for id in rids if self.redis.hmget('review:' + id, 'verified_purchase')[0] == 'Y']
        # f * (O(1) + C) :- con k = 1 en este caso, y retorna tamaño v <= f

        # Generar una llave aleatoria para el zset temporal
        tmpzset = 'tendencias_tmp_' + ''.join(random.choice(string.ascii_letters) for _ in range(6))

        for rid in verified:
            self.redis.zincrby(tmpzset, self.redis.hmget('review:' + rid, 'product_id'), 1)
        # Este es el término más importante !
        # Si todos los reviews son de productos diferentes
        # (log(1) + log(2) + ... + log(p)) = log(p!) <= p*log(p) con p = v

        # Si hay repetidos
        # (a1*log(1) + a2*log(2) + ... + ap*log(p)) -> con sum(ai) = v, p < v
        # Asumiendo que ap >> a_i, es decir el zset alcanza su tamaña máximo rápido
        # --> ap ~ v --> v*log(p) -> f*log(p) con p < f


        top_products = self.redis.zrange(tmpzset, 0, n, desc=True)
        # O(log(p) + N) :- N es el n que se recibe por parámetro, con N <= p

        self.redis.delete(tmpzset)
        # O(1)
        #
        # peor caso log(n) + n + n + log(n!) + log(n) + n
        # (n + 2)*log(n) + 3*n
        # O(n*log(n)) :- con n el tamaño de reviews:marketplace:<id>


        return top_products
