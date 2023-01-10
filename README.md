# Web_Fullstack


>Bienvenue dans FullSport Quiz !
Avec SAIPHOU Alexandre, DUONG Hoang-Duc et EFAYONG Anthony, nous constituons le groupe 6

[`Docker`](https://www.docker.com/get-started) est requis pour lancer notre application \
Assurez également d'avoir installé [`WSL 2`](https://docs.microsoft.com/fr-fr/windows/wsl/install) permettant une couche de compatibilité entre les éxecutables Linux et le système Windows.

Les liens *dockerhub* vers notre quiz-api et quiz-ui sont disponibles ci-dessous :\
https://hub.docker.com/r/efayonga/quiz-prod-api\
https://hub.docker.com/r/efayonga/quiz-prod-ui

---
## User Guide


Dans ce quiz autour du thème du sport, vous serez amenés à répondre à des questions sur des thèmes tels que la NFL, la F1, ou le football.


Pour lancer le projet, entrez les commandes suivantes :
- A partir des codes sources :
    + Dans le dossier quiz-api :
  
    ```docker
    docker image build -t quiz-local-api .
    docker container run -it --rm -p 5000:5000 --name quiz-local-api quiz-local-api
    ```
    

    + Dans le dossier quiz-ui:
    ```docker
    docker image build -t quiz-local-api .
    docker container run -it --rm -p 5000:5000 --name quiz-local-api quiz
    ```

    
- Depuis dockerhub :

    ```docker
    docker container run -it --rm -p 5000:5000 --name quiz-prod-api efayonga/quiz-prod-api
    docker container run -it --rm -p 3000:80 --name quiz-prod-ui efayonga/quiz-prod-ui
    ```
  


Une fois arrivé sur le site web, vous aurez à disposition le tableau des scores actuel ainsi qu'un bouton commencer. Lorsque vous souhaitez commencer, appuyez sur le bouton "Let's Start !" \
Vous aurez également la possibilité à tout moment de revenir à la page d'accueil avec le bouton "HomePage" situé sur le header.

Après avoir appuyé sur le bouton, renseignez votre pseudonyme dans le champ correspondant au milieu de l'écran. Une fois fait, vous pourrez appuyer sur le bouton "GO !" pour commencer le quiz.

Vous serez presenté avec une série de questions à répondre, les questions ne possèdent toutes qu'une seule bonne réponse. 

Répondez à chaque question en cochant la réponse que vous pensez être la bonne, puis en appuyant sur "Next".

Après avoir répondu à toutes les question, vous serez présenté devant la page finale du quiz. Sur cette page vous pourrez consulter votre score final, vos réponses aux différentes questions (vous y verez les réponses que vous avez mises, en rouge celles fausses et en verte celles bonnes), et le tableau des scores. 

Vous pouvez ensuite revenir au menu principal en appuyant sur le bouton "HomePage", ou recommencer le quiz avec le bouton "TryAgain".




---






## Developper Guide
\
Après avoir énumérer les étapes et fichiers nécessaires à l'initialisation de notre plateforme, voyons maintenant la structure de notre dossier projet:
- Questions/
    + nos questions au préalable en format JSON
- quiz-api/
    + Dockerfile
    + app.py
    + services.py
    + models.py
    + jwt_utils.py
    + requirements.txt
    + tuto.db 
    + quiz-api.code-workspace
- quiz-ui/
    + Dockerfile
    + node_modules/
    + public/
    + quiz-ui.code-workspace
    + src/
        - router/
        - components/
        - views/
        - App.vue
        - main.js
    + packages JSON
    + .env.development

Cette architecture nous a permis de mettre en valeur chaque partie du projet en évidence. On notera notamment les fichiers:
- `app.py` qui nous permettra d'instancier les différentes routes de notre site entre le backend et le frontend
- `services.py` fichier principal de requêtages et de travail des données dans notre backend
- `tuto.db` notre database qui va stocker les informations récupérées depuis le front
- `App.vue` fichier qui va aller chercher les informations des autres `views` à l'aide de routeurs lors de l'initialisation de notre projet
- `quizApiService.js` fichier qui va stocker les différentes fonctions utiles pour la page et retourne un appel des routes instanciées dans `app.py`

### First Step : Création de la base de données
\
Notre base de données est composée de 3 tables pour notre site:
- la table `Question` contenant toutes les questions de notre quiz. Elle va également cherché dans le backend toutes les réponses correspondantes avec l'id de la question `question_id`. 
- la table `Answer` qui va contenir les réponses du quiz qui pourra alimenter les questions dans la table Question.
- la table `Attempts` qui va enregistrer toutes les participations de chaque joueur, avec son pseudonyme, son score et la date de la tentative.


### Second Step : Définition des valeurs des liens de pages
\
On a défini pour chaque lien de notre `API` une fonctionnalité particulière, allant chercher chacune des actions de notre site.\
Ses actions seront ensuite acheminées dans chacune des routes de notre quiz.\
Il y aura majoritairement des requêtes liées à nos base de données, comme actualiser des informations sur les tables ou alors obtenir des requêtes en temps réel sur les routes.  


### Third Step : Application des fonctions sur les pages webs
\
Le front-end de l'application a été réalisé en Javascript avec l'aide du framework Vue, et le style a été fait en CSS avec l'aide du framework Bootstrap.\
Les actions de notre site seront surtout liées au clic sur un élément des pages.\
On prend par exemple le bouton `Next` d'une question qui va enregistrer les questions et envoyer la requête de chercher la question suivante à l'index suivant.
Le bouton `submit` dispose également de fonctionnalités multiples.\
Ce-dernier va envoyer l'ensemble des réponses choisies du quiz et calculer dans le back le score obtenu pour enfin le renvoyer sur la page des résultats avec le score et les informations générales comme le leaderboard actuel et un sommaire des réponses justes ou fausses.\
Pour le côté administrateur, nous pourrons modifier l'ordre de nos questions, créer de nouvelles question ou encore importer des nouvelles questions depuis un format JSON.


---


## Problèmes rencontrés

Lors du projet nous avons rencontré plusieurs problèmes tels que :
- Refresh de page, il faudra appuyer sur **F5** par exemple lorsque l'on implémente des nouvelles questions ou sinon il y aura uniquement des problèmes visuelles (aucune répecurtion sur le Back), il y a une duplication des questions précedentes lorsque l'on implémente des nouvelles questions. 
- Le surlignage du score dans le leaderboard, une fonctionnalité que nous n'arrivions pas à implémenter. `ClassComputed` dans Nouveaux Composants (Surement un problème de classe).
- Problème de bouton lorsque l'on est en mode administratif, sur les boutons en ligne sur le haut du site. Il faut cliquer sur la partie haute du bouton alors que les boutons sont  implémentés exactement comme les autres et que les autres n'ont pas de problèmes.  

## Améliorations futures

Les améliorations que nous pouvons faire sont :
- Ajout d'un background sur le site au lieu d'un fond uni.
- Ajout d'une option permettant à l'utilisateur de sélectionner un sport afin d'obtenir des questions uniquement sur ce sport sélectionné.
- Randomisation des questions 
- Ajout d'une récompense lorsque le joueur a eu un score parfait au quizz (page spéciale + son)
- Ajout d'un timer modulable dans le côté administratif et qui ferai un pop-up lorsqu'il ne reste plus beaucoup de temps pour répondre aux questions

