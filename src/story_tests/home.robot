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


Click add book
    Click Link  Lisää kirja
    Lisää kirja sivu Should Be Open

Click add article
    Click Link  Lisää artikkeli
    Lisää artikkeli sivu Should Be Open

Click add inproceeding
    Click Link  Lisää Konferenssijulkaisun Artikkeli
    Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open

Submit book
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


Submit article
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

Submit inproceeding
    Click Link  Lisää Konferenssijulkaisun Artikkeli
    Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open
    Input Text  title  Testinproceeding
    Input Text  author  Author
    Input Text  year  2020
    Input Text  booktitle  testbooktitle     
    Click Button  Tallenna Konferenssijulkaisun artikkeli
    Main Page Should Be Open
    Page Should Contain  Testinproceeding

Modify book
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

Delete book
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
    Click Button  Poista ilmoitus
    Main Page Should Be Open
    Page Should Not Contain  Testbook

Modify article
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

Delete article
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
    Click Button  Poista ilmoitus
    Main Page Should Be Open
    Page Should Not Contain  Testarticle

Modify inproceeding
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

Delete inproceeding
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
    Click Button  Poista ilmoitus
    Main Page Should Be Open
    Page Should Not Contain  Testinproceeding

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
    Title Should Be  Muokkaa artikkeli

Remove Article Page Should Be Open
    Title Should Be  Artikkelin poisto

Inproceeding Page Should Be Open
    Title Should Be  Inproceeding

Modify Inproceeding Page Should Be Open
    Title Should Be  Muokkaa inproceeding

Remove Inproceeding Page Should Be Open
    Title Should Be  Konferenssinjulkaisun artikkelin poisto

Lisää kirja sivu Should Be Open
    Title Should Be  Lisää kirja

Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open
    Title Should Be  Lisää Konferenssijulkaisun artikkeli

Lisää viite sivu Should Be Open
    Title Should Be  Lisää viite

References are reset
    Page Should Contain  Lisätyt viitteet: 0

Lisää artikkeli sivu Should Be Open
    Title Should Be  Lisää artikkeli

Final Cleanup
    Reset References
    Close Browser
