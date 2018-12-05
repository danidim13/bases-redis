#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import redis
import string

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

        con.zadd('reviews:marketplace:' + tupla['marketplace'], review_id, float(tupla['review_date']))

        count += 1

        if count%10000 == 0:
            print "{:d} líneas procesadas...".format(count)

    print "Se leyeron {:d} del archivo {:s}".format(count, file.name)

def main():
    if len(sys.argv) < 2:
        print "Error de argumentos!"
        print "Uso: {:s} [FILE]...".format(sys.argv[0])
        print ""


    for path in sys.argv[1:]:
        with open(path, mode='r') as file:
            procesar(file)



if __name__ == '__main__':
    main()
