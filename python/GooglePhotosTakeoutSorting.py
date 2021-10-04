import os, json, shutil
def main():
    dirs = ['Photos from 2019']
    #dirs = ['Photos from 2018' ,'Photos from 2019','Photos from 2020','Photos from 2021']
    
    #clear error log
    open("./errors.log", "w").close()
    totalfiles = 0
    NonPicFiles = 0
    PicOrVidFiles = 0
    for dir in dirs:
        for file in os.listdir("./"+dir):
            totalfiles+=1
            lenght = len(file) - 4
            if file[lenght:] == "json":
                NonPicFiles +=1
            else:
                PicOrVidFiles +=1

    print("You have approximately " + str(PicOrVidFiles) + " files (Pictures and Videos), not including the json Metadata Files (Of which you have "+ str(NonPicFiles) +". If we were to include these into the calculation you would have "+str(totalfiles)+" files)")
    input()
    NonPicFilesCurrent = 0
    currentfile = 0
    for dir in dirs:
        # print(dir)
        for file in os.listdir("./"+dir):
            #print(file)
            lenght = len(file) - 4
            if file[lenght:] == "json":
                outfile_json = open("./"+dir+"/"+file, "r")
                outfile = json.load(outfile_json)
                outfile_json.close()
                NonPicFilesCurrent+=1
                print("Currently reading json File "+str(NonPicFilesCurrent)+" of "+str(NonPicFiles))
                picturepath = "./"+dir+"/"+outfile["title"]
                #piclen = len(picturepath) - 3
                #if picturepath[piclen:] == "jpg":
                if 'mobileUpload' not in outfile["googlePhotosOrigin"]:
                    errors = open("./errors.log", "a")
                    errors.write("File > " + picturepath + " < was not uploaded via the Mobile App. ORIGIN_OF_ERROR=" + file+"\n")
                    errors.close()
                elif 'deviceFolder' not in outfile["googlePhotosOrigin"]["mobileUpload"]:
                    errors = open("./errors.log", "a")
                    errors.write("File > " + picturepath + " < some needed Data seems to be missing. ORIGIN_OF_ERROR=" + file+"\n")
                    errors.close()
                elif 'localFolderName' not in outfile["googlePhotosOrigin"]["mobileUpload"]["deviceFolder"]:
                    errors = open("./errors.log", "a")
                    errors.write("File > " + picturepath + " < does not seem to Contain Folderdata for specified Picture/Video. ORIGIN_OF_ERROR=" + file+"\n")
                    errors.close()
                else:
                    currentfile+=1
                    outfolder = outfile["googlePhotosOrigin"]["mobileUpload"]["deviceFolder"]["localFolderName"]
                    if os.path.exists("./sortedoutput/" + outfolder):
                        Sorting(outfile, dir, outfolder, file, picturepath, currentfile, PicOrVidFiles)
                    else:
                        os.mkdir("./sortedoutput/" + outfolder)
                        Sorting(outfile, dir, outfolder, file, picturepath, currentfile, PicOrVidFiles)

                                
def Sorting(outfile, dir, outfolder, file, picturepath, currentfile, PicOrVidFiles):
    destination = "./sortedoutput/" + outfolder
    if os.path.exists(picturepath):
        #print(picturepath + " > " + destination)
        print("Currently copying File "+str(currentfile)+" of "+str(PicOrVidFiles))
        shutil.copy2(picturepath, destination)
    else:
        errors = open("./errors.log", "a")
        errors.write("File > " + picturepath + " does not exists. ORIGIN="+file+"\n")
        errors.close()

if __name__ == '__main__':
    main()