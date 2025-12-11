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


Bibtex tiedostossa näkyy kirja
    Click Link  Lisää kirja
    Lisää kirja sivu Should Be Open
    Input Text  title  Bibtexbook
    Input Text  author  Author
    Input Text  year  2020
    Input Text  isbn  1234567890
    Input Text  publisher  TestPublisher
    Click Button  Tallenna kirja
    Main Page Should Be Open
    Click Link  Katsele bibtex tiedostoa
    Page should contain  title = {Bibtexbook}

Bibtex tiedostossa näkyy artikkeli
    Click Link  Lisää artikkeli
    Lisää artikkeli sivu Should Be Open
    Input Text  title  Bibtexarticle
    Input Text  author  Author
    Input Text  journal  Journal
    Input Text  year  2020
    Input Text  DOI  1     
    Input Text  volume  10  
    Input Text  pages  110
    Click Button  Tallenna artikkeli
    Main Page Should Be Open
    Click Link  Katsele bibtex tiedostoa
    Page should contain  title = {Bibtexarticle}

Bibtex tiedostossa näkyy inproceeding
    Click Link  Lisää Konferenssijulkaisun Artikkeli
    Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open
    Input Text  title  Bibtexinproceeding
    Input Text  author  Author
    Input Text  year  2020
    Input Text  booktitle  testbooktitle     
    Click Button  Tallenna Konferenssijulkaisun artikkeli
    Main Page Should Be Open
    Click Link  Katsele bibtex tiedostoa
    Page should contain  title = {Bibtexinproceeding}


*** Keywords ***

Reset Application And Go To Starting Page
  Reset References
  Go To Starting Page

Main Page Should Be Open
    Title Should Be  Etusivu

References are reset
    Page Should Contain  Viitteitä näkyvillä: 0

Lisää kirja sivu Should Be Open
    Title Should Be  Lisää kirja

Lisää artikkeli sivu Should Be Open
    Title Should Be  Lisää artikkeli

Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open
    Title Should Be  Lisää Konferenssijulkaisun artikkeli

Final Cleanup
    Reset References
    Close Browser

