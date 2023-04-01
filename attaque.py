from sys import argv
from chiffrement import *
from dechiffrement import *
import time
import pickle


def generation_listes(clair,chiffre):
	start = time.time()
	lm, lc = [[] for x in range(1<<24)],[[] for x in range(1<<24)]
	print("Listes Lm et Lc allouées en "+str(time.time()-start)+ " s, génération des listes ...")
	start = time.time()
	for cle in range(1<<22):
		lm[chiffrement(clair,cle)].append(cle)
	print("Liste Lm générée")
	for cle in range(1<<22):
		lc[dechiffrement(chiffre,cle)].append(cle)
	print("Clés générées en "+str(time.time()-start))
	return [lm,lc]


def trouver_collision(lmlc):
	collisions = []
	for i in range(1<<22):
		if (lmlc[0][i] !=[]) and (lmlc[1][i] != []) :
			collisions.append((lmlc[0][i],lmlc[1][i]))
	return collisions


def tests_cle(clair2, chiffre2, collisions):
	resultats = []
	for couple in collisions:
		for k1 in couple[0]:
			for k2 in couple[1]:
					if chiffrement(chiffrement(clair2,k1),k2) == chiffre2:
						resultats.append([k1,k2])
						#print(str(hex(k1))+" "+str(hex(k2)))
	return resultats

def attaque(couple1, couple2):
	collisions = trouver_collision(generation_listes(couple1[0],couple1[1]))
	return tests_cle(couple2[0], couple2[1], collisions)


########## CLI #########
if (len(argv)>5) and (argv[1] == "attaque"):
	couple1 = [int(argv[2], 16), int(argv[3], 16)]
	couple2 = [int(argv[4], 16), int(argv[5], 16)]
	cles = attaque(couple1, couple2)
	for couple in cles:
		print(str(hex(couple[0]))+" "+str(hex(couple[1])))




'''

########## TEST #########
fListes = open("listes","xb")

listes = generation_listes(0x2dc245,0x3d9a4e)

####Sérialisation####
pickle.dump(listes,fListes)
fListes.close()



#####TEST#####
fListes = open("listes","br")
listes = pickle.load(fListes)

maxlen=0
for i in range(1<<24):
	if len(listes[1][i]) > maxlen:
		maxlen = len(listes[1][i])
print(maxlen)


fCollisions = open("collisions2","xb")
pickle.dump(trouver_collision(listes[0],listes[1]),fCollisions)
fCollisions.close()


fCollisions = open("collisions2", "br")
collisions = pickle.load(fCollisions)
tests_cle(0x994a22,0xd75194,collisions)

'''





