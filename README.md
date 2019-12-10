# Spectrum Crawler

Avec le Crawler, notre objectif principal était de récupérer plusieurs chansons pour un genre donné et en extraire des primitives. Cependant, nous avions quelques contraintes techniques et pratiques à relever afin d’y arriver.

D’abord, nous devions trouver une API quelconque qui nous permettrait de rechercher des chansons pour un genre donné. Nous avons trouvé que l’API de LastFM nous permet de récupérer des chansons pour un genre, à l’aide de la route tag.gettoptracks.

Cependant, comme toute API, celle de LastFM comprend une limite de chansons à retourner par appel. Étant donné que nous voulions extraire beaucoup de chansons pour chaque genre, cela causait un problème. Nous avons résolu ce problème en concevant un algorithme récursif d’extraction, détaillé ci-dessous.

https://docs.google.com/document/d/1PT8uqIPv95id5zIYcO2h5l6QNIbxxM9kHHdYh5WLaSI/edit?usp=sharing
https://drive.google.com/file/d/1XZBFf8D1droDi1ibrjFMq31sO5tYXLLn/view?usp=sharing
