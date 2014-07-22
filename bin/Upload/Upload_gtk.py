# -*- coding: utf-8 -*-
'''
Created on 2014/04/25
Updated on 2014/07/05
@author: Otakusaikou
Description: This program is a GUI for uploading shapefile
'''

import os
import pygtk
import sys
import psycopg2
pygtk.require('2.0')
import gtk
import time

class GUI:
    def __init__(self, inputdir = os.getcwd()):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Upload')
        window.set_size_request(380, 170)
        window.connect('destroy', lambda w: gtk.main_quit())

        mainbox = gtk.VBox(False, 10)
        window.add(mainbox)
        mainbox.show()
        window.show()
        
        self.menu_items = (
            ('/_File', None, None, 0, '<Branch>'),
            ('/File/_Reset', '<control>R', self.reset, 0, None),
            ('/File/_Config Settings', '<control>P', self.setconfig, 0, None),
            ('/File/sep1', None, None, 0,'<Separator>'),
            ('/File/_Quit', '<control>Q', gtk.main_quit, 0, None),
            ('/_Help', None, None, 0,'<LastBranch>'),
            ('/Help/About', 'F1', self.show_about, 0, None)        
        )
        
    ##menu bar
        menubar = self.get_main_menu(window)
        mainbox.pack_start(menubar, False, True, 0)
        menubar.show()
        
    ##input file path
        label1 = gtk.Label("The input shapefile...")
        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, True, False, 0)
        hbox.pack_start(label1, False, True, 5)   
        
        label1.show()
        hbox.show()
          
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        filter = gtk.FileFilter()
        filter.add_pattern("*.shp")
        
        self.button1 = gtk.FileChooserButton(root)
        self.button1.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
        self.button1.set_current_folder(root)
        self.button1.connect("selection-changed", self.dialogChanged)
        self.button1.set_filter(filter)
        hbox.pack_start(self.button1, True, True, 0)  
        
        self.button1.show()
        hbox.show()
        
    ##config box
        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, True, False, 0)
        
        label2 = gtk.Label("Table Name:")
        hbox.pack_start(label2, False, True, 5)
        
        label2.show()
        
        self.entry1 = gtk.Entry()
        self.entry1.set_size_request(100, 20)
        hbox.pack_start(self.entry1, False, False, 0)
        
        self.entry1.show()
        
        self.checkbutton = gtk.CheckButton("Use Big5 Encoding")
        hbox.pack_start(self.checkbutton, False, True, 20)
        
        self.checkbutton.show()
        
        hbox.show()
        
    ##upload button box
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 5)

        button = gtk.Button('Upload')
        button.connect('clicked', self.uploadButton)
        button.set_size_request(70, 25)
        hbox.pack_start(button, True, False, 0)
        
        button.show()
        hbox.show()

    #about dialog
    def show_about(self, widget, data):
        dialog = gtk.AboutDialog()
        dialog.set_name("Upload")
        dialog.set_version("1.0")
        dialog.set_authors(["Jihn-Fa Jan", "Fan-En Kung", "Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_documenters(["Shih-Kuang Chang", "Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_artists(["Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_comments("This program is witten to load the results of landslide data to database.")
        dialog.set_license("Department of Land Economics, NCCU (c) All RIGHTS RESERVED\thttp://goo.gl/NK8Lk0")
        dialog.set_website("http://goo.gl/NK8Lk0")
        dialog.set_logo(gtk.gdk.pixbuf_new_from_file(os.path.join(uploadpath, "Img/ncculogo.png")))

        #show dialog
        dialog.run()

        #destroy method must be called otherwise the "Close" button will not work.
        dialog.destroy()
        
    def setconfig(self, tag, widget):
        cur = os.getcwd()
        os.chdir(uploadpath) 
        if len(sys.argv) > 1:
           result = os.popen("python conf.py 1")
        else:
           result = os.popen("python conf.py")
        os.chdir(cur)
        
    def uploadButton(self, widget):
        #reload config file
        self.reloadConfig()
        U = Upload(self.button1.get_filename(), self.entry1.get_text())
        msg, result, writelog, icon = U.upload(self.checkbutton.get_active())
        self.showMessage(msg, result, writelog, icon)
        
    def showMessage(self, msg, result = None, writelog = False, icon = gtk.MESSAGE_WARNING):
        print msg
        #pop up message
        messagedialog = gtk.MessageDialog(None, 
            gtk.DIALOG_DESTROY_WITH_PARENT, icon, 
            gtk.BUTTONS_CLOSE, msg) 
        messagedialog.set_position(gtk.WIN_POS_CENTER)
        messagedialog.run()
        messagedialog.destroy()
        
        if writelog:
            result += msg + "\n"
            os.chdir(root)
            log = open("log.txt", "a")
            log.write("-"*34 + time.strftime("%Y%m%d_%H%M%S", time.gmtime()) + "-"*34 + "\n")
            log.write(result)
            log.write("-"*34 + time.strftime("%Y%m%d_%H%M%S", time.gmtime()) + "-"*34 + "\n")
            log.close()
            os.chdir(root)
            
    def get_main_menu(self, window):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.MenuBar, '<main>', accel_group)
        item_factory.create_items(self.menu_items)
        window.add_accel_group(accel_group)
        self.item_factory = item_factory
        return item_factory.get_widget('<main>')
    
    def reset(self, tag, widget):
        self.button1.set_filename(os.path.join(root, " "))
        self.entry1.set_text("")
        self.checkbutton.set_active(False)
        
    def reloadConfig(self):
        settings = open(configpath)
        lines = settings.readlines()
        global host, port, dbname, user, passwords
        host = lines[0].split("=")[-1].replace("\n", "")
        port = lines[1].split("=")[-1].replace("\n", "")
        dbname = lines[2].split("=")[-1].replace("\n", "")
        user = lines[3].split("=")[-1].replace("\n", "")
        passwords = lines[4].split("=")[-1].replace("\n", "")
        settings.close()
        
    #reset table name entry after file chooser dialog changed
    def dialogChanged(self, widget):
        if self.button1.get_filename():
            dir, file = os.path.split(self.button1.get_filename())
            fname, ext = os.path.splitext(file)
            self.entry1.set_text(fname)
    
class Upload:
    def __init__(self, filename, tablename):
        self.filename = filename
        self.tablename = tablename
        
    def upload(self, checkbutton):
        result = ""
        if not self.filename:
            return "The input filename is empty!", result, False, gtk.MESSAGE_WARNING
            
        if self.tablename.replace(" ", "") == "":
            return "The input table name is empty!", result, False, gtk.MESSAGE_WARNING
            
        inputdir, shp_data = os.path.split(self.filename)
        
        #connect to database
        try:
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port='%s' password='%s'" % (dbname, user, host, port, passwords))
        except:
            return "Unable to connect to the database.\nCheck your config file.", result, True, gtk.MESSAGE_WARNING
        
        #check if table exists
        try:
            cur = conn.cursor()
            cur.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='" + self.tablename.lower() + "')")
            exists = cur.fetchone()[0]
            if exists:
                return "Table '%s' is exist in database '%s', please change a table name!" % (self.tablename, dbname), result, True, gtk.MESSAGE_WARNING
        except:
            conn.close()

        #import shapefile
        try:
            os.chdir(inputdir) #change current directory to target shapefile
            #check 'Use Big5 Encoding' option
            if checkbutton:
                cmdstr = "shp2pgsql -s 3826 -c -D -I -W big5 %s %s | psql -h %s -p %s -d %s -U %s" % (shp_data, self.tablename, host, port, dbname, user)
                result += os.popen(cmdstr).read()
            else:
                cmdstr = "shp2pgsql -s 3826 -c -D -I %s %s | psql -h %s -p %s -d %s -U %s" % (shp_data, self.tablename, host, port, dbname, user)
                result += os.popen(cmdstr).read()

            #check if target table exists 
            cur.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='" + self.tablename.lower() + "')")
            exists = cur.fetchone()[0]
            if exists:
                return "Import shapefile '%s' to database '%s' as table '%s' successfully." % (shp_data, dbname, self.tablename), result, True, gtk.MESSAGE_INFO
            else:
                return "Import shapefile data error", result, True, gtk.MESSAGE_WARNING
        except:
            return "Import shapefile data error", result, True, gtk.MESSAGE_WARNING
            
def main():
    gtk.main()
    return 0

if __name__ == '__main__':
    uploadpath = os.getcwd()
    if len(sys.argv) > 1:
        root = os.path.dirname(os.path.dirname(os.getcwd()))
        if not os.path.exists(os.path.join(uploadpath, "..", "conf")):
            os.mkdir(os.path.join(uploadpath, "..", "conf"))
        configpath = os.path.join(uploadpath, "..", "conf", "Upload.ini")
        GUI(os.path.join(root, "input"))
    else:
        root = os.getcwd()
        configpath = os.path.join(uploadpath, "Upload.ini")
        GUI()
    #read config file
    if not os.path.exists(configpath):
        settings = open(configpath, "w")
        settings.write("host=localhost\nport=5432\ndbname=gis\nuser=postgres\npasswords=mypassword")
        host = "localhost"
        port = "5432"
        dbname = "gis"
        user = "postgres"
        passwords = "mypassword"
        settings.close()
    else:
        settings = open(configpath)
        lines = settings.readlines()
        host = lines[0].split("=")[-1].replace("\n", "")
        port = lines[1].split("=")[-1].replace("\n", "")
        dbname = lines[2].split("=")[-1].replace("\n", "")
        user = lines[3].split("=")[-1].replace("\n", "")
        passwords = lines[4].split("=")[-1].replace("\n", "")
        settings.close()
    main()
