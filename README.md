# Projet 1 : Network Security Toolkit

Un scanner de ports TCP multi-threadé simple, écrit en Python. Ce projet utilise les modules natifs 'socket', 'threading', 'argparse', 'queue' et 'csv'.

* Ce projet a été réalisé dans le cadre d'un apprentissage personnel pour monter en compétences en Python appliqué à la sécurité réseau. *

## Fonctionnalités

* **Scan multi-threadé** : Utilise une file d'attente ('Queue') et des 'Threads' pour scanner des milliers de ports très rapidement.
* **Interface CLI** : Accepte une IP cible, une plage de ports ('1-1024') ou une liste de ports ('22,80,443').
* **Banner Grabbing** : Tente d'identifier le service qui tourne sur un port ouvert en récupérant sa "bannière".
* **Export CSV** : Sauvegarde automatiquement les résultats (Port, Service/Bannière) dans un fichier '.csv' nommé d'après l'IP cible.

## Avertissement Légal

Cet outil est conçu **uniquement à des fins éducatives**. N'utilisez cet outil que sur des réseaux et systèmes pour lesquels vous avez une autorisation explicite (par exemple, vos propres machines, des labs de type TryHackMe, ou des hôtes de test comme 'scanme.nmap.org').

## Utilisation

1.  Clonez le dépôt :
    '''bash
    git clone [https://github.com/TON_NOM/network-security-toolkit.git](https://github.com/TON_NOM/network-security-toolkit.git)
    cd network-security-toolkit
    '''

2.  (Optionnel mais recommandé) Créez un environnement virtuel :
    '''bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows: venv\Scripts\activate
    '''

3.  Lancez le script. L'IP cible est obligatoire.

### Exemples de commandes

**Scanner les 1024 ports par défaut (rapide) :**
'''bash
python scanner.py scanme.nmap.org
'''

**Scanner une plage de ports spécifique :**
'''bash
python scanner.py 127.0.0.1 -p 1-100
'''

**Scanner une liste de ports précise avec plus de threads :**
'''bash
python scanner.py 192.168.1.1 -p 22,80,443,8080 -t 200
'''

## Exemple de Sortie

Le script affiche les résultats en temps réel dans la console et génère un fichier '.csv' à la fin.

**Sortie Console :**
'''
Scan de scanme.nmap.org sur 1-1024 avec 100 threads...
[+] Port 22 Ouvert - Service : SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13...
[+] Port 80 Ouvert - Service : Apache/2.4.7 (Ubuntu)...
[+] Port 53 Ouvert - Service : Inconnu...
[+] Port 443 Ouvert - Service : Inconnu...

--- Scan Terminé ---

Sauvegarde des résultats dans scanme.nmap.org_scan_results.csv...
Sauvegarde terminée.
'''

**Fichier 'scanme.nmap.org_scan_results.csv' :**

| Port | Service/Bannière |
| :--- | :--- |
| 22 | 'SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13' |
| 53 | 'Inconnu' |
| 80 | 'Apache/2.4.7 (Ubuntu)' |
| 443 | 'Inconnu' |
