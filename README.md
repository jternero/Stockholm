
# Stockholm

## Simulación de ransomware
> Este código simula el proceso de cifrado/descifrado del ransomware WannaCry.

  

## Uso

*Para cifrar archivos:*

    python stockholm.py

> Se le solicitará que ingrese una clave de cifrado. 
> Ingrese una clave de 16 caracteres.

  

*Para descifrar archivos:*

    python stockholm.py -r TU_CLAVE

> Reemplace TU_CLAVE con la clave que ingresó durante el cifrado.

  

## Características

 - Cifra/descifra archivos con cifrado AES-CBC utilizando una clave y un IV
   
 - Agrega la extensión .ft a los archivos cifrado
   
 - Admite el cifrado/descifrado de una variedad de tipos de archivo comunes
 
 - Proporciona el modo silencioso para suprimir la salida  
 
 - Muestra información de versión con la opción -v


## Requisitos

> - Python 3.7+
> - La biblioteca Cryptodome

Instale la biblioteca Cryptodome con:

    pip install Cryptodome

## AVISO

*Este código es solo para fines educativos. No apruebo el uso de ransomware para dañar a otros.*
