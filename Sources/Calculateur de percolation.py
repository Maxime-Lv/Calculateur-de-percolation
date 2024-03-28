# -*- coding: utf-8 -*-

import tkinter as tk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from random import random
from matplotlib.colors import ListedColormap
from time import perf_counter


# Création de la fenêtre
window = tk.Tk()                       # Création de la fenêtre graphique
window.title('Percolation')            # Ajout du titre de la fenêtre
window.geometry('1080x720')            # Définition de la taille de la fenêtre
window.minsize(1080, 720)              # Définition de la taille minimum de la fenêtre
window.maxsize(1080, 720)              # Définition de la taille maximale de la fenêtre
window.config(background='#96E7FF')    # Mise en place d'un fond de couleur bleu clair
window.iconphoto(False, ImageTk.PhotoImage(Image.open('logo.png')))       # Ajout d'un logo en haut à gauche de la fenêtre


# Titre 
titre = tk.Label(window,text='Calculateur de percolation', font='Georgia 40 underline', bg='#96E7FF', fg='#fefefe')         # Création du titre de la fenêtre
titre.pack()            # Ajout du titre sur la fenêtre


# Champs de texte

# Champ de texte longueur grille
n = tk.Entry(window, width=24, bg='#b3fef7')       # Définition de l'entrée
n.place(x=50, y=150)                               # Placement du champ de texte sur la fenêtre
n.insert(0, "Longueur du tableau :")               # Ajout d'un texte dans le champ de texte pour indiquer à l'utilisateur ce qu'il faut rentrer
n.configure(state='disabled')                      # Défifnir le champ de texte comme désactivé, pour que l'utilisateur ne puisse pas modifier le texte 

n_focus_in = n.bind('<Button-1>', lambda x: focus_in(n))      # Cette ligne déclenche une fonction lorsque l'utilisateur clique dans l'entrée. Cette fonction enlevera le texte initial et autorise la saisie
n_focus_out = n.bind('<FocusOut>', lambda x: focus_out(n, 'Longueur du tableau :'))        # Cette ligne déclenche une autre fonction lorsque l'entrée perd le focus. Cette fonction fait que si le champ est vide après avoir cliqué dessus, il y a un retour du texte initial

# Champ de texte probabilité apparition cases blanches
p = tk.Entry(window, width=24, bg='#b3fef7')       # Définition de l'entrée
p.place(x=50, y=185)                               # Placement du champ de texte sur la fenêtre
p.insert(0, "Probabilité cases blanches :")        # Ajout d'un texte dans le champ de texte pour indiquer à l'utilisateur ce qu'il faut rentrer
p.configure(state='disabled')                      # Défifnir le champ de texte comme désactivé, pour que l'utilisateur ne puisse pas modifier le texte 

p_focus_in = p.bind('<Button-1>', lambda x: focus_in(p))      # Cette ligne déclenche une fonction lorsque l'utilisateur clique dans l'entrée. Cette fonction enlevera le texte initial et autorise la saisie
p_focus_out = p.bind('<FocusOut>', lambda x: focus_out(p, 'Probabilité cases blanches :'))        # Cette ligne déclenche une autre fonction lorsque l'entrée perd le focus. Cette fonction fait que si le champ est vide après avoir cliqué dessus, il y a un retour du texte initial


# Création du canvas pour afficher l'image
monCanvas = tk.Canvas(window, width=450, height=450, bg='white')          # Création du canva, pour afficher les futus images de percolation
monCanvas.place(x=320, y=150)                                             # Disposition du canvas sur la fenêtre graphique


# Variable golbale
grille_fin = 0          # Variable globale qui contiendra une grille après sa génération. Elle sera utilisée pour afficher et percoler sur la même grille


# placeholder champ de texte
def focus_in(entry):
    """Fonction appelée lors du clic dans un champ de texte pour supprimer le contenu et autoriser l'utilisateur à écrire."""
    if entry.cget('state') == 'disabled':       # Si le champ de texte est désactivé
        entry.configure(state='normal')         # Activation du champ pour permettre la saisie
        entry.delete(0, 'end')                  # Effacer le contenu actuel du champ


def focus_out(entry, placeholder):
    """Fonction appelée lorsque l'utilisateur "clique" autre part que le champ de texte (perd le focus),
    pour remettre le texte de base."""
    if entry.get() == "":                    # Si le champ de texte est vide
        entry.insert(0, placeholder)         # Insertion du placeholder dans le champ
        entry.configure(state='disabled')    # Désactivation du champ pour empêcher la saisie


# Fonction qui affiche la grille en percolation sur le canva depuis la console
def afficher_image(L: list):
    """Affiche l'image générée par la liste L sur le canvas."""
    fig, ax = plt.subplots(figsize=(7.5, 7.5))  # Définir la taille de la figure Matplotlib
    ax.matshow(L, cmap=ListedColormap(['black', 'aqua', 'white']), vmin=0.0, vmax=1.0)   # Associe au valeurs d'une matrice une couleur définie par une échelle. "vmin" et "vmax" définissent respectivement les valeurs minimale et maximale des données affichées.
    plt.close(fig)  # Fermer la figure pour éviter l'affichage dans la fenêtre
    photo = convertisseur(fig)    # Fait appel à la fonction convertisseur pour transformer un image Matplotlib en image compatible avec Tkinter
    monCanvas.create_image(-45, -40, anchor=tk.NW, image=photo)  # Crée une image dans le canvas aux coordonnées indiquées, en partant du coin Nord-Ouest du canva
    monCanvas.image = photo  # Stockage de la photo dans le canvas, utile pour éviter le garbage collector (pour éviter que la mémoire juge l'image inutile et la supprime)

# Fonction qui convertit une image en image compatible avec Tkinter
def convertisseur(fig):
    """Prend une image Matplotlib en argument et retourne une image Tkinter représentant cette image,
    prête à être affichée dans un un canva Tkinter."""
    fig.canvas.draw()   # Génère le contenue de l'image Matplotlib sur un autre canvas (de Matplotlib, pas sur Tkinter) pour récuperer un rendu, qui sera utilisé pour récuperer les données de l'image sous forme de bits
    width, height = fig.canvas.get_width_height()   # Récupèration de la largeur et la hauteur du canvas de l'image (ou figure) Matplotlib.
    return ImageTk.PhotoImage(Image.frombytes('RGB', (width, height), fig.canvas.tostring_rgb()))    # Création d'une image compatible avec Tkinter à partir des données de la figure Matplotlib.

# Fonction qui crée la grille
def creation_grille(longueur, proba): # Fonction qui gère la création de la grille de percolation
    """Crée un tableau de taille n*n simulant un milieu poreux."""
    grille = [[1.0 if random() <= proba else 0.0 for j in range(longueur)] for i in range(longueur)] # Création d'une matrice remplie de 0.0 et de 1.0 (avec une probalité d'apparaitre égale à celle rentrée précédement par l'utilisateur) disposés de manière aléatoire, par compréhension
    return grille      # On renvoie la grille

# Fonction qui affiche la grille pour le bouton "Afficher grille"
def voir_grille():
    """Génère une grille de percolation selon les paramètres renseignés, et l'affiche dans Tkinter."""
    temps.configure(state='normal')       # On active le champ de texte qui affichera le temps de génération de la grille
    temps.delete(0, "end")                # On supprime tous les caractères qui se trouvaient dedans pour éviter de faire une concaténation du texte
    temps.configure(state='disabled')     # On désactive le champs de texte pour que l'utilisateur ne puisse pas modifier le texte
    debut = perf_counter()                # Initialisation d'une variable pour la fonctionnalité permettant de voir le temps pris pour générer la grille 
    grille = creation_grille(int(n.get()), float(p.get()))     # Appel de la fonction creation_grille en prenant pour paramètres la taille n*n et la proba de cases blanches, renseignés précédement 
    afficher_image(grille)                # Appel de la fonction afficher_image avec un pour paramètre la grille générée par creation_grille
    global grille_fin
    grille_fin = grille                   # On stocke la grille dans la variable globale grille_fin, qui sera alors utilisée pour la percolation
    fin = perf_counter()                  # Initialisation d'une variable de fin pour calculer le temps
    temp = round(fin - debut, 5)          # Création de la variable contenant la valeur en secondes, du temps pris pour générer la grille. Calcul du temps finale moins le temps initial
    if temp <= 1:                         # Si le temps est inférieur à une seconde, 'seconde' ne prendra pas de "s"
        temps.configure(state='normal')           # On active le champ de texte pour modifier son contenu
        temps.insert(0, str(temp)+" seconde.")    # On insert dans le champs de texte le temps de génération de la grille et le mots "seconde"
        temps.configure(state='disabled')         # On désactive le champs de texte pour que l'utilisateur ne puisse pas modifier le texte
    else:                                 # Si le temps est supérieur à une seconde, 'secondes' prendra un "s"
        temps.configure(state='normal')           # On active le champ de texte pour modifier son contenu
        temps.insert(0, str(temp)+" secondes.")   # On insert dans le champs de texte le temps de génération de la grille et le mots "secondes"
        temps.configure(state='disabled')         # On désactive le champs de texte pour que l'utilisateur ne puisse pas modifier le texte
    return

# Fonction de percolation
def percolation():
    """ Fonction qui simule une percolation, c'est à dire le parcours de l'eau dans un milieu poreux, ici une grille. On va parcourir 
    la première ligne de la grille, à la recherche de case blanche, soit 1.0. Si la case est blanche, on la remplacera par de l'eau.
    Cette case prendra alors la valeur 0.5. L'échelle de couleur reconnaitra alors que le flottant 0.5 décrira l'eau"""
    L = []       # Initialisation d'une liste vide qui contiendra la liste de toute les cases blanches, et leurs voisins, où l'eau pourra percoler
    for j in range(len(grille_fin[0])):       # On parcourt la premiere ligne de la grille, pour placer l'eau sur les cases vides
        if grille_fin[0][j] == 1.0:           # Si la case est vide, (soit blanche), on va y mettre de l'eau
            L.append([0, j])
            grille_fin[0][j] = 0.5            # Il suffit alors de remplacer le flottant 1.0 par 0.5
    while len(L) > 0:                         # On va ensuite parcourir toutes les cases 0.5, et rechercher leurs voisins qui sont disponibles (les cases blanche haut,bas,gauche et droite), jusqu'à ce qu'il n'y ait plus de vosins disponibles
        h, l = L.pop() 
        if h < len(grille_fin)-1 and grille_fin[h+1][l] == 1.0:   # Recherche du voisin du dessus
            L.append([h+1, l])    # Si une case blanche est trouvée, elle est ajouté à la liste L
            grille_fin[h+1][l] = 0.5    # Modification de la case blanche de la matrice initiale en futur case bleue
        if h > 0 and grille_fin[h-1][l] == 1.0:        # Recherche du voisin du haut
            L.append([h-1, l])    # Si une case blanche est trouvée, elle est ajouté à la liste L
            grille_fin[h-1][l] = 0.5    # Modification de la case blanche de la matrice initiale en futur case bleue
        if l > 0 and grille_fin[h][l-1] == 1.0:         # Recherche du voisin gauche
            L.append([h, l-1])     # Si une case blanche est trouvée, elle est ajouté à la liste L 
            grille_fin[h][l-1] = 0.5    # Modification de la case blanche de la matrice initiale en futur case bleue
        if l < len(grille_fin)-1 and grille_fin[h][l+1] == 1.0:       # Recherche du voisin droite
            L.append([h, l+1])    # Si une case blanche est trouvée, elle est ajouté à la liste L
            grille_fin[h][l+1] = 0.5    # Modification de la case blanche de la matrice initiale en futur case bleue
        afficher_image(grille_fin)      # Préparation de l'affichage de la nouvelle grille percolée 0 à 4 carreaux en plus, sur le canva Tkinter
        window.update_idletasks()  # Mettre à jour l'affichage de la percolation sur le canvas
    if 0.5 in grille_fin[int(n.get())-1]:      # On va regarder si la percolation jusqu'en bas à eu lieu, pour prévenir l'utilisateur
        texte_perco = tk.Label(window, width=20, bg='#96E7FF', text='La percolation a réussie !', font='Georgia 18', fg='#fefefe')    # On crée une petit titre qui prévient l'utilisateur que la percolation a réussi
        texte_perco.place(x=782, y=150)          # On place le texte en haut a gauche
    else:         # La percolation n'a pas eu lieu entièrement
        texte_perco = tk.Label(window, width=20, bg='#96E7FF', text='La percolation a échoué...', font='Georgia 18', fg='#fefefe')    # On crée une petit titre qui prévient l'utilisateur que la percolation n'a pas réussi
        texte_perco.place(x=782, y=150)     # On place le texte en haut a gauche
    return


# Pour bouton 'Fermer le calculateur'
def fermer_fen():
    """Fonction qui est éxécutée lorsque qu'on appuie sur le bonton 'Fermer le calculateur', et ferme le calculateur"""
    window.destroy()         # Méthode qui permet de détruire le widget existant


# Boutons "voir la grille","Start" et "Stop"
btn_show = tk.Button(window, text='Voir la grille', font='Georgia 18', bg='#000000', fg='#fefefe',activebackground='#656565', activeforeground='#fefefe', bd=0, height=3, width=10, command=voir_grille)
# Création d'un bouton "Voir la grille", qui executera la fonction voir_grille, et fera afficher la grille générée sur le canva Tkinter
btn_show.place(x=50, y=225)                   # Placement du bouton sur la fenêtre

btn_start = tk.Button(window, text='Start', font='Georgia 18', bg='#4eeb36', fg='#fefefe',activebackground='#259713', activeforeground='#fefefe', bd=0, height=3, width=10, command=percolation)
# Création d'un bouton "Star", qui executera la fonction percolation, et fera afficher la simulation de la percolation sur la grille générée sur le canva Tkinter
btn_start.place(x=50, y=350)                   # Placement du bouton sur la fenêtre

btn_quit = tk.Button(window, text='Quitter le \n calculateur', font='Georgia 18', bg='#F50000', fg='#fefefe',activebackground='#ca0000', activeforeground='#fefefe', bd=0, height=3, width=10, command=fermer_fen)
# Création d'un bouton "Quitter le calculateur", qui executera la fonction ferme_fen, et fermera la fenêtre (ou widget)
btn_quit.place(x=50, y=475)                   # Placement du bouton sur la fenêtre
 
# Texte puis champs de texte pour temps de génération de la grille 
textetemps = tk.Label(window, text='Temps de génération : ', font='Georgia 11', bg='#96E7FF', fg='#fefefe')         # Création du texte pour le temps de génération
textetemps.place(x=470, y=608)               # Placement du champ de texte sur la fenêtre

temps = tk.Entry(window, width=25, bg='#b3fef7', state='disabled')         # Création du champ de texte pour le temps de génération. Le statut est défini sur désactivé. De ce fait, l'utilisateur ne pourrat pas écrire et modifer ce qui se trouve dans l'entrée
temps.place(x=470, y=635)                   # Placement de l'entrée sur la fenêtre


# Lancement de la fenêtre
window.mainloop()            # Démarre le gestionnaire d'évènements
