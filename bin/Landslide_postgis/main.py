# -*- coding: utf-8 -*-
'''
Created on 2013/08/15
Updated on 2014/05/10
@author: Otakusaikou
Description: This program is a GUI version of two shp file processor
'''

import os, pygtk, time, sys, psycopg2, glob
pygtk.require('2.0')
import gtk

from utils import img2map, landslide_analysis, extract_origin

class GUI:
    def get_main_menu(self, window):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.MenuBar, '<main>', accel_group)
        item_factory.create_items(self.menu_items)
        window.add_accel_group(accel_group)
        self.item_factory = item_factory
        return item_factory.get_widget('<main>')
    
    def reset(self, tag, widget):
        self.button1.set_current_folder(self.inputdir)
        self.button2.set_current_folder(self.outputdir)
        
    def __init__(self, inputdir = os.path.join(os.getcwd(), "input"), outputdir = os.path.join(os.getcwd(), "output")):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Landslide_processor.py')
        window.set_size_request(350, 220)
        window.connect('destroy', lambda w: gtk.main_quit())

        mainbox = gtk.VBox(False, 10)
        window.add(mainbox)
        
        self.menu_items = (
            ('/_File', None, None, 0, '<Branch>'),
            ('/File/_Reset', '<control>R', self.reset, 0, None),
            ('/File/sep1', None, None, 0,'<Separator>'),
            ('/File/_Quit', '<control>Q', gtk.main_quit, 0, None),
            ('/_Help', None, None, 0,'<LastBranch>'),
            ('/Help/About', None, None, 0, None)        
        )
        
        self.inputdir = inputdir
        self.outputdir = outputdir

        
    ##menu bar
        menubar = self.get_main_menu(window)
        mainbox.pack_start(menubar, False, True, 0)
        
    ##input directory path
        self.label1 = gtk.Label("The input directory path...")
        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, True, False, 0)
        hbox.pack_start(self.label1, False, True, 5)   
          
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        filter = gtk.FileFilter()
        filter.add_pattern("*.shp")
        
        self.button1 = gtk.FileChooserButton('Input directory')
        self.button1.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)   
        self.button1.set_current_folder(self.inputdir)
        self.button1.set_filter(filter)
        hbox.pack_start(self.button1, True, True, 0)  
        
    ##separator
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        hsaparator = gtk.HSeparator()
        hbox.pack_start(hsaparator, True, True, 10)
        
        hbox.show()
        hsaparator.show()

    ##output directory path
        self.label2 = gtk.Label("The output directory path...")
        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, True, False, 0)
        hbox.pack_start(self.label2, False, True, 5)   
          
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        self.button2 = gtk.FileChooserButton('Output directory')
        self.button2.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.button2.set_current_folder(self.outputdir)
        hbox.pack_start(self.button2, True, True, 0)   

    ##analyze button box
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 5)

        button = gtk.Button('Analyze')
        button.connect('clicked', self.transform, self.button1, self.button2)
        button.set_size_request(70, 25)
        hbox.pack_start(button, True, False, 0)

        window.show_all()
        
    def reloadConfig(self):
        settings = open(configpath)
        lines = settings.readlines()
        global host, database, user, password
        host = lines[0].split("=")[-1].replace("\n", "")
        database = lines[1].split("=")[-1].replace("\n", "")
        user = lines[2].split("=")[-1].replace("\n", "")
        password = lines[3].split("=")[-1].replace("\n", "")
        settings.close()
        settings.close()
        
    
    def transform(self, widget, inputfile, outputdir):
        #read config file
        self.reloadConfig()
        A = Analysis(self.button1.get_filename(), self.button2.get_filename())
        msg, result, writelog, icon = A.transform()
        self.showMessage(msg, result, writelog, icon)
        
    #pop up error message and write out result
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
            os.chdir(self.button2.get_filename())
            log = open("log.txt", "a")
            log.write("-"*34 + time.strftime("%Y%m%d_%H%M%S", time.gmtime()) + "-"*34 + "\n")
            log.write(result)
            log.write("-"*34 + time.strftime("%Y%m%d_%H%M%S", time.gmtime()) + "-"*34 + "\n")
            log.close()
            os.chdir(root)
        
class Analysis:
    def __init__(self, inputdir = os.path.join(os.getcwd(), "input"), outputdir = os.path.join(os.getcwd(), "output")):
        #initialize I/O directory
        self.inputdir = inputdir
        self.outputdir = outputdir
        self.tmpdir = os.path.join(self.outputdir, "tmpdir")
        
        if not os.path.exists(self.inputdir):
            os.mkdir(self.inputdir)
            
        if not os.path.exists(self.outputdir):
            os.mkdir(self.outputdir)
            
        if not os.path.exists(self.tmpdir):
            os.mkdir(self.tmpdir)
            
        if not os.path.exists(os.path.join(self.outputdir, "RiverSide")):
            os.mkdir(os.path.join(self.outputdir, "RiverSide"))
        
        if not os.path.exists(os.path.join(self.outputdir, "Landslide")):
            os.mkdir(os.path.join(self.outputdir, "Landslide")) 
            
    def transform(self):
        tStart = time.time()
        
        result = ""
        
        #connect to database
        try:
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (database, user, host, password))
            cur = conn.cursor()
        except:
            return "Unable to connect to the database.\nCheck your config file.", result, True, gtk.MESSAGE_WARNING
            
        #get shapefile list
        os.chdir(self.inputdir)
        shp_list = glob.glob("*.shp")
        os.chdir(analysispath)
        
        #check if the inputdir is empty
        if len(shp_list) == 0:
            conn.close()
            return "Can't find any shapefile in input directory.", result, False, gtk.MESSAGE_WARNING
        
        retult = ""
        
        #coordinate transformation
        result += img2map(shp_list, self.inputdir, self.tmpdir)
        
        #landslide analysis
        msg, result2, writelog, haveerror = landslide_analysis(conn, self.tmpdir, self.outputdir, host, database, user, password)
        
        #update result
        result += result2
        
        #check error
        if haveerror:
            return msg, result, writelog, gtk.MESSAGE_WARNING
        
        #get original landslide
        msg, result2, writelog, haveerror = extract_origin(self.inputdir, self.outputdir)
        
        #update result
        result += result2
        
        #check error
        if haveerror:
            return msg, result, writelog, gtk.MESSAGE_WARNING
            
        tEnd = time.time()
        
        return "Works done! It took %f sec" % (tEnd - tStart), result, True, gtk.MESSAGE_INFO
    
    
            
        
            
def main():
    gtk.main()
    return 0

if __name__ == '__main__':
    analysispath = os.getcwd()
    if len(sys.argv) > 1:
        root = os.path.dirname(os.path.dirname(os.getcwd()))
        if not os.path.exists(os.path.join(analysispath, "..", "conf")):
            os.mkdir(os.path.join(analysispath, "..", "conf"))
        configpath = os.path.join(analysispath, "..", "conf", "Analysis.ini")
        GUI(os.path.join(root, "input"), os.path.join(root, "output"))
    else:
        root = os.getcwd()
        configpath = os.path.join(analysispath, "Analysis.ini")
        GUI()
        
    #read config file
    if not os.path.exists(configpath):
        settings = open(configpath, "w")
        settings.write("host=localhost\ndbname=gis\nuser=postgres\npasswords=mypassword")
        settings.close()
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