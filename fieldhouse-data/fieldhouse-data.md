copy table element to local table.html file
modify prompt for appropriate output
`python tabletojson.py table.html summer-25-6th-schedule.json`


python pulltables.py && python tabletojson.py  

cd ..  

rm data/{standings,schedule}.json && mv fieldhouse-data/{standings,schedule}.json data/  

