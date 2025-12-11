*** Settings ***
Library  SeleniumLibrary
Library  ../AppLibrary.py

*** Variables ***
${SERVER}        localhost:5001
${DELAY}         0.5 seconds
${HOME_URL}      http://${SERVER}
${RESET_URL}     http://${SERVER}/reset_db
${BROWSER}       chrome
${HEADLESS}      false

*** Keywords ***
Open And Configure Browser
    IF  $BROWSER == 'chrome'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
        Call Method  ${options}  add_argument  --incognito
    ELSE IF  $BROWSER == 'firefox'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
        Call Method  ${options}  add_argument  --private-window
    END
    IF  $HEADLESS == 'true'
        Set Selenium Speed  0.01 seconds
        Call Method  ${options}  add_argument  --headless
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}

Go To Starting Page
    Go To  ${HOME_URL}

Reset References
    Go To  ${RESET_URL}

Reset Application And Go To Starting Page
  Reset References
  Go To Starting Page

Main Page Should Be Open
    Title Should Be  Etusivu

References are reset
    Page Should Contain  Viitteitä näkyvillä: 0

Final Cleanup
    Reset References
    Close Browser

Luo Kirja
    [Arguments]  ${title}  ${author}  ${year}  ${isbn}  ${publisher}
    Click Link  Lisää kirja
    Lisää kirja sivu Should Be Open
    Input Text  title  ${title}
    Input Text  author  ${author}
    Input Text  year  ${year}
    Input Text  isbn  ${isbn}
    Input Text  publisher  ${publisher}
    Click Button  Tallenna kirja
    Main Page Should Be Open

Luo Artikkeli
    [Arguments]  ${title}  ${author}  ${journal}  ${year}  ${doi}  ${volume}  ${pages}
    Click Link  Lisää artikkeli
    Lisää artikkeli sivu Should Be Open
    Input Text  title  ${title}
    Input Text  author  ${author}
    Input Text  journal  ${journal}
    Input Text  year  ${year}
    Input Text  DOI  ${doi}
    Input Text  volume  ${volume}
    Input Text  pages  ${pages}
    Click Button  Tallenna artikkeli
    Main Page Should Be Open

Luo Konferenssijulkaisun Artikkeli
    [Arguments]  ${title}  ${author}  ${year}  ${booktitle}
    Click Link  Lisää Konferenssijulkaisun Artikkeli
    Lisää Konferenssijulkaisun Artikkeli sivu Should Be Open
    Input Text  title  ${title}
    Input Text  author  ${author}
    Input Text  year  ${year}
    Input Text  booktitle  ${booktitle}
    Click Button  Tallenna Konferenssijulkaisun artikkeli
    Main Page Should Be Open