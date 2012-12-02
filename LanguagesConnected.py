#-------------------------------------------------------------------------------
# Name:        Languages Connected
# Purpose:
#
# Author:      Rogue
#
# Created:     26-11-2012
# Copyright:   (c) Rogue 2012
#-------------------------------------------------------------------------------

import ideone
from time import sleep
import Tkinter as tkinter
import tkSimpleDialog
import tkFileDialog
import tkMessageBox
import os

#The password is the api password which can be set in 'my account' setting of ideone website. http://ideone.com/account/
USERNAME="bitideone"
PASSWORD="bitideone"

class gui:
    ## temp
    #languages={1:'asdf',2:'ert'}
    def __init__(self, root, wsdl):
        self.root=root
        self.root.wm_title('Languages Connected: Untitled')
        self.keyBindings()
        self.wsdl=wsdl
        self.languages=self.wsdl.getLanguages()
        print self.languages
        self.design()

    def keyBindings(self):
        self.root.bind_all("<Control-n>", self.menu_new)
        self.root.bind_all("<Control-N>", self.menu_new)
        self.root.bind_all("<Control-l>", self.menu_openLink)
        self.root.bind_all("<Control-L>", self.menu_openLink)
        self.root.bind_all("<Control-o>", self.menu_open)
        self.root.bind_all("<Control-O>", self.menu_open)
        self.root.bind_all("<Control-s>", self.menu_save)
        self.root.bind_all("<Control-S>", self.menu_save)
        self.root.bind_all("<Control-z>", self.menu_undo)
        self.root.bind_all("<Control-Z>", self.menu_undo)
        self.root.bind_all("<Control-y>", self.menu_redo)
        self.root.bind_all("<Control-Y>", self.menu_redo)
        self.root.bind_all("<Control-u>", self.submit_code)
        self.root.bind_all("<Control-U>", self.submit_code)

    def design(self):
        self.design_menubar()
        self.design_workspace()

######## Workspace
    def design_workspace(self):
        self.pane=tkinter.PanedWindow(self.root,orient=tkinter.HORIZONTAL, showhandle=True)
        self.pane.pack(fill=tkinter.BOTH, expand=1)
        self.leftframe=tkinter.Frame(self.pane,relief=tkinter.RAISED, bd=5)
        self.rightframe=tkinter.Frame(self.pane, relief=tkinter.RAISED, bd=4)
        self.pane.add(self.leftframe)
        self.pane.add(self.rightframe)

        self.design_leftPane()
        self.design_rightPane()

######## END of Workspace

######## Left pane
    def design_leftPane(self):
        self.languagesList=tkinter.Listbox(self.leftframe, relief=tkinter.GROOVE, bd=4, selectmode=tkinter.SINGLE, exportselection=0)
        for i in self.languages:
            self.languagesList.insert(tkinter.END, self.languages[i])
        self.languagesList.selection_set(0)
        #self.languagesList.configure(yscrollcommand=self.addscrollbar(self.leftframe, self.languagesList.yview, tkinter.RIGHT, tkinter.Y))
        self.languagesList.pack(fill=tkinter.Y, side=tkinter.LEFT)
        self.design_leftPane_upper()
        self.design_leftPane_lower()
######## END of Left pane

######## Left upper pane
    def design_leftPane_upper(self):
        self.left_upper_frame=tkinter.Frame(self.leftframe)
        self.button_submit=tkinter.Button(self.left_upper_frame, text='Submit', command=self.submit_code, underline=1 )
        self.button_submit.pack(anchor='e')
        self.label_code=tkinter.Label(self.left_upper_frame, text='Code:')
        self.label_code.pack()
        self.sourceCode=tkinter.Text(self.left_upper_frame, wrap=tkinter.NONE, undo=True)
        self.sourceCode.configure(yscrollcommand=self.addscrollbar(self.left_upper_frame, self.sourceCode.yview, tkinter.RIGHT, tkinter.Y))
        self.sourceCode.configure(xscrollcommand=self.addscrollbar(self.left_upper_frame, self.sourceCode.xview, tkinter.BOTTOM, tkinter.X, tkinter.HORIZONTAL))
        self.sourceCode.pack(fill=tkinter.BOTH)
        self.left_upper_frame.pack(fill=tkinter.BOTH)
######## End of Left upper pane

######## Left lower pane
    def design_leftPane_lower(self):
        self.left_lower_frame=tkinter.Frame(self.leftframe)
        self.label_input=tkinter.Label(self.left_lower_frame, text='Input:')
        self.label_input.pack()
        self.input=tkinter.Text(self.left_lower_frame, wrap=tkinter.NONE, undo=True)
        self.input.configure(yscrollcommand=self.addscrollbar(self.left_lower_frame, self.input.yview, tkinter.RIGHT, tkinter.Y))
        self.input.pack(fill=tkinter.BOTH)
        self.left_lower_frame.pack(fill=tkinter.BOTH)
######## End of Left lower pane

    def submit_code(self, event=None):
        self.label_status.configure(text='Status : Sent')
        code=self.sourceCode.get(1.0, tkinter.END)
        print code
        lang=self.languagesList.get(int(self.languagesList.curselection()[0]))
        print lang
        langid=0
        for i in self.languages:
            if self.languages[i]==lang:
                langid=i
        inp=self.input.get(1.0,tkinter.END)
        print inp

        link=self.wsdl.createSubmission(code, langid, input=inp)
        self.getSubmission(link)


    def getSubmission(self, link):
        print link
        self.link.delete(0, tkinter.END)
        self.link.insert(0, 'http://ideone.com/'+link)
        while True:
            s=self.wsdl.getSubmissionStatus(link)[0]
            if s==0:
                self.label_status.configure(text='Status : Idle')
                break
            elif s==1:
                self.label_status.configure(text='Status : Compiling...')
            elif s==3:
                self.label_status.configure(text='Status : Running...')
            else:
                self.label_status.configure(text='Status : Waiting...')
            sleep(1)
        ret=self.wsdl.getSubmissionDetails(link)
        print ret
        langindex=0
        for lang in self.languagesList.get(0, tkinter.END):
            if lang==self.languages[ret['langId']]:
                break
            langindex+=1
        self.languagesList.selection_clear(0, tkinter.END)
        self.languagesList.selection_set(langindex)

        self.sourceCode.delete(1.0, tkinter.END)
        self.sourceCode.insert(1.0, ret['source'])

        self.input.delete(1.0, tkinter.END)
        self.input.insert(1.0, ret['input'])

        self.output.delete(1.0, tkinter.END)
        self.output.insert(1.0, ret['output']+"\nProgram executed in :"+str(ret['time'])+" seconds.\n"+"Memory used :"+str(ret['memory'])+" bytes.")

        self.error.delete(1.0, tkinter.END)
        self.error.insert(1.0, ret['stderr']+ret['cmpinfo'])
        print 'completed'
######## END of Left pane

######## Right pane
    def design_rightPane(self):
        self.label_status=tkinter.Label(self.rightframe, text='Status : Idle')
        self.label_status.pack()
        self.label_link=tkinter.Label(self.rightframe, text='Link:')
        self.label_link.pack()
        self.link=tkinter.Entry(self.rightframe)
        self.link.insert(0, 'http://ideone.com/')
        self.link.pack(fill=tkinter.X)
        self.label_output=tkinter.Label(self.rightframe, text='Output:')
        self.label_output.pack()
        self.output=tkinter.Text(self.rightframe, wrap=tkinter.NONE)
        self.output.pack(fill=tkinter.BOTH)
        self.label_error=tkinter.Label(self.rightframe, text='Error:')
        self.label_error.pack()
        self.error=tkinter.Text(self.rightframe, wrap=tkinter.NONE)
        self.error.pack(fill=tkinter.BOTH)
######## End of right pane

######## MENUBAR
    def design_menubar(self):
        self.menubar=tkinter.Menu(self.root)

        self.file_menu=tkinter.Menu(self.menubar)
        self.file_menu.add_command(label='New', command=self.menu_new, accelerator='Ctrl+N', underline=0)
        self.file_menu.add_command(label='Open Link...', command=self.menu_openLink, accelerator='Ctrl+L', underline=5)
        self.file_menu.add_command(label='Open...', command=self.menu_open, accelerator='Ctrl+O', underline=0)
        self.file_menu.add_command(label='Save', command=self.menu_save, accelerator='Ctrl+S', underline=0)
        self.file_menu.add_command(label='Save As...', command=self.menu_saveas)

        self.edit_menu=tkinter.Menu(self.menubar)
        self.edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', command=self.menu_undo)
        self.edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', command=self.menu_redo)

        self.help_menu=tkinter.Menu(self.menubar)
        #self.help_menu.add_command(label='Help', command=self.help_help)
        self.help_menu.add_command(label='About', command=self.help_about)

        self.menubar.add_cascade(label='File', menu=self.file_menu)
        self.menubar.add_cascade(label='Edit', menu=self.edit_menu)
        self.menubar.add_cascade(label='Help', menu=self.help_menu)

        self.root.config(menu=self.menubar)

    def menu_new(self, event=None):
        self.sourceCode.delete(1.0, tkinter.END)
        self.input.delete(1.0, tkinter.END)
        self.error.delete(1.0, tkinter.END)
        self.output.delete(1.0, tkinter.END)
        self.link.delete(0,tkinter.END)
        self.link.insert(0, 'http://ideone.com/')
        self.root.wm_title('Languages Connected: Untitled')
        self.sourceCode.edit_reset()
        self.input.edit_reset()

    def menu_openLink(self, event=None):
        link=tkSimpleDialog.askstring('Open Link', 'Enter the link')
        if link != None:
            self.label_status.configure(text='Status : Recieving')
            l=link.split('/')[-1]
            self.getSubmission(l)
            self.sourceCode.edit_reset()
            self.input.edit_reset()

    def menu_open(self, event=None):
        self.openedFile=tkFileDialog.askopenfilename()
        if self.openedFile:
            try:
                a=open(self.openedFile, 'r')
                self.sourceCode.delete(1.0, tkinter.END)
                self.sourceCode.insert(1.0, a.read())
                a.close()
                self.root.wm_title('Languages Connected: '+ self.openedFile)
                self.sourceCode.edit_reset()
            except:
                tkMessageBox.showerror('Error','Error in opening file!!!')

    def menu_save(self, event=None):
        if self.openedFile:
            try:
                a=open(self.openedFile, 'w')
                a.write(self.sourceCode.get(1.0, tkinter.END))
                a.close()
            except:
                tkMessageBox.showerror('Error','Error in saving file!!!')

    def menu_saveas(self):
        self.openedFile=tkFileDialog.asksaveasfilename()
        if self.openedFile:
            try:
                a=open(self.openedFile, 'w')
                a.write(self.sourceCode.get(1.0, tkinter.END))
                a.close()
                self.root.wm_title('Languages Connected: '+ self.openedFile)
            except:
                tkMessageBox.showerror('Error','Error in saving file!!!')

    def menu_undo(self, event=None):
        a=self.root.focus_get()
        try:
            if a==self.sourceCode:
                print 'foc source'
                self.sourceCode.edit_undo()
            if a==self.input:
                print 'foc input'
                self.input.edit_undo()
        except:
            print 'undo stack empty'

    def menu_redo(self, event=None):
        a=self.root.focus_get()
        try:
            if a==self.sourceCode:
                print 'foc source'
                self.sourceCode.edit_redo()
            if a==self.input:
                print 'foc input'
                self.input.edit_redo()
        except:
            print 'redo stack empty'

    def help_help(self):
        print 'Help'

    def help_about(self):
        info='''
        Developed by : Himanshu Shekhar (Rogue)
        Email : himanshu.coolshekhar@gmail.com

        This application uses Ideone API (ideone.com)
        by Sphere Research Labs (sphere-research.com)
        '''
        tkMessageBox.showinfo("About...", info)
########## END of MENUBAR

#yscrollcommand=self.addscrollbar(self.languagesList.yview, tkinter.RIGHT, tkinter.Y))
    def addscrollbar(self,root,view, _side, _fill, _orient=tkinter.VERTICAL):
        scroll=tkinter.Scrollbar(root, command=view, orient=_orient)
        scroll.pack(side=_side, fill=_fill)
        return scroll.set



def main():
    if USERNAME=="" or PASSWORD=="":
        print "Username or API password not set"
        exit(1)
    root=tkinter.Tk("LanguagesConnected")
    wsdl=ideone.IdeOne(user=USERNAME, password=PASSWORD)
    try:
        a=wsdl.testFunction()
    except:
        print "Error while connecting"
        exit(2)
    a=gui(root, wsdl)
    root.mainloop()

if __name__ == '__main__':
    main()
