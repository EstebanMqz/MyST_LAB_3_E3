
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
import plotly.graph_objects as go #plotly
import plotly.express as px
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
        A function whose output is a dictionary, that output dictionary must have 2 keys, 'df_1_table' and 'df_2_ranking':
        + col: Metrics, col: Value, col: Description

        - Ops totales ~ 83 ~ total_operations
        - Ganadoras ~ 45 ~ Winner operations
        - Ganadoras_c ~ 19 ~ Winner buy operations
        - Ganadoras_v ~ 26 ~ Losing sell operations
        - Perdedoras ~ 38 ~ Losing operations
        - Perdedoras_c ~ 19 ~ Losing buy operations
        - Perdedoras_v ~ 19 ~ Losing sell operations
        - Median (Profits) ~ 1.09 ~ Median operations profit
        - Median (Pips) ~ 2.8 ~ Median pips profit
        - r_efectividad ~ 0.54 ~ Total Winning/Total Trades
        - r_proporcion ~ 1.18 ~ Total Winners/Total Losers
        - r_efectividad_c ~ 0.23 ~ Winning Purchases/Total Transactions
        - r_efectividad_v ~ 0.31 ~ Winning Sales / Total Operations

        Parameters
        ----------
        param_data: DataFrame base.
        -------
        returns:
        df_1_tabla: col: Metrics, col: Value, col: Description.
        df_1_ranking: Effectiveness ratio of operations for each instrument.
        """


        
        return param_data
