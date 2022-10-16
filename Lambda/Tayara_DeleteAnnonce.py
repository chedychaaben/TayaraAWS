from headless_chrome import create_driver
import time, os, requests, io, random, string, json, threading
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

lifeCycleOfThisFunction = {
    "loggedIn" : False,
    "loginPageOnePassed" : False,
    "loginPageTwoPassed" : False,
    "loginTimeInSeconds" : None,
    "annonceDeleted" : False,
    "deleteAnnonceTimeInSeconds" : None,
}

def makeNewBrowser():
    """ Sample handle about how to use the imported the layer with custom parameters """
    new_params = [
        "--window-size=1920x1080",
        "--user-agent=MyUserAgent"
    ]
    browser = create_driver(new_params)
    return browser

def login(browser, username, password):
    start_time = time.time()
    browser.get('https://www.tayara.tn/fr/login/')

    #--------Page 1--------
    form = browser.find_element(By.CSS_SELECTOR, 'form.px-0')
    usernameInputHTML = form.find_element(By.CSS_SELECTOR, 'input')
    usernameInputHTML.click()
    usernameInputHTML.send_keys(username)
    Btn = form.find_elements(By.CSS_SELECTOR, 'button')[0].click()
    lifeCycleOfThisFunction['loginPageOnePassed'] = True # Logging
    
    # Make sure we switched to password's page
    wait = WebDriverWait(browser, 1000)
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Saisir votre mot de passe"))
    
    #--------Page 2--------
    form = browser.find_element(By.CSS_SELECTOR, 'form.px-0')
    passwordInputHTML = form.find_element(By.CSS_SELECTOR, 'input')
    passwordInputHTML.click()
    passwordInputHTML.send_keys(password)
    Btn = form.find_elements(By.CSS_SELECTOR, 'button')[0].click()
    lifeCycleOfThisFunction['loginPageTwoPassed'] = True # Logging

    # Make sure we are logged correctly
    wait = WebDriverWait(browser, 1000)
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Voir mon profil et mes annonces"))
    
    
    lifeCycleOfThisFunction['loggedIn'] = True # Logging
    lifeCycleOfThisFunction['loginTimeInSeconds'] = time.time() - start_time # Logging
    return True

def delete_annonce_by_tokenId(browser, annonceTokenId):
    start_time = time.time()
    annonce_url = f'https://www.tayara.tn/fr/item/{annonceTokenId}/'
    browser.get(annonce_url)
    # Make sure we have to supprimer btn            
    wait = WebDriverWait(browser, 1000)
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Supprimer l'annonce"))
    # Clicker Sur Supprimer
    ButtonsContainer = browser.find_element(By.CSS_SELECTOR, '.flex.flex-col.justify-start.gap-3')
    supprimerElement = ButtonsContainer.find_elements(By.CSS_SELECTOR, '.relative.w-full')[2-1]
    supprimerElement.find_elements(By.TAG_NAME, 'button')[1-1].click()
    # Refresh DOM and Clicker sur Confimer La Suppresion
    time.sleep(1)
    ButtonsContainer = browser.find_element(By.CSS_SELECTOR, '.flex.flex-col.justify-start.gap-3')
    supprimerElement = ButtonsContainer.find_elements(By.CSS_SELECTOR, '.relative.w-full')[2-1]
    supprimerElement.find_elements(By.TAG_NAME, 'button')[3-1].click()
    
    lifeCycleOfThisFunction['annonceDeleted'] = True # Logging
    lifeCycleOfThisFunction['deleteAnnonceTimeInSeconds'] = time.time() - start_time # Logging
    return True

def main(annonceToken):
    browser = makeNewBrowser()
    if login(browser, "chedychaaben@gmail.com", "23447715") and annonceToken != None:
        if requests.get(f"https://www.tayara.tn/fr/item/{annonceToken}/").status_code == 200:
            delete_annonce_by_tokenId(browser, annonceToken)
    # Quitting
    browser.close()
    browser.quit()


def lambda_handler(event, _context):
    prod = True
    if prod:
        #Getting annonce Data From Headers Data
        try:
            event['headers']
        except:
            return "Please make sure you are passing headers with the request"
        #
        try:
            event['headers']['annoncetoken']
        except:
            return "Please make sure you are passing annoncetoken inside headers with the request"
        #
        try:
            annonceToken = event['headers']['annoncetoken']
        except:
            return "Please make sure the data json object is in correct format"
    else:
        annonceToken = "632f010932140be961ac4272"


    # Running the main program
    main(annonceToken)
    #
    return lifeCycleOfThisFunction