import socket
import sys
import argparse #biibliothèque pour la CLI
from queue import Queue # Pour la file d'attente
import threading # Pour les serveurs
import csv

# Variables globales
open_ports_info = [] #stockera des (port, bannière)

# Verrou pour sécuriser l'écriture dans la liste open_ports.
list_lock = threading.Lock()

def check_port(ip,port):
    """ 
    Tente de se connecter à une IP sur un port donné.
    Renvoie True si le port est ouvert, False sinon.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.0)

    try:
        if sock.connect_ex((ip,port)) == 0:
            return True
        else:
            return False
    finally:
        sock.close()

# Nouvelle fonction : grab_banner pour demander la bannière du port
def grab_banner(ip,port):
    """
    Tente de récupérer la "bannière" d'un service sur un port ouvert.
    """
    try:
        # On crée un socket comme dans check_port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2.0) #on lui lasse 2s pour répondre
            sock.connect((ip, port))

            # On envoie des données factices pour provquer une réponse.
            # Un 'GET' simple marche souvent pour les services web (HTTP).
            # D'autres services (FTP, SSH) envoient la bannière dès la connexion.
            sock.send(b'GET / HTTP/1.1\r\nHost: ' + ip.encode() + b'\r\n\r\n')

            # On écoute la réponse (max 1024 bytes)
            banner_bytes = sock.recv(1024)

            # On décode la réponse en texte en ignorant les erreurs
            banner_text = banner_bytes.decode(errors='ignore').strip()

            # On ne garde que la première ligne pour que ce soit propre
            return banner_text.split('\n')[0]
    except Exception:
        #Si ça échoue (port SSL, service muet, etc.), on renvoie "Inconnu"
        return "Inconnu"
    
# Nouvelle fonction : le travailleur
def worker(queue, ip):
    """
    C'est la fonction que chaque thread va éxecuter. 
    """

    while not queue.empty():
        port = queue.get()

        # On scanne le port
        if check_port(ip, port):
            # Le port est ouvert ! On va chercher la bannière.
            banner = grab_banner(ip, port)

            with list_lock:
                # On affiche direct pour avoir un retour
                # On limite la bannière à 50 caractères pour l'affichage
                print(f"[+] Port {port} Ouvert - Service : {banner[:50]}...")

                # On stocke le TUPLE (port, bannière)
                open_ports_info.append((port, banner))

        # On indique à la file que cette tâche est terminée.
        queue.task_done()

def main():
    """
    Fonction principale du script.
    Analyse les arguments de la ligne de commande (IP, ports, threads),
    initialise la file d'attente, lance les threads de scan
    et sauvegarde les résultats dans un fichier CSV.
    """
    parser = argparse.ArgumentParser(description="Scanner de ports simple et rapide")

    parser.add_argument("ip", type=str, help="L'adresse IP cible à scanner")
    parser.add_argument("-p", "--ports", type=str, default="1-1024", help="La plage de ports à scanner (ex: '1-1024', '22,80,443')")

    #nouvel argument pour le nombre de threads
    parser.add_argument("-t", "--threads", type=int, default=100, help="Nombre de threads à utiliser (défaut: 100)")

    args= parser.parse_args()

    target_ip =args.ip
    port_range_str = args.ports
    num_threads = args.threads

    print(f"Scan de {target_ip} sur {port_range_str} avec {num_threads} threads...")

    # Logique pour parser la plage de ports (comme dernière version du code)

    ports_to_scan = []
    if '-' in port_range_str:
        start, end=map(int, port_range_str.split('-'))
        ports_to_scan = range(start, end+1)
    else:
        ports_to_scan=map(int,port_range_str.split(','))

    # Configuration et lancement du threading
    # Création de la file d'attente
    port_queue= Queue()

    #Remplissage de la file avec les ports à scanner
    for port in ports_to_scan:
        port_queue.put(port)
    
    # On lance les serveurs
    for _ in range(num_threads):
        #On crée un thread qui éxecuter la fonction worker
        t = threading.Thread(target=worker, args=(port_queue, target_ip), daemon= True)
        # 'daemon=True' signifie que le thread s'arrêtera si le script principal s'arrête
        t.start()

    # 4. Attendre que la file d'attente soit complètemment vide
    # .join() bloque le script ici jusqu'à ce que tous .task_donc() aient été appelés
    port_queue.join()

    # Fin du scan
    print("\n--- Scan Terminé ---")

    # On trie la liste par numéro de port (le premier élément du tuple)
    open_ports_info.sort(key=lambda x: x[0])

    # Affichage finale (on l'enlève on l'a déjà fait dans le worker)
    # On peut garder un résumé si on veut, mais c'est optionnel car tout est affiché en direct.

    if not open_ports_info:
        print("Aucun port ouvert trouvé.")
        sys.exit() # On quitte s'il n'y a rien à sauvegarder

    #On fait une sauvegarde CSV
    # On crée un nom de fichier dynamique
    output_file = f"{target_ip}_scan_results.csv"
    print(f"\nSauvegarde des résultats dans {output_file}...")

    try:
        with open(output_file, 'w', newline='') as f:
            #Crée un écrivain CSV
            writer = csv.writer(f)

            #Écrit la ligne d'en-tête
            writer.writerow(["Port", "Service/Bannière"])

            # Écrit toutes nos données (la liste de tuples) d'un coup
            writer.writerows(open_ports_info)
        
        print("Sauvegarde terminée.")
    
    except IOError as e:
        print(f"Erreur lors de l'écriture du fichier CSV : {e}")

if __name__ == "__main__":
    main()
