import socket
import sys
import argparse #biibliothèque pour la CLI

def check_port(ip, port):
    """
    Tente de se connecter à une IP sur un port donné.
    Renvoie True si le port est ouvert, False sinon.
    """
    # Crée un nouveau socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Définit un timeout court (ex: 1 seconde)
    sock.settimeout(1.0)

    # Tente la connexion
    try:
        # .connect_ex() renvoie 0 si la connexion réussit
        if sock.connect_ex((ip, port)) == 0:
            print(f"[+] Port {port} (TCP) est Ouvert")
            return True
        else:
            # Inutile de printer les ports fermés, ça pollue
            # print(f"[-] Port {port} (TCP) est Fermé")
            return False
    except socket.error as e:
        # Gère les erreurs (ex: impossible de résoudre l'IP)
        print(f"Erreur socket : {e}")
        return False
    finally:
        # Ferme toujours le socket
        sock.close()

def main(): # Configuration de l'analyseur d'arguments
    parser = argparse.ArgumentParser(description="Scanner de ports simple")

    # Ajoute les arguments
    parser.add_argument("ip", type=str, help="L'adresse IP cible à scanner")
    parser.add_argument("-p", "--ports", type=str, default="1-1024", help="La plage de ports à scanner (ex: '1-1024', '22,80,443')")

    args = parser.parse_args()

    target_ip = args.ip
    port_range_str = args.ports

    print(f"Scan de {target_ip} sur les ports : {port_range_str}")

    # -- Logique pour parser la plage de ports --
    ports_to_scan = []
    if '-' in port_range_str:
        # C'est une plage (ex: 1-1024)
        start, end = map(int, port_range_str.split('-'))
        ports_to_scan = range(start, end + 1)
    else :
        # C''eest une liste (ex : 22, 80, 443)
        ports_to_scan = map(int, port_range_str.split(','))

    # --- Lancement du scan ---
    print("\nRésultats :")
    for port in ports_to_scan:
        # On appelle la fonction de la session 1 
        check_port(target_ip, port)

if __name__ == "__main__":
    main()