from requests import get
import socket
import os



# Color
green = "\x1b[32m"
blue = "\x1b[34m"
red = "\x1b[31m"
orange = "\x1b[38;5;220m"
reset = "\x1b[0m"

if os.name.lower() == "posix":
    _os_ = "MAC"
    print(f"{green} [+] System Mac OS")
    try:
        output = os.popen('openssl version').read()
        if output.split(' ')[0] in ["LibreSSL", "OpenSSL"]:
            print(" [+] OpenSSL is installed")
    except:
        print(f"{red} [-] Error SSL\n     Try 'sudo apt install openssl'")
        exit(0)
elif os.name.lower() == "nt":
    _os_ = "WIN"
    print(f"{green} [+] System Windows")
    try:
        output = os.popen('openssl version').read()
        if output.split(' ')[0] in ["LibreSSL", "OpenSSL"] :
            print(" [+] OpenSSL is installed")
    except:
        print(f"{red} [-] Error SSL\n     Try to install Open SLL from 'https://slproweb.com/products/Win32OpenSSL.html' or another site...\n     Then copy that in cmd 'set PATH=%PATH%;C:\Program Files\OpenSSL-Win64\bin\'")
        exit(0)
else:
    print("Your OS is not reconize, ERROR can be detected")

#Start Generation
if True:
    """
    CA = Certificate Authority
        Organisme responsable de signer un certificat
    
    Cert = Certificat
        Certificat individuel

    -- CA GENERATION -- 
    openssl genrsa -aes256 -out ca-key.pem 4096
    openssl req -new -x509 -sha256 -days 365 -key ca-key.pem -out ca.pem
    -------------------

    -- CERT GENERAT. --
    openssl genrsa -out cert-key.pem 4096
    openssl req -new -sha256 -subj "/CN=<CN NAME>" -key cert-key.pem -out cert.csr
    echo "subjectAltName=IP:<IP SERVER>" >> extfile.cnf
    openssl x509 -req -sha256 -days 365 -in cert.csr -CA ca.pem -CAkey ca-key.pem -out cert.pem -extfile extfile.cnf -CAcreateserial
    -------------------

    (( Outfile ))
    ______
    I-- CA
        I-- ca-key.pem    (private key to CA)
        I-- ca.pem        (authority certificate)
    I-- CERT
        I-- cert-key.pem  (private key to cert)
        I-- cert.pem      (certificate)
    ______


    (( Way of working ))
    ______
    I-- Server
        I-- cert.pem      (Public key + Authentication)                                 || cert-server.pem ||
        I-- cert-key.pem  (Private key lik to cert.pem public key)                      || cert-key.pem    ||
    I-- Client
        I-- ca.pem        (To check out the cert.pem authentication provide by server)  || ca-cert.pem     ||
    ______
    """
    # REPOSITORY
    try:
        print(f"{green} [+] Repesitory Generation")
        os.mkdir("CA")
        os.mkdir("CERT")
    except:
        print(f"{red} [-] Error Repesitory Generation (CA & CERT Directory)\n     Create these directories by yourselves if they don't already exist")
    
    #-----------------------------#

    # CA KEY
    try:
        print(f"{green} [+] CA KEY Generation ({orange}enter a pass-phrase{green}){reset}")
        os.system("openssl genrsa -aes256 -out CA/ca-key.pem 4096")
    except:
        print(f"{red} [-] Error CA KEY Generation \n     Check if you enter a passphrase")
        exit(0)
    
    # CA CERT
    try:
        print(f"{green} [+] CA CERT Generation")
        print(f"     {orange}Complete the form{reset} (All, except 1 & 2, can stay empty)")
        os.system(f"openssl req -new -x509 -sha256 -days 365 -key CA/ca-key.pem -out CA/ca-cert.pem")
    except:
        print(f"{red} [-] Error CA Generation \n     Check this 'openssl req -new -x509 -sha256 -days 365 -key CA/ca-key.pem -out CA/ca-cert.pem'")
        exit(0)
    
    #-----------------------------#

    # CERT SERVER KEY 
    try:
        print(f"{green} [+] CERT KEY Generation{reset}")
        os.system(f"openssl genrsa -out CERT/cert-key.pem 4096")
    except:
        print(f"{red} [-] Error CA Generation \n     Check this 'openssl genrsa -out CERT/cert-key.pem 4096'")
        exit(0)
    
    # CERT SERVER QUERY
    # (demande en attente de signature)
    try:
        print(f"{green} [+] CERT SERVER QUERY Generation")
        cn_name = str(input(f"     {orange}Enter CN Name : {reset}"))
        os.system(f"openssl req -new -sha256 -subj \"/CN={cn_name}\" -key CERT/cert-key.pem -out CERT/cert-query.csr")
    except:
        print(f"{red} [-] Error CERT SERVER QUERY Generation \n     Check this 'openssl req -new -sha256 -subj \"/CN=<CN_NAME>\" -key CERT/cert-key.pem -out CERT/cert-query.csr'")
        exit(0)
    
    # CERT SERVER IP
    try:
        print(f"{green} [+] CERT SERVER IP extfile")
        try:
            hostname=socket.gethostname()
            your_ip=socket.gethostbyname(hostname)
        except:
            your_ip = ""
        try:
            your_ip_public = get('https://api.ipify.org').content.decode('utf8')
        except:
            your_ip_public = ""
        print(f"{reset}     Your current local IP is {orange}{your_ip}{reset}\n          current public IP   {orange}{your_ip_public}")
        _ip_ = str(input(f"     {orange}Enter SERVER IP : {reset}")).split("\n")[0]
        os.system(f"echo \"subjectAltName=IP:{_ip_}\" > CERT/extfile.cnf")
    except:
        print(f"{red} [-] Error CERT SERVER IP extfile \n     Create a extfile.cnf in CERT directory, then write this inside 'subjectAltName=IP:<SERVER_IP>'")
        exit(0)
    
    # CERT SERVER GENERATION
    try:
        print(f"{green} [+] CERT SERVER Generation{reset}")
        os.system(f"openssl x509 -req -sha256 -days 365 -in CERT/cert-query.csr -CA CA/ca-cert.pem -CAkey CA/ca-key.pem -out CERT/cert-server.pem -extfile CERT/extfile.cnf -CAcreateserial")
    except:
        print(f"{red} [-] Error CERT Generation \n     Check this 'openssl x509 -req -sha256 -days 365 -in CERT/cert-query.csr -CA CA/ca-cert.pem -CAkey CA/ca-key.pem -out CERT/cert-server.pem -extfile CERT/extfile.cnf -CAcreateserial'")
        exit(0)
    
    #-----------------------------#

    # REMOVE FILE
    try:
        print(f"{green} [+] Remove file")
        os.remove("CERT/cert-query.csr")
        os.remove("CERT/extfile.cnf")
    except:
        print(f"{red} [-] Error Remove file \n     Remove CERT/cert-query.csr and CERT/extfile.cnf by your-self")
        exit(0)
    print("  [+] END SUCCESFULLY")
    
if _os_ == "MAC":
    print(f"{blue} LAST STEP ON CLIENT PC\n Now you have to add CA/ca.pem file into your key bundle\n Then click on 'always trust this certificate' and it's done")
elif _os_ == "WIN":
    print(f"{blue} LAST STEP ON CLIENT PC\n To trust the Certificate Authority (CA), open Administrator PowerShell\n Then copy 'Import-Certificate -FilePath \".CA\ca.pem\" -CertStoreLocation Cert:\LocalMachine\Root'")

    

    
    
