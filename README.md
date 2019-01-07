# Backup-the-Python
O script é parametrizável para política de retenção.
No início do script tem as varáveis onde informamos o diretório a ser feito e o diretório onde será armazenado o backup.
O script também busca backups antigo com a mesma nomeclatura e deleta, deixando apenas os backups dentro do periodo de retenção

#PARAMETROS A SER EDITADO:
path_origem = "/home/edilson"
path_destino = "/mnt/BACKUP/"

excluir_do_bkp = "nohup.out" # Arquivos que serão ignorados


# variavel usada para politica de retencao
dias_retencao = 3
remover_ate_mes = 4 # Buscar e remover backups ate 4 meses anterior ao atual
