# PRESENT24

## USAGE

Pour chiffrer/déchiffrer un message de 24 bits, il faut exécuter le fichier chiffrement.py/dechiffrement.py avec comme arguments le message/chiffré, la première clé et éventuellement la seconde clé pour le chiffrement 2PRESENT24. Les messages, chiffrés et clés sont en format hexadécimal
Pour lancer l'attaque, il suffit d'entrer les deux couples clair/chiffré à la suite

### CLI

    python chiffrement.py chiffrement <message> <clé 1> [<clé 2>]
    python dechiffrement.py dechiffrement <chiffré> <clé 1> [<clé 2>]
    python attaque.py attaque <clair 1> <chiffré 1> <clair 2> <chiffré 2>

### Make
