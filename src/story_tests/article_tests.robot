*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Final Cleanup
Test Setup      Reset Application And Go To Starting Page

*** Test Cases ***

Artikkelin lomake on olemassa
    Click Link  Lisää artikkeli
    Lisää artikkeli sivu Should Be Open

Lisätty artikkeli näkyy etusivulla
    Luo Artikkeli  Testarticle  Author  Journal  2020  1  10  110
    Page Should Contain  Testarticle

Artikkelia pystyy muokkaamaan
    Luo Artikkeli  Testarticle  Author  Journal  2020  1  10  110
    Page Should Contain  Testarticle
    Click Link  Testarticle
    Article Page Should Be Open
    Click Link  Muokkaa
    Modify Article Page Should Be Open
    Input Text  author  NewAuthor
    Click Button  Tallenna muutokset
    Main Page Should Be Open
    Page Should Contain  NewAuthor

Artikkelin pystyy poistamaan
    Luo Artikkeli  Testarticle  Author  Journal  2020  1  10  110
    Page Should Contain  Testarticle
    Click Link  Testarticle
    Article Page Should Be Open
    Click Link  Poista
    Remove Article Page Should Be Open
    Click Button  Poista artikkeli
    Main Page Should Be Open
    Page Should Not Contain  Testarticle

*** Keywords ***

Article Page Should Be Open
    Title Should Be  Article 

Modify Article Page Should Be Open
    Title Should Be  Muokkaa artikkelia

Remove Article Page Should Be Open
    Title Should Be  Artikkelin poisto

Lisää artikkeli sivu Should Be Open
    Title Should Be  Lisää artikkeli