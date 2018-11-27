# bases-redis

## Estructura del proyecto

Guardar las clases en la carpeta src/redisapp, otros scripts en src o hacer subdirectorios según sea necesario.

## Estilos y documentación

Vamos a usar el estándar PEP8 en la medida de lo posible. Pueden revisar este [link](https://www.datacamp.com/community/tutorials/pep8-tutorial-python-code), lo más importante es que sigan el estándar de nombres y que por favor configuren su editor para **usar 4 espacios en vez de tabs**! En cuanto a documentación yo uso docstrings con el estilo de google, en este [link](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) pueden ver ejemplos.

Ejemplo:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys

class NombreClase(object):
    r""" Documentación de la clase (brief), los nombres de clase usan CamelCase.
    
    Explicación más extensa de lo que hace la clase. Yo usualmente
    incluyo la documentación del constructor (__init__).  
    
    Args:
        param (int): Descripción de lo que hace param.
        param_optional (int, optional): Un parámetro opcional.
      
    Attributes:
        important_data (str): Un atributo de la clase.
        
    Note:
        Información adicional.
    """
    
        def __init__(self, param, param_optional=None):
            # Este es el constructor!
            self.important_data = 'blabla'
            
            if param_optional is not None:
                self.important_data + ' ' + str(param);
                
        def nombre_metodo(self, x, y):
            r""" Documentación del método, los métodos y las funciones usan snake_case.
            
            Args:
                x (float): Lorem ipsum dolor sit amet consectetur.
                y (float): Adipiscing elit erat ultricies velit
                    ut sollicitudin.
                    
            Returns:
                float: Información de lo que retorna el método.
            """
            
            # nombres de variables también en minúsculas.
            result = x + y
            
            return result

# Así se acostrumbra escribir el main!
def main():
    print 'Hola Mundo!'
    return

# Esta línea es mágica
if __name__ == "__main__":
    main()
```
