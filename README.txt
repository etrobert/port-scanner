============
port-scanner
============

Description:
============
port-scanner est un scanner de port simple à utiliser qui sort ses résultats en une page HTML.

Dépendances:
============
python    -> Python Interpreter (v2 or 3)
nmap      -> Scan
vulscan   -> Script de Scan de Vulnérabilités (Module Nmap)
xsltproc  -> Génération de HTML

Instructions d'utilisation:
===========================
Usage: port-scanner [options] [cible...]

port-scanner prend une liste de cibles à scanner en argument.
Une cible peut être un host, une addresse IP, un réseau...
Ex: port-scanner scanme.nmap.org
Ex: port-scanner microsoft.com/24 192.168.0.1
Ex: port-scanner 10.0.0-255.1-254
Alternativement, une liste de cibles peut être lue depuis un fichier, avec l'option:
-iL <inputfilename>
Ex: port-scanner -iL cibles.txt

port-scanner peut déterminer l'addresse MAC des machines cibles dans un réseau local, SEULEMENT SI il est exécuté en tant que super utilisateur.

Option pour executer le scan CVE Vulscan avec votre propre base de donnée:
--script-args vulscandb=your_own_database
Ex: port-scanner --script-args vulscandb=./cve.csv scanme.nmap.org

port-scanner part du principe que le réseau utilisé est raisonnablement rapide et fiable afin d'accélerer le processus.

port-scanner transmet toute option passée en argument à nmap.
Aussi toute option définie dans nmap(1) qui ne rentre pas en conflit avec les options ajoutées d'office par port-scanner (cf. Implémentation) peuvent être ajoutées en paramètre de port-scanner.

Instructions de déploiement:
============================
1) Installer les dépendances
  a) python
    python est probablement disponible dans votre package manager.
    Pour plus d'indications ou si ça n'est pas le cas, suivre ces instructions:
    https://docs.python.org/3.8/using/index.html
  b) nmap
    nmap est probablement disponible dans votre package manager.
    Si non, il est possible de l'installer à partir des sources:
    https://nmap.org/book/install.html
  c) vulscan
    Suivre les instructions d'installation:
    https://github.com/scipag/vulscan#installation
  d) xsltproc
    xsltproc est probablement disponible dans votre package manager.
    Sous ArchLinux, installer les packages docbook-xml et docbook-xsl.
    Sinon, les sources et certains binaires sont disponibles ici:
    http://xmlsoft.org/XSLT/downloads.html
2) Extraire l'archive là où vous souhaitez installer port-scanner
3) Add port-scanner to the PATH
  Ajouter port-scanner dans un chemin du PATH.
  Sous Linux, se placer dans le répertoire où vous avez installé port-scanner puis:
  sudo ln -s `pwd`/port-scanner.py /usr/local/bin/port-scanner

Instructions de tests:
======================
port-scanner est un wrapper extremement léger autour de nmap et xsltproc.
En tant que tel, il ne possède pas de tests.

Implémentation:
======
port-scanner fait l'appel à nmap suivant:
nmap -v -sV -Taggressive --script=vulscan/vulscan.nse -oX file args
