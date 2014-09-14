# -*- coding: utf-8 -*-
'''
Created on 2014/04/21
Updated on 2014/09/14
@author: Otakusaikou
'''
import pygtk
pygtk.require('2.0')
import gtk
import os
import subprocess

root = os.getcwd()

class ToolBox:
    #for upload button 
    def upload_button_event(self, widget, toolbar):
        #change directory to target program 
        os.chdir(os.path.join(root, "bin", "Upload"))

        #open target program with subprocess
        p = subprocess.Popen("python Upload_gtk.py 1")

        #update subprocess list
        self.subproc.append(p)

        #change directory back to main program 
        os.chdir(root)
        print "Upload"
        
    #for export button 
    def export_button_event(self, widget, toolbar):
        #change directory to target program 
        os.chdir(os.path.join(root, "bin", "Export"))

        #open target program with subprocess
        p = subprocess.Popen("python Export_gtk.py 1")

        #update subprocess list
        self.subproc.append(p)

        #change directory back to main program 
        os.chdir(root)
        print "Export"

    #for analysis button 
    def analysis_button1_event(self, widget, toolbar):
        #change directory to target program 
        os.chdir(os.path.join(root, "bin", "Landslide_postgis"))

        #open target program with subprocess
        p = subprocess.Popen("python main.py 1")

        #update subprocess list
        self.subproc.append(p)

        #change directory back to main program 
        os.chdir(root)
        print "Landslide processor"
        
    #for merge button 
    def analysis_button2_event(self, widget, toolbar):
        #change directory to target program 
        os.chdir(os.path.join(root, "bin", "Merge"))

        #open target program with subprocess
        p = subprocess.Popen("python MergeShp_gtk.py 1")

        #update subprocess list
        self.subproc.append(p)

        #change directory back to main program 
        os.chdir(root)
        print "Merge"
        
    #for zonal split button 
    def analysis_button3_event(self, widget, toolbar):
        #change directory to target program 
        os.chdir(os.path.join(root, "bin", "Zonal_split"))

        #open target program with subprocess
        p = subprocess.Popen("python ZonalSplit_gtk.py 1")

        #update subprocess list
        self.subproc.append(p)

        #change directory back to main program 
        os.chdir(root)
        print "Zonal Split"

    #close button 
    def close_button_event(self, widget, toolbar=None):
        #check whether all the subprocess are terminated
        if None in map(lambda p: p.poll(), self.subproc):
            messagedialog = gtk.MessageDialog(None, 
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                gtk.BUTTONS_YES_NO, "There still have subprocess running, are you sure you want to close all of them?") 
            messagedialog.set_position(gtk.WIN_POS_CENTER)
            response = messagedialog.run()
            messagedialog.destroy()
            if response == gtk.RESPONSE_NO:
                return

        #turn off every subprocess 
        try:
            for p in self.subproc:
                p.terminate()
        except:
            pass

        gtk.main_quit()
    #config setting menu    
    def config_menu(self, widget, data):
        label = data.get_label()
        #change directory to target program and open config setting panel 
        if label == "Upload":
            os.chdir(os.path.join(root, "bin", "Upload"))
            os.popen("python conf.py 1")
            os.chdir(root)
        elif label == "Export":
            os.chdir(os.path.join(root, "bin", "Export"))
            os.popen("python conf.py 1")
            os.chdir(root)
        elif label == "Analysis":
            os.chdir(os.path.join(root, "bin", "Landslide_postgis"))
            os.popen("python conf.py 1")
            os.chdir(root)
        elif label == "Merge":
            os.chdir(os.path.join(root, "bin", "Merge"))
            os.popen("python conf.py 1")
            os.chdir(root)
        elif label == "Zonal Split":
            os.chdir(os.path.join(root, "bin", "Zonal_Split"))
            os.popen("python conf.py 1")
            os.chdir(root)
        #quit event 
        elif label == "_Quit":
            #check whether all the subprocess are terminated
            if None in map(lambda p: p.poll(), self.subproc):
                messagedialog = gtk.MessageDialog(None, 
                    gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                    gtk.BUTTONS_YES_NO, "Still have subprocess running, are you sure you want to close all of them?") 
                messagedialog.set_position(gtk.WIN_POS_CENTER)
                response = messagedialog.run()
                messagedialog.destroy()
                if response == gtk.RESPONSE_NO:
                    return

            #turn off every subprocess 
            try:
                for p in self.subproc:
                    p.terminate()
            except:
                pass

            gtk.main_quit()

    #about dialog
    def show_about(self, widget, data):
        dialog = gtk.AboutDialog()
        dialog.set_name("Landslide Toolbox")
        dialog.set_version("1.0")
        dialog.set_authors(["Jihn-Fa Jan", "Fan-En Kung", "Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_documenters(["Shih-Kuang Chang", "Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_artists(["Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_comments("This program is witten for preprocessing of landslide data.")
        dialog.set_license("Department of Land Economics, NCCU (c) All RIGHTS RESERVED\thttp://goo.gl/NK8Lk0")
        dialog.set_website("http://goo.gl/NK8Lk0")
        dialog.set_logo(gtk.gdk.pixbuf_new_from_file("bin\\Img\\logo.png"))

        #show dialog
        dialog.run()

        #destroy method must be called otherwise the "Close" button will not work.
        dialog.destroy()
            
    #get itemfactory widget    
    def get_main_menu(self, window):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.MenuBar, '<main>', accel_group)
        item_factory.create_items(self.menu_items)
        window.add_accel_group(accel_group)
        self.item_factory = item_factory
        return item_factory.get_widget('<main>')
 
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Landslide Toolbox')
        window.set_size_request(520, 120)
        window.set_resizable(True)
        window.connect('destroy', self.close_button_event)
        
        mainbox = gtk.VBox(False, 0)
        window.add(mainbox)
        #for menu bar 
        self.menu_items = (
            ('/_File', None, None, 0, '<Branch>'),
            #('/File/Config/Toolbox', None, self.config_menu, 0, None),
            ('/File/Config/Upload', None, self.config_menu, 0, None),
            ('/File/Config/Export', None, self.config_menu, 0, None),
            ('/File/Config/Analysis', None, self.config_menu, 0, None),
            ('/File/Config/Merge', None, self.config_menu, 0, None),
            ('/File/Config/Zonal Split', None, self.config_menu, 0, None),
            ('/File/sep1', None, None, 0,'<Separator>'),
            ('/File/_Quit', '<control>Q', self.config_menu, 0, None),
            ('/_Help', None, None, 0,'<LastBranch>'),
            ('/Help/About', 'F1', self.show_about, 0, None)        
        )
        
        menubar = self.get_main_menu(window)
        mainbox.pack_start(menubar, False, True, 0)
        
        handlebox = gtk.HandleBox()
        mainbox.pack_start(handlebox, False, False, 0)
        
        #define directories
        self.inputdir = os.path.join(os.getcwd(), "input")
        self.outputdir = os.path.join(os.getcwd(), "output")
        if not os.path.exists(self.inputdir):
            os.mkdir(os.path.join(os.getcwd(), "input"))
        if not os.path.exists(self.outputdir):
            os.mkdir(os.path.join(os.getcwd(), "output"))
        
 
        #for toolbar widget
        toolbar = gtk.Toolbar()
        toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        toolbar.set_style(gtk.TOOLBAR_BOTH)
        toolbar.set_border_width(5)
        toolbar.set_size_request(520, 100)
        handlebox.add(toolbar)
        
        #upload data to database
        iconw = gtk.Image()
        iconw.set_from_file(upload_button_path)
        upload_button = toolbar.append_element(gtk.TOOLBAR_CHILD_BUTTON, None, 'Upload',
            'Upload shapefile/raster data', 'Private', iconw, self.upload_button_event, toolbar)
        toolbar.append_space()
        self.upload_button = upload_button 
        
        #export data to database
        iconw = gtk.Image()
        iconw.set_from_file(export_button_path)
        export_button = toolbar.append_element(gtk.TOOLBAR_CHILD_BUTTON, None, 'Export',
            'Export shapefile data', 'Private', iconw, self.export_button_event, toolbar)
        toolbar.append_space()
        self.export_button = export_button 
                 
        #landslide processor
        iconw = gtk.Image()
        iconw.set_from_file(analysis_button1_path)
        analysis_button1 = toolbar.append_element(gtk.TOOLBAR_CHILD_BUTTON, None,
            'Analysis', 'Lanslide processor(step1)', 'Private', iconw, self.analysis_button1_event,
            toolbar)
        toolbar.append_space()
        self.analysis_button1 = analysis_button1
        
        #merge
        iconw = gtk.Image()
        iconw.set_from_file(analysis_button2_path)
        analysis_button2 = toolbar.append_element(gtk.TOOLBAR_CHILD_BUTTON, None,
            'Merge', 'Merge shapefiles(step2)', 'Private', iconw, self.analysis_button2_event,
            toolbar)
        toolbar.append_space()
        self.analysis_button2 = analysis_button2
        
        #zonal split
        iconw = gtk.Image()
        iconw.set_from_file(analysis_button3_path)
        analysis_button3 = toolbar.append_element(gtk.TOOLBAR_CHILD_BUTTON, None,
            'Zonal Split', 'Zonal split(step3)', 'Private', iconw, self.analysis_button3_event,
            toolbar)
        toolbar.append_space()
        self.analysis_button3 = analysis_button3
        
        #exit icon button
        iconw = gtk.Image()
        iconw.set_from_stock("gtk-close", gtk.ICON_SIZE_BUTTON)
        close_button = toolbar.append_item('close', 'Close this app',
            'Private', iconw, self.close_button_event, toolbar)
        toolbar.append_space()    
        
        entry = gtk.Entry()
        toolbar.append_widget(entry, 'This is just an entry', 'Private')
                 
        window.show_all()
        self.subproc = []
 
 
def main():
    gtk.main()
    return 0
 
if __name__ == '__main__':
    #read config file
    if not os.path.exists(os.path.join(os.getcwd(), "bin", "conf")):
        os.mkdir(os.path.join(os.getcwd(), "bin", "conf"))
    #if config file is not exist, generate a new one    
    if not os.path.exists(os.path.join(os.getcwd(), "bin", "conf", "Toolbox.ini")):
        settings = open(os.path.join(os.getcwd(), "bin", "conf", "Toolbox.ini"), "w")
        settings.write("upload_button=bin/Img/load32x32.png\nexport_button=bin/Img/export32x32.png\nanalysis_button1=bin/Img/analysis132x32.png\nanalysis_button2=bin/Img/merge32x32.png\nanalysis_button3=bin/Img/zonal32x32.png")
        settings.close()
        upload_button_path = "bin/Img/load32x32.png"
        export_button_path = "bin/Img/export32x32.png"
        analysis_button1_path = "bin/Img/analysis132x32.png"
        analysis_button2_path = "bin/Img/merge32x32.png"
        analysis_button3_path = "bin/Img/zonal32x32.png"
        settings.close()
    else:
        settings = open(os.path.join(os.getcwd(), "bin", "conf", "Toolbox.ini"))
        lines = settings.readlines()
        upload_button_path = lines[0].split("=")[-1].replace("\n", "")
        export_button_path = lines[1].split("=")[-1].replace("\n", "")
        analysis_button1_path = lines[2].split("=")[-1].replace("\n", "")
        analysis_button2_path = lines[3].split("=")[-1].replace("\n", "")
        analysis_button3_path = lines[4].split("=")[-1].replace("\n", "")
        settings.close()
    ToolBox()
    main()
