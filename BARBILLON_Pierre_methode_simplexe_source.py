################## ALGORITHME DU SIMPLEXE #####################
'''
Auteur : Pierre Barbillon
Contexte : Module de mathématiques ur la programmation Linéaire. (sujet de TP durant la totalité du module)

Description :

Ce programme met en oeuvre l'algorithme du simplexe sur un problème de première espèce (contraintes uniquement de type <=)
Les données ne sont pas entrées par l'utilisateur pour l'instant, il faut modifier les tableaux.

Comment modifier les tableaux :

tabEq est le tableau qui correspond à L0, celle de la fonction économique en quelques sortes.
Ce tableau est sous la forme : [X1, X2...XN, E1, E2...EN, 0]
Le dernier nombre est le nombre qui suit Z dans le tableau. Donc c'est le 0 de Z-0. Ce nombre ne peut qu'être négatif ou nul.

tabCons est le tableau des contraintes, initialisé avec les lignes e1, e2 etc... Le dernier nombre correspond à la colonne Z (ou Z-0).

Ce programme montre toutes les étapes. Il est possible d'afficher les index pour les critères de Danzig 1 et 2
Ce programme est commenté pour faciliter la compréhension du code.

Ne pas hésiter à voir le mémoire pour en savoir plus s'il y a un soucis de compréhension quelque part.
'''
# On importe la bibliothèque numpy qui facilite les calculs avec des tableaux multidimensionnels (tableau tabCons)
import numpy as np

# On initialise les tableaux avec les coefficients de l'exemple 1 du cours avec la façon décrite plus haut
# Note, les nombres sont notés x.0 pour que les nombres soient comptés comme des réels en cas de division non entière (1/3 par exemple dans l'exemple 2 du cours)
tabEq = np.array([3.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
tabCons = np.array([[1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 12.0],
					[1.0, -1.0, 0.0, 1.0, 0.0, 0.0, 3.0],
					[-2.0, 1.0, 0.0, 0.0, 1.0, 0.0, 3.0],
					[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 6.0]])

#On affiche le tableau à l'initialisation, les étapes n'ont pas commencées
print("Initialisation : \n")
print("L0 |", tabEq[0], " |", tabEq[1], " |", tabEq[2], " |", tabEq[3], " |", tabEq[4], " |", tabEq[5], " |", tabEq[6])
print("L1 |", tabCons[0, 0], " |", tabCons[0, 1], " |", tabCons[0, 2], " |", tabCons[0, 3], " |", tabCons[0, 4], " |", tabCons[0, 5], " |", tabCons[0, 6], " |")
print("L2 |", tabCons[1, 0], " |", tabCons[1, 1], " |", tabCons[1, 2], " |", tabCons[1, 3], " |", tabCons[1, 4], " |", tabCons[1, 5], " |", tabCons[1, 6], " |")
print("L3 |", tabCons[2, 0], " |", tabCons[2, 1], " |", tabCons[2, 2], " |", tabCons[2, 3], " |", tabCons[2, 4], " |", tabCons[2, 5], " |", tabCons[2, 6], " |")
print("L4 |", tabCons[3, 0], " |", tabCons[3, 1], " |", tabCons[3, 2], " |", tabCons[3, 3], " |", tabCons[3, 4], " |", tabCons[3, 5], " |", tabCons[3, 6], " |")

# On récupère la taille d'une colonne dans le tableau tabCons, afin de pouvoir l'explorer verticalement
tailleCol = len(tabCons[:, 0])
# On récupère la taille d'une ligne (peu importe, ici c'est la taille du tableau unidimensionnel tabEq)
tailleLin = len(tabEq)

# La variable run permet de savoir quand on s'arrête (voir plus loin)
run = 1

# La variable noPhase permet de connaître le numéro de l'étape
noPhase = 0

# Algorithme du simplexe :
while run == 1:
	# Si le coefficient max de L0 est négatif ou nul, alors on s'arrête, car ça veut dire que TOUS les coefficients de L0 sont négatifs ou nuls
	if max(tabEq) <= 0:
		# On met run à 0 pour pouvoir sortir de la boucle (et éviter une boucle infinie)
		run = 0
		# On indique à l'écran que l'algorithme est terminé
		print("ALGORITHME TERMINÉ")
	# Sinon, il y a au moins un coefficient de L0 strictement positif : on continue
	else:
		# On augmente le numéro de l'étape de 1
		noPhase = noPhase + 1
		# On affiche le numéro de l'étape
		print("\nÉtape ", noPhase, " :")

		# Premier critère de Danzig : On cherche dans L0 l'indice du premier plus grand nombre et on le stocke dans la variable danzig1
		danzig1 = np.argmax(tabEq)
		# Bien que non obliatoire ici, on créé la variable danzig2 à 0 qui stockera le deuxième critère de Danzig (évite les problèmes d'initialisation)
		danzig2 = 0
		# On explore le tableau des contraintes verticalement
		for i in range(tailleCol):
			# Si à la ligne voulue, et à la colonne correspondant au 1er critère de Danzig, le nombre est supérieur strict à 0
			if tabCons[i, danzig1] > 0:
				# Si on n'a pas commencé à vérifier le 2ème critère de Danzig
				if i == 0:
					# On met la première division dans la variable div
					div = tabCons[i, len(tabCons[0, :]) -1] / tabCons[i, danzig1]
					# On met la variable danzig2 à la ligne actuellement testée
					danzig2 = i
				# Sinon, on a commencé à vérifier le 2ème critère de Danzig
				else:
					# On met la division à la ligne actuelle dans une variable test
					test = tabCons[i, len(tabCons[0, :]) -1] / tabCons[i, danzig1]
					# Si la division actuelle est plus petite que la précédente,
					if test < div:
						# On met l'index du critère de Danzig n°2 à la ligne actuellement testée
						danzig2 = i
						# et on met la valeur de la division égale à la valeur testée, puisque le test a réussi (permet de répéter le processus)
						div = test
		# Une fois cette boucle faite, on a les deux critères de Danzig, on va pouvoir commencer les opérations sur les lignes et colonnes

		# Tout d'abord, on fait les calculs de la ligne L0 en premier, sinon les autres colonnes auront changées et le coefficient ne sera plus bon.
		coef = tabEq[danzig1]/tabCons[danzig2, danzig1]
		tabEq = tabEq - coef*tabCons[danzig2, :]

		# Opérations sur les lignes des contraintes :
		for i in range(tailleCol):
			# Si on n'est pas sur la ligne où le critère de Danzig n°2 s'applique
			if i != danzig2:
				# Calcul du coefficient avant soustraction
				coef = tabCons[i, danzig1] / tabCons[danzig2, danzig1]
				# Soustraction et remplacement de la ligne sour la forme LX = LX - coef*LD2 (LD2 étant la ligne où le critère D2 de Danzig s'applique)
				tabCons[i] = tabCons[i] - coef * tabCons[danzig2]
			# Sinon, si on est à la ligne où le critère de Danzig n°2 s'applique
			elif i == danzig2:
				# Calcul du coef (différent de précédemment)
				coef = tabCons[danzig2, danzig1]
				# On remplace la ligne actuelle sous la forme LD2 = LD2/coef
				# (dans l'exemple 1, le coefficient est toujours à 1 donc la ligne ne change pas, mais dans l'exemple 2, il y a des étapes où cette ligne a un coef > 1)
				tabCons[i] = tabCons[i] / coef

		# On fait un retour à la ligne et on affiche l'état du tableau après changements.
		print("\n")
		print("   |  x1  |  x2  |  e1  |  e2  |  e3  |  e4  |")
		print("L0 |", tabEq[0], " |", tabEq[1], " |", tabEq[2], " |", tabEq[3], " |", tabEq[4], " |", tabEq[5], " |", tabEq[6])
		print("L1 |", tabCons[0, 0], " |", tabCons[0, 1], " |", tabCons[0, 2], " |", tabCons[0, 3], " |", tabCons[0, 4], " |", tabCons[0, 5], " |", tabCons[0, 6], " |")
		print("L2 |", tabCons[1, 0], " |", tabCons[1, 1], " |", tabCons[1, 2], " |", tabCons[1, 3], " |", tabCons[1, 4], " |", tabCons[1, 5], " |", tabCons[1, 6], " |")
		print("L3 |", tabCons[2, 0], " |", tabCons[2, 1], " |", tabCons[2, 2], " |", tabCons[2, 3], " |", tabCons[2, 4], " |", tabCons[2, 5], " |", tabCons[2, 6], " |")
		print("L4 |", tabCons[3, 0], " |", tabCons[3, 1], " |", tabCons[3, 2], " |", tabCons[3, 3], " |", tabCons[3, 4], " |", tabCons[3, 5], " |", tabCons[3, 6], " |")
