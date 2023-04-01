from sys import argv
from chiffrement import *


def liste_inversion(liste):
	inversee = [None]*len(liste)
	for i in range(len(liste)):
		inversee[liste[i]] = i
	return inversee

#Version des listes utilisées pour le déchiffrement
liste_permutation_inverse = liste_inversion(liste_permutation)
sbox_inverse = liste_inversion(sbox)


#message : message (entier) à déchiffrer de taille 24 bits
#cle : clé (entier)
#Renvoie le clair (entier)
def dechiffrement(chiffre, cle):
	k = cadencement(cle)
	etat = chiffre ^ k[10]
	for i in range(10,0,-1):
		etat = substitution(permutation(etat, liste_permutation_inverse),sbox_inverse)^k[i-1]
	return etat




########## TEST #########
def tests_dechiffrement(num_test):
	match num_test:
		case 0:
			print(hex(dechiffrement(chiffrement(0xf955b9,0xd1bd2d),0xd1bd2d)))
		case 1: #Permutations
			print(hex(permutation(0x800002, liste_permutation)))
			print(hex(permutation(permutation(0x800002,liste_permutation), liste_permutation_inverse)))
		case 2: #substitutions
			print(hex(substitution(0x800002, sbox)))
			print(hex(substitution(substitution(0x800002, sbox), sbox_inverse)))

#tests_dechiffrement(int(argv[1]))

########## CLI #########
if (len(argv)>3) and (argv[1] == "dechiffrement"):
	chiffre = int(argv[2], 16)
	if len(argv)>4:
		cle2 = int(argv[4], 16)
		chiffre = dechiffrement(chiffre, cle2)
	cle1 = int(argv[3], 16)
	message = dechiffrement(chiffre, cle1)
	print(hex(message))


