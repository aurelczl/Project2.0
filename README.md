# Projet Personel Django - Gestion de média

Un site web permettant aux utilisateurs de créer, afficher et gérer leurs livres, films et séries préférés.

## 🚀 Site en ligne

👉 [Voir le site déployé sur Render](https://project2-0-qa7x.onrender.com)

## 🚀 Améliorations 

- Faire le pèle mèle automatique - STATUT : A améliorer

- Plusieurs auteurs de livres - STATUT : Faire de auteur une base de donnée comme genre

- Faire de statut une base de donnée également - STATUT : 4 états, ajouté le un critère pour reprendre la poursuite si en cours + l'ajouter au niveau des filtres -- FAIT

- Ajouter dans la page web detail, en dessous des détails du livres : Du même auteur 

- Trouver une solution pour mettre un superuser sur le site deployé -- FAIT 

- Faire en sorte que les noms des champs des formulaires ne soient pas les noms de dev

- Ajouter dans le formulaire livre, la langue de lecture, et si on possède le livre ou non.

- API pour la recherche de photo et le remplissage automatique des lignes

- Mettre une page de stats !! hihi

## 🚀 Remplissage automatique de champs :

Mise en place d'une API par item.

### Une API publique gratuite selon le type de média :

- Livres : Google Books API -- mis sur les livres (pb : en anglais) 
Pas très pratique --> Titre doit etre exacte dépend de l'ortographe et connait peu de livre en francais
Essayer avec OpenLibrary.org

Manque de contenu --> Integration d'un choix d'api : openlib, babelio ou booknode

- Séries TV / Films : TMDB

- Mangas / animés : Anilist GraphQL API

### Un champ de titre avec un script JS qui :

- déclenche une requête AJAX dès qu'on tape (par exemple 3+ lettres),

- reçoit une réponse (JSON) contenant des infos,

- remplit les autres champs avec les valeurs proposées.

- Un petit endpoint Django qui sert d’intermédiaire (car il ne faut pas exposer tes clés API côté client).
