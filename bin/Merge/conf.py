#/usr/bin/python27
'''
Created on 2013/06/20
Updated on 2014/06/2
@author: Otakusaikou
Description: This program is a GUI for config settings
'''

import os, pygtk, time, sys, psycopg2, glob
pygtk.require('2.0')
import gtk

class Config:
    def __init__(self): 
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Merge Config Settings')
        window.set_size_request(300, 270)
        window.connect('destroy', lambda w: gtk.main_quit())

        mainbox = gtk.VBox(False, 5)
        mainbox.set_border_width(10)
        window.add(mainbox)
        mainbox.show()
        window.show()
 
    ##host
        self.label1 = gtk.Label("Host")
        hbox = gtk.HBox(False, 5)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 5)
        hbox.show()
        self.label1.set_size_request(110, 20)
        self.label1.show()
        hbox.pack_start(self.label1, False, False, 5)   
      
        self.entry1 = gtk.Entry()
        self.entry1.set_size_request(20, 25)
        self.entry1.show()
        self.entry1.set_text(host)
        hbox.pack_start(self.entry1, True, True, 0)
        
    ##database name
        self.label2 = gtk.Label("Database Name")
        hbox = gtk.HBox(False, 5)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 5)
        hbox.show()
        self.label2.set_size_request(110, 20)
        self.label2.show()
        hbox.pack_start(self.label2, False, False, 5)   
        
        self.entry2 = gtk.Entry()
        self.entry2.set_size_request(20, 25)
        self.entry2.show()
        self.entry2.set_text(database)
        hbox.pack_start(self.entry2, True, True, 0)
    
    ##user name
        self.label3 = gtk.Label("User Name")
        hbox = gtk.HBox(False, 5)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 5)
        hbox.show()
        self.label3.set_size_request(110, 20)
        self.label3.show()
        hbox.pack_start(self.label3, False, False, 5)   

        self.entry3 = gtk.Entry()
        self.entry3.set_size_request(20, 25)
        self.entry3.show()
        self.entry3.set_text(user)
        hbox.pack_start(self.entry3, True, True, 0)
    
    ##password
        self.label4 = gtk.Label("Password")
        hbox = gtk.HBox(False, 5)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 5)
        hbox.show()
        self.label4.set_size_request(110, 20)
        self.label4.show()
        hbox.pack_start(self.label4, False, False, 5)   
          
        self.entry4 = gtk.Entry()
        self.entry4.set_size_request(20, 25)
        self.entry4.set_text(password)
        self.entry4.set_visibility(gtk.FALSE)
        self.entry4.show() 
        hbox.pack_start(self.entry4, True, True, 0)
    
    ##check button box
        hbox = gtk.HBox(False, 0)
        mainbox.pack_start(hbox, True, False, 5)
        hbox.show()
        
        self.showpasswordbtn = gtk.CheckButton("Show Password")
        self.showpasswordbtn.set_active(False)
        self.showpasswordbtn.connect("toggled", self.changeVisibility)
        self.showpasswordbtn.show()
        hbox.pack_end(self.showpasswordbtn, False, False, 15)

    ##separator
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 10)
        
        hsaparator = gtk.HSeparator()
        hbox.pack_start(hsaparator, True, True, 10)
        
        hbox.show()
        hsaparator.show()
    
    ##apply/close button box
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(15)
        mainbox.pack_start(hbox, True, False, 0)
        hbox.show()
        
        button = gtk.Button('Save')
        button.set_size_request(70, 25)
        button.connect('clicked', self.change, 1)
        hbox.pack_start(button, True, False, 0)
        button.show()

        button = gtk.Button('Apply')
        button.set_size_request(70, 25)
        button.connect('clicked', self.change, 0)
        hbox.pack_start(button, True, False, 0)
        button.show()
        
        button = gtk.Button('Close')
        button.set_size_request(70, 25)
        button.connect('clicked', lambda x: gtk.main_quit())
        hbox.pack_start(button, True, False, 0)
        button.show()
    
    def changeVisibility(self, widget):
        self.entry4.set_visibility(not self.entry4.get_visibility())
        

    def change(self, widget, tag):
        try:
            settings = open(configpath, "w")
            settings.write("host=%s\ndbname=%s\nuser=%s\npassword=%s" % (self.entry1.get_text(), self.entry2.get_text(), self.entry3.get_text(), self.entry4.get_text()))
            settings.close()
            messagedialog = gtk.MessageDialog(None, 
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                gtk.BUTTONS_CLOSE, "Change applied successfully!") 
            messagedialog.set_position(gtk.WIN_POS_CENTER)
            messagedialog.run()
            messagedialog.destroy()
        except:
            messagedialog = gtk.MessageDialog(None, 
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
                gtk.BUTTONS_CLOSE, "Apply change failed!") 
            messagedialog.set_position(gtk.WIN_POS_CENTER)
            messagedialog.run()
            messagedialog.destroy()
        if tag == 1:
            gtk.main_quit()
        
        

def main():
    Config()
    gtk.main()
    return 0

if __name__ == '__main__':
    mergepath = os.getcwd()
    if len(sys.argv) > 1:
        root = os.path.dirname(os.path.dirname(os.getcwd()))
        if not os.path.exists(os.path.join(mergepath, "..", "conf")):
            os.mkdir(os.path.join(mergepath, "..", "conf"))
        configpath = os.path.join(mergepath, "..", "conf", "MergeShp.ini")
    else:
        root = os.getcwd()
        configpath = os.path.join(mergepath, "MergeShp.ini")
        
    #read config file
    if not os.path.exists(configpath):
        settings = open(configpath, "w")
        settings.write("host=localhost\ndbname=gis\nuser=postgres\npassword=mypassword")
        host = "localhost"
        database = "gis"
        user = "postgres"
        password = "mypassword"
        settings.close()
    else:
        settings = open(configpath)
        lines = settings.readlines()
        host = lines[0].split("=")[-1].replace("\n", "")
        database = lines[1].split("=")[-1].replace("\n", "")
        user = lines[2].split("=")[-1].replace("\n", "")
        password = lines[3].split("=")[-1].replace("\n", "")
        settings.close()
    main()
