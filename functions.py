
"""
# -- ---------------------------------------------------------------------------------------------------------      -- #
# -- project: Lab 3 (Behavioral Finance) is a project that has tools to analyze the performance of trade history.   -- #
# -- script: functions.py : Python script with the main functionality                                               -- #
# -- author: EstebanMqz                                                                                             -- #
# -- license: GNU General Public License v3.0                                                                       -- #
# -- repository: https://github.com/EstebanMqz/MyST_LAB_3_E3                                                        -- #
# -- ---------------------------------------------------------------------------------------------------------      -- #
"""

from dataclasses import dataclass
from lib2to3.pgen2.grammar import opmap_raw
import numpy as np
from data import *

def f_leer_archivo(param_archivo):
    """
    Function that reads csv files and returns a dataframe of its content.
        Parameters
        ----------
        param_archivo: csv data.
        Returns
        -------
        data: pd.DataFrame(param_archivo)
    """

    df = pd.read_csv(param_archivo)
    return df


def symbols(param_sym):
        """
        A function to get unique values of the traded symbols in historical data and return
        its globally accepted denomination
        Parameters
        ----------
        param_sym: Instrument Symbols Column (Str) 
        ej: data.Símbolo
        -------
        Returns
        -------
        Symbols : Searchable traded symbols from historical data [List].      
        """
        symbols=param_sym.unique()
        symbols=[symbols[i][:3] + '_' + symbols[i][3:] for i in range(3)] #Applicable to currencies
        return symbols


def f_pip_size(param_ins, param_pips):
        """
        A function to get the multiplier number to express the price difference in pips.
        Mult = 100 for instruments denominated in monetary units.
        Parameters
        ----------
        param_ins: Instrument name to be associated with the corresponding pip multiplier (Str).
        param_pips: Instruments_pips values provided in the general tick size csv.
        -------
        Returns
        -------
        Pip Size : Int.      
        """

        Instr=param_pips[param_pips['Instrument'] == param_ins]
        pip_size=1/Instr['TickSize']
        return pip_size


def f_columnas_tiempos(param_data,Open,Close):
        """
        Function that calculates column Open_pos for the existing dataframe.
        Open_Pos: Calculates the difference between Open and Close time columns.

        Parameters
        ----------
        Open: Column of Open date as datetime64 format. 
        ej. data.Fecha/Hora for columns in files/Historics.csv
        Close: Column of Close date as datetime64 format. 
        ej. data.Fecha/Hora.1 for columns in files/Historics.csv
        -------
        returns: Time elapsed for an Open Position in seconds.
        + Open_Pos: A new column as datetime64 column, that represents the seconds for which the trade was open.
        """
        param_data['Open'] = pd.to_datetime(Open)
        param_data['Close'] = pd.to_datetime(Close)
        param_data['Open_Pos'] = pd.to_datetime(Close)-pd.to_datetime(Open)
        param_data['Open_Pos'] = param_data['Open_Pos'].dt.total_seconds()

        return param_data


def f_columnas_pips(param_data, pips):
        """
        Function that adds more columns of pip transformations.
        + Pips: Column where the number of resulting pips for each operation should be, including its sign:
        - Buy Trade: (closeprice - openprice)*mult.
        - Sell Trade: (openprice - closeprice)*mult.
        + pips_acm: The accumulated value of the pips column.
        + profit_acm: The accumulated value of the profit column.

        Parameters
        ----------
        param_data: DataFrame base.
        pips: General tick size file instruments.csv
        -------
        returns: Historic data with Pips, pips_acm, profit_acm new columns.
        """
        trades = []
        for i in range(len(param_data)):
                trades.append(f_pip_size(param_data.loc[i,'Símbolo'], pips))
        pips = pd.DataFrame(trades, columns=['Pips'])
        param_data["Pips"] = np.where(param_data['Tipo'] == "buy", 
        param_data["Precio.1"] - param_data["Precio"], 
        param_data["Precio"] - param_data["Precio.1"])
        param_data['pips_acm'] = param_data["Pips"].cumsum()
        param_data['Beneficio']=pd.to_numeric(param_data['Beneficio'].replace('-',np.nan)) 
        param_data['profit_acm'] = param_data["Beneficio"].cumsum()
        
        return param_data

def f_estadisticas_ba(param_data):
        """
        Function that makes a df of general statistics columns from historic operations.

        Parameters
        ----------
        param_data: DataFrame base.
        -------
        returns: Dataframe with metrics columns calculated.
        """
        metrics = ["Ops totales","Ganadoras","Ganadoras_c","Ganadoras_v","Perdedoras","Perdedoras_c","Perdedoras_v",
               "Mediana (Profit)","Mediana (Pips)","r_efectividad","r_proporcion","r_efectividad_c","r_efectividad_v"]
    
        description = ["Operaciones totales","Operaciones ganadoras","Operaciones ganadoras de compra",
               "Operaciones perdedoras de venta","Operaciones perdedoras","Operaciones perdedoras de compra",
               "Operaciones perdedoras de venta","Mediana de profit de operaciones",
               "Mediana de pips de operaciones","Ganadoras Totales/Operaciones Totales",
               "Ganadoras Totales/Perdedoras Totales","Ganadoras Compras/Operaciones Totales",
               "Ganadoras Ventas/ Operaciones Totales"]
    
        valor = np.zeros(13)
    
        datos_df1 = {"medidas":metrics,"valor":valor,"description":description}
        df_1_tabla = pd.DataFrame(datos_df1)

        param_data["Ops Totales"] = np.ones(len(param_data["Beneficio"]))
        param_data["Ops Ganadoras"] = np.zeros(len(param_data["Tipo"]))
        param_data["Ops Perdedoras"] = np.zeros(len(param_data["Tipo"]))
        param_data["Ops Ganadoras_C"] = np.zeros(len(param_data["Tipo"]))
        param_data["Ops Perdedoras_C"] = np.zeros(len(param_data["Tipo"]))
        param_data["Ops Ganadoras_V"] = np.zeros(len(param_data["Tipo"]))
        param_data["Ops Perdedoras_V"] = np.zeros(len(param_data["Tipo"]))
    
        df_1_tabla.valor[0] = len(param_data.Tipo)
    
        for i in range(len(param_data["Beneficio"])):
            if param_data["Beneficio"][i] > 0:
                param_data["Ops Ganadoras"][i] = 1
                param_data["Ops Perdedoras"][i] = 0
            else:
                param_data["Ops Ganadoras"][i] = 0
                param_data["Ops Perdedoras"][i] = 1
    
        df_1_tabla.valor[1] = sum(param_data["Ops Ganadoras"])
        df_1_tabla.valor[4] = sum(param_data["Ops Perdedoras"])
    
        for i in range(len(param_data["Beneficio"])):
            if param_data["Ops Ganadoras"][i] == 1 and param_data["Tipo"][i] == "buy" :
                param_data["Ops Ganadoras_C"][i] = 1
            elif param_data["Ops Ganadoras"][i] == 1 and param_data["Tipo"][i] == "sell" :
                param_data["Ops Ganadoras_V"][i] = 1
            elif param_data["Ops Perdedoras"][i] == 1 and param_data["Tipo"][i] == "buy" :
                param_data["Ops Perdedoras_C"][i] = 1
            elif param_data["Ops Perdedoras"][i] == 1 and param_data["Tipo"][i] == "sell" :
                param_data["Ops Perdedoras_V"][i] = 1
            else:
                param_data["Ops Ganadoras_C"][i] = 0
                param_data["Ops Ganadoras_V"][i] = 0
                param_data["Ops Perdedoras_C"][i] = 0
                param_data["Ops Perdedoras_V"][i] = 0
            
        df_1_tabla.valor[2] = sum(param_data["Ops Ganadoras_C"])
        df_1_tabla.valor[3] = sum(param_data["Ops Ganadoras_V"])
        df_1_tabla.valor[5] = sum(param_data["Ops Perdedoras_C"])
        df_1_tabla.valor[6] = sum(param_data["Ops Perdedoras_V"])
        
        df_1_tabla.valor[7] = param_data["Beneficio"].median()
        df_1_tabla.valor[8] = param_data["Pips"].median()
        
        df_1_tabla.valor[9] = round(sum(param_data["Ops Ganadoras"])/len(param_data["Ops Perdedoras"]),3)
        df_1_tabla.valor[10] = round(sum(param_data["Ops Ganadoras"])/sum(param_data["Ops Ganadoras"]),3)
        df_1_tabla.valor[11] = round(sum(param_data["Ops Ganadoras_C"])/len(param_data["Ops Ganadoras"]),3)
        df_1_tabla.valor[12] = round(sum(param_data["Ops Ganadoras_V"])/len(param_data["Ops Ganadoras"]),3)
        
        return df_1_tabla

def estadisticas_ba2(param_data):
    for i in range(len(param_data)):
        if param_data["Beneficio"][i] > 0:
            param_data["Ops Ganadoras"][i] = 1
            param_data["Ops Perdedoras"][i] = 0
        else:
            param_data["Ops Ganadoras"][i] = 0
            param_data["Ops Perdedoras"][i] = 1

    for i in range(len(param_data["Beneficio"])):
        if param_data["Ops Ganadoras"][i] == 1 and param_data["Tipo"][i] == "buy" :
            param_data["Ops Ganadoras_C"][i] = 1
        elif param_data["Ops Ganadoras"][i] == 1 and param_data["Tipo"][i] == "sell" :
            param_data["Ops Ganadoras_V"][i] = 1
        elif param_data["Ops Perdedoras"][i] == 1 and param_data["Tipo"][i] == "buy" :
            param_data["Ops Perdedoras_C"][i] = 1
        elif param_data["Ops Perdedoras"][i] == 1 and param_data["Tipo"][i] == "sell" :
            param_data["Ops Perdedoras_V"][i] = 1
        else:
            param_data["Ops Ganadoras_C"][i] = 0
            param_data["Ops Ganadoras_V"][i] = 0
            param_data["Ops Perdedoras_C"][i] = 0
            param_data["Ops Perdedoras_V"][i] = 0
            
    df_2_ranking = pd.pivot_table(param_data,index=["Símbolo"],aggfunc={"Ops Ganadoras":np.sum,"Ops Totales":np.sum})
    df_2_ranking["rank"] = (df_2_ranking["Ops Ganadoras"]/df_2_ranking["Ops Totales"])
    df_2_ranking = df_2_ranking.drop(["Ops Ganadoras","Ops Totales"],axis=1)
    df_2_ranking = df_2_ranking.sort_values('rank',ascending=False)
    df_2_ranking["rank"] = round(df_2_ranking["rank"],2)
    df_2_ranking["rank %"] = df_2_ranking["rank"].map(lambda x:format(x,'.2%'))
    #pivot_ord["rank"] = pivot_ord["rank"].map(lambda x:format(x,'.2%'))
    return df_2_ranking