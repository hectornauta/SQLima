import datetime
import logging

logging.basicConfig(
    filename = './SQLima.log',
    level = logging.DEBUG,
    filemode = 'w'
    )
logger = logging.getLogger()

def crear_csv(fecha_de_hoy):

    archivo = open("registro_temperatura365d_smn.txt", "r")

    lineas = archivo.readlines()
    archivo.close()

    csv = open(fecha_de_hoy, "w",encoding='utf-8')

    lineas.pop(0)
    lineas.pop(1)
    for linea in lineas:
        fecha = linea[0:8]
        fecha = fecha.strip()
        temperaturas = linea[8:20]
        temperaturas = temperaturas.split()
        ubicacion = linea[20:]
        ubicacion = ubicacion.strip()
        #datos = str(fecha) + ';' + str(temperaturas) + ';' + str(ubicacion)
        #logging.info(datos) 
        if len(temperaturas)==2:
            nueva_linea = str(fecha) + ';' + str(temperaturas[0]) + ';' + str(temperaturas[1]) + ';' + str(ubicacion)
            csv.write(nueva_linea)
            csv.write('\n')
    csv.close()

def main():
    crear_csv(datetime.datetime.now())

if __name__ == "__main__":
    main()