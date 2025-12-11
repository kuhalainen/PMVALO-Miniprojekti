*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Final Cleanup
Test Setup      Reset Application And Go To Starting Page

*** Test Cases ***
Inproceeding lomake on olemassa
    Click Link  Lisää Konferenssijulkaisun Artikkeli
    Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open

Lisätty inproceeding näkyy etusivulla
    Luo Konferenssijulkaisun Artikkeli  Testinproceeding  Author  2020  testbooktitle
    Page Should Contain  Testinproceeding

Inproceedingia pystyy muokkaamaan
    Luo Konferenssijulkaisun Artikkeli  Testinproceeding  Author  2020  testbooktitle
    Page Should Contain  Testinproceeding
    Click Link  Testinproceeding
    Inproceeding Page Should Be Open
    Click Link  Muokkaa
    Modify Inproceeding Page Should Be Open
    Input Text  author  NewAuthor
    Click Button  Tallenna muutokset
    Main Page Should Be Open
    Page Should Contain  NewAuthor

Inproceedingin pystyy poistamaan
    Luo Konferenssijulkaisun Artikkeli  Testinproceeding  Author  2020  testbooktitle
    Page Should Contain  Testinproceeding
    Click Link  Testinproceeding
    Inproceeding Page Should Be Open
    Click Link  Poista
    Remove Inproceeding Page Should Be Open
    Click Button  Poista konferenssinjulkaisun artikkeli
    Main Page Should Be Open
    Page Should Not Contain  Testinproceeding

*** Keywords ***

Inproceeding Page Should Be Open
    Title Should Be  Inproceeding

Modify Inproceeding Page Should Be Open
    Title Should Be  Muokkaa konferenssinjulkaisun artikkelia

Remove Inproceeding Page Should Be Open
    Title Should Be  Konferenssinjulkaisun artikkelin poisto

Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open
    Title Should Be  Lisää Konferenssijulkaisun artikkeli