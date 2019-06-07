#  Do prawidłowego działania programu niezbędne jest zainstalowanie środowiska Python w wersji wyższej niż 3.0
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys, os, time
from datetime import datetime

#####################################
#  PARAMETERS
#####################################
CHROME_DRIVER = "./chrome_webdriver/chromedriver.exe"
URL = "https://messages.google.com/web/conversations/new?redirected=true"
#dodać wszystkie stałe z nazwami elementów


#####################################
def addLog( mess ):
    logs = open('./logs.log', 'a')
    dateTime = str(datetime.now()) + '  '
    logs.write(dateTime + mess)
    logs.write('\n')
    logs.close()

#####################################
def driverSetup( driverPath ):
    # linijka potrzebna przy budowaniu pliku .exe z użyciem pyinstallera
    # cdriver_path = os.path.join(sys._MEIPASS, "chromedriver")
    global driver
    driver = webdriver.Chrome(driverPath)
    # driver.minimize_window()
    logString = 'Uruchomienie skryptu ' + os.path.basename(__file__)
    addLog(logString)


#####################################
def initializeConnection( url ):
    driver.get(URL)
    time.sleep(5)       #zamienić aby program czekał do momentu załadowania całego contentu
    driver.find_element_by_id('mat-slide-toggle-1').click()
    addLog('Oczekiwanie na zeskanowanie kodu QR')
    print('Zeskanuj kod QR ...')

    test = True
    while test:
        try:
            test = driver.find_element_by_class_name("qr-code-container").is_displayed()
        except:
            #sprawdzić czy po zeskanowaniu przeszło na poprawną stronę
            print('Kod QR został zeskanowany')
            addLog('Zeskanowano kod QR')
            break

        time.sleep(1)

    logString = 'Synchronizacja z telefonem ustanowiona'
    addLog(logString)

#####################################
def checkArgs():
    print()
    # zastanowić się nad walidacją danych
    # na razie funkcja nie wykorzystywana

#####################################
def sendMessage( phoneNumber, mess):
    time.sleep(3)
    #jak się pojawi .mat-dialog-container, to kliknąć .action-button
    driver.find_element_by_class_name('new-chat').click()
    time.sleep(2)
    driver.find_element_by_class_name('input').send_keys( phoneNumber )
    driver.find_element_by_tag_name('input').send_keys(Keys.RETURN)
    time.sleep(6)
    driver.find_element_by_tag_name('textarea').send_keys( mess )
    driver.find_element_by_class_name('send-button').click()
    print('Wiadomość do ' + phoneNumber + ' została wysłana.  Treść wiadomości: ' +  mess)
    addLog(phoneNumber + '      ' + mess + '    Wiadomość została wysłana')
    #sprawdzić warunek i obsłużyć kiedy wiadomość nie zostanie wysłana

#####################################
def loadDataToSend( fileLocation ):
    global DATA_TO_SEND
    file = open( fileLocation )
    numberOfAdvertisement = file.read()
    file.close()

#####################################
def sendMessagesFromFile( fileLocation ):

#####################################
#  MAIN
#####################################
driverSetup( CHROME_DRIVER )
initializeConnection( URL )

if (len(sys.argv) == 3):
    sendMessage(str(sys.argv[1]), str(sys.argv[2]))
elif (len(sys.argv) == 2):
    sendMessagesFromFile(str(sys.argv[1]))
else:
     print('Niepoprawna ilość argumentów. Możesz użyć jednego lub dwóch argumentów. Przykład użycia poniżej')
     print('    > sms [numer_telefonu] [wiadomosc]')
     print('    > sms [plik_z_danymi]')
     addLog('Podano nieprawidłową ilość argumentów. Wyjście z programu.')
     driver.quit()

driver.quit()