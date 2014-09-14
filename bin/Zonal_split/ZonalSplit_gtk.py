# -*- coding: utf-8 -*-
'''
Created on 2014/05/02
Updated on 2014/09/14
@author: Otakusaikou
'''
import os
import pygtk
import sys
import psycopg2
import glob
pygtk.require('2.0')
import gtk
import time
import string

class GUI:
    def __init__(self, inputdir = os.path.join(os.getcwd(), "input"), outputdir = os.path.join(os.getcwd(), "output"), identitylayer = os.path.join(os.getcwd(), "identityLayer")):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('ZonalSplit')
        window.set_size_request(350, 320)
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
        
        self.inputfile = inputdir
        self.outputdir = outputdir
        self.identitylayer = identitylayer
        
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
        self.button1.set_filter(filter)
        hbox.pack_start(self.button1, True, True, 0)  
        
        self.button1.show()
        hbox.show()
        
    ##separator
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        hsaparator = gtk.HSeparator()
        hbox.pack_start(hsaparator, True, True, 10)
        
        hbox.show()
        hsaparator.show()
        
    ##identity layer directory
        label2 = gtk.Label("The identity layer directory path...")
        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, True, False, 0)
        hbox.pack_start(label2, False, True, 5)  
        
        label2.show()
        hbox.show() 
          
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        self.button2 = gtk.FileChooserButton('Identity layer directoryy')
        self.button2.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.button2.set_current_folder(self.identitylayer)
        self.button2.set_filter(filter)
        hbox.pack_start(self.button2, True, True, 0)
        
        hbox.show()
        self.button2.show()
        
    ##separator
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        hsaparator = gtk.HSeparator()
        hbox.pack_start(hsaparator, True, True, 10)
        
        hbox.show()
        hsaparator.show()

    ##output directory path
        label3 = gtk.Label("The output directory path...")
        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, True, False, 0)
        hbox.pack_start(label3, False, True, 5)  
        
        label3.show()
        hbox.show() 
          
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        self.button3 = gtk.FileChooserButton('Output directory')
        self.button3.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.button3.set_current_folder(self.outputdir)
        hbox.pack_start(self.button3, True, True, 0)
        
        hbox.show()
        self.button3.show()
        
    ##output file name
        hbox = gtk.HBox(False, 5)
        hbox.set_border_width(5)
        mainbox.pack_start(hbox, True, False, 10)

        label4 = gtk.Label("Output File Name:")
        hbox.pack_start(label4, False, False, 0)  
        label4.show()
        
        self.entry1 = gtk.Entry()
        self.entry1.set_text("Result.shp")
        self.entry1.set_size_request(150, 25)
        hbox.pack_start(self.entry1, False, False, 0)
        self.entry1.show()
        hbox.show()

    ##zonal split button box
        hbox = gtk.HBox(False, 0)   
        mainbox.pack_start(hbox, True, False, 25)

        button = gtk.Button('Zonal Split')
        button.connect('clicked', self.zonalSplitButton)
        button.set_size_request(90, 25)
        hbox.pack_start(button, True, False, 0)
        
        button.show()
        hbox.show()
    
    #about dialog
    def show_about(self, widget, data):
        dialog = gtk.AboutDialog()
        dialog.set_name("Zonal Split")
        dialog.set_version("1.0")
        dialog.set_authors(["Jihn-Fa Jan", "Fan-En Kung", "Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_documenters(["Shih-Kuang Chang", "Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_artists(["Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_comments("This program is witten for getting position attributes of landslide data.")
        dialog.set_license("Department of Land Economics, NCCU (c) All RIGHTS RESERVED\thttp://goo.gl/NK8Lk0")
        dialog.set_website("http://goo.gl/NK8Lk0")
        dialog.set_logo(gtk.gdk.pixbuf_new_from_file(os.path.join(zonpath, "Img/logo.png")))

        #show dialog
        dialog.run()

        #destroy method must be called otherwise the "Close" button will not work.
        dialog.destroy()
        
    def setconfig(self, tag, widget):
        cur = os.getcwd()
        os.chdir(zonpath) 
        if len(sys.argv) > 1:
           result = os.popen("python conf.py 1")
        else:
           result = os.popen("python conf.py")
        os.chdir(cur)
        
    def get_main_menu(self, window):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.MenuBar, '<main>', accel_group)
        item_factory.create_items(self.menu_items)
        window.add_accel_group(accel_group)
        self.item_factory = item_factory
        return item_factory.get_widget('<main>')
    
    def reset(self, tag, widget):
        self.button1.set_filename(os.path.join(root, " "))
        self.button2.set_current_folder(self.identitylayer)
        self.button3.set_current_folder(self.outputdir)
        self.entry1.set_text("Result.shp")

    def reloadConfig(self):
        settings = open(configpath)
        lines = settings.readlines()
        global host, port, dbname, user, passwords
        host = lines[0].split("=")[-1].replace("\n", "").replace("\r", "")
        port = lines[1].split("=")[-1].replace("\n", "").replace("\r", "")
        dbname = lines[2].split("=")[-1].replace("\n", "").replace("\r", "")
        user = lines[3].split("=")[-1].replace("\n", "").replace("\r", "")
        passwords = lines[4].split("=")[-1].replace("\n", "").replace("\r", "")
        settings.close()
        
    def zonalSplitButton(self, widget):
        #reload config file
        self.reloadConfig()
        Z = ZonalSplit(self.button1.get_filename(), self.button3.get_filename(), self.button2.get_filename())
        
        #check file name
        filename = self.entry1.get_text()
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in filename if c in valid_chars)
        if filename.replace(" ", "") == "":
            msg, result, writelog, icon = "Invalid file name!", None, False, gtk.MESSAGE_WARNING
            self.showMessage(msg, result, writelog, icon)
            return
        if not self.entry1.get_text().endswith(".shp"):
            filename += ".shp"
        
        #rename file as filename_N if have same outputfile, N is a number
        if os.path.exists(os.path.join(self.button3.get_filename(), filename)):
            filename = os.path.splitext(filename)[0] + "_1.shp"
            num = 2
            #if still exists, increase the number of N
            while os.path.exists(os.path.join(self.button3.get_filename(), filename)):
                filename = os.path.splitext(filename)[0][:-2] + "_%d.shp" % num
                num += 1
                
        msg, result, writelog, icon = Z.split(filename)
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
            os.chdir(self.button3.get_filename())
            log = open("log.txt", "a")
            log.write("-"*34 + time.strftime("%Y%m%d_%H%M%S", time.gmtime()) + "-"*34 + "\n")
            log.write(result)
            log.write("-"*34 + time.strftime("%Y%m%d_%H%M%S", time.gmtime()) + "-"*34 + "\n")
            log.close()
            os.chdir(root)
            

class ZonalSplit:
    def __init__(self, inputfile = os.path.join(os.getcwd(), "input"), outputdir = os.path.join(os.getcwd(), "output"), identitylayer = os.path.join(os.getcwd(), "identityLayer")):
        #initialize I/O directory
        self.inputfile = inputfile
        self.outputdir = outputdir
        self.identitylayer = identitylayer
         
    def split(self, filename):
        tStart = time.time()
        
        result = ""
        #connect to database
        try:
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port='%s' password='%s'" % (dbname, user, host, port, passwords))
            cur = conn.cursor()
        except:
            return "Unable to connect to the database.\nCheck your config file.", result, True, gtk.MESSAGE_WARNING
            
        #check shapefile
        if not self.inputfile:
            return "The input filename is empty!", result, False, gtk.MESSAGE_WARNING
            
        #get shapefile
        inputdir, shp_name = os.path.split(self.inputfile)
        os.chdir(inputdir)
        
        #clean old table merged
        cur.execute("DROP TABLE IF EXISTS merged;")
        conn.commit()
        
        #get identity layer list
        os.chdir(self.identitylayer)
        shp_list = glob.glob("*.shp")
        
        #check identity layer
        if len(shp_list) == 0:
            return "Cannot find any shapefile in identity layer!", result, False, gtk.MESSAGE_WARNING
         
        os.chdir(inputdir)
        #import merged table
        try:
            #upload merged
            cmdstr = "shp2pgsql -s 3826 -c -D -I -W big5 %s merged | psql -h %s -p %s -d %s -U %s" % (shp_name, host, port, dbname, user)
            print "Import shapefile '%s' to database '%s'..." % (shp_name, dbname)
            result += "Import shapefile '%s' to database '%s'...\n" % (shp_name, dbname)
            result += os.popen(cmdstr).read()

        except:
            #delete template tables
            cur.execute("DROP TABLE IF EXISTS merged;")
            conn.commit()
            conn.close()
            return "Import shapefile data error.", result, True, gtk.MESSAGE_WARNING
            
        #clean old identity layer tables
        cur.execute(";".join(["DROP TABLE IF EXISTS public.%s" % os.path.splitext(shp_data)[0] for shp_data in shp_list]))
        conn.commit()
        
        #import identity layers
        os.chdir(self.identitylayer)
        for shp_data in shp_list:
            tablename = os.path.splitext(shp_data)[0]
            try:
                #upload identity layer
                cmdstr = "shp2pgsql -s 3826 -c -D -I -W big5 %s %s | psql -h %s -p %s -d %s -U %s" % (shp_data, tablename, host, port, dbname, user)
                print "Import shapefile '%s' to database '%s'..." % (shp_data, dbname)
                result += "Import shapefile '%s' to database '%s'...\n" % (shp_data, dbname)
                result += os.popen(cmdstr).read()
    
            except:
                #delete identity layer tables
                cur.execute("DROP TABLE IF EXISTS merged;" + ";".join(["DROP TABLE IF EXISTS %s" % os.path.splitext(shp_data)[0] for shp_data in shp_list]))
                conn.commit()
                conn.close()
                return "Import identity layer data error.", result, True, gtk.MESSAGE_WARNING
        
        try:
            #Identity analysis with all layers
            result += "Execute identity analysis with all layers...\n"
            print "Execute identity analysis with all layers..."
            cur.execute(open(os.path.join(zonpath, "reference_data", "zonalSplit.sql"), "r").read())
            conn.commit()
        except:
            #delete template tables
            conn.rollback()
            #delete identity layer tables
            cur.execute("DROP SEQUENCE IF EXISTS GEOM_ID;DROP TABLE IF EXISTS merged;" + ";".join(["DROP TABLE IF EXISTS %s" % os.path.splitext(shp_data)[0] for shp_data in shp_list]))
            conn.commit()
            conn.close()
            return "Identity analysis error.", result, True, gtk.MESSAGE_WARNING
    
        #export result
        try:
            os.chdir(self.outputdir)
            cmdstr = 'pgsql2shp -f %s -h %s -p %s -u %s %s "SELECT * FROM merged2"' % (filename, host, port, user, dbname)
            print "Export final result..."
            result += "Export final result...\n"
            result += os.popen(cmdstr).read()

            #write out statistic report
            layer_list = [("Working Circle", "working_id", "working_ci"), ("Forest District", "forest_id", "forest_dis"), ("County", "county_id", "county"), ("Township", "town_id", "township"), ("Reservoir", "reserv_id", "reservoir"), ("Watershed", "watersh_id", "watershed"), ("Basin", "basin_id", "basin")]


            fout = open("Statistics.txt", "w")
            fout.write("Statistic Report\n")
            fout.write("Record time: " + time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()) + "\n\n")
            #get statistic data from database
            cur.execute("""
            SELECT SUM(area), AVG(area), MAX(area), MIN(area), COUNT(*)
            FROM merged2
            """)
            ans = cur.fetchall()
            fout.write("{:{fill}{align}60}".format("All", fill = "-", align = "^") + "\n")
            fout.write("%-20s%-20s%-20s%-20s%-5s\n" % ("Sum Area (m^2)", "Average Area (m^2)", "Max Area (m^2)", "Min Area (m^2)", "Number of Landslide")) 
            fout.write("%-20f%-20f%-20f%-20f%-5d\n" % ans[0]) 
            fout.write("{:{fill}{align}60}".format("All", fill = "-", align = "^") + "\n\n")

            sql = """
            SELECT %s, %s, SUM(area), AVG(area), MAX(area), MIN(area), COUNT(*)
            FROM merged2
            GROUP BY %s, %s;
            """

            for layer in layer_list:
                cur.execute(sql % (layer[1:]*2))
                ans = cur.fetchall()
                fout.write("{:{fill}{align}60}".format(layer[0], fill = "-", align = "^") + "\n")
                fout.write("%-10s%-25s%-20s%-20s%-20s%-20s%-5s\n" % ("Layer ID", "Layer Name", "Sum Area (m^2)", "Average Area (m^2)", "Max Area (m^2)", "Min Area (m^2)", "Number of Landslide")) 
                for row in ans:
                    fout.write("%-10s%-25s%-20f%-20f%-20f%-20f%-5d\n" % row)
                fout.write("{:{fill}{align}60}".format(layer[0], fill = "-", align = "^") + "\n\n")

            fout.close()
                      
            #delete template tables
            cur.execute("DROP TABLE IF EXISTS merged;DROP TABLE IF EXISTS merged2;DROP SEQUENCE IF EXISTS GEOM_ID;" + ";".join(["DROP TABLE IF EXISTS %s" % os.path.splitext(shp_data)[0] for shp_data in shp_list]))
            conn.commit()
            
        except:
            #delete template tables
            conn.rollback()
            cur.execute("DROP TABLE IF EXISTS merged;DROP TABLE IF EXISTS merged2;DROP SEQUENCE IF EXISTS GEOM_ID;" + ";".join(["DROP TABLE IF EXISTS %s" % os.path.splitext(shp_data)[0] for shp_data in shp_list]))
            conn.commit()
            conn.close()
            return "Export data error.", result, True, gtk.MESSAGE_WARNING
        
        conn.close()
        tEnd = time.time()
        
        return "Works done! It took %f sec" % (tEnd - tStart), result, True, gtk.MESSAGE_INFO
        
def main():
    os.environ["pgclientencoding"] = "big5"
    gtk.main()
    return 0
  
if __name__ == '__main__':
    zonpath = os.getcwd()
    if len(sys.argv) > 1:
        root = os.path.dirname(os.path.dirname(os.getcwd()))
        if not os.path.exists(os.path.join(zonpath, "..", "conf")):
            os.mkdir(os.path.join(zonpath, "..", "conf"))
        configpath = os.path.join(zonpath, "..", "conf", "ZonalSplit.ini")

        inputdir = os.path.join(root, "input")
        if not os.path.exists(inputdir):
            os.mkdir(inputdir)

        outputdir = os.path.join(root, "output")
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)

        identityLayer = os.path.join(root, "identityLayer")
        if not os.path.exists(identityLayer):
            os.mkdir(identityLayer)

        GUI(inputdir, outputdir, identityLayer)
    else:
        root = os.getcwd()
        configpath = os.path.join(zonpath, "ZonalSplit.ini")
        
        inputdir = os.path.join(root, "input")
        if not os.path.exists(inputdir):
            os.mkdir(inputdir)

        outputdir = os.path.join(root, "output")
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)
       
        identityLayer = os.path.join(root, "identityLayer")
        if not os.path.exists(identityLayer):
            os.mkdir(identityLayer)

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
        host = lines[0].split("=")[-1].replace("\n", "").replace("\r", "")
        port = lines[1].split("=")[-1].replace("\n", "").replace("\r", "")
        dbname = lines[2].split("=")[-1].replace("\n", "").replace("\r", "")
        user = lines[3].split("=")[-1].replace("\n", "").replace("\r", "")
        passwords = lines[4].split("=")[-1].replace("\n", "").replace("\r", "")
        settings.close()
    main()
