from sys import argv
from chiffrement import *


def liste_inversion(liste):
	inversee = [None]*len(liste)
	for i in range(len(liste)):
		inversee[liste[i]] = i
	return inversee

#Version des listes utilisées pour le déchiffrement
sbox_inverse = liste_inversion(sbox)

def inverse_permutation(value):
    value = permutation_step(value, 0x540540, 1)
    value = permutation_step(value, 0x333000, 2)
    value = permutation_step(value, 0xc30, 16)
    value = permutation_step(value, 0x409050a, 4)
    value = permutation_step(value, 0x480084, 8)
    value = permutation_step(value, 0x004812, 16)
    value = permutation_step(value, 0x122112, 2)
    value = permutation_step(value, 0x505050, 1)
    return value

def dechiffrement(etat, cle):
	"""
	message : message (entier) à déchiffrer de taille 24 bits
	cle : clé (entier)
	Renvoie le clair (entier)
	les étapes du chiffrement sont effectuées dans l'ordre inverse
	"""
	k = cadencement(cle)
	for i in range(9,-1,-1):
		etat = substitution(inverse_permutation(etat^k[i]),sbox_inverse)
	return etat


########## CLI #########
if (len(argv)>3) and (argv[1] == "dechiffrement"):
	chiffre = int(argv[2], 16)
	if len(argv)>4:
		cle2 = int(argv[4], 16)
		chiffre = dechiffrement(chiffre, cle2)
	cle1 = int(argv[3], 16)
	message = dechiffrement(chiffre, cle1)
	print(hex(message))


