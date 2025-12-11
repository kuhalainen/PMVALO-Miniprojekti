*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Final Cleanup
Test Setup      Reset Application And Go To Starting Page

*** Test Cases ***

Kirjan lomake on olemassa
    Click Link  Lisää kirja
    Lisää kirja sivu Should Be Open

Lisätty kirja näkyy etusivulla
    Luo Kirja  Testbook  Author  2020  1234567890  TestPublisher
    Page Should Contain  Testbook

Kirjaa pystyy muokkaamaan
    Luo Kirja  Testbook  Author  2020  1234567890  TestPublisher
    Page Should Contain  Testbook
    Click Link  Testbook
    Book Page Should Be Open
    Click Link  Muokkaa
    Modify Book Page Should Be Open
    Input Text  title  Testbook_EDITED
    Click Button  Tallenna muutokset
    Go To  ${HOME_URL}
    Main Page Should Be Open
    Page Should Contain  Testbook_EDITED

Kirjan pystyy poistamaan
    Luo Kirja  Testbook  Author  2020  1234567890  TestPublisher
    Page Should Contain  Testbook
    Click Link  Testbook
    Book Page Should Be Open
    Click Link  Poista
    Remove Book Page Should Be Open
    Click Button  Poista kirja
    Main Page Should Be Open
    Page Should Not Contain  Testbook

*** Keywords ***
Book Page Should Be Open
    Title Should Be  Book

Modify Book Page Should Be Open
    Title Should Be  Muokkaa kirjaa

Remove Book Page Should Be Open
    Title Should Be  Kirjan poisto

Lisää kirja sivu Should Be Open
    Title Should Be  Lisää kirja

