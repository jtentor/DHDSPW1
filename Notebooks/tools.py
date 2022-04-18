import pandas as pd
import numpy as np
import seaborn as sns
import re
import matplotlib.pyplot as plt


#funcion para borrar outliers.
def borrar_outliers(data, columnas):
    """Solo recibo columnas con valores numericos. 
    Las columnas que quieras borrar outliers van en forma de tupla"""
    cols_limpiar = columnas
    mask=np.ones(shape=(data.shape[0]), dtype=bool)

    for i in cols_limpiar:
        
        #calculamos cuartiles, y valores de corte
        Q1=data[i].quantile(0.25)
        Q3=data[i].quantile(0.75)
        RSI=Q3-Q1
        max_value=Q3+1.5*RSI
        min_value=Q1-1.5*RSI
        
        #ajusto el min value 
            # No puede ser negativo
            # No puede estar fuera del boxplot para outliers
            # Criterio experto se decide dejar desde el 5% hacia adelante en el precio
            
        min_value=max(data[i].quantile(0.05), min_value, 10)
        
        #filtramos por max y min
        mask=np.logical_and(mask, np.logical_and(data[i]>=min_value, data[i]<=max_value))
    return data[mask]

#Funcion para hacer correlacion.
def check_corr(data, place, tipo, ver_correlacion):
    """Funcion que checkea correlacion entre las variables ver_correlacion.Internamente llama a la funcion borrar_outliers
    
    data: pd.DatFrame
    place: indica filtro por lugar
    tipo indica filtro por tipo de propierdad 
    *ver_correlacion debe ser una tupla con dos columnas del dataframe donde vamos a borrar outliers y calcular correlacion"""
    
    data_place = data[data.place_name==place]
    data_tipo = data_place[data_place.property_type==tipo]

    data_outliers = borrar_outliers(data_tipo, ver_correlacion)
    
    
    corr = data_outliers[[ver_correlacion[0], ver_correlacion[1]]].corr()
    return corr.iloc[0,1]


def regex_to_tags(col, reg, match, not_match = np.NaN) :
    u"""Returns a series with 'match' values result of apply the regular expresion to the column
    the 'match' value will be when the regular expression search() method found a match
    the 'not_match' value will be when the regular expression serach() method did not found a match
    col : column where to apply regular expresion
    reg : regular expresion compiled
    """
    
    serie = col.apply(lambda x : x if x is np.NaN else reg.search(x))
    serie = serie.apply(lambda x : match if x is not None else not_match)
   
    return serie


def regex_to_values(col, reg) :
    u"""Returns a serie with the result of apply the regular expresion to the column
    the serie have a float value only when regular expression search() method found a match
    
    col : column where to apply regular expresion
    reg : regular expresion compiled
    """
    
    serie = col.apply(lambda x : x if x is np.NaN else reg.search(x))
    serie = serie.apply(lambda x : np.NaN if x is np.NaN or x is None else float(x.group(1)))

    return serie

