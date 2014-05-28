﻿# -*- coding: utf-8 -*-
'''
Created on 2013/10/15
Updated on 2014/05/10
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

class GUI(gtk.Window):
    def __init__(self, outputdir = os.path.join(os.getcwd(), "output")):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("delete_event", self.close_application)
        window.set_size_request(700, 720)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_title("Export Gtk")
        window.show()
        
        mainbox = gtk.VBox(False, 10)
        mainbox.show()###
        window.add(mainbox)
        
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
        self.liststore1 = self.create_model(create_field_list(), True)
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
        frame3.set_size_request(680, 80)
        hbox3.pack_start(frame3, False, False, 10)
        
        vbox2 = gtk.VBox(True, 0)
        vbox2.show()###
        frame3.add(vbox2)
        
        hbox4 = gtk.HBox(False, 0)
        hbox4.show()###
        vbox2.pack_start(hbox4, True, False, 0)
        
        label1 = gtk.Label("%s: " % split_field)
        hbox4.pack_start(label1, False, False, 10)
        label1.show()      
 
        self.entry1 = gtk.Entry()
        self.entry1.set_size_request(250, 20)
        hbox4.pack_start(self.entry1, False, False, 0)
        self.entry1.show()###
        
        self.checkbutton1 = gtk.CheckButton("Split Shapefile By %s" % split_field)
        hbox4.pack_end(self.checkbutton1, False, False, 60)
        self.checkbutton1.show()###
        
        hbox5 = gtk.HBox(False, 0)
        hbox5.show()###
        vbox2.pack_start(hbox5, True, False, 0)
        
        label2 = gtk.Label("Output Name: ")
        hbox5.pack_start(label2, False, False, 10)
        label2.show()      
 
        self.entry2 = gtk.Entry()
        self.entry2.set_size_request(202, 20)
        self.entry2.set_text(table)
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
        if sample:
            records, isstring = get_records(self.selected_feature, 10)
        else: 
            records, isstring = get_records(self.selected_feature, -1)
        treeview.set_model(self.create_model(records, False, isstring))
        
    def clear(self, widget):
        textbuffer = self.textview.get_buffer()
        textbuffer.set_text("")
        self.entry1.set_text("")
        
    def close_application(self, widget, event, data=None):
        gtk.main_quit()
        return False
        
    def test_value(self, widget):
        textbuffer = self.textview.get_buffer()
        start = textbuffer.get_start_iter()
        end = textbuffer.get_end_iter()
        statement = textbuffer.get_text(start, end)
        
        if statement.replace(" ", "") == "":
            sql = "SELECT gid FROM %s " % table
        else:
            sql = "SELECT gid FROM %s where %s" % (table, statement)

        buffer = self.entry1.get_text().replace(" ", "").split(",")
        f_list = []
        if self.entry1.get_text().replace(" ", "") != "":
            for element in buffer:
                if len(str(element).split("-")) == 2:
                    for f in [d for d in range(int(str(element.split("-")[0])), int(str(element.split("-")[1])) + 1)]:
                        f_list.append(f)
                else:
                    f_list.append(int(element))
            f_list.sort()
            tmp = ""
            for i in range(len(f_list)):
                if i == 0:
                    tmp += "%s = %d " % (split_field, f_list[i])
                else:
                    tmp += "OR %s = %d " % (split_field, f_list[i])

            if "where" not in sql:
                sql += "WHERE (" + tmp + ")"
            else:
                sql += "AND (" + tmp + ")"

        sql = sql.decode("utf-8")
        try:
            con = psycopg2.connect(database = dbname, user = user, password = passwords, host = host)
            cur = con.cursor()
            cur.execute(sql)
            results = cur.fetchall()
            messagedialog = gtk.MessageDialog(self, 
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                gtk.BUTTONS_CLOSE, "The where clause returned %d row(s)" % len(results))          
        
        except psycopg2.DatabaseError, e:
            messagedialog = gtk.MessageDialog(self, 
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
                gtk.BUTTONS_CLOSE, "An error occurred when executing the query.")
            print 'Could not open a database. Please check the config file: "Export.ini"'
            
        messagedialog.set_position(gtk.WIN_POS_CENTER)
        messagedialog.run()
        messagedialog.destroy()
            
    def export(self, widget):
        count = 0
        log = open("log.txt", "w")
        textbuffer = self.textview.get_buffer()
        start = textbuffer.get_start_iter()
        end = textbuffer.get_end_iter()
        if self.entry2.get_text().replace(" ", "") == "":
            outshp = table
        else:
            outshp = self.entry2.get_text().replace(" ", "").encode("big5")
        
        statement = textbuffer.get_text(start, end)
        if statement.replace(" ", "") == "":
            sql = "select * from %s " % table
        else:
            sql = "select * from %s where %s" % (table, statement)
            
        buffer = self.entry1.get_text().replace(" ", "").split(",")
        f_list = []
        for element in buffer:
            if len(str(element).split("-")) == 2:
                for f in [d for d in range(int(str(element.split("-")[0])), int(str(element.split("-")[1])) + 1)]:
                    f_list.append(f)
            else:
                if element != "":
                    f_list.append(int(element))
        f_list.sort()
        
        if len(f_list) == 0:
            cmdStr = '..\\bin\\pgsql2shp -f %s -h %s -u %s -P %s %s "%s"' % (outshp + ".shp", host, user, passwords, dbname, sql.encode("big5")) 
            result = os.popen(cmdStr).read()
            count += 1
            log.write("Generating shapefile %s...\n" % (outshp + ".shp"))
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
        
        else:
            if self.checkbutton1.get_active():
                for f in f_list:
                    if "where" not in sql:
                        tmpsql = sql + "where %s = %d " % (split_field, f)
                    else:
                        tmpsql = sql + " AND %s = %d" % (split_field, f)
                    cmdStr = '..\\bin\\pgsql2shp -f %s -h %s -u %s -P %s %s "%s"' % (outshp + str(f) + ".shp", host, user, passwords, dbname, tmpsql.encode("big5")) 
                    result = os.popen(cmdStr).read()
                    count += 1
                    log.write("Generating shapefile %s...\n" % (outshp + str(f) + ".shp"))
                    log.write(cmdStr + "\n")
                    log.write(result + "\n")
                    if "ERROR" in result or "Failed" in result:
                        count -= 1
                        try:
                            dllist = glob.glob(outshp + str(f) + "*")
                            for file in dllist:
                                os.remove(file)
                        except:
                            print "Can't remove error files!"
                
            else:
                tmp = ""
                for i in range(len(f_list)):
                    if i == 0:
                        tmp += "%s = %d " % (split_field, f_list[i])
                    else:
                        tmp += "OR %s = %d " % (split_field, f_list[i])
                if tmp != "":
                    if "where" not in sql:
                        sql += "where (" + tmp + ")"
                    else:
                        sql += "AND (" + tmp + ")"
                    
                cmdStr = '..\\bin\\pgsql2shp -f %s -h %s -u %s -P %s %s "%s"' % (outshp + ".shp", host, user, passwords, dbname, sql.encode("big5")) 
                result = os.popen(cmdStr).read()
                count += 1
                log.write("Generating shapefile %s...\n" % (outshp + ".shp"))
                log.write(cmdStr + "\n")
                log.write(result + "\n")
                if "ERROR" in result or "Failed" in result:
                    count -= 1
                
        messagedialog = gtk.MessageDialog(self, 
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                gtk.BUTTONS_CLOSE, '%d shapefile(s) have been generated.\n\nCheck the log file "log.txt" in output directory for more information.' % count)
                
        log.close()
        messagedialog.set_position(gtk.WIN_POS_CENTER)
        messagedialog.run()
        messagedialog.destroy()

        
        
        
        
def create_field_list():
    try:
        con = psycopg2.connect(database = dbname, user = user, password = passwords, host = host)
        cur = con.cursor()
        sql = "SELECT COLUMN_NAME FROM Information_Schema.COLUMNS WHERE TABLE_NAME = '%s' ORDER BY ORDINAL_POSITION" % table
        cur.execute(sql)
        
    except psycopg2.DatabaseError, e:
        print 'Could not open a database. Please check the config file: "Export.ini"'
    
    results = [row[0] for row in cur.fetchall()]
    del results[results.index('geom')]
    
    return results

def get_records(fieldname, num):
    try:
        con = psycopg2.connect(database = dbname, user = user, password = passwords, host = host)
        cur = con.cursor()
        sql = "SELECT DISTINCT %s FROM %s WHERE %s IS NOT NULL" % (fieldname, table, fieldname)
        cur.execute(sql)
        
    except psycopg2.DatabaseError, e:
        print 'Could not open a database. Please check the config file: "Export.ini"'
    
    result = cur.fetchall()
    
    if len(result) == 0:
        return [[], False]

    if num == 10:
        if isinstance(result[0][0], str) or isinstance(result[0][0], unicode):
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
        
def main():
    os.environ["pgclientencoding"] = "big5"   
    gtk.main()
    return 0

if __name__ == '__main__':
    erportpath = os.getcwd()
    if len(sys.argv) > 1:
        root = os.path.dirname(os.path.dirname(os.getcwd()))
        isDefault = False
        configpath = os.path.join(erportpath, "..", "conf", "Export.ini")
    else:
        root = os.getcwd()
        isDefault = True
        configpath = os.path.join(erportpath, "Export.ini")
    #read config file
    if not os.path.exists(configpath):
        settings = open(configpath, "w")
        settings.write("host=localhost\ndbname=landslide\nuser=postgres\npasswords=Zeiss10\ntable=new_table\ndatefield=YEAR")
        settings.close()
        host = "localhost"
        dbname = "landslide"
        user = "postgres"
        passwords = "Zeiss10"
        table = "new_table"
        datefield = "YEAR"
        settings.close()
    else:
        settings = open(configpath)
        lines = settings.readlines()
        host = lines[0].split("=")[-1].replace("\n", "")
        dbname = lines[1].split("=")[-1].replace("\n", "")
        user = lines[2].split("=")[-1].replace("\n", "")
        passwords = lines[3].split("=")[-1].replace("\n", "")
        table = lines[4].split("=")[-1].replace("\n", "")
        split_field = lines[5].split("=")[-1].replace("\n", "")
        settings.close()
    
    if isDefault:
        GUI()
    else:
        GUI(os.path.join(root, "output"))

    main()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 