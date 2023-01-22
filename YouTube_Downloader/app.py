from pytube import YouTube
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import re
import threading

class Application:

    def __init__(self,root):
        self.root=root
        self.root.grid_rowconfigure(0,weight=2)
        self.root.grid_columnconfigure(0,weight=1)
        self.root.config(bg="#ffdddd")

        top_lable = Label(self.root,text="Youtube Downloader",fg="orange",font=('Type Xero',70))
        top_lable.grid(pady=(0,10))

        link_lable = Label(self.root,text="Please paste any youtube video link below",font=('Type Xero',30))
        link_lable.grid(pady=(0,20))

        self.youtubeEntryVar = StringVar()

        self.youtubeEntry = Entry(self.root,width=70,textvariable=self.youtubeEntryVar,font=('Type Xero',25),fg='red')
        self.youtubeEntry.grid(pady=(0,15),ipady=6)

        self.youtubeEntryError = Label(self.root,text="",font=('Type Xero',25))
        self.youtubeEntryError.grid(pady=(0,8))

        self.youtubeFileSaveLabel = Label(self.root,text="Choose Directory",font=('Type Xero',30))
        self.youtubeFileSaveLabel.grid()

        self.youtubeFileDirectoryButton = Button(self.root,text="Directory",font=('Type Xero',15),command=self.openDirectory)
        self.youtubeFileDirectoryButton.grid(pady=(10,3))

        self.filelocationLabel = Label(self.root,text="",font=('Type Xero',25))
        self.filelocationLabel.grid()

        self.youtubeChooselabel = Label(self.root,text="Choose the download type",font=('Type Xero',25))
        self.youtubeChooselabel.grid()

        self.downloadChoices = [("Audio MP3",1),("Video MP4",2)]
        self.ChoicesVar = StringVar()
        self.ChoicesVar.set(1)

        for text,mode in self.downloadChoices:
            self.youtubeChoices = Radiobutton(self.root,text=text,font=('Type Xero',15),variable=self.ChoicesVar,value=mode)
            self.youtubeChoices.grid()

        self.downloadButton = Button(self.root,text="Download",width=10,font=('Type Xero',15),command=self.checkyoutubelink)
        self.downloadButton.grid(pady=(30,5))

    def checkyoutubelink(self):
        self.matchyoutubelink = re.match("^https://www.youtube.com/.",self.youtubeEntryVar.get())
        if not self.matchyoutubelink:
            self.youtubeEntryError.config(text="Invalid youtube link",fg='red')
        elif not self.openDirectory:
            self.filelocationLabel.config(text="Please choose a Directory")
        elif (self.matchyoutubelink and self.openDirectory):
            self.downladWindow()

    def downladWindow(self):
        self.newWindow = Toplevel(self.root)
        self.root.withdraw()
        self.newWindow.state("zoomed")
        self.newWindow.grid_rowconfigure(0,weight=0)
        self.newWindow.grid_columnconfigure(0,weight=1)

        self.app = SecondApp(self.newWindow,self.youtubeEntryVar.get(),self.FolderName,self.ChoicesVar.get())

    def openDirectory(self):
        self.FolderName=filedialog.askdirectory()

        if (len(self.FolderName)>0):
            self.filelocationLabel.config(text=self.FolderName,fg='green')
            return True
        else:
            self.filelocationLabel.config(text="Please choose a directory",fg='red')

class SecondApp:
    def __init__(self,downloadWindow,youtubelink,FolderName,Choices):
        self.downloadWindow = downloadWindow
        self.youtubelink = youtubelink
        self.FolderName = FolderName
        self.Choices = Choices

        self.yt = YouTube(self.youtubelink)

        if (Choices == "1"):
            self.video_type = self.yt.streams.filter(only_audio=True).first()
            self.MaxFileSize = self.video_type.filesize
        if (Choices == "2"):
            self.video_type = self.yt.streams.first()
            self.MaxFileSize = self.video_type.filesize

        self.loadingLabel = Label(self.downloadWindow,text="Downloading in progress",font=("Small Fonts",40))
        self.loadingLabel.grid(pady=(100,0))

        self.loadingPercent = Label(self.downloadWindow,text="0",fg="green",font=("Agency Fb",40))
        self.loadingPercent.grid(pady=(50,0))

        self.progressbar = ttk.Progressbar(self.downloadWindow,length=500,orient='horizontal',mode='indeterminate')
        self.progressbar.grid(pady=(50,0))
        self.progressbar.start()

        threading.Thread(target=self.yt.register_on_progress_callback(self.show_progress)).start()

        threading.Thread(target=self.downloadFile).start()

    def downloadFile(self):
        if self.Choices == "1":
            self.yt.streams.filter(only_audio=True).first().download(self.FolderName)
        if self.Choices == "2":
            self.yt.streams.first().download(self.FolderName)

    def show_progress(self,streams=None,Chunks=None,filehandle=None,bytes_remaining=0):
        self.percentCount = float("%0.2f"% (100-(100*(bytes_remaining/self.MaxFileSize))))
        print(self.percentCount)
        if self.percentCount < 100:
            self.loadingPercent.config(text=self.percentCount)
        else:
            self.progressbar.stop()
            self.loadingLabel.grid_forget()
            self.progressbar.grid_forget()

            self.downloadFinished = Label(self.downloadWindow,text="Download Finished",font=("Agency Fb",30))
            self.downloadFinished.grid(pady=(150,0))

            self.downloadedFileName = Label(self.downloadWindow,text=self.yt.title,font=('Terminal',30))
            self.downloadedFileName.grid(pady=(50,0))

            MB = float("%0.2f"%(self.MaxFileSize/1000000))
            self.dowloadFileSize = Label(self.downloadWindow,text=str(MB),font=('Agency Fb',30))
            self.dowloadFileSize.grid(pady=(50,0))

if __name__=="__main__":
    window = Tk()
    window.title("Welcome to Youtube downloader")
    window.state("zoomed")
    app = Application(window)

    mainloop()