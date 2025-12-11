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

Viitetyypin valitsemalla näkymä muuttuu etusivulla
    Luo Kirja  Testbook  Author  2020  1234567890  TestPublisher
    Luo Artikkeli  Testarticle  Author  Journal  2020  1  10  110
    Luo Konferenssijulkaisun Artikkeli  Testinproceeding  Author  2020  testbooktitle
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

Lisää artikkeli sivu Should Be Open
    Title Should Be  Lisää artikkeli

Lisää viite sivu Should Be Open
    Title Should Be  Lisää viite

