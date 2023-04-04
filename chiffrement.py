from sys import argv

#liste de substitution du PRESENT24
#sbox[i] => nouvelle valeur du mot i
sbox = [0xc,5,6,0xb,9,0,0xa,0xd,0x3,0xe,0xf,8,4,7,1,2]


#message : message (entier) à chiffrer de taille 24 bits
#cle : clé (entier)
#Renvoie le chiffré (entier)
def chiffrement(etat, cle):
	"""
	Entrée : message à chiffrer (int) et clé (int)
	Sortie : PRESENT24(cle)(message)
	Le chiffré est produit en cadençant la clé
	Ensuite pour chaqur tour, les bits du message sont substitués puis 
	permutés et XORé à la sous-clé du tour correspondant
	"""
	k = cadencement(cle)
	for i in k:
		etat = permutation(substitution(etat, sbox))^i
	return etat



def permutation(value):
	"""
	value : suite de bits (entier) de 24 bits à permuter
	Renvoie l'entier dont les bits ont été permutés
	"""
	value = permutation_step(value, 0x00001100, 16)
	value = permutation_step(value, 0x000c080c, 4)
	value = permutation_step(value, 0x00220022, 2)
	value = permutation_step(value, 0x10144114, 1)
	value = permutation_step(value, 0x21121212, 2)
	value = permutation_step(value, 0x08090606, 4)
	value = permutation_step(value, 0x000c0030, 8)
	value = permutation_step(value, 0x00000c3c, 16)
	return value


def permutation_step(value, mask, shift):
	result = ((value >> shift) ^ value) & mask
	return (value ^ result) ^ (result << shift)



def substitution(entree, liste_substitution):
	"""
	entree : suite de 24 bits (entier) à substituer
	Renvoie l'entier substitué
	"""
	sortie = 0
	mask = 0xf
	for i in [0, 4, 8, 12, 16, 20]:
		#les 4 derniers bits sont passés à sbox puis sont insérés à la sortie
		sortie += liste_substitution[entree & mask] << i
		entree = entree >> 4
	return sortie



def cadencement(K):
	"""
	Renvoie une liste contenant les 11 sous-cĺés à partir de la clé 'maitre'
	"""
	resultat = []
	K <<= 56
	for i in range(1,11):
		K = (K << 61) & 0xffffffffffffffffffff | K >> 19
		K = (sbox[K >>76] << 76) + ( K & 0xfffffffffffffffffff)
		K ^= i << 15
		resultat.append(K>>16 & 0xffffff)
	#resultat.append(K>>16 & 0xffffff) #derniere sous clé
	return resultat

########## CLI #########

if (len(argv)>3) and (argv[1] == "chiffrement"):
	message = int(argv[2], 16)
	cle1 = int(argv[3], 16)
	chiffre = chiffrement(message, cle1)
	if len(argv)>4:
		cle2 = int(argv[4], 16)
		chiffre = chiffrement(chiffre, cle2)
	print(hex(chiffre))
