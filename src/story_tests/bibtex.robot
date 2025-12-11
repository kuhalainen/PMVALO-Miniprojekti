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
    Luo kirja  Bibtexbook  Author  2020  1234567890  TestPublisher
    Click Link  Katsele bibtex tiedostoa
    Page should contain  title = {Bibtexbook}

Bibtex tiedostossa näkyy artikkeli
    Luo artikkeli  Bibtexarticle  Author  Journal  2020  1  10  110
    Click Link  Katsele bibtex tiedostoa
    Page should contain  title = {Bibtexarticle}

Bibtex tiedostossa näkyy inproceeding
    Luo konferenssijulkaisun artikkeli  Bibtexinproceeding  Author  2020  testbooktitle
    Click Link  Katsele bibtex tiedostoa
    Page should contain  title = {Bibtexinproceeding}


*** Keywords ***

Reset Application And Go To Starting Page
  Reset References
  Go To Starting Page

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

