"""Este script lee, limpia y transforma un dataset con la ayuda de pandas, con la finalidad de alimentar a un dashboard de Power Bi.

Reflexiones:
1. Se separó la lógica en 3 funciones(leer, limpiar, guardar) para poder realizar el mantenimiento y mejora del código rápidamente.Además de facilitar
el testeo y  la reutilización de funciones.

2. Las rutas de archivos viven en un .env en lugar de estar hardcodeadas, esto con la finalidad de que el usuario pueda configurar rápidamente sus propias rutas

"""


import pandas as pd
import os
from dotenv import load_dotenv  
import logging
from datetime import datetime


#Configurar el logging
"""Configuracion del logging para realizar el seguimiento del proceso"""
logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

#Definicion de orígenes
"""Configuración de los archivos para evitar hardcodear el código y sea fácil su implementación"""
load_dotenv()

RUTA_CSV = os.getenv('RUTA_CSV_ENTRADA')
RUTA_SALIDA = os.getenv('RUTA_SALIDA')
NOMBRE_ARCHIVO = os.getenv('NOMBRE_ARCHIVO')

def leer_csv():
    """Leer el csv de ecommerce"""
    try:
        df = pd.read_csv(RUTA_CSV)
        logging.info(f"CSV leído: {len(df)} registros")
        return df
    except Exception as e:
        logging.error(f"Error al leer el csv: {e}")
        raise

def limpiar_datos(df):
    """Limpia y transforma los datos
    - Colocar el formato correcto a la fecha para un buen análisis
    - Renombramiento del nombre de las columnas para poder trabajar en el idioma propio"""
    try:
        #Seleccionar columnas
        columnas = ['Order_ID', 'Order_Date', 'Order_Status', 'Region',
                    'Delivery_Days', 'Quantity', 'Net_Sales']
        df_limpio = df[columnas].copy()

        #Transformando Order_Date a tipo datetime
        df_limpio['Order_Date'] = pd.to_datetime(df_limpio['Order_Date'])

        #Eliminar nulos
        df_limpio = df_limpio.dropna()

        #Renombrando columnas a español
        df_limpio.rename(columns={
            'Order_ID':'Pedido',
            'Order_Date':'Fecha_Pedido',
            'Order_Status':'Estado_Orden',
            "Delivery_Days":'Dias_Entrega',
            'Quantity':'Cantidad',
            'Net_Sales':'Venta_Neta'
        }, inplace=True)

        logging.info(f"Datos limpios: {len(df_limpio)} registros")
        return df_limpio

    except Exception as e:
        logging.error(f"Error al limpiar los datos: {e}")
        raise

def guardar_resultado(df):
    """Guardar el dataset limpio"""
    try:
        fecha_hoy = datetime.now().strftime('%Y%m%d')
        nombre_final = f"{NOMBRE_ARCHIVO}_{fecha_hoy}.csv"
        ruta_completa = os.path.join(RUTA_SALIDA, nombre_final)

        df.to_csv(ruta_completa, index=False, encoding='utf-8')
        logging.info(f"Archivo guardado: {ruta_completa}")
        print(f"Pipeline completado:{nombre_final}")

    except Exception as e:
        logging.error(f"Error al guardar: {e}")
        raise

if __name__ == "__main__" :
    
    try:
        logging.info("Iniciando pipeline")

        df= leer_csv()
        df_limpio = limpiar_datos(df)
        guardar_resultado(df_limpio)

        logging.info("Pipeline finalizado exitosamente")

    except Exception as e:
        logging.error(f"Pipeline falló: {e}")
        print(f"Error: {e}")



