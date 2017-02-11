import urllib.request # for getting the page from the internet
import re # for using regex 
import sys # needed for sys.exit(), which ends execution
import os # for making a directory
import html # for converting escape characters into ascii (e.g. turns &amp; into &)
from bs4 import BeautifulSoup

# recipe to search and ingredient to search for
# recipeNum = 3
ingredient = 'salt'

# folders where pages are saved
folderName_String = "RecipeScrapes_Improved"
folderName_Results = "ProcessResults_soup"

        
print('\n\n')
print('-----------------------------------------------------------')




# Find the path that the script is running from
localFolder = os.path.dirname(__file__)

# Create the complete path to folders (so they are placed in the directory where the script is running from)
filePath_String = localFolder + "\\" + folderName_String
filePath_Results = localFolder + "\\" + folderName_Results

# Create the results folder if it doesn't exit already
if not os.path.isdir(filePath_Results):
    os.makedirs(filePath_Results)


def trim(s):
    '''
	remove whitespace on left and right of string s.
	trim whitespace between characters to a single space
	'''
    
    # This seems to be the only way to properly handle the Betty Crocker website which has a bunch of stuff in between the amount for an ingredient and the rest of the ingredient entry
    
    return " ".join(s.split())
    
def isSchemaOrgStandard(soup):
    '''Determine if the recipe uses the schema.org/Recipe standard'''
    
    # see if any tags are found that contain the itemtype flag for schema.org/Recipe standard
    try:
        return soup.findAll(True, {"itemtype" : re.compile("http://schema.org/Recipe", re.IGNORECASE)}) != []
        
    except Exception as e:
        logging.debug(e)
        return False


def findIngList(soup):
    '''Extract the list of ingredients from the HTML'''
    
    # if the soup fits the schema.org format
    if isSchemaOrgStandard(soup):
        ingList = soup.findAll(True, {"itemprop" : re.compile("ingredients", re.IGNORECASE)})    
        
        # for each element in the list, set the element to the text inside the html tags (i.e. remove the html tags themselves)
        for ndx, member in enumerate(ingList):            
            ingList[ndx] = trim(ingList[ndx].get_text()) # set the list elements to be just the text without the HTML tags and strip any whitespace off the ends
    
        return ingList
        
    return ['']
    
def findStepList(soup):
    '''Extract the list of recipe steps from the HTML'''
    
    # if the soup fits the schema.org format
    if isSchemaOrgStandard(soup):
        stepList = soup.findAll(True, {"itemprop" : re.compile("instructions", re.IGNORECASE)})
    
        # for each element in the list, set the element to the text inside the html tags (i.e. remove the html tags themselves)
        for ndx, member in enumerate(stepList):            
            stepList[ndx] = trim(stepList[ndx].get_text()) # set the list elements to be just the text without the HTML tags and strip any whitespace off the ends
    
        return stepList
    return ['']
    
def findTitle(soup):

    # first try to use og:title tag
    og_title = (soup.find("meta", attrs={"property": "og:title"}) or soup.find("meta", attrs={"name": "og:title"}))
    
    if og_title and og_title["content"]:
        print("Title found using og:title tag.")
        return og_title["content"]
    
  
    # if that didn't work get the recipe title from a <title> tag
    if soup.title and soup.title.string:
        print("Title found using <title> tag.")
        return soup.title.string
    
    # if nothing worked, return None
    return ''    

    
    
    
    
    
    
    
    
    
    
for ndx in range(33):

    #read the contents of a file
    print("Reading text file", ndx)
       
    #get the file name
    recipeFile = "recipe" + str(ndx) + ".txt"

    # open the recipe file and save the text to a soup object
    with open(filePath_String + "\\" + recipeFile, 'rt', encoding='utf-8') as inf:              
        url = inf.readline()  # get the url from the first line of the file
        filetext = inf.read()  # get the rest of the file (doesn't include the first line because that was already read)
    filetext = html.unescape(filetext)
    soup = BeautifulSoup(filetext, 'html.parser')


    
    

    print("schema.org? " + str(isSchemaOrgStandard(soup)))
        
    rcpTitle = findTitle(soup)    
    if rcpTitle:
        print("Title: "+rcpTitle)

    rcpIngList = findIngList(soup)
    rcpStepList = findStepList(soup)
    
    
    
    
    # open a file. Write the url, title, and ingredient list to that file
    with open(filePath_Results + "\\" + recipeFile, 'w+t', encoding='utf-8') as fid:   
        fid.write(url)
        fid.write('\n\n\n')
        fid.write(rcpTitle)
        fid.write('\n------------------------------------------------\n')
        
        fid.write('Ingredients:')
        for ndx, member in enumerate(rcpIngList):
            fid.write('\n'+rcpIngList[ndx])
    
        fid.write('\n\n')
        fid.write('Instructions:')
        for ndx, member in enumerate(rcpStepList):
            fid.write('\n'+rcpStepList[ndx])    
    
    
    
    
    
    
    
    
    
    # print("\nIngredients:")
    # for elem in rcpIngList:
        # print(elem)
        
        
    # print("\nInstructions:")
    # for elem in rcpStepList:
        # print(elem)