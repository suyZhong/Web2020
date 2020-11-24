import os

def getfilelist(mail_dir, filelist):
    if os.path.isfile(mail_dir):
        filelist.append(mail_dir)
    elif os.path.isdir(mail_dir):
        for s in os.listdir(mail_dir):
            newdir = os.path.join(mail_dir, s)
            getfilelist(newdir, filelist)
    return filelist

if __name__ == "__main__":
    file = open("../dataset/path", 'a')
    filelist=[]
    getfilelist(mail_dir="../dataset/maildir/", filelist=filelist)
    for p in filelist:
        p=p+'\n'
        file.write(p)
    file.close()