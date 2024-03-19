#DownloadSorter.py 
#Author: Alexander DeFalco
#Date: March 19th, 2024
'''
Checks all items within a target directory, intended to be the downloads folder of the user, and
sorts all of the files into specific folders according to their file type.

A dictionary is used to correlate multiple file extensions with the same category/target folder, and
this dictionary can be expanded easily to incorporate more file types/extensions.

Users can change the "downloadPath" assignment in order to set their own download folder path.
Right clicking the file explorer bar in Windows and clicking "copy as text address" is sufficient.
Be sure to include the r if backslashes are used, and omit the r if forward slashes are used.
'''
import os
import filecmp
#from time import sleep #used for debugging


#function definition to move file to respective folder, with checks for duplicates by name and by data.
def moveFile(fileName, fileDirectory, offset, dupeCount):

    #try renaming file
    try:    
        os.rename(fileName, fileDirectory)    #move file to new 
        print("File successfully moved")
    #if duplicate file exists in target directory, check for equal data, byte by byte
    except:
        #filecmp == true implies the files are equal, safe to delete
        if (filecmp.cmp(fileName, fileDirectory, shallow=False)) == True:
            #delete duplicate file
            os.remove(fileName)
        #filecmp == false implies files are not equal
        elif (filecmp.cmp(fileName, fileDirectory, shallow=False)) == False:
            #append (dupeCount) before the file extension, and try moving it to target directory
            try:
                dupeCount += 1
                dupeFileDirectory = f"{fileDirectory[:offset]} ({dupeCount}){newFileDirectory[offset:]} "
                os.rename(fileName, dupeFileDirectory)
                print("Duplicate move successful")

            #if appended file name still exists there, reiterate with (#) incremented by one.    
            except Exception as e:
                #throw exception to cmd
                print(f"Error: {e}")
                #recursively call function to try next (#)
                moveFile(fileName, fileDirectory, offset, dupeCount)
            
#set path = r'directory that you would like sorted'
#r'C:...' lets it ignore \ as a string literal. Else, use / instead for directory paths and omit r.
#'C:/Users/ajdfa/Downloads'  is equivalent in this case.             
downloadPath = r'C:\Users\ajdfa\Downloads'        

#sets current working directory to path
os.chdir(downloadPath)

#creates a list called downloads that stores name of all items within downloads folder
downloads = os.listdir(downloadPath)
categoryFolders = []

#Dictionary for folder name and respective file type permitted.
#folder name:file extensions stored as lists (key:value) 
categoryDict = {
    'PDFs':['.pdf'],
    'Applications':['.exe', 'app', '.msi'],
    'Zipped':['.rar', '.zip'],
    'Images':['.png', '.jpg', '.jpeg', '.gif', '.bmp'],
    'Videos':['.mp4', '.mov', '.avi', '.webm', '.wmv', '.mkv' ],
    'Word Documents':['.doc', '.docm', '.docx', '.dot', '.dotx'],
    'Powerpoints':['.pot', '.potm', '.potx', '.ppam', '.pps', '.ppsm', '.ppsx', '.ppt' ,'.pptx'],
    'Java':['.java', '.jar'],
    'CorelDraw':['.cdr']
    }#end dictionary

#for loop to create folders for every category desired.
for category, extensions in categoryDict.items():
  #create directory for each dictionary key, mode = default, exist = ok throws no error when directory already exists.
  os.makedirs(category, mode = 0o777, exist_ok = True )

#nested for loops to iterate through each item in downloads, checking each extension (value) for each respective category (dictionary key)
for category, extensions in categoryDict.items():
    print(f"************************************************{category}************************************************")
    for extension in extensions:
        for download in downloads:
            dupeCount=0 #init to 0 on each iteration, used to append (#) to duplicate names/different data files
            print(download) 
            #if pdf file
            if (download.endswith(extension)):
                #negative value to use in slicing during function call
                fileExtensionOffset = (-1 * len(extension)) 
                workingFileName = os.path.join(downloadPath, download)  #path\filename
                newFileDirectory = os.path.join(category, download)   #path\CategoryFolder\filename
                #calling function to commit to moving/sorting file.
                moveFile(workingFileName, newFileDirectory, fileExtensionOffset, dupeCount)
