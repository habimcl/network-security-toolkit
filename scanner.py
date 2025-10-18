import socket
import sys

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

# --- Section de Test ---
if __name__ == "__main__":
    target_ip = "127.0.0.1"  # Ton propre PC (localhost)

    print(f"Scan de {target_ip}...")

    # Teste quelques ports
    check_port(target_ip, 80)  # Port HTTP (probablement fermé)
    check_port(target_ip, 443) # Port HTTPS (probablement fermé)
    check_port(target_ip, 22)  # Port SSH (peut-être ouvert ?)

    # Teste un site qui le permet
    target_ip_public = "scanme.nmap.org"
    print(f"\nScan de {target_ip_public}...")
    check_port(target_ip_public, 22) # Devrait être ouvert
    check_port(target_ip_public, 80) # Devrait être ouvert
    check_port(target_ip_public, 81) # Devrait être fermé