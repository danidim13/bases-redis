#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import string
import random
import time

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

    def set_average(self):
        products = self.redis.hgetall('reviews.by.product')
        cont = 0

        for product_id, reviews_id in products.iteritems():
            #print
            #"El product_id es {:s}".format(product_id)

            array = reviews_id.split(" ")
            total_reviews = len(array)
            #print
            #"El total de review_id es {:d}".format(total_reviews)

            for i in array:
            #    print
            #    "El review_id es {:s}".format(i)
                cont += float(self.redis.hmget('star.rating.by.review', i)[0])

            average = cont / total_reviews

           # print
           # "El average es {:f}\n".format(average)
            self.redis.zadd('products.by.average', product_id, average)

            if self.redis.hexists('products.by.average.hash', average):
                existent_product = self.redis.hmget('products.by.average.hash', average)
                existent_product[0] = existent_product[0] + ' ' + product_id
                self.redis.hset('products.by.average.hash', average, existent_product[0])
            else:
                self.redis.hset('products.by.average.hash', average, product_id)

            cont = 0

    def get_average_from_zset(self, n):
        products = self.redis.zrevrange('products.by.average', 0, n)

       # print "Los {:s} mejores promedios son: ".format(str(n))

        for i in products:
            title = self.redis.hmget('product.title.by.product.id', i)
           # print title[0]


    def get_average_from_zset(self, n):
        products = self.redis.zrevrange('products.by.average', 0, n)

       # print "Los {:s} mejores promedios son: ".format(str(n))

        for i in products:
            title = self.redis.hmget('product.title.by.product.id', i)
           # print title[0]

    def get_average_from_hash(self,n):
       # print "Los {:s} mejores promedios son: ".format(str(n))

        averages = self.redis.hkeys('products.by.average.hash')
        cont = 0
        for i in averages:
            products = self.redis.hmget('products.by.average.hash', i)[0].split(' ')
            for j in products:
                if(cont < n):
                    title = self.redis.hmget('product.title.by.product.id', j)
                  #  print title[0]

                    cont += 1
                    continue
                else:
                    break

    def run_querys(self):
        cont = 0

        for i in range(100, 201):
            start_time = time.time()
            self.get_average_from_zset(i)
            cont += time.time() - start_time

        print "Tiempo de duración zset {:f}".format((cont/100)*100)

        cont = 0

        for i in range(100, 201):
            start_time = time.time()
            self.get_average_from_hash(i)
            cont += time.time() - start_time

        print "Tiempo de duración hash {:f}".format((cont/100)*100)