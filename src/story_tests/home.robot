*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application And Go To Starting Page

*** Test Cases ***
At start there are no references
    Go To  ${HOME_URL}
    Title Should Be  Etusivu
    Page Should Contain  Lisätyt kirjat


Click Lisaa Viite
    Click Link  Lisää kirja
    Lisää viite sivu Should Be Open

*** Keywords ***

Reset Application And Go To Starting Page
  Reset References
  Go To Starting Page

Main Page Should Be Open
    Title Should Be  Etusivu

Lisää viite sivu Should Be Open
    Title Should Be  Lisää viite