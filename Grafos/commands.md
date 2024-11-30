###  Rodar postgres aqui no computador
`brew services start postgresql@14`
`brew services stop postgresql`


### Rodar postgres no HDD
`pg_ctl status -D data`
`pg_ctl -D data stop`
`pg_ctl -D data start`
`pg_ctl restart -w -D data -c -m i`

## Get Flight
### Rodar o código
1. Ative o ambiente virtual
`source .venv/bin/activate`
2. O ambiente já tem as bibliotecas instaladas
3. Rode o código
`python3 GetFlight.py`
    1. As opções são as seguintes
        - s -> scraprun, serve para saber se roda ou não o scrapping da página do google
        - l -> listrun, serve para saber se vai ou não rodar as paradas do arquivo pra construir as linhas
        - i -> insert, serve para saber se a lista produzida vai ser inserida no banco de dados (util para quando não estiver com o banco de dados disponivel)
