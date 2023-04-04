from sys import argv
from chiffrement import *
from dechiffrement import *
import time



def attaque(couple1,couple2):
	"""
	Affiche les couples de clés potentiels en prenant en paramètre 2 couples clair-chiffré (int)
	Le calcul est fait en plusieurs étapes :
	- Pour les clés k1 de 0 à 2^24-1 on stocke la clé k1 dans la liste lm à l'indice lm[chiffré produit par k1 et clair1]
		On a donc la relation lm[PRESENT24(k1)(clair1)] = k1
	-Ensuite pour chaque clé k2 de 0 à 2^24-1, on calcule clair = PRESENT24-1(k2)(chiffre1)
		si ce clair correspond à un chiffré dans la liste lm, c'est à dire si lm[chiffré] =/= vide
		on sait que ce couple de clés produisent le même message avec clair1 et chiffre1, donc on le stocke dans collisions
	-Enfin on calcule 2PRESENT24 avec k1 et k2 sur le clair2 et on teste si on retrouve bien chiffre2
	"""

	collisions = []
	#lm : dict de listes vides, la liste a pour indice tous les messages possibles
	lm = {k: [] for k in range(1<<24)}
	for cle in range(1<<24):
		#chaque clé est ajoutée au tableau à l'indice correspondant au message qu'elle produit
		lm[chiffrement(couple1[0],cle)].append(cle)
	for cle in range(1<<24):
		c = dechiffrement(couple1[1],cle)
		if lm[c] != []: #si ce clair est aussi un chiffré produit par une des clés k1
			for k1 in lm[c]: #pour chaque clé produisant ce chiffré
				collisions.append((k1,cle)) #on stocke ce couple
	print("Nombre de collisions : " + str(len(collisions)))
	for couple in collisions:
		#on teste pour chaque clé qui produisent des sorties identiques
		if chiffrement(chiffrement(couple2[0],couple[0]),couple[1]) == couple2[1]:
			print(str(hex(couple[0])) + " " + str(hex(couple[1])))



########## CLI #########
if (len(argv)>5) and (argv[1] == "attaque"):
	couple1 = [int(argv[2], 16), int(argv[3], 16)]
	couple2 = [int(argv[4], 16), int(argv[5], 16)]
	attaque(couple1, couple2)



