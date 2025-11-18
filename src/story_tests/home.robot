*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application And Go To Starting Page

*** Test Cases ***
Click Lisaa Viite
    Click Link  Lisää viite
    Lisää viite sivu Should Be Open

*** Keywords ***

Reset Application And Go To Starting Page
  Reset Application
  Go To Starting Page

Main Page Should Be Open
    Title Should Be  Etusivu

Lisää viite sivu Should Be Open
    Title Should Be  Lisää viite