*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Final Cleanup
Test Setup      Reset Application And Go To Starting Page

*** Test Cases ***
At start there are no references
    Go To  ${HOME_URL}
    Title Should Be  Etusivu
    References are reset


Kirjan lomake on olemassa
    Click Link  Lisää kirja
    Lisää kirja sivu Should Be Open

Artikkelin lomake on olemassa
    Click Link  Lisää artikkeli
    Lisää artikkeli sivu Should Be Open

Inproceeding lomake on olemassa
    Click Link  Lisää Konferenssijulkaisun Artikkeli
    Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open

Lisätty kirja näkyy etusivulla
    Click Link  Lisää kirja
    Lisää kirja sivu Should Be Open
    Input Text  title  Testbook
    Input Text  author  Author
    Input Text  year  2020
    Input Text  isbn  1234567890
    Input Text  publisher  TestPublisher
    Click Button  Tallenna kirja
    Main Page Should Be Open
    Page Should Contain  Testbook


Lisätty artikkeli näkyy etusivulla
    Click Link  Lisää artikkeli
    Lisää artikkeli sivu Should Be Open
    Input Text  title  Testarticle
    Input Text  author  Author
    Input Text  journal  Journal
    Input Text  year  2020
    Input Text  DOI  1     
    Input Text  volume  10  
    Input Text  pages  110
    Click Button  Tallenna artikkeli
    Main Page Should Be Open
    Page Should Contain  Testarticle

Lisätty inproceeding näkyy etusivulla
    Click Link  Lisää Konferenssijulkaisun Artikkeli
    Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open
    Input Text  title  Testinproceeding
    Input Text  author  Author
    Input Text  year  2020
    Input Text  booktitle  testbooktitle     
    Click Button  Tallenna Konferenssijulkaisun artikkeli
    Main Page Should Be Open
    Page Should Contain  Testinproceeding

Kirjaa pystyy muokkaamaan
    Click Link  Lisää kirja
    Lisää kirja sivu Should Be Open
    Input Text  title  Testbook
    Input Text  author  Author
    Input Text  year  2020
    Input Text  isbn  1234567890
    Input Text  publisher  TestPublisher
    Click Button  Tallenna kirja
    Main Page Should Be Open
    Page Should Contain  Testbook
    Click Link  Testbook
    Book Page Should Be Open
    Click Link  Muokkaa
    Modify Book Page Should Be Open
    Input Text  author  NewAuthor
    Click Button  Tallenna muutokset
    Main Page Should Be Open

Kirjan pystyy poistamaan
    Click Link  Lisää kirja
    Lisää kirja sivu Should Be Open
    Input Text  title  Testbook
    Input Text  author  Author
    Input Text  year  2020
    Input Text  isbn  1234567890
    Input Text  publisher  TestPublisher
    Click Button  Tallenna kirja
    Main Page Should Be Open
    Page Should Contain  Testbook
    Click Link  Testbook
    Book Page Should Be Open
    Click Link  Poista
    Remove Book Page Should Be Open
    Click Button  Poista kirja
    Main Page Should Be Open
    Page Should Not Contain  Testbook

Artikkelia pystyy muokkaamaan
    Click Link  Lisää artikkeli
    Lisää artikkeli sivu Should Be Open
    Input Text  title  Testarticle
    Input Text  author  Author
    Input Text  journal  Journal
    Input Text  year  2020
    Input Text  DOI  1     
    Input Text  volume  10  
    Input Text  pages  110
    Click Button  Tallenna artikkeli
    Main Page Should Be Open
    Page Should Contain  Testarticle
    Click Link  Testarticle
    Article Page Should Be Open
    Click Link  Muokkaa
    Modify Article Page Should Be Open
    Input Text  author  NewAuthor
    Click Button  Tallenna muutokset
    Main Page Should Be Open

Artikkelin pystyy poistamaan
    Click Link  Lisää artikkeli
    Lisää artikkeli sivu Should Be Open
    Input Text  title  Testarticle
    Input Text  author  Author
    Input Text  journal  Journal
    Input Text  year  2020
    Input Text  DOI  1     
    Input Text  volume  10  
    Input Text  pages  110
    Click Button  Tallenna artikkeli
    Main Page Should Be Open
    Page Should Contain  Testarticle
    Click Link  Testarticle
    Article Page Should Be Open
    Click Link  Poista
    Remove Article Page Should Be Open
    Click Button  Poista artikkeli
    Main Page Should Be Open
    Page Should Not Contain  Testarticle

Inproceedingia pystyy muokkaamaan
    Click Link  Lisää Konferenssijulkaisun Artikkeli
    Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open
    Input Text  title  Testinproceeding
    Input Text  author  Author
    Input Text  year  2020
    Input Text  booktitle  testbooktitle     
    Click Button  Tallenna Konferenssijulkaisun artikkeli
    Main Page Should Be Open
    Page Should Contain  Testinproceeding
    Click Link  Testinproceeding
    Inproceeding Page Should Be Open
    Click Link  Muokkaa
    Modify Inproceeding Page Should Be Open
    Input Text  author  NewAuthor
    Click Button  Tallenna muutokset
    Main Page Should Be Open

Inproceedingin pystyy poistamaan
    Click Link  Lisää Konferenssijulkaisun Artikkeli
    Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open
    Input Text  title  Testinproceeding
    Input Text  author  Author
    Input Text  year  2020
    Input Text  booktitle  testbooktitle     
    Click Button  Tallenna Konferenssijulkaisun artikkeli
    Main Page Should Be Open
    Page Should Contain  Testinproceeding
    Click Link  Testinproceeding
    Inproceeding Page Should Be Open
    Click Link  Poista
    Remove Inproceeding Page Should Be Open
    Click Button  Poista konferenssinjulkaisun artikkeli
    Main Page Should Be Open
    Page Should Not Contain  Testinproceeding

Viitetyypin valitsemalla näkymä muuttuu etusivulla
    Click Link  Lisää kirja
    Lisää kirja sivu Should Be Open
    Input Text  title  Testbook
    Input Text  author  Author
    Input Text  year  2020
    Input Text  isbn  1234567890
    Input Text  publisher  TestPublisher
    Click Button  Tallenna kirja
    Click Link  Lisää artikkeli
    Lisää artikkeli sivu Should Be Open
    Input Text  title  Testarticle
    Input Text  author  Author
    Input Text  journal  Journal
    Input Text  year  2020
    Input Text  DOI  1     
    Input Text  volume  10  
    Input Text  pages  110
    Click Button  Tallenna artikkeli
    Click Link  Lisää Konferenssijulkaisun Artikkeli
    Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open
    Input Text  title  Testinproceeding
    Input Text  author  Author
    Input Text  year  2020
    Input Text  booktitle  testbooktitle     
    Click Button  Tallenna Konferenssijulkaisun artikkeli
    Main Page Should Be Open
    Select From List By Label  name=category  Näytä kirjat
    Page Should Not Contain  Testarticle  Testinproceeding
    Select From List By Label  name=category  Näytä artikkelit
    Page Should Not Contain  Testbook  Testinproceeding
    Select From List By Label  name=category  Näytä konferenssijulkaisujen artikkelit
    Page Should Not Contain  Testbook  Testarticle
    Select From List By Label  name=category  Näytä kaikki
    Page Should Contain  Testbook
    Page Should Contain  Testarticle
    Page Should Contain  Testinproceeding


*** Keywords ***

Reset Application And Go To Starting Page
  Reset References
  Go To Starting Page

Main Page Should Be Open
    Title Should Be  Etusivu

Book Page Should Be Open
    Title Should Be  Book

Modify Book Page Should Be Open
    Title Should Be  Muokkaa kirjaa

Remove Book Page Should Be Open
    Title Should Be  Kirjan poisto

Article Page Should Be Open
    Title Should Be  Article 

Modify Article Page Should Be Open
    Title Should Be  Muokkaa artikkelia

Remove Article Page Should Be Open
    Title Should Be  Artikkelin poisto

Inproceeding Page Should Be Open
    Title Should Be  Inproceeding

Modify Inproceeding Page Should Be Open
    Title Should Be  Muokkaa konferenssinjulkaisun artikkelia

Remove Inproceeding Page Should Be Open
    Title Should Be  Konferenssinjulkaisun artikkelin poisto

Lisää kirja sivu Should Be Open
    Title Should Be  Lisää kirja

Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open
    Title Should Be  Lisää Konferenssijulkaisun artikkeli

Lisää viite sivu Should Be Open
    Title Should Be  Lisää viite

References are reset
    Page Should Contain  Viitteitä näkyvillä: 0

Lisää artikkeli sivu Should Be Open
    Title Should Be  Lisää artikkeli

Final Cleanup
    Reset References
    Close Browser
