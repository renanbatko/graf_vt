#/usr/bin/env python
import urllib
import time
import re
#import os

def compara_data(data1, data2):
	dia1 = data1.split("/", 1)[0]
	mes1 = data1.split("/", 2)[1]
	ano1 = data1.split("/", 3)[2]
	dia2 = data2.split("/", 1)[0]
	mes2 = data2.split("/", 2)[1]
	ano2 = data2.split("/", 3)[2]
	
	#print dia1+" "+mes1+" "+ano1+" "+dia2+" "+mes2+" "+ano2
	
	if (ano1 > ano2):
		return 1
	if (ano1 == ano2):
		if (mes1 > mes2):
			return 1
		if (mes1 == mes2):
				if (dia1 >= dia2):
					return 1
	return 0
	
def ordena_arquivo(nome_arq):
	arq = open(nome_arq, "r")
	
	dates = []
	for line in arq:
		temp01 = line.split(" ", 1)[0]
		dates.append(temp01)
	arq.close()
	
	for i in range(0, len(dates)):
		for j in range(len(dates)-1, i, -1):
			if (compara_data(dates[i], dates[j]) == 1):
				aux = dates[i]
				dates[i] = dates[j]
				dates[j] = aux
	
	fp = open("sorteddates.txt", "w")
	arq = open(nome_arq, "r")
	for date in dates:
		#print "date = "+date
		arq.seek(0)
		for lin in arq:
			#print "lin = "+lin
			col1 = lin.split(" ", 1)[0]
			col2 = lin.split(" ", 2)[1]
			#print date+" == "+col1
			if (date == col1):
				fp.write(date+" "+col2)
	arq.close()
	fp.close()
	#print dates

def num_pages(pagina):
	for linha in pagina:
		if linha.find("sprite-last") != -1:
			temp = linha.split("page=",1)[1]
			num = temp.split('"', 1)[0]
			num = int(num)
			return num

#comeco da main
url_base = raw_input("URL do topico: ")

pagina = urllib.urlopen(url_base)
num = num_pages(pagina)
pagina.close()

#print("esse topico tem "+str(num)+" paginas.")
dates = []

for index in range(1, num+1):
	url_atual = url_base + "?page=" + str(index)
	pagina = urllib.urlopen(url_atual)
	for linha in pagina:
		if (linha.find("  Mensagem publicada  em ") != -1):
			m = re.search(r"(\d+/\d+/\d+)", linha)
			if (m != None):
				dates.append(m.group(1))
				
				
				#print m.group(1)

dic_datas = {}
for i in range(0, len(dates)):
	dic_datas[dates[i]] = 1

for i in range(0, len(dates)):
	dic_datas[dates[i]] += 1

#print "linha de separacao-----------------------------------------------"
#print dic_datas


#for x in dic_datas:
	#print x +" "+ str(dic_datas[x])

arq = open("unsorteddates.txt", "w")
for x in dic_datas:
	arq.write(x +" "+ str(dic_datas[x]) +"\n")
arq.close()

ordena_arquivo("unsorteddates.txt")
print "Pronto!"
