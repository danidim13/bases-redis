#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

def main():

    if len(sys.argv) != 2:
        print len(sys.argv)
        print "Error de argumentos!"
        sys.exit(1)

    with open(sys.argv[1], 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        data = []
        for line in reader:
            data.append(line)

        print data

        arr = np.array(data, dtype=np.float_)
        plt.plot(arr[:,0], arr[:,1], 'o')
        plt.xlabel('Reviews [n]')
        plt.ylabel('Tiempo [s]')
        plt.title('Tiempo de consulta Tendencias')
        plt.grid(True)
        plt.show()

    sys.exit()

if __name__ == '__main__':
    main()
