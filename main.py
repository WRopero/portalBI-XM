import requests
import pandas as pd
import os
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row
import bokeh.palettes as pl
from bs4 import BeautifulSoup
from common import config
import time
import io

def _get_queries(type_, folder):
    """
    Obtiene los queries de los archivos yaml para demanda
    """
    url = config()[type_]['url']
    queries = config()[type_][folder]['queries']
    folder = config()[type_][folder]['folder']
    
    return url, queries, folder

def _main_download_load(ano, type_, type_2):
    """
    Función para descargar la información de demanda.
    """
    ano = str(ano)
    type_ = type_.strip().lower()
    type_2 = type_2.strip().lower()
    diferencia_anos = int(time.strftime('%Y')) - int(ano)
#########################################################################
    if type_ == 'comercial':
        info_ini = _get_queries(type_ = 'load_files', 
                                folder='load_comercial_folder')
        #################################################################
        if type_2 == "ciiu":
            """
            Demanda No regulada por CIIU
            """
            if int(ano) <= 2016:
                intervalos_anos = ["-T1(ENE-MAR)","-T2(ABR-JUN)","-T3(JUL-SEP)","-T4(OCT-DIC)"]
            elif int(ano) in [2018,2017] :
                intervalos_anos = ["__SEM1_","__SEM2_"]            
            else:
                intervalos_anos = ["_TRI1_","_TRI2_","_TRI3_","_TRI4_"]

            if diferencia_anos <=1: #para saber si esta en las carpetas de afuera
                file = info_ini[0]+info_ini[1]['demanda_noregulada_CIUU']
            else:
                file = info_ini[0]+info_ini[2]+info_ini[1]['demanda_noregulada_CIUU']

            load_all = []   
                
            for i in intervalos_anos:
                try:
                    if int(ano) <= 2016:
                        file_ = file+"_"+ano+i+'.xlsx'
                        print(file_)
                        df = pd.read_excel(file_)
                        df = df.rename(columns=df.iloc[2]).drop([0,2],axis=0).reset_index(drop=True)
                        load_all.append(df)

                    elif int(ano) in [2018,2017]:
                        file_ = file+i+ano+'.xlsx'
                        print(file_)
                        df = pd.read_excel(file_)
                        df = df.rename(columns=df.iloc[2]).drop([0,2],axis=0).reset_index(drop=True)
                        load_all.append(df)

                    else:
                        file_ = file+i+ano+'.xlsx'
                        print(file_)
                        df = pd.read_excel(file_)
                        df = df.rename(columns=df.iloc[2]).drop([0,2],axis=0).reset_index(drop=True)
                        load_all.append(df)
                except:
                    print("Archivo no encontrado")
                
            load_end = pd.concat(load_all, axis=0)            
            df = load_end.reset_index(drop=True)
        #################################################################
        elif type_2 == "comercializador":
            """
            Demanda No regulada por Comercializador
            """
            if int(ano) <= 2017:
                intervalos_anos = ["SEM1","SEM2"]         
            else:
                intervalos_anos = ["SEME1_","SEME2_"] 

            if diferencia_anos <=1: #para saber si esta en las carpetas de afuera
                file = info_ini[0]+info_ini[1]['demanda_por_comercializador']
            else:
                file = info_ini[0]+info_ini[2]+info_ini[1]['demanda_por_comercializador']

            load_all = []   
                
            for i in intervalos_anos:
                try:
                    if int(ano) <= 2017:
                        file_ = file+ano+i+'.xlsx'
                        print(file_)
                        df = pd.read_excel(file_)
                        df = df.rename(columns=df.iloc[1]).drop([0,1],axis=0).reset_index(drop=True)
                        load_all.append(df)

                    else:
                        file_ = file+i+ano+'.xlsx'
                        print(file_)
                        df = pd.read_excel(file_)
                        df = df.rename(columns=df.iloc[1]).drop([0,1],axis=0).reset_index(drop=True)
                        load_all.append(df)
                except:
                    print("Archivo no encontrado")
            load_end = pd.concat(load_all, axis=0)            
            df = load_end.reset_index(drop=True)
        #################################################################
        elif type_2 == "or":
            """
            Demanda No regulada por Operador de Red
            """
            if diferencia_anos <=1: #para saber si esta en las carpetas de afuera
                file = info_ini[0]+info_ini[1]['demanda_por_OR']
            else:
                file = info_ini[0]+info_ini[2]+info_ini[1]['demanda_por_OR']

            try:
                file_ = file+ano+'.xlsx'
                print(file_)
                df = pd.read_excel(file_)
                df = df.rename(columns=df.iloc[1]).drop([0,1],axis=0).reset_index(drop=True)
                
            except:
                print("Archivo no encontrado")
            
        #################################################################
        elif type_2 == "perdidas":
            """
            Perdidas_De_Energia_Por_Comercializador_
            """
            if diferencia_anos <=1: #para saber si esta en las carpetas de afuera
                file = info_ini[0]+info_ini[1]['perdidas_por_com']
            else:
                file = info_ini[0]+info_ini[2]+info_ini[1]['perdidas_por_com']

            try:
                file_ = file+ano+'.xlsx'
                print(file_)
                df = pd.read_excel(file_)
                df = df.rename(columns=df.iloc[1]).drop([0,1],axis=0).reset_index(drop=True)
                
            except:
                print("Archivo no encontrado")

        else:
            print(f"Error: {type_2}",
                    "Seleccione un tipo de demanda comercial valido")
                            #_download_file(file, save)

#########################################################################
    elif type_ == 'nacional':
        info_ini = _get_queries(type_ = 'load_files', 
                                folder='load_national_folder')       

        if type_2 == 'sin':
            try:
                tipo = 'demanda_energia_SIN'
                if diferencia_anos <=1:
                    file = info_ini[0]+info_ini[1][tipo]
                else:
                    file = info_ini[0]+info_ini[2]+info_ini[1][tipo]
                file = file+ano+'.xlsx'
                print(file)
                save = info_ini[1][tipo]+ano+'.xlsx'
                #_download_file(file, save)
                df = pd.read_excel(file)
                df = df.rename(columns=df.iloc[2]).drop([0,3],axis=0).reset_index(drop=True)
                
            except:
                print("error")

        elif type_2 == 'ties_ecuador':
            try:
                tipo = 'ties_ecuador'
                if diferencia_anos <=1:
                    file = info_ini[0]+info_ini[1][tipo]
                else:
                    file = info_ini[0]+info_ini[2]+info_ini[1][tipo]
                file = file+ano+'.xlsx'
                print(file)
                save = info_ini[1][tipo]+ano+'.xlsx'
                #_download_file(file, save)
                df = pd.read_excel(file)
                df = df.rename(columns=df.iloc[2]).drop([0,3],axis=0).reset_index(drop=True)
            #Aquí meto la función para descargue el archivo
            except:
                print("error")

        elif type_2 == 'ties_venezuela':
            try:
                tipo = 'ties_venezuela'
                if diferencia_anos <=1:
                    file = info_ini[0]+info_ini[1][tipo]
                else:
                    file = info_ini[0]+info_ini[2]+info_ini[1][tipo]
                file = file+ano+'.xlsx'
                save = info_ini[1][tipo]+ano+'.xlsx'
                #_download_file(file, save)
                print(file)
                df = pd.read_excel(file)
                df = df.rename(columns=df.iloc[2]).drop([0,3],axis=0).reset_index(drop=True)
                #Aquí meto la función para descargue el archivo
            except:
                print("error\n")
        else:
            print(type_,"Metodo no existe")

#########################################################################    
    elif type_ == 'potencia':
        info_ini = _get_queries(type_ = 'load_files', 
                                folder='load_potencia')

        if diferencia_anos <=1: #para saber si esta en las carpetas de afuera
            file = info_ini[0]+info_ini[1]['demanda_potencia']
        else:
            file = info_ini[0]+info_ini[2]+info_ini[1]['demanda_potencia']

        try:
            file_ = file+ano+'.xlsx'
            print(file_)
            df = pd.read_excel(file_)
            df = df.rename(columns=df.iloc[2]).drop([0,2],axis=0).reset_index(drop=True)
            
        except:
            print("Archivo no encontrado")
#########################################################################
    elif type_ == 'excedentes_cargo':
        info_ini = _get_queries(type_ = 'load_files', 
                                folder='load_energia_cargo_exce')

        if diferencia_anos <=1: #para saber si esta en las carpetas de afuera
            file = info_ini[0]+info_ini[1]['load_en_exc_cargo']
        else:
            file = info_ini[0]+info_ini[2]+info_ini[1]['load_en_exc_cargo']

        try:
            file_ = file+ano+'.xlsx'
            print(file_)
            df = pd.read_excel(file_)
            df = df.rename(columns=df.iloc[1]).drop([0,1],axis=0).reset_index(drop=True)
            
        except:
            print("Archivo no encontrado")
    else:
        print(type_,"'No encontrado en las funciones'")
        df = None   

    return df





if __name__ == '__main__':
    import time

    start = time.time()

    data_ini = _get_queries(type_='load_files', 
                 folder='load_comercial_folder')

    """DEMANDA COMERCIAL"""
  #  demanda_ciiu = _main_download_load(2020, "comercial", "CIIU")
    demanda_comercializador = _main_download_load(2020, "comercial", "comercializador")
  # demanda_perdidas = _main_download_load(2020, "comercial", "perdidas")
  # demanda_OR = _main_download_load(2020, "comercial", "or")
  #     
  # """DEMANDA DE ENERGÍA NACIONAL"""
  # demanda_SIN = _main_download_load(2020, "nacional", "SIN")
  # ties_ecuador = _main_download_load(2020, "nacional", "ties_ecuador")
  # ties_venezuela = _main_download_load(2020, "nacional", "ties_venezuela")

  # """DEMANDA DE POTENCIA"""
  # demanda_potencia = _main_download_load(2020, "potencia", "")

  # """DEMANDA DE CARGO EXCEDENTE"""
  # demanda_cargo_exce = _main_download_load(2020, "excedentes_cargo", "")


    """Ejemplo para trar la demanda mensual por comercializador"""

    df = demanda_comercializador
    df.columns = ['h' +str(int(x)+1) if len(str(x))<=4 else x for x in df.columns]

    from datetime import datetime

    df["mes"] = ""
    for j in range(len(df)):
        df.iloc[j,-1] = datetime.strptime(df.iloc[j,0],"%Y-%m-%d").month

    lista_grupos = []
    for k in list(df.columns)[3:-1]:
        lista_grupos.append(df.groupby(['Codigo Comercializador','Mercado',"mes"])[k].agg("sum"))
    
    mercado = pd.concat(lista_grupos, axis = 1)    
    mercado["Total/dia(GWh)"] = mercado.sum(axis=1) 
    Total_mes_ano = pd.DataFrame(mercado.loc[:,"Total/dia(GWh)"].apply(lambda x: x/1000000)).reset_index()
    
    end = time.time()
    print("El tiempo transcurrido es:",(end-start)/60, "mn")






