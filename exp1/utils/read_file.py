import os

def getfilelist(maildir, filelist):
    if os.path.isfile(maildir):
        filelist.append(maildir)
    elif os.path.isdir(maildir):
        for s in os.listdir(maildir):
            newdir = os.path.join(maildir, s)
            getfilelist(newdir, filelist)
    return filelist

if __name__ == "__main__":
    file = open("../dataset/path", 'w')
    filelist = []
    docID = 1
    getfilelist(maildir="../dataset/maildir/", filelist=filelist)
    for p in filelist:
        p=p+'\n'
        file.write(p)
        docID += 1
    file.close()