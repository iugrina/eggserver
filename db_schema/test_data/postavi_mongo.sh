#!/bin/bash 

mongoimport --db eggdb --collection status --file mongo-status-iugrina-20121118.json 
mongoimport --db eggdb --collection baskets --file mongo-baskets-iugrina-200121021.json 
zcat mongo-recommended-iugrina-200121021.json.gz |  mongoimport --db eggdb --collection recommended 
