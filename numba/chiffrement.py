from sys import argv
from numba import njit, jit
#liste de substitution du PRESENT24
#sbox[i] => nouvelle valeur du mot i
#sbox = [0xc,5,6,0xb,9,0,0xa,0xd,0x3,0xe,0xf,8,4,7,1,2]


#message : message (entier) à chiffrer de taille 24 bits
#cle : clé (entier)
#Renvoie le chiffré (entier)
@njit
def chiffrement(etat, cle):
	sbox = [0xc,5,6,0xb,9,0,0xa,0xd,0x3,0xe,0xf,8,4,7,1,2]
	k = cadencementnmba(cle)
	for i in k:
		etat = permutation(substitution(etat, sbox))^i
	return etat


#value : suite de bits (entier) de 24 bits à permuter
#Renvoie l'entier dont les bits ont été permutés
@njit
def permutation(value):
	value = permutation_step(value, 0x00001100, 16)
	value = permutation_step(value, 0x000c080c, 4)
	value = permutation_step(value, 0x00220022, 2)
	value = permutation_step(value, 0x10144114, 1)
	value = permutation_step(value, 0x21121212, 2)
	value = permutation_step(value, 0x08090606, 4)
	value = permutation_step(value, 0x000c0030, 8)
	value = permutation_step(value, 0x00000c3c, 16)
	return value

@njit
def permutation_step(value, mask, shift):
	result = ((value >> shift) ^ value) & mask
	return (value ^ result) ^ (result << shift)


#entree : suite de 24 bits (entier) à substituer
#Renvoie l'entier substitué
@njit
def substitution(entree, liste_substitution):
	sortie = 0
	mask = 0xf
	for i in [0, 4, 8, 12, 16, 20]:
		#les 4 derniers bits sont passés à sbox puis sont insérés à la sortie
		sortie += liste_substitution[entree & mask] << i
		entree = entree >> 4
	return sortie


#Rotation gauche d'un entier 'nombre' de taille 'taille' sur 'decalage' bits
def rotation_gauche(nombre, decalage, taille):
	mask_taille_limite = (1 << taille) -1
	return ((nombre << decalage) & mask_taille_limite) | (nombre >> (taille - decalage))


#Renvoie une liste contenant les 11 sous-cĺés à partir de la clé 'maitre'
def cadencement(K):
	resultat = []
	K <<= 56
	for i in range(1,11):
		K = (K << 61) & 0xffffffffffffffffffff | K >> 19
		K = (sbox[K >>76] << 76) + ( K & 0xfffffffffffffffffff)
		K ^= i << 15
		resultat.append(K>>16 & 0xffffff)
	#resultat.append(K>>16 & 0xffffff) #derniere sous clé
	return resultat

@njit
def cadencementnmba(maitre):
	sbox = [0xc,5,6,0xb,9,0,0xa,0xd,0x3,0xe,0xf,8,4,7,1,2]
	resultat = []
	k1 = maitre << 16
	k0 = 0
	for i in range(1,11):
		k1_next = ((k0 & 0x7ffff) << 21) + (k1 >> 19)
		k0_next = ((k1 & 0x7ffff) << 21) + (k0 >> 19)
		k1 = (sbox[k1_next >> 36] << 36) + (k1_next & 0xfffffffff)
		k0 = k0_next ^ (i<<15)
		resultat.append((k0 >>16) & 0xffffff )
	return resultat



###NON UTILISÉ###
'''
#liste de permutation du chiffrement du PRESENT24
#liste[i] => nouvelle position du bit i
liste_permutation = [0,6,12,18,1,7,13,19,2,8,14,20,3,9,15,21,4,10,16,22,5,11,17,23]

def permutation3(entree):
	sortie = 0
	bit_sortie=0
	for i in range(4): #colonne
		for i4 in range(i,24,4):
			# += plus rapide que |= ^=
			sortie += (((1<<i4) & entree ) and (1<< (bit_sortie)))
			bit_sortie += 1
	return sortie

def generation_sbox_large():
	sortie = []
	for k in range(6):
		sortie.append([(x<<k) for x in sbox])
	return sortie

sbox_large = generation_sbox_large()

def permutation_old(entree, permutations):
	sortie = 0
	mask = 1 << 23
	for i in range(24):
		#Pour chaque bit entrée à 1, on ajoute 1 à la position indiquée dans la liste
		sortie += (mask & entree) and (1 << 23-permutations[i])
		mask >>= 1
	return sortie
'''
################




########## TEST #########
def tests_chiffrement(num_test):
	match num_test:
		case 0: #Substitution
			print(hex(substitution(0x30000f,sbox)))
		case 1: #Permutation
			print(bin(permutation(0x888888)))
		case 2: #Rotation Gauche
			print(bin(rotation_gauche(0b111010000,3,9)))
		case 3:
			res = cadencement(0)
			print([hex(x) for x in res])
		case 4:
			print(hex(chiffrement(0xf955b9,0xd1bd2d)))
#tests_chiffrement(int(argv[1]))



########## CLI #########

if (len(argv)>3) and (argv[1] == "chiffrement"):
	message = int(argv[2], 16)
	cle1 = int(argv[3], 16)
	chiffre = chiffrement(message, cle1)
	if len(argv)>4:
		cle2 = int(argv[4], 16)
		chiffre = chiffrement(chiffre, cle2)
	print(hex(chiffre))
