# Sécurisation des Sockets avec SSL/TLS

Pour sécuriser une connexion socket, on a besoin d'un **certificat SSL server** signé par une Authorité de Certification (signé par une **CA**)
Comme la signature de CA officielle coute de l'argent, on va donc crée notre propre **CA** qui signera ensuite notre **certificat SSL server**.
Cette façon de procédé se nomme le *"self-signed certificate"* est consiste à auto-signé ses certificats.

Cette technique possède des avantages :
- gratuit
- personnalisable
- rend le SSL accessible à tous

Mais comporte 1 désavantage :
- Comme nous créons notre propre **CA**, il faut manipuler le PC client afin qu'il **fasse confiance** à notre **CA**

*Effectivement, comme nous avons crée notre CA, le PC client ne la connait pas et ne lui fait pas confiance... On doit palier à ça manuellement (voir ***Section5***)*

___________________________________

### SECTION 1 : Installation de OpenSSL

Sur MacOS, il faut installer l'outil [*homebrew*](https://brew.sh/) puis rentrer la commande :
````
brew install openssl
````

Sur Windows, il faut sélectionner l'installeur d' [*openSSL*](https://slproweb.com/products/Win32OpenSSL.html) adapté à votre machine. Ensuite vous devez ajouter le dossier OpenSSL au Path...
- Session unique (cmd)

````
set PATH=%PATH%;C:\Program Files\OpenSSL-Win64\bin\
````
- Modification Permanante

````
1. Panneau de Configuration
2. Système
3. Modifier les variables d'environnement pour votre compte
4. Selectionner PATH
5. Modifier
6. Nouveau
7. Valider
````

___________________________________

### SECTION 2 : Récap des fichiers

Mais avant voici un récap des fichiers que l'on va créer :
````
I-- SSL
    I-- CA
        I-- ca-key.pem         (Private Key of CA)
        I-- ca-cert.pem        (Public Certificate of CA)
    I-- CERT
        I-- cert-key.pem       (Private Key of Server)
        /:: cert-query.pem     (Requete de Certificat -> En attente de signature)
        /:: extfile.cnf        (IP server)
        I-- cert-server.pem    (Public Certificate of Server)
````
 
Dans le dossier SSL, on a 2 dossiers : le **CA** (pour l'Authorité de Certification) et le **CERT** (pour le certificat serveur). Les deux fichiers */::* sont des **fichiers temporaires** nécessaire pour la signature de *cert-server.pem*...
Une fois le certificat publique du serveur généré, on peut supprimer les fichiers temporaires qui ont servit à sa génération (soit *cert-query.pem* et *extfile.cnf*)

Ainsi on va créer les différents dossiers (*SSL*, *CA* et *CERT*)
````
mkdir SSL
cd SSL
mkdir CA
mkdir CERT
````
___________________________________

### SECTION 3 : Génération de la CA

On se déplace donc dans le dossier *CA* :
````
cd CA
````

1. Génération de la Clef Privée *du CA*
````
openssl genrsa -aes256 -out ca-key.pem 4096
````
2. Génération du Certificat Public CA
````
openssl req -new -x509 -sha256 -days 365 -key ca-key.pem -out ca-cert.pem
````

*Pour les informations à rentrer, seules le Country NAME et le State sont obligatoire*

___________________________________

### SECTION 4 : Génération du Certificat Serveur

On se déplace donc dans le dossier *CERT* :
````
cd ..
cd CERT
````

1. Génération de la Clef Privée *du Serveur*
````
openssl genrsa -out cert-key.pem 4096
````
2. Génération de la Demande de Certificat
````
openssl req -new -sha256 -subj "/CN=<CN NAME>" -key cert-key.pem -out cert-query.csr
````
3. Génération de extfile.cnf (précisant l'IP du serveur)
````
echo subjectAltName=IP:<IP-SERVER> > extfile.cnf
````
4. Signature de la requête de Certificat par la CA
````
openssl x509 -req -sha256 -days 365 -in cert-query.csr -CA ../CA/ca-cert.pem -CAkey ../CA/ca-key.pem -out cert-server.pem -extfile extfile.cnf -CAcreateserial
````
5. Suppression des fichiers temporaires
Sur MAC-OS
````
rm cert-query.csr
rm extfile.cnf
````
Sur Windows
````
del cert-query.csr
del extfile.cnf
````

Enfin, on peut vérifier que les fichier ont bien été crée en ouvrant l'explorateur de fichier :
`````
open .
explorer .
`````

___________________________________

### SECTION 5 : Faire confiance au CA

- Sur MAC OS
````
1. Trousseaux d'accès
2. Fichier > Nouveau Trousseau
3. Fichier > Importer des éléments... > ca-cert.pem
4. Double clique sur le Certificat Publique de la CA
5. Se fier >  Toujours approuver
6. Valider (en fermant l'application)
````

- Sur Windows (*dans un PowerShell ADMIN*)
````
Import-Certificate -FilePath .\ca-cert.pem -CertStoreLocation Cert:\LocalMachine\Root
````


