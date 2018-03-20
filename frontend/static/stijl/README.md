In deze repo wordt de huisstijl van data.amsterdam.nl bewaard en bewaakt.

## usage
Voeg de volgende regel toe in je package.json:

`"stijl": "git+https://git@github.com/Amsterdam/stijl.git"`

#### ams-stijl.css
Je kan nu in jouw project `node_modules/stijl/css/ams-stijl.css` toevoegen om gebruik 
te maken van de amsterdam huisstijl.

Zie https://patternlab-amsterdam.infoprojects.nl/?p=all voor beschikbare classes en patronen.

#### gebruik maken van variables
Importeer een of meerdere files van de `/scss/` folder in jouw .scss files.


## contribute
* run `npm install` 
* run `npm run build-all`
    * Dit zal de onderliggende style (gemeente-amsterdam-patterns - https://gitlab.infoprojects.nl/pattern-lab/gemeente-amsterdam/) 
    bouwen en beschikbaar stellen in dit project  

***Voordat je je werk commit, doe een `npm run build-stijl` om er zeker 
van te zijn dat de aanpassingen beschikbaar zijn als je het project als 
dependency in een ander project gebruikt***   
