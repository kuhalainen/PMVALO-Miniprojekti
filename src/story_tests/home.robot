*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application And Go To Starting Page

*** Test Cases ***
At start there are no references
    Go To  ${HOME_URL}
    Title Should Be  Etusivu
    References are reset


Click Lisaa Viite
    Click Link  Lisää kirja
    Lisää viite sivu Should Be Open

Click Lisaa Artikkeli                
    Click Link  Lisää artikkeli
    Lisää artikkeli sivu Should Be Open

Click Home Link
    Click Link  Lisää artikkeli
    Lisää artikkeli sivu Should Be Open
    Input Text  title  "Testititle"
    Input Text  author  "Author"
    Input Text  journal  "Journal"
    Input Text  year  "2020"
    Input Text  DOI  "1"     
    Input Text  volume  "10"  
    Input Text  pages  "110"
    Click Button  Tallenna artikkeli
    Main Page Should Be Open

*** Keywords ***

Reset Application And Go To Starting Page
  Reset References
  Go To Starting Page

Main Page Should Be Open
    Title Should Be  Etusivu

Lisää viite sivu Should Be Open
    Title Should Be  Lisää viite

References are reset
    Page Should Contain  Lisätyt kirjat: 0
    Page Should Contain  Lisätyt artikkelit: 0

Lisää artikkeli sivu Should Be Open
    Title Should Be  Lisää artikkeli
