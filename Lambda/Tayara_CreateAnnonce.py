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
    "annonceCreated" : False,
    "newCreatedArticleToken" : None,
    "createAnnoncePageOnePassed" : False,
    "createAnnoncePageTwoPassed" : False,
    "createAnnoncePageThreePassed" : False,
    "createAnnoncePageFourPassed" : False,
    "createAnnonceTimeInSeconds" : None,
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

def create_annonce(browser, annonceObject):
    start_time = time.time()
    # Init
    categorie = int(annonceObject['categorie'])
    sousCategorie = int(annonceObject['sousCategorie'])
    titre = str(annonceObject['titre'])
    description = str(annonceObject['description'])
    prix = str(annonceObject['prix'])
    livraison = bool(annonceObject['livraison'])
    imagesUrls = annonceObject['imagesUrls']
    ville = annonceObject['ville']
    delegation = annonceObject['delegation']
    principalPhoneNumber = bool(annonceObject['principalPhoneNumber'])
    phoneNumber = str(annonceObject['phoneNumber'])
    #

    browser.get('https://www.tayara.tn/fr/post-listing/')

    
    #--------Page 1--------
    formElements = browser.find_elements(By.CSS_SELECTOR, '.relative.w-full')
    # Categorie 
    categorieSelect = formElements[1].find_element(By.TAG_NAME, 'select')
    categorieSelect.find_elements(By.TAG_NAME, 'option')[categorie].click()

    # sousCategorie
    sousCategorieSelect = formElements[2].find_element(By.TAG_NAME, 'select')
    sousCategorieSelect.find_elements(By.TAG_NAME, 'option')[sousCategorie].click()

    # Title
    titreInput = formElements[3].find_element(By.TAG_NAME, 'input')
    titreInput.send_keys(titre)
    
    # Description
    descriptionInput = formElements[4].find_element(By.TAG_NAME, 'textarea')
    descriptionInput.send_keys(description)

    # Prix
    prixInput = formElements[5].find_element(By.TAG_NAME, 'input')
    prixInput.send_keys(prix)

    # Click Suivant
    suivantBtn = browser.find_elements(By.TAG_NAME, 'button')[1]
    suivantBtn.click()


    time.sleep(1)
    lifeCycleOfThisFunction['createAnnoncePageOnePassed'] = True # Logging
    #--------Page 2--------
    formElements = browser.find_elements(By.CSS_SELECTOR, '.relative.w-full')
    # Livraison 
    livraisonSelect = formElements[1].find_element(By.TAG_NAME, 'select')
    if livraison:
        livraisonSelect.find_elements(By.TAG_NAME, 'option')[1].click()
    else:
        livraisonSelect.find_elements(By.TAG_NAME, 'option')[2].click()

    # Click Suivant
    suivantBtn = browser.find_elements(By.TAG_NAME, 'button')[1]
    suivantBtn.click()

    
    time.sleep(1)
    lifeCycleOfThisFunction['createAnnoncePageTwoPassed'] = True # Logging
    #--------Page 3--------
    formElements = browser.find_elements(By.CSS_SELECTOR, '.max-w-sm.mx-auto')
    #Images
    imagesInput = formElements[0].find_element(By.TAG_NAME, 'input')
    imagesCreatedByThis = []
    for imageUrl in imagesUrls:
        URL = imageUrl
        # Load the image and download it locally => Send it via upload to tayara => Delete the local image
    
        randomSting = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        imageAbsolutePath = "/tmp/" + randomSting + '.jpg'
        # Load from url and save to local using Pillow
        image = Image.open(io.BytesIO(requests.get(URL).content)).save(imageAbsolutePath)
        # Send to Form (Uploading...)
        imagesInput.send_keys(imageAbsolutePath)
        imagesCreatedByThis.append(imageAbsolutePath)


    # Click Suivant
    suivantBtn = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
    suivantBtn.click()
    
    time.sleep(1)
    lifeCycleOfThisFunction['createAnnoncePageThreePassed'] = True # Logging
    #--------Page 4--------
    formElements = browser.find_elements(By.CSS_SELECTOR, '.relative.w-full')
    # Ville
    villeSelect = formElements[1].find_element(By.TAG_NAME, 'select')
    villeSelect.find_elements(By.TAG_NAME, 'option')[ville].click()

    # Délégation
    time.sleep(2) # Sleep because these options only appear after selecting the ville 
    delegationSelect = formElements[2].find_element(By.TAG_NAME, 'select')
    delegationSelect.find_elements(By.TAG_NAME, 'option')[delegation].click()
    
    # Utiliser votre numéro principal ?(It's on by default)
    if principalPhoneNumber == False:
        phoneNumberStateChooser = browser.find_element(By.CSS_SELECTOR, '.py-3').find_element(By.TAG_NAME, 'button')
        phoneNumberStateChooser.click()
        # Numero de contact
        '''Refresh DOM'''
        formElements = browser.find_elements(By.CSS_SELECTOR, '.relative.w-full')
        # Add phonenumber
        phoneNumberSelect = formElements[3].find_element(By.TAG_NAME, 'input')
        phoneNumberSelect.send_keys(phoneNumber)
    
    # Click Suivant
    time.sleep(1)
    suivantBtn = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
    suivantBtn.click()

    # Make sure it finished posting by checkin for the button booster l'annonce
    print("Waiting for it to post")
    wait = WebDriverWait(browser, 1000)
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Booster l'annonce"))
    print("Finished Waiting")
    
    
    lifeCycleOfThisFunction['createAnnoncePageFourPassed'] = True # Logging
    

    # Clicker sur Booster l'annonce and get the post id from the url that comes
    browser.find_element(By.TAG_NAME, 'main').find_element(By.TAG_NAME, 'button').click()
    # Wait for url to change
    wait.until(EC.url_contains("boost"))
    # Get Url
    urlThatComes = browser.current_url
    newCreatedArticleToken = urlThatComes[-25:-1]

    # Delete Images Created By This Post
    for img in imagesCreatedByThis:
        os.remove(img)

    
    lifeCycleOfThisFunction['createAnnonceTimeInSeconds'] = time.time() - start_time # Logging
    lifeCycleOfThisFunction['annonceCreated'] = True # Logging
    lifeCycleOfThisFunction['newCreatedArticleToken'] = newCreatedArticleToken # Logging
    return True


def main(annonceObject):
    browser = makeNewBrowser()
    if login(browser, "chedychaaben@gmail.com", "23447715"):
        create_annonce(browser, annonceObject)
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
            event['headers']['data']
        except:
            return "Please make sure you are passing data inside headers with the request"
        #
        try:
            urlparams = json.loads(event['headers']['data'])
            annonceObject = {
                    'categorie'            : urlparams['categorie'] ,
                    'sousCategorie'        : urlparams['sousCategorie'] ,
                    'titre'                : urlparams['titre'] ,
                    'description'          : urlparams['description'] ,
                    'prix'                 : urlparams['prix'] ,
                    'livraison'            : urlparams['livraison'] ,
                    'imagesUrls'           : urlparams['imagesUrls'] ,
                    'ville'                : urlparams['ville'] ,
                    'delegation'           : urlparams['delegation'] ,
                    'principalPhoneNumber' : urlparams['principalPhoneNumber'] ,
                    'phoneNumber'          : urlparams['phoneNumber']
            }
        except:
            return "Please make sure the data json object is in correct format"
    else:
        annonceObject= {
                    'categorie'            : 7 ,
                    'sousCategorie'        : 6 ,
                    'titre'                : "Testing From Lambda" ,
                    'description'          : "Description" ,
                    'prix'                 : 999 ,
                    'livraison'            : False ,
                    'imagesUrls'           : ["https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg"] ,
                    'ville'                : 15 ,
                    'delegation'           : 13 ,
                    'principalPhoneNumber' : True ,
                    'phoneNumber'          : "50215486"
        }


    # Running the main program
    main(annonceObject)
    #
    return lifeCycleOfThisFunction