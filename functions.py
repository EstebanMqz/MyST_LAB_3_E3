
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


def f_columnas_tiempos(data,Open,Close):
        """
        Function that calculates columns Open_pos and Pip_Size for the existing dataframe.
        Open_Pos: Calculates the difference between open and close time columns.

        Parameters
        ----------
        Open: Column of Open date as datetime64 format. 
        ej. data.Fecha/Hora for columns in files/Historics.csv
        Close: Column of Close date as datetime64 format. 
        ej. data.Fecha/Hora.1 for columns in files/Historics.csv

        -------
        returns: Time elapsed for an Open Position in seconds.
        
        Open_Pos: A new column as datetime64 column, that represents the seconds for which the trade was open.
        """
        data['Open'] = pd.to_datetime(Open)
        data['Close'] = pd.to_datetime(Close)
        data['Open_Pos'] = pd.to_datetime(Close)-pd.to_datetime(Open)
        data['Open_Pos'] = data['Open_Pos'].dt.total_seconds()

        return data
        