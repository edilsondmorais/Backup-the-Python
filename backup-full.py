#!/usr/bin/python
# -*- coding: utf-8 -*-
#backup-full.py

import subprocess
import time
import os, os.path


#PARAMETROS A SER EDITADO:
path_origem = "/home/edilson/Documentos/DOC/Pessoal/Edilson-Doc/Edilson/CASA/"
path_destino = "/home/edilson/BACKUP/"
excluir_do_bkp = "nohup.out"

# variavel usada para politica de retencao
destino_backup = '/home/edilson/BACKUP/'
dias_retencao = 3

remover_ate_mes = 4 # Buscar e remover backups ate esta quantidades de mes anterior

## NAO E NESCESSARIO ALTERAR NADA DESTE PONTO EM DIANTE
#######################################################

#Essa função gera um banner com a hora inicial do Backup
def inicio(horaInicio):

    inicio = '''
  ===========================================================================
||   ____          _____ _  ___    _ _____    ______ _    _ _      _         ||
||  |  _ \   /\   / ____| |/ / |  | |  __ \  |  ____| |  | | |    | |        ||
||  | |_) | /  \ | |    | ' /| |  | | |__) | | |__  | |  | | |    | |        ||
||  |  _ < / /\ \| |    |  < | |  | |  ___/  |  __| | |  | | |    | |        ||
||  | |_) / ____ \ |____| . \| |__| | |      | |    | |__| | |____| |____    ||
||  |____/_/    \_\_____|_|\_ \____/|_|      |_|     \____/|______|______|   ||
||                                                                           ||
||                       BACKUP FULL DE {path1}                                        ||
||                                                                           ||
  ===========================================================================

  ===========================================================================
                 BACKUP FULL DE {path}  INICIADO ÀS {hora}
  ===========================================================================
''' .format(path1=path_origem,path=path_origem, hora=horaInicio)
    return inicio

#Termino e calculos
def termino(diaInicio, horaInicio, backup, pathlog):
    hoje = (time.strftime("%d-%m-%Y"))
    horaFinal   = time.strftime('%H:%M:%S')
    backup = backup.replace('tar cvf', '')
    final = '''
  ===========================================================================
                            BACKUP FULL FINALIZADO

                HORA INICIAL:    %s  -  %s
              HORA FINAL  :    %s  -  %s
                LOG FILE    :    %s
                BAK FILE    :    %s
  ===========================================================================

    ''' % (diaInicio, horaInicio, hoje, horaFinal, pathlog, backup)
    return final


#ESSA FUNÇÃO DESMONTA O HD DE BACKUP POR SEGURANÇA.
#DESCOMENTE A LINHA desmonta_hd() DENTRO DE backupfull() PARA UTILIZÁ-LA
def desmonta_hd(disk):
    try:
        umount = 'umount %s' % disk
        subprocess.call(umount, shell=True)
        return True
    except:
        return False


#CONSTROI OS LOGS DO SISTEMA - Aqui selecionamos o nome do backup e o arquivo de logs que iremos criar.
def geralog():
    date = (time.strftime("%Y-%m"))             #
    logfile     = '%s-backup-full.txt' % date       # Cria o arquivo de Log
    pathlog     = path_destino + logfile    # Arquivo de log

    return pathlog


#CONSTROI O ARQUIVO E PATH DE BACKUP E RETORNA
def gerabackup():
    #date_str = (time.strftime("%Y-%m-%d"))
    dia = int(time.strftime('%d'))
    mes = int(time.strftime('%m'))
    ano = int(time.strftime('%Y'))
    dia = str(dia) # ESTA CONVERSAO FOI NECESSARIA PARA TIRAR O "0" DA DATA
    mes = str(mes)
    ano = str(ano)
    date = ano+"-"+mes+"-"+dia
    backupfile  = '%s-backup-full.tar.gz' % date    # Cria o nome do arquivo de Backup
    pathdestino = path_destino + backupfile   # Destino onde será gravado o Backup
    #pathorigem  = '/var/www/playland/'                   # pasta que será 'backupeada'
    cam_backup      = 'tar --exclude=%s -czvf %s %s' % (excluir_do_bkp,pathdestino, path_origem) # Comando de execução

    return cam_backup

# Para definir quantidade de dias do mês
def dias_mes(ver_qt_dias):
    ver_qt_dias = int(ver_qt_dias)
    if ver_qt_dias >= 1 and ver_qt_dias <= 7:

        if ver_qt_dias % 2 == 0:  # idenficar se o mes e par
            if ver_qt_dias == 2:  # mes de fevereiro
                dias_mes = 28
            else:
                dias_mes = 30
        else:
            dias_mes = 31
    else:
        if ver_qt_dias % 2 == 0:  # idenficar se o mes e par
            dias_mes = 31
        else:
            dias_mes = 30

    return dias_mes


def remover_backup(arq):
    inicio_evento = time.strftime('%d-%m-%Y  %H:%M:%S')
    pathlog = geralog()
    os.remove(arq)
    retorno = "%s Arquivo %s  removido com sucesso\n" % (inicio_evento, arq)
    l = open(pathlog, 'a')
    l.write(retorno)
    l.close()


#POLITICA DE RETENCAO
def clean():
    #date = (time.strftime("%Y-%m-%d"))
    dia = int(time.strftime('%d'))
    #dia_bkp = int(time.strftime('%d'))
    mes = int(time.strftime('%m'))
    ano = int(time.strftime('%Y'))
    mes_limit_rem = 0
    while mes_limit_rem <= remover_ate_mes:
        dias_mes_ant = dias_mes(mes)

        if dia <= 2:
            dia = dias_mes_ant + dia

        dia_ini_rem = dia - dias_retencao
        a = ano
        m = mes
        d = dia_ini_rem
        while d > 0:  # retrocede dias partindo da data inicio da remocao
            ano_remove = str(a)
            mes_remove = str(m)
            dia_remove = str(d)
            data_remove = ano_remove + "-" + mes_remove + "-" + dia_remove
            arq_remove = '%s-backup-full.tar.gz' % data_remove
            caminho_completo = destino_backup + arq_remove
            ver_arquivo = os.path.exists(caminho_completo)
            if ver_arquivo == True: # Chama funcao e remove o arquivo
                remover_backup(caminho_completo)

            d -= 1
            if d == 0:
                if m == 1:
                    m = 12
                    a -= 1
                else:
                    m -= 1

        while mes_limit_rem <= remover_ate_mes: # retrocede dias partindo do mes anterior
            dias = dias_mes(m) # Consultar quantos dias tem no mês
            d = dias
            print("Verificando backups do mes {}".format(mes_remove))
            while d > 0:  # retrocede dias
                ano_remove = str(a)
                mes_remove = str(m)
                dia_remove = str(d)
                data_remove = ano_remove + "-" + mes_remove + "-" + dia_remove
                arq_remove = '%s-backup-full.tar.gz' % data_remove
                caminho_completo = destino_backup + arq_remove
                ver_arquivo = os.path.exists(caminho_completo)
                if ver_arquivo == True:  # Chama funcao e remove o arquivo
                    remover_backup(caminho_completo)
                d -= 1

            if m == 1:
                m = 12
                a -= 1
            else:
                m -= 1

            mes_limit_rem += 1

    print("Busca por backups antigo finalizada")



#CRIA OS BACKUPs
def backupfull():
    #disk = '/dev/sdb'        #Define onde está a partição que será usada para guardar o backup
    horaInicio = time.strftime('%H:%M:%S')
    pathlog = geralog()
    caminho_backup = gerabackup()
    log = ' >> %s' % pathlog
    start = inicio(horaInicio)

    #RODA O BACKUP
    #subprocess.call(backup + log, shell=True)
    resp_comando = os.system(caminho_backup)

    #Printa o final e relatório
    diaInicio   = (time.strftime("%d-%m-%Y"))
    final       = termino(diaInicio, horaInicio, caminho_backup, pathlog)
    r           = open(pathlog, 'w')
    r.write(final)
    r.close()

    clean()
    #Descomente essa função para desmontar a partição que será utilizada para armazenar o backup
    #desmonta_hd(disk)

backupfull()

