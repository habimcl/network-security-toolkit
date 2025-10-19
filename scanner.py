import socket
import sys
import argparse #biibliothèque pour la CLI
from queue import Queue # Pour la file d'attente
import threading # Pour les serveurs

# Variables globales
open_ports = []
# Verrou pour sécuriser l'écriture dans la liste open_ports.
list_lock = threading.Lock()

def check_port(ip,port):
    """ Tente de se connecter à une IP sur un port donné.
    Renvoie True si le port est ouvert, False sinon.
    Note : Cette fonction est maintenant silencieuse.
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

# Nouvelle fonction : le travailleur
def worker(queue, ip):
    """
    C'est la fonction que chaque thread va éxecuter. Elle prend un port dans la file, le scanna et recommence.
    """

    while not queue.empty():
        port = queue.get()

        # On scanne le port
        if check_port(ip, port):
            # Si c'est ouvert on utilise le verrou pour écrire dans la liste
            with list_lock:
                print(f"[+] Port {port} (TCP) est Ouvert")
                open_ports.append(port)
        # On indique à la file que cette tâche est terminée.
        queue.task_done()

def main():
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
        ports_to_scan=map(int,port_range_str(','))

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

    #On trie la lsite pour un affichage plus propre
    open_ports.sort()

    if open_ports:
        print("Ports ouverts trouvés:")
        for port in open_ports:
            print(f" Port{port} (TCP)")
    else:
        print("Aucun port ouvert trouvé")

if __name__ == "__main__":
    main()
