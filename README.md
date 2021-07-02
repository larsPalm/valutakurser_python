# valutakurser_python
simple valutakalkulator basert på csv-filer over valutakurser fra Norges bank\
valutakurs.py kjøres med ./valutakurs.py eller python3 valutakurs.py\
make_pictures.py kjøres med ./make_pictures.py eller python3 make_pictures.py\
simple valutakalkulator basert på api fra den europeiske sentralbanken og csv-filer basert på dette api-et\
api.py kjøres med ./api.py eller python3 api.py(fungerer ikke pga endringer i api-et)\
ny simple valutakalkulator, denne gang med api fra norges bank, dataene blir lagret som\
csv-filer og oppdatert første gang en bruker bruker programmet per dag\
api_20.py kjøres med python3 api_20.py\
egen valutakalkulator som henter data fra egen local server som kjører som localhost,koden for server er nå på github i mappen api_server\
api_30.py kjøres med python3 api_30.py (serveren må startes før api_30)\
update_db.py er et script for å oppdatere db-en til serveren\
stresstest.py er et script for å teste forskjellen på sqlite og postgresql\
plot_stresstest.py kjører metoder fra stresstest.py og plotter resultatet, kan brukes på både api_server og currencyapiserver for å vise forskjellen på sqlite og postgresql\
atomicInteger er en klasse som brukes i stresstest.py og plot_stresstest.py
