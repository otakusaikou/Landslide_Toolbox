# -*- coding: utf-8 -*-
'''
Created on 2013/08/15
Updated on 2014/09/15
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
        self.button2.set_filename(os.path.join(self.demlayer, " "))
        self.button3.set_filename(os.path.join(self.slopelayer, " "))
        self.button4.set_filename(os.path.join(self.aspectlayer, " "))
        self.button5.set_current_folder(self.outputdir)
        self.doTransOnly.set_active(False)
        self.overwriteBtn1.set_active(False)
        self.overwriteBtn2.set_active(False)
    
    def setconfig(self, tag, widget):
        cur = os.getcwd()
        os.chdir(analysispath) 
        if len(sys.argv) > 1:
           result = os.popen("python conf.py 1")
        else:
           result = os.popen("python conf.py")
        os.chdir(cur)

    def setFileChooser(self, widget):
        flag = not self.doTransOnly.get_active()
        self.label3.set_sensitive(flag)
        self.label4.set_sensitive(flag)
        self.button3.set_sensitive(flag)
        self.button4.set_sensitive(flag)
        self.overwriteBtn1.set_sensitive(flag)
        self.overwriteBtn2.set_sensitive(flag)

    #about dialog
    def show_about(self, widget, data):
        dialog = gtk.AboutDialog()
        dialog.set_name("Analysis")
        dialog.set_version("1.1")
        dialog.set_authors(["Jihn-Fa Jan", "Fan-En Kung", "Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_documenters(["Shih-Kuang Chang", "Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_artists(["Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_comments("This program is witten for coordinate transformation and filtering of landslide data.")
        dialog.set_license("Department of Land Economics, NCCU (c) All RIGHTS RESERVED\thttp://goo.gl/NK8Lk0")
        dialog.set_website("http://goo.gl/NK8Lk0")
        dialog.set_logo(gtk.gdk.pixbuf_new_from_file(os.path.join(analysispath, "Img\\logo.png")))

        #show dialog
        dialog.run()

        #destroy method must be called otherwise the "Close" button will not work.
        dialog.destroy()
 
    def __init__(self, inputdir = os.path.join(os.getcwd(), "input"), outputdir = os.path.join(os.getcwd(), "output"), demlayer = os.path.join(os.getcwd(), "reference_data"), slopelayer = os.path.join(os.getcwd(), "reference_data"),  aspectlayer = os.path.join(os.getcwd(), "reference_data")):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Analysis')
        window.set_size_request(430, 500)
        window.connect('destroy', lambda w: gtk.main_quit())

        mainbox = gtk.VBox(False, 10)
        window.add(mainbox)
        
        self.menu_items = (
            ('/_File', None, None, 0, '<Branch>'),
            ('/File/_Reset', '<control>R', self.reset, 0, None),
            ('/File/_Config Settings', '<control>P', self.setconfig, 0, None),
            ('/File/sep1', None, None, 0,'<Separator>'),
            ('/File/_Quit', '<control>Q', gtk.main_quit, 0, None),
            ('/_Help', None, None, 0,'<LastBranch>'),
            ('/Help/About', 'F1', self.show_about, 0, None)        
        )
        
        self.inputdir = inputdir
        self.outputdir = outputdir
        self.demlayer = demlayer
        self.slopelayer = slopelayer
        self.aspectlayer = aspectlayer

        
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
        
    
    ##dem layer 
        self.label2 = gtk.Label("The dem layer path...")
        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, True, False, 0)
        hbox.pack_start(self.label2, False, True, 5)  
        
          
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        self.button2 = gtk.FileChooserButton('DEM layer path')
        self.button2.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
        self.button2.set_current_folder(self.demlayer)
        filter = gtk.FileFilter()
        filter.add_pattern("*.img")
        filter.add_pattern("*.tif")
        filter.add_pattern("*.adf")
        self.button2.set_filter(filter)
        hbox.pack_start(self.button2, True, True, 0)
        
    ##separator
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        hsaparator = gtk.HSeparator()
        hbox.pack_start(hsaparator, True, True, 10)

    ##Just do Coordinates Transformation Check Button
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(5)
        mainbox.pack_start(hbox, True, False, 0)

        self.doTransOnly = gtk.CheckButton("Just Do Coordinates Transformation")
        self.doTransOnly.set_active(False)
        self.doTransOnly.connect("toggled", self.setFileChooser)
        hbox.pack_start(self.doTransOnly, False, False, 10)
        
    ##slope layer 
        self.label3 = gtk.Label("The slope layer path...")
        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, True, False, 0)
        hbox.pack_start(self.label3, False, True, 5)  
        
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        self.button3 = gtk.FileChooserButton('Slope layer path')
        self.button3.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
        self.button3.set_current_folder(self.slopelayer)
        self.button3.set_filter(filter)
        hbox.pack_start(self.button3, True, True, 0)
        
        self.overwriteBtn1 = gtk.CheckButton("Overwrite Old Table")
        self.overwriteBtn1.set_active(False)
        hbox.pack_start(self.overwriteBtn1, False, False, 10)
        
    ##aspect layer 
        self.label4 = gtk.Label("The aspect layer path...")
        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, True, False, 0)
        hbox.pack_start(self.label4, False, True, 5)  
        
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        self.button4 = gtk.FileChooserButton('Aspect layer path')
        self.button4.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
        self.button4.set_current_folder(self.aspectlayer)
        self.button4.set_filter(filter)
        hbox.pack_start(self.button4, True, True, 0)
        
        self.overwriteBtn2 = gtk.CheckButton("Overwrite Old Table")
        self.overwriteBtn2.set_active(False)
        hbox.pack_start(self.overwriteBtn2, False, False, 10)
        
    ##separator
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        hsaparator = gtk.HSeparator()
        hbox.pack_start(hsaparator, True, True, 10)
        
    ##output directory path
        self.label5 = gtk.Label("The output directory path...")
        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, True, False, 0)
        hbox.pack_start(self.label5, False, True, 5)   
          
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        self.button5 = gtk.FileChooserButton('Output directory')
        self.button5.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.button5.set_current_folder(self.outputdir)
        hbox.pack_start(self.button5, True, True, 0)   

    ##analyze button box
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 10)

        button = gtk.Button('Analyze')
        button.connect('clicked', self.transform)
        button.set_size_request(70, 25)
        hbox.pack_start(button, True, False, 0)

        window.show_all()
        
    def reloadConfig(self):
        settings = open(configpath)
        lines = settings.readlines()
        global host, port, database, user, password
        host = lines[0].split("=")[-1].replace("\n", "")
        port = lines[1].split("=")[-1].replace("\n", "")
        database = lines[2].split("=")[-1].replace("\n", "")
        user = lines[3].split("=")[-1].replace("\n", "")
        password = lines[4].split("=")[-1].replace("\n", "")
        settings.close()
    
    def transform(self, widget):
        #read config file
        self.reloadConfig()

        #get shapefile list
        os.chdir(self.button1.get_filename())
        shp_list = glob.glob("*.shp")
        os.chdir(analysispath)
        
        #check if the inputdir is empty
        if len(shp_list) == 0:
            self.showMessage("Can't find any shapefile in input directory.", None, False, gtk.MESSAGE_WARNING)
            return 
 
        #check if the dem raster file is valid
        if not self.button2.get_filename():
            self.showMessage("Can't find any valid dem raster file.", None, False, gtk.MESSAGE_WARNING)
            return

        flag = not self.doTransOnly.get_active()
        #check if the slope raster file is valid
        #flag means that the program will do both coordinate transformation and analysis
        if not self.button3.get_filename() and flag:
            self.showMessage("Can't find any valid slope raster file.", None, False, gtk.MESSAGE_WARNING)
            return

        #check if the aspect raster file is valid
        if not self.button4.get_filename() and flag:
            self.showMessage("Can't find any valid aspect raster file.", None, False, gtk.MESSAGE_WARNING)
            return 

        A = Analysis(self.button1.get_filename(), self.button5.get_filename(), self.button2.get_filename(), self.button3.get_filename(), self.button4.get_filename())
        msg, result, writelog, icon = A.transform(shp_list, self.overwriteBtn1.get_active(), self.overwriteBtn2.get_active(), flag)
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
            os.chdir(self.button5.get_filename())
            log = open("log.txt", "a")
            log.write("-"*34 + time.strftime("%Y%m%d_%H%M%S", time.gmtime()) + "-"*34 + "\n")
            log.write(result)
            log.write("-"*34 + time.strftime("%Y%m%d_%H%M%S", time.gmtime()) + "-"*34 + "\n")
            log.close()
            os.chdir(root)
        
class Analysis:
    def __init__(self, inputdir = os.path.join(os.getcwd(), "input"), outputdir = os.path.join(os.getcwd(), "output"), demlayer = os.path.join(os.getcwd(), "reference_data"), slopelayer = os.path.join(os.getcwd(), "reference_data"),  aspectlayer = os.path.join(os.getcwd(), "reference_data")):
        #initialize I/O directory
        self.inputdir = inputdir
        self.outputdir = outputdir
        self.demlayer = demlayer
        self.slopelayer = slopelayer
        self.aspectlayer = aspectlayer
        self.tmpdir = os.path.join(self.outputdir, "tmpdir")
        
        if not os.path.exists(self.inputdir):
            os.mkdir(self.inputdir)
            
        if not os.path.exists(self.outputdir):
            os.mkdir(self.outputdir)
            
            
    def transform(self, shp_list, overwriteSlope, overwriteAspect, flag):
        tStart = time.time()
        result = ""
        #connect to database
        try:
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port='%s' password='%s'" % (database, user, host, port, password))
            cur = conn.cursor()
        except:
            return "Unable to connect to the database.\nCheck your config file.", result, True, gtk.MESSAGE_WARNING

        result = ""
        
        #flag means that program will do both coordinate transformation and zonal statistic analysis
        if flag:
            if not os.path.exists(self.tmpdir):
                os.mkdir(self.tmpdir)
                
            #coordinate transformation
            result += img2map(shp_list, self.inputdir, self.tmpdir, self.demlayer, flag)
                
            if not os.path.exists(os.path.join(self.outputdir, "RiverSide")):
                os.mkdir(os.path.join(self.outputdir, "RiverSide"))
            
            if not os.path.exists(os.path.join(self.outputdir, "Landslide")):
                os.mkdir(os.path.join(self.outputdir, "Landslide")) 
            #landslide analysis
            msg, result2, writelog, haveerror = landslide_analysis(conn, os.path.join(self.tmpdir, "landslide_97"), self.outputdir, self.slopelayer, overwriteSlope, self.aspectlayer, overwriteAspect, host, port, database, user, password)
        
            #update result
            result += result2
        
            #check error
            if haveerror:
                return msg, result, writelog, gtk.MESSAGE_WARNING
        
            #get original landslide
            msg, result2, writelog, haveerror = extract_origin(self.inputdir, self.outputdir)
            
            #check error
            if haveerror:
                return msg, result, writelog, gtk.MESSAGE_WARNING
        
            #update result
            result += result2
            
        else:
            #coordinate transformation
            result += img2map(shp_list, self.inputdir, self.outputdir, self.demlayer, flag)
        
        conn.close()
        tEnd = time.time()

        
        return "Works done! It took %f sec" % (tEnd - tStart), result, True, gtk.MESSAGE_INFO
    
            
def main():
    gtk.main()
    return 0

if __name__ == '__main__':
    analysispath = os.getcwd()
    #opened by Toolbox
    if len(sys.argv) > 1:
        root = os.path.dirname(os.path.dirname(os.getcwd()))
        if not os.path.exists(os.path.join(analysispath, "..", "conf")):
            os.mkdir(os.path.join(analysispath, "..", "conf"))
        configpath = os.path.join(analysispath, "..", "conf", "Analysis.ini")
        
        inputdir = os.path.join(root, "input")
        if not os.path.exists(inputdir):
            os.mkdir(inputdir)

        outputdir = os.path.join(root, "output")
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)

        GUI(inputdir, outputdir)
    #opened directly
    else:
        root = os.getcwd()
        configpath = os.path.join(analysispath, "Analysis.ini")
        
        inputdir = os.path.join(root, "input")
        if not os.path.exists(inputdir):
            os.mkdir(inputdir)

        outputdir = os.path.join(root, "output")
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)
        
        GUI()
        
    #read config file
    if not os.path.exists(configpath):
        settings = open(configpath, "w")
        settings.write("host=localhost\nport=5432\ndbname=gis\nuser=postgres\npassword=mypassword")
        host = "localhost"
        port = "5432"
        database = "gis"
        user = "postgres"
        password = "mypassword"
        settings.close()
    else:
        settings = open(configpath)
        lines = settings.readlines()
        host = lines[0].split("=")[-1].replace("\n", "")
        port = lines[1].split("=")[-1].replace("\n", "")
        database = lines[2].split("=")[-1].replace("\n", "")
        user = lines[3].split("=")[-1].replace("\n", "")
        password = lines[4].split("=")[-1].replace("\n", "")
        settings.close()
    main()
