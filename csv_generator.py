import datetime
import logging

logging.basicConfig(
    filename = './SQLima.log',
    level = logging.DEBUG,
    filemode = 'w'
    )
logger = logging.getLogger()

def crear_csv(fecha_de_hoy):

    archivo = open("registro_temperatura365d_smn_1.txt", "r")

    lineas = archivo.readlines()
    archivo.close()

    csv = open(fecha_de_hoy, "w",encoding='utf-8')
    for i in range(3):
        lineas.pop(0)
    nueva_linea = 'año;mes;dia;tmax;tmin;ubicacion\n'
    csv.write(nueva_linea)
    for linea in lineas:
        ano = linea[4:8]
        ano = ano.strip()
        mes = linea[2:4]
        mes = mes.strip()
        dia = linea[0:2]
        dia = dia.strip()
        temperaturas = linea[8:20]
        temperaturas = temperaturas.split()
        ubicacion = linea[20:]
        ubicacion = ubicacion.strip()
        #datos = str(fecha) + ';' + str(temperaturas) + ';' + str(ubicacion)
        #logging.info(datos) 
        if len(temperaturas)==2:
            nueva_linea = str(ano) + ';' + str(mes) + ';' + str(dia) + ';' + str(temperaturas[0]) + ';' + str(temperaturas[1]) + ';' + str(ubicacion)
            csv.write(nueva_linea)
            csv.write('\n')
    csv.close()

def main():
    crear_csv(datetime.datetime.now())

if __name__ == "__main__":
    main()