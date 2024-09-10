import optparse  # Importation du module obsolète optparse (argparse est recommandé à la place)
import pxssh  # Importation de pxssh pour automatiser les connexions SSH

# Classe Client qui représente une connexion SSH à une machine distante
class Client:
    def __init__(self, host, user, password):
        # Initialisation de l'objet Client avec l'adresse du host, le nom d'utilisateur et le mot de passe
        self.host = host
        self.user = user
        self.password = password
        # Tentative de connexion SSH lors de l'initialisation de l'objet
        self.session = self.conect()  # Typo dans le nom de la méthode 'conect' (devrait être 'connect')
    
    # Méthode pour établir la connexion SSH
    def connect(self):
        try:
            s = pxssh.pxssh()  # Création d'une instance pxssh
            s.login(self.host, self.user, self.password)  # Tentative de connexion avec les informations d'identification
            return s  # Retourne l'objet pxssh si la connexion réussit
        except Exception as e:
            # Gestion des exceptions si la connexion échoue
            print(e)  # Affichage de l'exception
            print('error connecting')  # Message d'erreur pour signaler l'échec de la connexion
    
    # Méthode pour envoyer des commandes SSH et retourner la sortie de la commande
    def send_command(self, cmd):
        self.session.sendline(cmd)  # Envoie de la commande à la session SSH
        self.session.prompt()  # Attente de l'invite de commande
        return self.session.before  # Retourne la sortie de la commande exécutée
    
    # Méthode statique pour exécuter une commande sur tous les clients (botnet)
    def botnetcommand(command):
        for client in botnet:  # Parcours de tous les clients dans le botnet
            output = client.send_command(command)  # Envoi de la commande à chaque client
            print(f"output from {client.host}")  # Affichage du host
            print(f"[+] {output}")  # Affichage de la sortie de la commande
    
    # Méthode statique pour ajouter un client au botnet
    def add_client(host, user, password):
        client = Client(host, user, password)  # Création d'une nouvelle instance Client
        botnet.append(client)  # Ajout du client à la liste botnet

# Liste des clients (botnet) initialisée à vide
botnet = []

# Ajout d'un client au botnet avec les informations d'identification fournies
Client.add_client('your_host', 'username', 'password')

# Exécution de commandes sur tous les clients du botnet
Client.botnetcommand('uname -v')  # Exécute la commande 'uname -v' pour obtenir des informations sur le noyau
Client.botnetcommand('cat /etc/issue')  # Exécute la commande 'cat /etc/issue' pour afficher des informations sur le système


