import urllib.request # for getting the page from the internet
import re # for using regex 
import os # for making a directory
import sys
import html # for extracting html characters


# This is used to bypass some of the webpages that attempt to block access from Python
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
opener = AppURLopener()


def saveRecipe(url, recipeFile):
    '''Save the contents of a url to a .txt file at a given location'''
    
    print("Retrieving webpage")
    
    # try to get the webpage content
    try:
        # Get the webpage content
        req = opener.open(url)
        page_content = req.read()
    
    except (FileNotFoundError, ValueError):
        print("Webpage could not be reached!")
        page_content = "<title>Failed to load webpage</title>".encode()
        raise
        
    
    # save the page content to the provided .txt file
    try:
        with open(recipeFile, 'w+t', encoding='utf-8') as fid:   
            fid.write(url)
            fid.write('\n\n\n')
            fid.write(page_content.decode())
    except FileNotFoundError:
        print("Destination directory not found!")
        raise
        
        
  
def getTitle(recipeFile):
    '''Get the title from the recipe file'''
    
    print("Finding title")
    
    # open the file and get its text
    with open(recipeFile, 'rt', encoding='utf-8') as inf:              
        url = inf.readline()  # get the url from the first line of the file
        filetext = inf.read()  # get the rest of the file (doesn't include the first line because that was already read)
      
    # escape html character encodings
    filetext = html.unescape(filetext)
    
    #search for the first thing that is found between <title></title> tags
    pattern = re.compile("(?<=\<title\>)(.*?)(?=\<\/title\>)",re.DOTALL)
    match = re.search(pattern, filetext)
    
    # check if a title was a found and clean it up
    try:
        # try to clean up the result that was found.
        title = re.sub(r'[^\x00-\x7F]+',' ', match.group(0)) #remove non-ASCII characters by replacing them with white space
        title = re.sub(r'[\t\n\r\f\v]','', title) #remove most "blank" characters that aren't spaces
        title.strip()  #remove leading or trailing white space from title
        
       
    except AttributeError:
        # if cleaning failed because no title was found, set the title to "Title not found!"
        print("Title not found!")
        title = "Title not found!"
        
    finally:
        return title


  
def getIngredientList(recipeFile):
        
    print("Finding ingredients")
    
    # open the file and get its text
    with open(recipeFile, 'rt', encoding='utf-8') as inf:              
        url = inf.readline()  # get the url from the first line of the file
        filetext = inf.read()  # get the rest of the file (doesn't include the first line because that was already read)
    
    filetext = html.unescape(filetext)
    #
    # find an ingredient list
    #

    # find all html tags that include contain "ingredient (keep the open quote to avoid finding extra stuff, but leave off the closing quote so that it still works if labels are plural or have suffixes)
    # or maybe leave off the open quote to help find "p-ingredient" tags or "RecipeIngredient" tags
    ingpattern1 = re.compile("<[^>]*?ingredient[^>]*>.*?<",re.IGNORECASE)
    ingList = re.findall(ingpattern1, filetext)

    # for each item that was found, strip out the html tags and leave behind what was in between them
    for ndx, member in enumerate(ingList):
        # print('\n')
        # print(ndx)
        # print(ingList[ndx])
        ingpattern2 = re.compile("(?<=>)(.*?)(?=<)") # pattern that finds everything between '>' and '<' (can also end with a new line)
        ingList[ndx] = re.search(ingpattern2,ingList[ndx]).group(0) # sets the element in ingList to the version with html stripped out
        ingList[ndx].strip()

    # remove any blank elements from ingList
    ingList = [x for x in ingList if x != '']

    return ingList
        
        
def setup(url):
    '''Setup function that is called when first receiving the url.
    This runs all of the functions to save the webpage, extract the title, and extract the ingredients.
    '''
    
    global rcpTitle
    global rcpIngList
    
    #attempt to open the url and save the contents to a file
    # if there is an error, end code execution
    try:
        # saveRecipe(url, rcpFile)
        pass
    except (FileNotFoundError, ValueError):
        print("Something went wrong while retrieving the recipe. Ending execution.") 
        sys.exit()

        
        
    # get the recipe title and the list of ingredients
    rcpTitle = getTitle(rcpFile)      
    rcpIngList = getIngredientList(rcpFile)

    print("Setup complete!")    

#
#   
# functions to use after recipe has been loaded
#   
#

def findIngredient(ingredient, ingList):
    ''' when given an ingredient and an ingredient list, find all entries of the list that mention the ingredient'''
    ingResult = [x for x in ingList if ingredient in x]
    
    return ingResult



    
    

# parameters        
rcpUrl = "http://www.lecremedelacrumb.com/slow-cooker-ranch-chicken-tacos/"
rcpIngredient = "onion"
folderName = "testRun3"           
fileName = "recipe.txt"        


# build the file path based on the directory the script is running from
localFolder = os.path.dirname(__file__) 
filePath = localFolder + "\\" + folderName
rcpFile = filePath + "\\" + fileName

# Create the results folder if it doesn't exit already
if not os.path.isdir(filePath):
    os.makedirs(filePath)



#    
#
# actual code
#
#   
    
    
    
    
setup(rcpUrl) #retrieve the recipe and get the relevant data


print(rcpTitle)

rcpIngAmt = findIngredient(rcpIngredient, rcpIngList)

print(rcpIngAmt)



        
        
        
        
        
        
        
        
        
        
        
        