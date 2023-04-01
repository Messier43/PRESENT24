from sys import argv

#liste de substitution du PRESENT24
#sbox[i] => nouvelle valeur du mot i
sbox = [0xc,5,6,0xb,9,0,0xa,0xd,0x3,0xe,0xf,8,4,7,1,2]

#liste de permutation du chiffrement du PRESENT24
#liste[i] => nouvelle position du bit i
liste_permutation = [0,6,12,18,1,7,13,19,2,8,14,20,3,9,15,21,4,10,16,22,5,11,17,23]


#message : message (entier) à chiffrer de taille 24 bits
#cle : clé (entier)
#Renvoie le chiffré (entier)
def chiffrement(message, cle):
	k = cadencement(cle)
	etat = message
	for i in range(1,11):
		etat = permutation(substitution(etat^k[i-1], sbox), liste_permutation)
	return etat ^ k[10]


#entree : suite de bits (entier) de 24 bits à permuter
#permutations : liste de permutation
#Renvoie l'entier dont les bits ont été permutés
def permutation(entree, permutations):
	sortie = 0
	mask = 1 << 23
	for i in range(24):
		#Pour chaque bit entrée à 1, on ajoute 1 à la position indiquée dans la liste
		sortie += (mask & entree) and (1 << 23-permutations[i])
		mask >>= 1
	return sortie


#entree : suite de 24 bits (entier) à substituer
#Renvoie l'entier substitué
def substitution(entree, liste_substitution):
	sortie = 0
	mask = 0xf
	for i in range(6):
		#les 4 derniers bits sont passés à sbox puis sont insérés à la sortie
		sortie += liste_substitution[entree & mask] << 4*i
		entree = entree >> 4
	return sortie


#Rotation gauche d'un entier 'nombre' de taille 'taille' sur 'decalage' bits
def rotation_gauche(nombre, decalage, taille):
	mask_taille_limite = (1 << taille) -1
	return ((nombre << decalage) & mask_taille_limite) | (nombre >> (taille - decalage))


#Renvoie une liste contenant les 11 sous-cĺés à partir de la clé 'maitre'
def cadencement(maitre):
	resultat = []
	K = maitre << 56
	for i in range(1,11):
		resultat.append(K>>16 & 0xffffff)
		K = rotation_gauche(K,61,80)
		K = (sbox[K >>76] << 76) | (~(0xf<<76) & K)
		K ^= i << 15
	resultat.append(K>>16 & 0xffffff) #derniere sous clé
	return resultat




###NON UTILISE###
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
################


########## TEST #########
def tests_chiffrement(num_test):
	match num_test:
		case 0: #Substitution
			print(hex(substitution(0x30000f,sbox)))
		case 1: #Permutation
			print(bin(permutation(0x888888,liste_permutation)))
		case 2: #Rotation Gauche
			print(bin(rotation_gauche(0b111010000,3,9)))
		case 3:
			res = cadencement(0)
			print([hex(x) for x in res])
		case 4:
			print(hex(chiffrement(0xf955b9,0xd1bd2d)))
#tests_chiffrement(int(argv[1]))

if (len(argv)>3) and (argv[1] == "chiffrement"):
	message = int(argv[2], 16)
	cle1 = int(argv[3], 16)
	chiffre = chiffrement(message, cle1)
	if len(argv)>4:
		cle2 = int(argv[4], 16)
		chiffre = chiffrement(chiffre, cle2)
	print(hex(chiffre))
