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
    def __init__(self, inputdir = os.path.join(os.getcwd(), "input"), outputdir = os.path.join(os.getcwd(), "output")):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Merge')
        window.set_size_request(350, 250)
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
        
        self.inputdir = inputdir
        self.outputdir = outputdir
        
    ##menu bar
        menubar = self.get_main_menu(window)
        mainbox.pack_start(menubar, False, True, 0)
        menubar.show()
        
    ##input directory path
        label1 = gtk.Label("The input directory path...")
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
        
        self.button1 = gtk.FileChooserButton(self.inputdir)
        self.button1.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.button1.set_current_folder(self.inputdir)
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

    ##output directory path
        label2 = gtk.Label("The output directory path...")
        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, True, False, 0)
        hbox.pack_start(label2, False, True, 5)  
        
        label2.show()
        hbox.show() 
          
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(10)
        mainbox.pack_start(hbox, True, False, 0)
        
        self.button2 = gtk.FileChooserButton('Output directory')
        self.button2.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.button2.set_current_folder(self.outputdir)
        hbox.pack_start(self.button2, True, True, 0)
        
        hbox.show()
        self.button2.show()

    ##output file name
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(5)
        mainbox.pack_start(hbox, True, False, 0)

        label3 = gtk.Label("Output Name:")
        hbox.pack_start(label3, False, True, 5)  
        label3.show()
        
        self.entry1 = gtk.Entry()
        self.entry1.set_text("Merged.shp")
        hbox.pack_start(self.entry1, True, False, 0)
        self.entry1.show()
        hbox.show()
        
    ##merge button box
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(5)
        mainbox.pack_start(hbox, True, False, 15)
        
        button = gtk.Button('Merge')
        button.connect('clicked', self.mergeButton)
        button.set_size_request(70, 25)
        hbox.pack_start(button, True, False, 0)
        
        button.show()
        hbox.show()

    #about dialog
    def show_about(self, widget, data):
        dialog = gtk.AboutDialog()
        dialog.set_name("Merge")
        dialog.set_version("1.0")
        dialog.set_authors(["Jihn-Fa Jan", "Fan-En Kung", "Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_documenters(["Shih-Kuang Chang", "Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_artists(["Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_comments("This program is witten for merge and dissolve of landslide data.")
        dialog.set_license("Department of Land Economics, NCCU (c) All RIGHTS RESERVED\thttp://goo.gl/NK8Lk0")
        dialog.set_website("http://goo.gl/NK8Lk0")
        dialog.set_logo(gtk.gdk.pixbuf_new_from_file(os.path.join(mergepath, "Img/logo.png")))

        #show dialog
        dialog.run()

        #destroy method must be called otherwise the "Close" button will not work.
        dialog.destroy()
        
    def setconfig(self, tag, widget):
        cur = os.getcwd()
        os.chdir(mergepath) 
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
        self.button1.set_current_folder(self.inputdir)
        self.button2.set_current_folder(self.outputdir)
        self.entry1.set_text("Merged.shp")
        
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
        
    def mergeButton(self, widget):
        #reload config file
        self.reloadConfig()
        M = Merge(self.button1.get_filename(), self.button2.get_filename())
        
        #check table name
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
        if os.path.exists(os.path.join(self.button2.get_filename(), filename)):
            filename = os.path.splitext(filename)[0] + "_1.shp"
            num = 2
            #if still exists, increase the number of N
            while os.path.exists(os.path.join(self.button2.get_filename(), filename)):
                filename = os.path.splitext(filename)[0][:-2] + "_%d.shp" % num
                num += 1
        msg, result, writelog, icon = M.merge(filename)
        
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

class Merge:
    def __init__(self, inputdir = os.path.join(os.getcwd(), "input"), outputdir = os.path.join(os.getcwd(), "output")):
        #initialize I/O directory
        self.inputdir = inputdir
        self.outputdir = outputdir
        if not os.path.exists(inputdir):
            os.mkdir(inputdir)
            
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)
            
    def dissolve(self, cur, conn, tablename):
        result = ""

        threshold = 0.00000001
        while threshold <= 0.0000001:
            try:
                ##have no tolerance for buffering
                if threshold == 0.00000001:
                    cur.execute(open(os.path.join(mergepath, "reference_data", "mergeall.sql"), "r").read().replace("input_table", tablename))
                    conn.commit()
                    break
                else:
                    print "Change the ST_buffer tolerance to %.7f" % threshold
                    result += "Change the ST_buffer tolerance to %.7f\n" % threshold
                    cur.execute(open(os.path.join(mergepath, "reference_data", "mergeall.sql"), "r").read().replace("0", "%.7f" % threshold).replace("input_table", tablename))
                    conn.commit()
                    break
            except:
                conn.rollback()
            #change the ST_buffer tolerance
            threshold *= 10

        #get intersetion attributes from input table and unishp table
        cur.execute("SELECT U.gid AS gid, t1.dmcdate AS dmcdate FROM t1, unishp U WHERE ST_Intersects(t1.geom, U.geom) GROUP BY U.gid, t1.dmcdate;".replace("t1", tablename))
        ans = cur.fetchall()
        sql = "ALTER TABLE unishp ADD COLUMN dmcdate date;"
        for i in range(len(ans)):
            sql += "UPDATE unishp SET dmcdate = '%s'\n WHERE gid = %d;\n" % (str(ans[i][1]), ans[i][0])
        cur.execute(sql)
        conn.commit()
        
        cur.execute("DROP TABLE IF EXISTS %s;ALTER TABLE unishp RENAME TO %s;" % (tablename, tablename))
        conn.commit()
        
        return result
         
    def merge(self, filename):
        tStart = time.time()
        
        result = ""
        #connect to database
        try:
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port='%s' password='%s'" % (dbname, user, host, port, passwords))
            cur = conn.cursor()
        except:
            return "Unable to connect to the database.\nCheck your config file.", result, True, gtk.MESSAGE_WARNING

        #get shapefile list
        os.chdir(self.inputdir)
        shp_list = glob.glob("*.shp")
        
        #check if the inputdir is empty
        if len(shp_list) == 0:
            conn.close()
            return "Can't find any shapefile in input directory.", result, False, gtk.MESSAGE_WARNING
        
        #check if the number of shapefile is enougth
        if len(shp_list) == 1:
            conn.close()
            return "There must have at least two shpefiles in input directory.", result, False, gtk.MESSAGE_WARNING
        
        #clean old table t1, t2 if exists for uploading new tables
        cur.execute("DROP TABLE IF EXISTS t1;DROP TABLE IF EXISTS t2;")
        conn.commit()
        
        #merge fist two tables
        os.chdir(self.inputdir)
        #import two tables
        try:
            #upload t1
            cmdstr = "shp2pgsql -s 3826 -c -D -I -W big5 %s t1 | psql -h %s -p %s -d %s -U %s" % (shp_list[0], host, port, dbname, user)
            print "Import shapefile '%s' to database '%s'..." % (shp_list[0], dbname)
            result += "Import shapefile '%s' to database '%s'...\n" % (shp_list[0], dbname)
            result += os.popen(cmdstr).read()
            
            #upload t2
            cmdstr = "shp2pgsql -s 3826 -c -D -I -W big5 %s t2 | psql -h %s -p %s -d %s -U %s" % (shp_list[1], host, port, dbname, user)
            print "Import shapefile '%s' to database '%s'..." % (shp_list[1], dbname)
            result += "Import shapefile '%s' to database '%s'...\n" % (shp_list[1], dbname)
            result += os.popen(cmdstr).read()
           
            print "Dissolve shapefile '%s'..." % (shp_list[0])
            result += "Dissolve shapefile '%s'...\n" % (shp_list[0])
            result += self.dissolve(cur, conn, "t1")
            
            print "Dissolve shapefile '%s'..." % (shp_list[1])
            result += "Dissolve shapefile '%s'...\n" % (shp_list[1])
            result += self.dissolve(cur, conn, "t2")
            
            #get intersection area (two tables, table1 and table2) and delete them from t1 and t2
            result += "Get intersection area of two shapefiles '%s' and '%s'...\n" % (shp_list[0], shp_list[1]) 
            print "Get intersection area of two shapefiles '%s' and '%s'..." % (shp_list[0], shp_list[1])
            cur.execute(open(os.path.join(mergepath, "reference_data", "getIntersection.sql"), "r").read())
            conn.commit()

            result += "Create union with shapefiles '%s' and '%s'...\n" % (shp_list[0], shp_list[1]) 
            print "Create union with shapefiles '%s' and '%s'..." % (shp_list[0], shp_list[1])
            #merge t1 and t2 and rename result table name to t1
            cur.execute(open(os.path.join(mergepath, "reference_data", "fastunion.sql"), "r").read())
            
            conn.commit()
        except:
            #delete template tables
            conn.rollback()
            cur.execute("DROP SEQUENCE IF EXISTS GEO_ID;DROP TABLE IF EXISTS table2;DROP TABLE IF EXISTS table1;DROP TABLE IF EXISTS unishp;DROP TABLE IF EXISTS t1;DROP TABLE IF EXISTS t2;DROP TABLE IF EXISTS t1t;DROP TABLE IF EXISTS t2t;")
            conn.commit()
            conn.close()
            return "Import shapefile data error.", result, True, gtk.MESSAGE_WARNING
        
        if len(shp_list) > 2:
            #merge all shapefiles        
            for shp_data in shp_list[2:]:
                #import tables
                try:
                    #upload t2
                    cmdstr = "shp2pgsql -s 3826 -c -D -I -W big5 %s t2 | psql -h %s -p %s -d %s -U %s" % (shp_data, host, port, dbname, user)
                    print "Import shapefile '%s' to database '%s'..." % (shp_data, dbname)
                    result += "Import shapefile '%s' to database '%s'...\n" % (shp_data, dbname)
                    result += os.popen(cmdstr).read()
                    print "Dissolve union table..." 
                    result += "Dissolve union table...\n" 
                    result += self.dissolve(cur, conn, "t1")
                    
                    print "Dissolve shapefile '%s'..." % (shp_data)
                    result += "Dissolve shapefile '%s'...\n" % (shp_data)
                    result += self.dissolve(cur, conn, "t2")
                    
                    #get intersection area (two tables, table1 and table2) and delete them from t1 and t2
                    result += "Get intersection area of union table and new shapefile '%s'...\n" % shp_data 
                    print "Get intersection area of union table and new shapefile '%s'..." % shp_data 
                    cur.execute(open(os.path.join(mergepath, "reference_data", "getIntersection.sql"), "r").read())
                    conn.commit()

                    result += "Create union with shapefile '%s'...\n" % shp_data 
                    print "Create union with shapefile '%s'..." % shp_data
                    cur.execute(open(os.path.join(mergepath, "reference_data", "fastunion.sql"), "r").read())
                    conn.commit()
                except:
                    #delete template tables
                    conn.rollback()
                    cur.execute("DROP SEQUENCE IF EXISTS GEO_ID;DROP TABLE IF EXISTS table2;DROP TABLE IF EXISTS table1;DROP TABLE IF EXISTS unishp;DROP TABLE IF EXISTS t1;DROP TABLE IF EXISTS t2;DROP TABLE IF EXISTS t1t;DROP TABLE IF EXISTS t2t;")
                    conn.commit()
                    conn.close()
                    return "Import shapefile data error.\nShapefile name is '%s'.\n" % shp_data, result, True, gtk.MESSAGE_WARNING
        
        #dissolve union
        print "Dissolve shapefile union..."
        result += "Dissolve shapefile union...\n"
        result += self.dissolve(cur, conn, "t1")
        
        #export result
        try:
            os.chdir(self.outputdir)
            cmdstr = 'pgsql2shp -f %s -h %s -p %s -u %s %s "SELECT geom, gid AS shp_id, dmcdate FROM t1 ORDER BY gid"' % (filename, host, port, user, dbname)
            print "Export merged landslide..."
            result += "Export merged landslide...\n"
            result += os.popen(cmdstr).read()
                      
            #delete template tables
            cur.execute("DROP SEQUENCE IF EXISTS GEO_ID;DROP TABLE IF EXISTS T1_exp;DROP TABLE IF EXISTS T2_exp;DROP TABLE IF EXISTS T1_T2_combo;DROP TABLE IF EXISTS T1_T2_overlay;DROP TABLE IF EXISTS T1_T2_overlay_pts;DROP TABLE IF EXISTS T1_T2_unionjoin;DROP TABLE IF EXISTS table2;DROP TABLE IF EXISTS unishp;")
            conn.commit()
            
        except:
            #delete template tables
            conn.rollback()
            cur.execute("DROP SEQUENCE IF EXISTS GEO_ID;DROP TABLE IF EXISTS table2;DROP TABLE IF EXISTS table1;DROP TABLE IF EXISTS unishp;DROP TABLE IF EXISTS t1;DROP TABLE IF EXISTS t2;DROP TABLE IF EXISTS t1t;DROP TABLE IF EXISTS t2t;")
            conn.commit()
            conn.close()
            return "Export data error.", result, True, gtk.MESSAGE_WARNING

        
        print "All shapefile are merged successfully!"
        result += "All shapefile are merged successfully!\n"
               
        #delete template tables
        cur.execute("DROP SEQUENCE IF EXISTS GEO_ID;DROP TABLE IF EXISTS table2;DROP TABLE IF EXISTS table1;DROP TABLE IF EXISTS unishp;DROP TABLE IF EXISTS t1;DROP TABLE IF EXISTS t2;DROP TABLE IF EXISTS t1t;DROP TABLE IF EXISTS t2t;")
        conn.commit()
        conn.close()
        tEnd = time.time()
        
        return "Works done! It took %f sec" % (tEnd - tStart), result, True, gtk.MESSAGE_INFO
        
def main():
    gtk.main()
    return 0
  
if __name__ == '__main__':
    mergepath = os.getcwd()
    if len(sys.argv) > 1:
        root = os.path.dirname(os.path.dirname(os.getcwd()))
        if not os.path.exists(os.path.join(mergepath, "..", "conf")):
            os.mkdir(os.path.join(mergepath, "..", "conf"))
        configpath = os.path.join(mergepath, "..", "conf", "MergeShp.ini")
        
        inputdir = os.path.join(root, "input")
        if not os.path.exists(inputdir):
            os.mkdir(inputdir)

        outputdir = os.path.join(root, "output")
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)
        
        GUI(inputdir, outputdir)
    else:
        root = os.getcwd()
        configpath = os.path.join(mergepath, "MergeShp.ini")
        
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
