from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcrJWXq8if2AnRr1glQtPXSJDx4NDHTx0IohuLCnzJ1WCU0U2CRn5yZEUOBdstaHWbEqUv9ftp7KmLI41LomMUebqunnfDQpqA2qewViHN8vOmACc-1cgo8tjrFKdMsu47Fb9Lh7MfTWivoHbyp6UYv7AkPFmIn2EhH_xKczJvTNl2_71ez-nbcONSOHH7ps5e8SkW'

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
