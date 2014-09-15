# -*- coding: utf-8 -*-
'''
Created on 2013/10/15
Updated on 2014/09/15
@author: Otakusaikou
'''
#The GUI for Db_extractor.

import pygtk
pygtk.require("2.0")
import gtk
import os
import glob
import psycopg2
import sys
import time

class GUI(gtk.Window):
    def __init__(self, outputdir = os.path.join(os.getcwd(), "output")):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("delete_event", self.close_application)
        window.set_size_request(700, 810)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_title("Export")
        window.show()
        
    ##menu bar
        self.menu_items = (
            ('/_File', None, None, 0, '<Branch>'),
            ('/File/_Config Settings', '<control>P', self.setconfig, 0, None),
            ('/File/sep1', None, None, 0,'<Separator>'),
            ('/File/_Quit', '<control>Q', gtk.main_quit, 0, None),
            ('/_Help', None, None, 0,'<LastBranch>'),
            ('/Help/About', 'F1', self.show_about, 0, None)        
        )
        
        mainbox = gtk.VBox(False, 10)
        mainbox.show()###
        window.add(mainbox)
        
        menubar = self.get_main_menu(window)
        mainbox.pack_start(menubar, False, True, 0)
        menubar.show()
        
        hbox1 = gtk.HBox(True, 10)
        hbox1.show()###
        mainbox.pack_start(hbox1, False, False, 20)
        
        #Field List-------------
        frame1 = gtk.Frame('Fields')
        frame1.show()###
        frame1.set_size_request(300, 280)
        hbox1.pack_start(frame1, False, False, 0)
        
        scrollwindow1 = gtk.ScrolledWindow()
        scrollwindow1.show()###
        #scrollwindow1.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scrollwindow1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow1.set_border_width(10)
        
        frame1.add(scrollwindow1)
        
        self.selected_feature = None
        try:
            self.liststore1 = self.create_model(create_field_list(), True)
        except:
            print 'Could not open a database. Please check the config file: "Export.ini"'
            messagedialog = gtk.MessageDialog(self, 
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
                gtk.BUTTONS_CLOSE, 'Could not open a database. Please check the config file: "Export.ini"')
        
            messagedialog.set_position(gtk.WIN_POS_CENTER)
            messagedialog.run()
            messagedialog.destroy()
            exit()
        
        self.treeview1 = gtk.TreeView(self.liststore1)
        self.treeview1.connect("cursor-changed", self.on_activated)
        self.treeview1.set_rules_hint(True)
        self.treeview1.connect('button_press_event', self.selection_double_clicked)
        self.treeview1.show()
        
        scrollwindow1.add(self.treeview1)
        self.create_columns(self.treeview1)
        
        
        
        #Field List-------------
        #Value List-------------
        frame2 = gtk.Frame('Values')
        frame2.show()###
        frame2.set_size_request(300, 280)
        hbox1.pack_start(frame2, False, False, 0)
        
        scrollwindow2 = gtk.ScrolledWindow()
        scrollwindow2.show()###
        scrollwindow2.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scrollwindow2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        vbox1 = gtk.VBox(False, 5)
        vbox1.set_border_width(10)
        vbox1.show()###
        frame2.add(vbox1)
        
        self.liststore2 = self.create_model([])
        self.treeview2 = gtk.TreeView(self.liststore2)
        vbox1.pack_start(scrollwindow2, True, True, 0)
        
        hbox2 = gtk.HBox(True, 5)
        hbox2.show()
        vbox1.pack_start(hbox2, False, False, 0)

        
        SAMPLE = gtk.Button("Get Sample")
        SAMPLE.connect("clicked", self.get_records, self.treeview2)
        hbox2.pack_start(SAMPLE, True, True, 0)
        SAMPLE.show()
        ALL = gtk.Button("Get All")
        ALL.connect("clicked", self.get_records, self.treeview2)
        hbox2.pack_start(ALL, True, True, 0)
        ALL.show()
        
        self.treeview2.set_rules_hint(True)
        self.treeview2.connect('button_press_event', self.selection_double_clicked)
        self.treeview2.show()
        
        scrollwindow2.add(self.treeview2)
        self.create_columns(self.treeview2)
        
              
        #Value List-------------
        
        #Buttons----------------
        hbox6 = gtk.HBox(True, 10)
        hbox6.show()###
        mainbox.pack_start(hbox6, False, False,  0)
        
        frame4 = gtk.Frame('Operands')
        frame4.show()###
        frame4.set_size_request(680, 100)
        hbox6.pack_start(frame4, False, False, 10)
        
        hbox7 = gtk.HBox(True, 10)
        hbox7.show()###
        mainbox.pack_start(hbox7, False, False,  0)
        
        frame5 = gtk.Frame('SQL where expression')
        frame5.show()###
        frame5.set_size_request(680, 130)
        hbox7.pack_start(frame5, False, False, 10)
        
        vbox3 = gtk.VBox(True, 0)
        vbox3.show()###
        frame4.add(vbox3)
        
        hbox8 = gtk.HBox(True, 5)
        hbox8.show()###
        vbox3.pack_start(hbox8, True, False, 0)
        
        hbox9 = gtk.HBox(True, 5)
        hbox9.show()###
        vbox3.pack_start(hbox9, True, False, 0)
        
        EQUAL = gtk.Button('=')
        EQUAL.show()###
        BIGGER = gtk.Button('>')
        BIGGER.show()###
        SMALLER = gtk.Button('<')
        SMALLER.show()###
        LIKE = gtk.Button('LIKE')
        LIKE.show()###
        PERCENT = gtk.Button('%')
        PERCENT.show()###
        IN = gtk.Button('IN')
        IN.show()###
        NOT_IN = gtk.Button('NOT IN')
        NOT_IN.show()###
        
        EQUAL.connect("clicked", self.add_statement, "=")
        BIGGER.connect("clicked", self.add_statement, ">")
        SMALLER.connect("clicked", self.add_statement, "<")
        LIKE.connect("clicked", self.add_statement, "LIKE")
        PERCENT.connect("clicked", self.add_statement, "%")
        IN.connect("clicked", self.add_statement, "IN")
        NOT_IN.connect("clicked", self.add_statement, "NOT IN")
        
        hbox8.pack_start(EQUAL, True, True, 5)
        hbox8.pack_start(BIGGER, True, True, 5)
        hbox8.pack_start(SMALLER, True, True, 5)
        hbox8.pack_start(LIKE, True, True, 5)
        hbox8.pack_start(PERCENT, True, True, 5)
        hbox8.pack_start(IN, True, True, 5)
        hbox8.pack_start(NOT_IN, True, True, 5)
        
        SMALLER_EQUAL = gtk.Button('<=')
        SMALLER_EQUAL.show()###
        BIGGER_EQUAL = gtk.Button('>=')
        BIGGER_EQUAL.show()###
        NOT_EQUAL = gtk.Button('!=')
        NOT_EQUAL.show()###
        ILIKE = gtk.Button('ILIKE')
        ILIKE.show()###
        AND = gtk.Button('AND')
        AND.show()###
        OR = gtk.Button('OR')
        OR.show()###
        NOT = gtk.Button('NOT')
        NOT.show()###

        SMALLER_EQUAL.connect("clicked", self.add_statement, "<=")
        BIGGER_EQUAL.connect("clicked", self.add_statement, ">=")
        NOT_EQUAL.connect("clicked", self.add_statement, "!=")
        ILIKE.connect("clicked", self.add_statement, "ILIKE")
        AND.connect("clicked", self.add_statement, "AND")
        OR.connect("clicked", self.add_statement, "OR")
        NOT.connect("clicked", self.add_statement, "NOT")
        
        hbox9.pack_start(SMALLER_EQUAL, True, True, 5)
        hbox9.pack_start(BIGGER_EQUAL, True, True, 5)
        hbox9.pack_start(NOT_EQUAL, True, True, 5)
        hbox9.pack_start(ILIKE, True, True, 5)
        hbox9.pack_start(AND, True, True, 5)
        hbox9.pack_start(OR, True, True, 5)
        hbox9.pack_start(NOT, True, True, 5)
        
        #Buttons----------------
        #SQL statement textbox--
        
        self.textview = gtk.TextView()
        self.textview.show()###
        
        scrollwindow3 = gtk.ScrolledWindow()
        scrollwindow3.show()###
        scrollwindow3.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scrollwindow3.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow3.set_border_width(10)
        scrollwindow3.add(self.textview)

        frame5.add(scrollwindow3)

        textbuffer = self.textview.get_buffer()
        textbuffer.set_text(" ")
        
        self.textview.set_editable(True)
        self.textview.set_cursor_visible(True)

        #SQL statement textbox--
        
        #Output settings----------
        hbox3 = gtk.HBox(True, 10)
        hbox3.show()###
        mainbox.pack_start(hbox3, False, False,  0)
        
        frame3 = gtk.Frame('Output Settings')
        frame3.show()###
        frame3.set_size_request(680, 120)
        hbox3.pack_start(frame3, False, False, 10)
        
        vbox2 = gtk.VBox(True, 15)
        vbox2.show()###
        frame3.add(vbox2)
        
        #Day, month, year spinbuttons
        #Get latest and earliest date
        try:
            reloadConfig()
            con = psycopg2.connect(database = dbname, user = user, password = password, host = host, port = port)
            cur = con.cursor()
            sql = "SELECT DISTINCT MIN(project_date), MAX(project_date) FROM tmp_query WHERE project_date IS NOT NULL" 
            cur.execute(sql)
            
        except psycopg2.DatabaseError, e:
            print 'Could not open a database. Please check the config file: "Export.ini"'
        results = cur.fetchall()
        con.close()
        fyear, fmon, fday = map(int, results[0][0].split("-"))
        tyear, tmon, tday = map(int, results[0][1].split("-"))

        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(5)
        vbox2.pack_start(hbox, True, True, 5)
        hbox.show()
        
        self.object_list = []
        
        #From
        vbox = gtk.VBox(False, 0)
        hbox.pack_start(vbox, False, False, 5)
        vbox.show()

        label = gtk.Label("From :")
        label.set_size_request(50, -1)
        self.object_list.append(label)
        label.set_alignment(0, 0.5)
        label.show()
        vbox.pack_start(label, False, False, 5)

        vbox = gtk.VBox(False, 0)
        hbox.pack_start(vbox, False, False, 5)
        vbox.show()

        label = gtk.Label("Year :")
        label.set_alignment(0, 0.5)
        label.set_size_request(55, -1)
        self.object_list.append(label)
        label.show()
        vbox.pack_start(label, False, True, 0)
  
        self.fyear_adj = gtk.Adjustment(fyear, 0.0, 2100.0, 1.0, 100.0, 0.0)
        spinbutton = gtk.SpinButton(self.fyear_adj, 0, 0)
        spinbutton.set_wrap(False)
        spinbutton.show()
        spinbutton.set_size_request(55, -1)
        self.object_list.append(spinbutton)
        vbox.pack_start(spinbutton, False, True, 0)

        vbox = gtk.VBox(False, 0)
        hbox.pack_start(vbox, False, False, 5)
        vbox.show()
  
        label = gtk.Label("Month :")
        label.set_alignment(0, 0.5)
        label.set_size_request(45, -1)
        self.object_list.append(label)
        label.show()
        vbox.pack_start(label, False, True, 0)

        self.fmon_adj = gtk.Adjustment(fmon, 1.0, 12.0, 1.0, 5.0, 0.0)
        spinbutton = gtk.SpinButton(self.fmon_adj, 0, 0)
        spinbutton.set_wrap(True)
        spinbutton.set_size_request(45, -1)
        self.object_list.append(spinbutton)
        spinbutton.show()
        vbox.pack_start(spinbutton, False, True, 0)
  
        vbox = gtk.VBox(False, 0)
        hbox.pack_start(vbox, False, False, 5)
        vbox.show()

        label = gtk.Label("Day :")
        label.set_alignment(0, 0.5)
        label.set_size_request(45, -1)
        self.object_list.append(label)
        label.show()
        vbox.pack_start(label, False, True, 0)
  
        self.fday_adj = gtk.Adjustment(fday, 1.0, 31.0, 1.0, 5.0, 0.0)
        spinbutton = gtk.SpinButton(self.fday_adj, 0, 0)
        spinbutton.set_wrap(True)
        spinbutton.set_size_request(45, -1)
        self.object_list.append(spinbutton)
        spinbutton.show()
        vbox.pack_start(spinbutton, False, False, 0)

        #To
        vbox = gtk.VBox(False, 0)
        hbox.pack_start(vbox, False, False, 5)
        vbox.show()

        label = gtk.Label("To :")
        label.set_alignment(0.5, 0.5)
        label.set_size_request(50, -1)
        self.object_list.append(label)
        label.show()
        vbox.pack_start(label, False, False, 5)

        vbox = gtk.VBox(False, 0)
        hbox.pack_start(vbox, False, False, 5)
        vbox.show()

        label = gtk.Label("Year :")
        label.set_alignment(0, 0.5)
        label.set_size_request(55, -1)
        self.object_list.append(label)
        label.show()
        vbox.pack_start(label, False, True, 0)
  
        self.tyear_adj = gtk.Adjustment(tyear, 0.0, 2100.0, 1.0, 100.0, 0.0)
        spinbutton = gtk.SpinButton(self.tyear_adj, 0, 0)
        spinbutton.set_wrap(False)
        spinbutton.show()
        spinbutton.set_size_request(55, -1)
        self.object_list.append(spinbutton)
        vbox.pack_start(spinbutton, False, True, 0)
  
        vbox = gtk.VBox(False, 0)
        hbox.pack_start(vbox, False, False, 5)
        vbox.show()
  
        label = gtk.Label("Month :")
        label.set_alignment(0, 0.5)
        label.set_size_request(45, -1)
        self.object_list.append(label)
        label.show()
        vbox.pack_start(label, False, True, 0)

        self.tmon_adj = gtk.Adjustment(tmon, 1.0, 12.0, 1.0, 5.0, 0.0)
        spinbutton = gtk.SpinButton(self.tmon_adj, 0, 0)
        spinbutton.set_wrap(True)
        spinbutton.set_size_request(45, -1)
        self.object_list.append(spinbutton)
        spinbutton.show()
        vbox.pack_start(spinbutton, False, True, 0)
  
        vbox = gtk.VBox(False, 0)
        hbox.pack_start(vbox, False, False, 5)
        vbox.show()

        label = gtk.Label("Day :")
        label.set_alignment(0, 0.5)
        label.set_size_request(45, -1)
        self.object_list.append(label)
        label.show()
        vbox.pack_start(label, False, True, 0)
  
        self.tday_adj = gtk.Adjustment(tday, 1.0, 31.0, 1.0, 5.0, 0.0)
        spinbutton = gtk.SpinButton(self.tday_adj, 0, 0)
        spinbutton.set_wrap(True)
        spinbutton.set_size_request(45, -1)
        self.object_list.append(spinbutton)
        spinbutton.show()
        vbox.pack_start(spinbutton, False, False, 0)

        vbox = gtk.VBox(False, 0)
        hbox.pack_end(vbox, False, False, 5)
        vbox.show()

        self.checkbutton1 = gtk.CheckButton("Split Shapefile By Date")
        vbox.pack_start(self.checkbutton1, False, False, 5)
        self.checkbutton1.show()
        
        hbox5 = gtk.HBox(False, 0)
        hbox5.show()###
        vbox2.pack_start(hbox5, True, False, 0)
        
        label = gtk.Label("Output Name: ")
        hbox5.pack_start(label, False, False, 10)
        label.show()      
 
        self.entry2 = gtk.Entry()
        self.entry2.set_size_request(202, 20)
        self.entry2.set_text("QueryResult.shp")
        hbox5.pack_start(self.entry2, False, False, 0)
        self.entry2.show()###
        
        #Output settings----------
            
        #Export button box------
        hbox10 = gtk.HBox(False, 0)
        hbox10.show()###
        mainbox.pack_start(hbox10, False, False,  5)
        
        OK = gtk.Button("OK")
        OK.set_size_request(80, 30)
        OK.connect("clicked", self.export)
        OK.show()###
        TEST = gtk.Button("Test")
        TEST.set_size_request(80, 30)
        TEST.connect("clicked", self.test_value)
        TEST.show()###
        CLEAR = gtk.Button("Clear")
        CLEAR.set_size_request(80, 30)
        CLEAR.connect("clicked", self.clear)
        CLEAR.show()###
        EXIT = gtk.Button("Exit")
        EXIT.connect_object("clicked", self.close_application, window, None)
        EXIT.set_size_request(80, 30)
        EXIT.show()###
        
        hbox11 = gtk.HBox(False, 0)
        hbox11.show()###
        hbox10.pack_end(hbox11, False, False,  30)
        
        hbox11.pack_end(EXIT, False, True, 5)
        hbox11.pack_end(CLEAR, False, True, 5)
        hbox11.pack_end(TEST, False, True, 5)
        hbox11.pack_end(OK, False, True, 5)
        
        #Export button box------
        
        #initial variables
        self.outputdir = outputdir
        if not os.path.exists(self.outputdir):
            os.mkdir(self.outputdir)
        os.chdir(self.outputdir)
    
    #about dialog
    def show_about(self, widget, data):
        dialog = gtk.AboutDialog()
        dialog.set_name("Export")
        dialog.set_version("1.1")
        dialog.set_authors(["Jihn-Fa Jan", "Fan-En Kung", "Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_documenters(["Shih-Kuang Chang", "Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_artists(["Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_comments("This program is witten for export of landslide data.")
        dialog.set_license("Department of Land Economics, NCCU (c) All RIGHTS RESERVED\thttp://goo.gl/NK8Lk0")
        dialog.set_website("http://goo.gl/NK8Lk0")
        dialog.set_logo(gtk.gdk.pixbuf_new_from_file(os.path.join(exportpath, "Img\\logo.png")))

        #show dialog
        dialog.run()

        #destroy method must be called otherwise the "Close" button will not work.
        dialog.destroy()
        
    def setconfig(self, tag, widget):
        cur = os.getcwd()
        os.chdir(exportpath) 
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
        
    def create_model(self, list, isfields = False, isstring = False):
        store = gtk.ListStore(str)
        if isfields:
            for i in range(len(list)):
                try:
                    field = list[i].lower()
                    #if "date" in field:
                        #continue
                        #pass
                    store.append([list[i]])
                except:
                    store.append([list[i]])
        else:
            if isstring:
                for element in list:
                    store.append(["\'" + element + "\'"])
            else:
                for element in list:
                    store.append([element])

        return store
    
    def on_activated(self, widget):
        treeselection = widget.get_selection()
        (model, iter) = treeselection.get_selected()
        field = model.get_value(iter, 0)
        self.selected_feature = field
        #self.statusbar.push(0, text)
        
    def create_columns(self, treeview):
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("", rendererText, text=0)
        column.set_sort_column_id(0)    
        treeview.append_column(column)

    def add_statement(self, widget, data):
        textbuffer = self.textview.get_buffer()
        start = textbuffer.get_start_iter()
        end = textbuffer.get_end_iter()
        if textbuffer.get_text(start, end) == "":
            textbuffer2 = gtk.TextBuffer()
            textbuffer2.set_text(data + " ")
            self.textview.set_buffer(textbuffer2)
        else:    
            textbuffer.insert_at_cursor(data + " ")
            self.textview.set_buffer(textbuffer)

        
    def selection_double_clicked(self, widget, event):
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:      
            treeselection = widget.get_selection()
            (model, iter) = treeselection.get_selected()
            field = model.get_value(iter, 0)

            self.add_statement(widget, field)
        
    def get_records(self, widget, treeview):
        sample = widget.get_label() == "Get Sample"
        #get 10 sample reocrds
        if sample:
            records, isstring = get_records(self.selected_feature, 10)
        #get all records
        else: 
            records, isstring = get_records(self.selected_feature, -1)
        treeview.set_model(self.create_model(records, False, isstring))
        
    #clear SQL where expression text box
    def clear(self, widget):
        textbuffer = self.textview.get_buffer()
        textbuffer.set_text("")
        #self.entry1.set_text("")
        
    def close_application(self, widget, event, data=None):
        gtk.main_quit()
        return False
        
    #test number of rows after SQL where expression applied
    def test_value(self, widget):
        textbuffer = self.textview.get_buffer()
        start = textbuffer.get_start_iter()
        end = textbuffer.get_end_iter()
        statement = textbuffer.get_text(start, end)

        _from = "%04d-%02d-%02d" % (self.object_list[2].get_value(), self.object_list[4].get_value(), self.object_list[6].get_value())
        _to = "%04d-%02d-%02d" % (self.object_list[9].get_value(), self.object_list[11].get_value(), self.object_list[13].get_value())
        
        #for the case that where statement is empty
        if statement.replace(" ", "") == "":
            sql = "SELECT DISTINCT COUNT(slide_id) FROM tmp_query WHERE project_date >= '%s' AND project_date <= '%s'" % (_from, _to)
        #for the case that something input in SQL where expression textbox
        else:
            sql = "SELECT DISTINCT COUNT(slide_id) FROM tmp_query WHERE %s AND project_date >= '%s' AND project_date <= '%s'" % (statement, _from, _to)

        sql = sql.decode("utf-8")
        try:
            reloadConfig()
            con = psycopg2.connect(database = dbname, user = user, password = password, host = host, port = port)
            cur = con.cursor()
            cur.execute(sql)
            numrow = cur.fetchall()[0]
            messagedialog = gtk.MessageDialog(self, 
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                gtk.BUTTONS_CLOSE, "The where clause returned %d row(s)" % numrow)          

            con.close()
        
        except psycopg2.DatabaseError, e:
            print sql
            messagedialog = gtk.MessageDialog(self, 
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
                gtk.BUTTONS_CLOSE, "An error occurred when executing the query.")
            print 'Could not open a database. Please check the config file: "Export.ini"'
            
        messagedialog.set_position(gtk.WIN_POS_CENTER)
        messagedialog.run()
        messagedialog.destroy()
            
    def export(self, widget):
        count = 0
        log = open("log.txt", "a")
        log.write("-"*34 + time.strftime("%Y%m%d_%H%M%S", time.gmtime()) + "-"*34 + "\n")
        textbuffer = self.textview.get_buffer()
        start = textbuffer.get_start_iter()
        end = textbuffer.get_end_iter()

        statement = textbuffer.get_text(start, end)
        _from = "%04d-%02d-%02d" % (self.object_list[2].get_value(), self.object_list[4].get_value(), self.object_list[6].get_value())
        _to = "%04d-%02d-%02d" % (self.object_list[9].get_value(), self.object_list[11].get_value(), self.object_list[13].get_value())

        if self.checkbutton1.get_active():
            #get all different dates
            con = psycopg2.connect(database = dbname, user = user, password = password, host = host, port = port)
            cur = con.cursor()
            cur.execute("SELECT DISTINCT project_date FROM tmp_query WHERE project_date >= '%s' AND project_date <= '%s'" % (_from, _to))
            all_date = cur.fetchall()
            con.close()

            for date in all_date:
                date = date[0]
                #check file name 
                if self.entry2.get_text().replace(" ", "") == "":
                    messagedialog = gtk.MessageDialog(self, 
                            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
                            gtk.BUTTONS_CLOSE, 'Invalid file name!')
                    log.write("Invalid file name!\n")
                    log.close()
                    messagedialog.set_position(gtk.WIN_POS_CENTER)
                    messagedialog.run()
                    messagedialog.destroy()
                    return
                else:
                    outshp = self.entry2.get_text().replace(" ", "").encode("big5")
                    if not outshp.endswith(".shp"):
                        outshp += ".shp"
                    f, e = os.path.splitext(outshp)
                    outshp = f + date + e

                    #rename file as filename_N if have same outputfile, N is a number
                    if os.path.exists(os.path.join(os.getcwd(), outshp)) or os.path.exists(os.path.join(os.getcwd(), outshp + ".shp")):
                        outshp = os.path.splitext(outshp)[0] + "_1.shp"
                        num = 2
                        #if still exists, increase the number of N
                        while os.path.exists(os.path.join(os.getcwd(), outshp)) or os.path.exists(os.path.join(os.getcwd(), outshp + ".shp")):
                            outshp = os.path.splitext(outshp)[0][:-2] + "_%d.shp" % num
                            num += 1
            
                #for the case that where statement is empty
                if statement.replace(" ", "") == "":
                    sql = "SELECT * FROM tmp_query WHERE project_date = '%s'" % date
                #for the case that something input in SQL where expression textbox
                else:
                    sql = "SELECT * FROM tmp_query WHERE %s AND project_date = '%s'" % (statement, date)
                
                cmdStr = 'pgsql2shp -f %s -h %s -u %s -p %s -P %s %s "%s"' % (outshp, host, user, port, password, dbname, sql.encode("big5")) 
                result = os.popen(cmdStr).read()
                count += 1
                log.write("Generating shapefile %s...\n" % (outshp))
                log.write(cmdStr + "\n")
                log.write(result + "\n")
                if "ERROR" in result or "Failed" in result:
                    count -= 1
                    try:
                        dllist = glob.glob(f + date + "*")
                        for file in dllist:
                            os.remove(file)
                    except:
                        print "Can't remove error files!"
                        
                messagedialog = gtk.MessageDialog(self, 
                        gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                        gtk.BUTTONS_CLOSE, '%d shapefile(s) have been generated.\n\nCheck the log file "log.txt" in output directory for more information.' % count)
        else:
            #check file name 
            if self.entry2.get_text().replace(" ", "") == "":
                messagedialog = gtk.MessageDialog(self, 
                        gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
                        gtk.BUTTONS_CLOSE, 'Invalid file name!')
                log.write("Invalid file name!\n")
                log.close()
                messagedialog.set_position(gtk.WIN_POS_CENTER)
                messagedialog.run()
                messagedialog.destroy()
                return
            else:
                outshp = self.entry2.get_text().replace(" ", "").encode("big5")
                if not outshp.endswith(".shp"):
                    outshp += ".shp"

                #rename file as filename_N if have same outputfile, N is a number
                if os.path.exists(os.path.join(os.getcwd(), outshp)) or os.path.exists(os.path.join(os.getcwd(), outshp + ".shp")):
                    outshp = os.path.splitext(outshp)[0] + "_1.shp"
                    num = 2
                    #if still exists, increase the number of N
                    while os.path.exists(os.path.join(os.getcwd(), outshp)) or os.path.exists(os.path.join(os.getcwd(), outshp + ".shp")):
                        outshp = os.path.splitext(outshp)[0][:-2] + "_%d.shp" % num
                        num += 1
            
            #for the case that where statement is empty
            if statement.replace(" ", "") == "":
                sql = "SELECT * FROM tmp_query WHERE project_date >= '%s' AND project_date <= '%s'" % (_from, _to)
            #for the case that something input in SQL where expression textbox
            else:
                sql = "SELECT * FROM tmp_query WHERE %s AND project_date >= '%s' AND project_date <= '%s'" % (statement, _from, _to)
            cmdStr = 'pgsql2shp -f %s -h %s -u %s -p %s -P %s %s "%s"' % (outshp, host, user, port, password, dbname, sql.encode("big5")) 
            result = os.popen(cmdStr).read()
            count += 1
            log.write("Generating shapefile %s...\n" % (outshp))
            log.write(cmdStr + "\n")
            log.write(result + "\n")
            if "ERROR" in result or "Failed" in result:
                count -= 1
                try:
                    dllist = glob.glob(outshp + "*")
                    for file in dllist:
                        os.remove(file)
                except:
                    print "Can't remove error files!"
                    
            messagedialog = gtk.MessageDialog(self, 
                    gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                    gtk.BUTTONS_CLOSE, '1 shapefile have been generated.\n\nCheck the log file "log.txt" in output directory for more information.')
                    
        log.write("-"*34 + time.strftime("%Y%m%d_%H%M%S", time.gmtime()) + "-"*34 + "\n")
        log.close()
        messagedialog.set_position(gtk.WIN_POS_CENTER)
        messagedialog.run()
        messagedialog.destroy()
        
def create_field_list():
    try:
        reloadConfig()
        con = psycopg2.connect(database = dbname, user = user, password = password, host = host, port = port)
        cur = con.cursor()
        sql = """
              DROP VIEW IF EXISTS tmp_query;
              CREATE VIEW tmp_query AS
              SELECT *
              FROM (SELECT slide_id, project_date::text, workingcircle_name, forest_name, county_name, town_name, reservoir_name, water_name, basin_name, area, centroid_x, centroid_y, geom
                    FROM slide_area, project, admin_area, working_circle, reservoir, watershed, forest_district, basin
                    WHERE project_no = project_id AND county_no = county_id AND town_no = town_id AND workingcircle_no = workingcircle_id AND reservoir_no = reservoir_id AND water_no = water_id AND forest_no = forest_id AND basin_no = basin_id
                    GROUP BY slide_id, geom, project_date, workingcircle_name, forest_name, county_name, town_name, reservoir_name, water_name, basin_name, area, centroid_x, centroid_y) AS T
        """
        cur.execute(sql)
        con.commit()
        
        sql = "SELECT COLUMN_NAME FROM Information_Schema.COLUMNS WHERE TABLE_NAME = 'tmp_query' ORDER BY ORDINAL_POSITION"
        cur.execute(sql)
        
    except psycopg2.DatabaseError, e:
        print 'Could not open a database. Please check the config file: "Export.ini"'
    
    results = [row[0] for row in cur.fetchall()]
    if 'geom' in results:
        del results[results.index('geom')]
    
    con.close()
    return results

def get_records(fieldname, num):
    try:
        con = psycopg2.connect(database = dbname, user = user, password = password, host = host, port = port)
        cur = con.cursor()
        sql = "SELECT DISTINCT %s FROM tmp_query WHERE %s IS NOT NULL" % (fieldname, fieldname)
        cur.execute(sql)
        
    except psycopg2.DatabaseError, e:
        print 'Could not open a database. Please check the config file: "Export.ini"'
    
    result = cur.fetchall()
    con.close()
    
    if len(result) == 0:
        return [[], False]

    if num == 10:
        if isinstance(result[0][0], str) or isinstance(result[0][0], unicode) or isinstance(result[0][0], unicode):
            result = [row[0].decode("big5") for row in result][:10]
            result.sort()
            return [result, True]
        else:
            result = [row[0] for row in result][:10]
            result.sort()
            return [result, False]
    else:
        if isinstance(result[0][0], str) or isinstance(result[0][0], unicode):
            result = [row[0].decode("big5") for row in result] 
            result.sort()
            return [result, True]
        else:
            result = [row[0] for row in result]
            result.sort()
            return [result, False]

#read config file
def reloadConfig():
    settings = open(configpath)
    lines = settings.readlines()
    global host, port, dbname, user, passwords
    host = lines[0].split("=")[-1].replace("\n", "")
    port = lines[1].split("=")[-1].replace("\n", "")
    dbname = lines[2].split("=")[-1].replace("\n", "")
    user = lines[3].split("=")[-1].replace("\n", "")
    passwords = lines[4].split("=")[-1].replace("\n", "")
    settings.close()
        
def main():
    os.environ["pgclientencoding"] = "big5"   
    gtk.main()
    return 0

if __name__ == '__main__':
    exportpath = os.getcwd()
    if len(sys.argv) > 1:
        root = os.path.dirname(os.path.dirname(os.getcwd()))
        isDefault = False
        if not os.path.exists(os.path.join(exportpath, "..", "conf")):
            os.mkdir(os.path.join(exportpath, "..", "conf"))
        configpath = os.path.join(exportpath, "..", "conf", "Export.ini")
    else:
        root = os.getcwd()
        isDefault = True
        configpath = os.path.join(exportpath, "Export.ini")
    #read config file
    if not os.path.exists(configpath):
        settings = open(configpath, "w")
        settings.write("host=localhost\nport=5432\ndbname=landslide\nuser=postgres\npassword=mypassword\n")
        host = "localhost"
        port = "5432"
        dbname = "landslide"
        user = "postgres"
        password = "mypassword"
        settings.close()
    else:
        settings = open(configpath)
        lines = settings.readlines()
        host = lines[0].split("=")[-1].replace("\n", "")
        port = lines[1].split("=")[-1].replace("\n", "")
        dbname = lines[2].split("=")[-1].replace("\n", "")
        user = lines[3].split("=")[-1].replace("\n", "")
        password = lines[4].split("=")[-1].replace("\n", "")
        settings.close()
    
    if isDefault:
        GUI()
    else:
        GUI(os.path.join(root, "output"))

    main()
