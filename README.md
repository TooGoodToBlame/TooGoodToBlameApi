
Zainstaluj wymagane pakiety  
`pip3 install -r .\requirements.txt`

Przygotuj bazę danych  
`python3 manage.py migrate`

uruchom server  
`python3 manage.py runserver`


linki:

ADMIN:
http://127.0.0.1:8000/admin/
    użytkownik testowy: test:test

Pozwala na pełną edycję całej bazy danych. Widok automatycznie generowany przez Django.

API:

lista wszystkich ustaw
http://127.0.0.1:8000/api/bill_list/

Możliwe sortowania: id, voting_date, title
Możliwe filtrowania: member_of_parliament, member_of_parliament_name
Przykład użycia:
http://127.0.0.1:8000/api/bill_list/?member_of_parliament=1&ordering=id


detale o ustawie
http://127.0.0.1:8000/api/bill_list/<pk>/

Lista wszystkich europośle
http://127.0.0.1:8000/api/member_of_parliament_list/

Możliwe sortowania: party, number_on_list
Możliwe filtrowania: party, region
Przykład użycia:
http://127.0.0.1:8000/api/member_of_parliament_list/?ordering=party,number_on_listt&party=PO&region=DS

detale o europośle
http://127.0.0.1:8000/api/member_of_parliament_list/<pk>/


Lista ustaw, w których dany parlamentarzysta oddał głos.
http://127.0.0.1:8000/api/member_of_parliament_bills/<pk>/

Lista głosów oddanych na daną ustawę.
Adres: http://127.0.0.1:8000/api/bill_votes/<pk>/

Edytor:
http://127.0.0.1:8000/edit-bill/search/

Na ekranie wyszukiwania można skorzystać z formularza do filtracji ustaw. każda ustawa jest linkiem pozwalającym na jej edycję.

http://127.0.0.1:8000/edit-bill/edit-bill/<pk>
jest formularzem edycji pozwalającym zmienić informacje o ustawie. W przyszłości poziom edycji będzie zależeć od uprawnień zalogowanego użytkownika.
