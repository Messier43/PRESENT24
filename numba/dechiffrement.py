from sys import argv
from chiffrement import *


def liste_inversion(liste):
	inversee = [None]*len(liste)
	for i in range(len(liste)):
		inversee[liste[i]] = i
	return inversee

#Version des listes utilisées pour le déchiffrement
#liste_permutation_inverse = liste_inversion(liste_permutation)
#sbox = [0xc,5,6,0xb,9,0,0xa,0xd,0x3,0xe,0xf,8,4,7,1,2]
#sbox_inverse = liste_inversion(sbox)
#print(sbox_inverse)
@njit
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

#message : message (entier) à déchiffrer de taille 24 bits
#cle : clé (entier)
#Renvoie le clair (entier)
@njit
def dechiffrement(etat, cle):
	sbox_inverse = [5, 14, 15, 8, 12, 1, 2, 13, 11, 4, 6, 3, 0, 7, 9, 10]
	k = cadencementnmba(cle)
	for i in range(9,-1,-1):
		etat = substitution(inverse_permutation(etat^k[i]),sbox_inverse)
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


