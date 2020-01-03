============
port_scanner
============

Description:
============
port_scanner est un scanner de port simple à utiliser qui sort ses résultats en une page HTML.

Dépendances:
============
python    -> Interpreteur Python (v2 or 3)
nmap      -> Scan
vulscan   -> Script de Scan de Vulnérabilités (Module Nmap)
xsltproc  -> Génération de HTML

Dépendances d'installation:
===========================
setuptools      -> Outil de packaging python
pip (optionnel) -> Installeur de packages

Dépendances de tests:
=====================
ip  -> Création, modification et destruction de Linux Network Namespaces
tox -> Automatisation de création de virtualenvs pour les tests

Instructions d'utilisation:
===========================
usage: port_scanner [options] cible(s)
usage détaillé: port_scanner [-h] [-o OUTFILE] (-f INFILE | target [target ...])

options:
  -h, --help  affiche un message d'aide et quitte
  -o OUTFILE  écris le résultat du programme dans le fichier OUTFILE.
              Vaut scan.html par default

cible(s):
port_scanner prend une liste de cibles à scanner en argument.
Une cible peut être un host, une addresse IP, un réseau...
Ex: port_scanner scanme.nmap.org
Ex: port_scanner microsoft.com/24 192.168.0.1
Alternativement, une liste de cibles peut être lue depuis un fichier, avec l'option:
-f INFILE
Ex: port_scanner -f cibles.txt

port_scanner peut déterminer l'addresse MAC des machines cibles dans un réseau local, SEULEMENT SI il est exécuté en tant que super utilisateur.

port_scanner part du principe que le réseau utilisé est raisonnablement rapide et fiable afin d'accélerer le processus.

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
2) Extraire l'archive
Ex: tar -xvf exercise.tgz
3) Se placer dans le dossier extrait
Ex: cd exercise
4) Installer
Ex (avec pip): pip install .
Ex (sans pip): python ./setup.py install

Instructions de tests:
======================
La plupart des tests d'intégration utilisent les Linux Network Namespaces.
Pour pouvoir les créer, utiliser et supprimer,
les tests nécessitent d'être lancés sous Linux en tant que super utilisateur.

Vérifier que les dépendances de port_scanner sont bien installées.
Vérifier que les dépendances de tests sont bien installées.
Se placer dans le répertoire d'extraction et lancer tox.
Ex: cd exercise && sudo tox
