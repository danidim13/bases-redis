#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import redis
import string
import csv


csv.register_dialect('athena', delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)


def procesar_csv(file, host='localhost', port=6379):

    con = redis.Redis(host, port)
    csv_reader = csv.DictReader(file, dialect='athena')
    count = 0

    for tupla in csv_reader:

        review_id = tupla.pop('review_id')

        con.hmset('review:' + review_id, tupla)
        
        product_id = tupla.pop('product_id')
        product_title = tupla.pop('product_title')
        star_rating = tupla.pop('star_rating')

        con.zadd('reviews:marketplace:' + tupla['marketplace'], review_id, float(tupla['review_date']))

        if con.hexists("reviews.by.product", product_id):
            existent_id = con.hget("reviews.by.product", product_id)
            existent_id = existent_id + ' ' + review_id
            con.hset('reviews.by.product', product_id, existent_id)
        else:
            con.hset('reviews.by.product', product_id, review_id)

        con.hset('product.title.by.product.id', product_id, product_title)

        con.hset('star.rating.by.review', review_id, star_rating)
        count += 1

        if count%10000 == 0:
            print "{:d} líneas procesadas...".format(count)


    print "Se leyeron {:d} del archivo {:s}".format(count, file.name)
    print "Formato:"
    print csv_reader.fieldnames

    return

def procesar(file, host='localhost', port=6379):
    """ Cargar datos en los mapas "review:<valor>" y en los zsets "reviews:marketplace:<valor>"
    """

    # Conexión con Redis
    con = redis.Redis(host, port)
    header = [item.strip('"') for item in file.readline().rstrip('\n').split('","')]

    # Leer la primera línea para obtener el orden de los campos
    print header

    count = 0
    for line in file:

        # Leer los datos y guardarlos en un diccionario
        #print line
        valores = [item.strip('"') for item in line.rstrip('\n').split('","')]
        #print valores
        tupla = {}
        for i in xrange(len(valores)):
            tupla[header[i]] = valores[i]

        # Insertar los datos en review:<id>
        review_id = tupla.pop('review_id')

        con.hmset('review:' + review_id, tupla)

        product_id = tupla.pop('product_id')
        product_title = tupla.pop('product_title')
        star_rating = tupla.pop('star_rating')


        con.zadd('reviews:marketplace:' + tupla['marketplace'], review_id, float(tupla['review_date']))

        if con.hexists("reviews.by.product", product_id):
            existent_id = con.hmget("reviews.by.product", product_id)
            existent_id[0] = existent_id[0] + ' ' + review_id
            con.hset('reviews.by.product', product_id, existent_id[0])
        else:
            con.hset('reviews.by.product', product_id, review_id)

        con.hset('product.title.by.product.id', product_id, product_title)

        con.hset('star.rating.by.review', review_id, star_rating)
        count += 1

        if count%10000 == 0:
            print "{:d} líneas procesadas...".format(count)

    print "Se leyeron {:d} del archivo {:s}".format(count, file.name)

    return

def main():
    if len(sys.argv) < 2:
        print "Error de argumentos!"
        print "Uso: {:s} [FILE]...".format(sys.argv[0])
        print ""


    for path in sys.argv[1:]:
        with open(path, mode='r') as file:
            procesar_csv(file)



if __name__ == '__main__':
    main()
