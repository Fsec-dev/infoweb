#!/usr/bin/env python
# Coded by Andrew

import os, sys, random
import requests, socket
import subprocess
import json

__version__ = "1.0"
__author__ = "Andrew - Fsec-Dev"
__dateDev__ = "2020"

# Colores para la terminal (solo Linux)
R = "\033[1;31m" # Rojo
G = "\033[1;92m" # Verde
B = "\033[1m"    # Negrita
W = "\033[1;37m" # Negrita + Blanco
N = "\033[0m"	 # Escapar de la secuencia de colores

def banner():
	print G + """
---------------------------------------------------
\t_ _  _ ____ ____ _ _ _ ____ ___  
\t| |\\ | |___ |  | | | | |___ |__] 
\t| | \\| |    |__| |_|_| |___ |__]
---------------------------------------------------  
\t   - Information Gathering -
Version: {} Author: {} Release: {}        			
--------------------------------------------------- 				                 
	""".format(__version__, __author__, __dateDev__) + N

# Funcion encargada de lanzarnos un USERAGENT de forma aleatoria
def randomUA():
	UA = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
		  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5',
		  'Mozilla/5.0 (X11; FreeBSD amd64; rv:40.0) Gecko/20100101 Firefox/40.0',
		  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.49 Safari/537.36 OPR/48.0.2685.7',
		  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
		  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
		  'Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36']
	return random.choice(UA)

# Obteniendo la geolocalizacion del servidor
def geoip(target):
	url = "https://ipinfo.io/"+target+"/json"
	r = requests.get(url, headers={'User-agent':randomUA()})
	
	if r.status_code != 200:
			print "\nError {}\n".format(r.status_code)
	else:
		j = json.loads(r.content)

		ip = j['ip']
		city = j['city']
		region = j['region']
		geo = j['loc']
		isp = j['org']
		
		print """
IP: {}
Ciudad: {}
Region: {}
Geolocalizacion: {}
ISP: {}
		""".format(ip, city, region, geo, isp)

# Obteniendo fichero robots.txt de servidor
def readRobot(host):
	re = requests.get(host + "/robots.txt", headers={'User-agent':randomUA()})
	
	if re.status_code == 404:
		return "[-] Fichero robots.txt no encontrado"
	return re.text

def main(target):
	try:
		#Obteniendo ip del servidor
		ip = socket.gethostbyname(target.split("//")[1])
		print G + "[IP: {}]\n".format(ip) + N

		r = requests.get(target, headers={'User-agent':randomUA()})

		if r.ok:
			print G + "- HEADERS del Servidor -\n" + N

			for infoheaders in r.headers:
				print infoheaders + " : " + r.headers[infoheaders]
		else:
			print "[-] Error al conectarse con el servidor\nError: {}".format(r.status_code)
		
		#Obteniendo fichero robots.txt
		print G + "\n-- ROBOTS.txt --\n" + N
		print readRobot(target)

		print G + "\n-- Geolocacion del servidor --\n" + N
		geoip(ip)
		
		# Obteniendo datos WHOIS del servidor		
		print G + "\n-- WHOIS --\n" + N
		out = subprocess.Popen(["whois", ip], stdout=subprocess.PIPE).communicate()[0]
		print out

	except Exception as ex:
		print R + "\n[-] No se a podido establecer la conexion\n" + N
		print "Exception error: {}\n".format(ex)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		banner()
		print W + "\nUso: {} <target>\n".format(sys.argv[0]) + N
	else:
		if sys.argv[1] in ['--help', '-h']:
			banner()
			print W + "\nUso: {} <target>\n".format(sys.argv[0]) + N
			print W + "Ejemplo: {} https://www.google.com\n".format(sys.argv[0]) + N
		else:
			if not sys.argv[1].startswith("http") == True:
				main("http://" + sys.argv[1])
			else:
				main(sys.argv[1])
