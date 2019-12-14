============
port-scanner
============

Description:
============
port-scanner est un scanner de port simple à utiliser qui sort ses résultats en une page HTML.

Dépendances:
============
nmap      -> Scan
xsltproc  -> Génération de HTML

Instructions d'utilisation:
===========================
Usage: port-scanner [cible...] [options]

port-scanner prend une liste de cibles à scanner en argument.
Une cible peut être un host, une addresse IP, un réseau...
Ex: port-scanner scanme.nmap.org
Ex: port-scanner microsoft.com/24 192.168.0.1
Ex: port-scanner 10.0.0-255.1-254
-iL <inputfilename>: Alternativement, une liste de cibles peut être lue depuis un fichier.
Ex: port-scanner -iL cibles.txt

port-scanner peut déterminer l'addresse MAC des machines cibles dans un réseau local, SEULEMENT SI il est exécuté en tant que super utilisateur.

port-scanner transmet toute option passée en argument à nmap.
Aussi toute option définie dans nmap(1) qui ne rentre pas en conflit avec les options ajoutées d'office par port-scanner (cf. Implémentation) peuvent être ajoutées en paramètre de port-scanner.

Instructions de déploiement:
============================

Instructions de tests:
======================

Implémentation:
======
port-scanner fait l'appel à nmap suivant:
nmap -v -sV -oX file args
où file est un fichier xml temporaire et args sont les arguments passés à port-scanner
