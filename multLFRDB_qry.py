# multLFRDB_qry.py - multiple LFRDB query tool
# C. Toney, christoney@fs.fed.us
#
# v. 1,03, 2007-05-14
#   -fixed handling of Access illegal field names (Date, SECTION, Description)
# v. 1.02, 2007-04-05:
#   -fixed bug with SELECT DISTINCT and SELECT DISTINCTROW
# v. 1.01, 2007-04-01:
#   -improvements to user interface
#   -added check for duplicate mdbs before executing sql
# v. 1.0, 2007-03-28
#   -new

from Tkinter import *
import tkFileDialog, tkMessageBox
import os
from datetime import datetime
import win32com.client
import re


class ModalDialog(Toplevel):
    def __init__(self, master=None, **kw):
        Toplevel.__init__(self, master, **kw)
        self.master = master
        self.geometry("+%d+%d" % (self.master.winfo_rootx()+100,self.master.winfo_rooty()+100))
        self.withdraw()
        
    def show(self):
        self.deiconify()
        self.transient(self.master)
        self.grab_set()

        
class Gui:
    def __init__(self):
        self.root = root = Tk()
        self.rClickbinder(self.root)
        self.lastDir = '/'
        self.title = 'multLFRDB_qry.py'
        self.version = '1.03'
        self.validDestMdb = False

        root.minsize(650,400)
        root.title(self.title)
        root.resizable(width=False,height=False)

        Label(root, text='Multiple LFRDB Query', fg='blue', font='bold').grid(row=0,columnspan=2,sticky='NW')

        Label(root, text='Directory with LFRDBs to query, or list of mdb files:').grid(row=1, sticky='NW')
        self.txtMdbs = Text(root, height=6,wrap='word')
        self.txtMdbs.grid(row=2,sticky='NW')
        self.scrollMdbs = Scrollbar(root, orient='vertical', command=self.txtMdbs.yview)
        self.scrollMdbs.grid(row=2, column=1, sticky=N+S+W)
        self.txtMdbs["yscrollcommand"] = self.scrollMdbs.set

        self.btnFiles = Button(root, text='Add files', relief='raised', command=self.addFiles)
        self.btnFiles.grid(row=2,column=2,sticky='NW')
        self.btnDir = Button(root, text='Add dir', relief='raised', command=self.addDir)
        self.btnDir.grid(row=2,column=3,sticky='NW')

        Label(root, text='SQL statement:').grid(row=3,sticky='NW')
        self.txtSQL = Text(root, height=6, wrap='word')
        self.txtSQL.grid(row=4,sticky='NW')
        self.scrollSQL = Scrollbar(root, orient='vertical', command=self.txtSQL.yview)
        self.scrollSQL.grid(row=4, column=1, sticky=N+S+W)
        self.txtSQL["yscrollcommand"] = self.scrollSQL.set

        Label(root, text='Destination/link mdb (optional for UPDATE statements):').grid(row=5,sticky='NW')
        self.txtDestMdb = Label(root, text='', anchor='w', bg='white', relief='sunken')
        self.txtDestMdb.grid(row=6,sticky=E+W)
        self.btnDestMdb = Button(root, text='Select mdb', relief='raised', command=self.selDestMdb)
        self.btnDestMdb.grid(row=6,column=2,columnspan=2,sticky='NW')

        Label(root, text='Link table (optional):').grid(row=7,sticky='NW')
        self.mb = Menubutton(root, relief='raised',text='Select a table', state='disabled')
        self.mb.grid(row=8,sticky='NW')
        self.mb.menu = Menu(self.mb, tearoff=0)
        self.mb['menu'] = self.mb.menu
        self.tbl = StringVar() # control variable behind mb.menu

        self.btnRun = Button(root, text='Execute SQL', relief='raised', command=self.runQuery)
        self.btnRun.grid(row=9,columnspan=3)

        Label(root, text='Messages:').grid(row=10,sticky='NW')
        self.txtMsgs = Text(root, height=8, wrap='word')
        self.txtMsgs.grid(row=11,sticky='NW')
        self.scrollMsgs = Scrollbar(root, orient='vertical', command=self.txtMsgs.yview)
        self.scrollMsgs.grid(row=11, column=1, sticky=N+S+W)
        self.txtMsgs["yscrollcommand"] = self.scrollMsgs.set

        self.btnUsage = Button(root, text='Usage', relief='raised', command=self.usage)
        self.btnUsage.grid(row=11,column=2,sticky='SE')
        self.btnExit = Button(root, text='Quit', relief='raised', command=root.quit)
        self.btnExit.grid(row=11,column=3,sticky='S')
        
    def rClicker(self, e):
        ''' right click context menu for Entry and Text widgets '''
        try:    
            def rClick_Copy(e, apnd=0):
                e.widget.event_generate('<Control-c>')

            def rClick_Cut(e):
                e.widget.event_generate('<Control-x>')

            def rClick_Paste(e): 
                e.widget.event_generate('<Control-v>')

            e.widget.focus()

            nclst=[
                #('      ',None),   #
                (' Cut', lambda e=e: rClick_Cut(e)),  
                (' Copy', lambda e=e: rClick_Copy(e)),
                (' Paste', lambda e=e: rClick_Paste(e)),
                ]
            
            rmenu = Menu(None, tearoff=0, takefocus=0)
        
            for (txt, cmd) in nclst:
                if txt == ' ------ ':
                    rmenu.add_separator()
                else:
                    rmenu.add_command(label=txt, command=cmd)

            #rmenu.entryconfigure(0, state = 'disabled')
            rmenu.tk_popup(e.x_root-3, e.y_root+3,entry="0")
        
        except TclError:
            print ' - rClick menu, something wrong'
            pass

        return "break"

    def rClickbinder(self, r):
        try:
            for b in ['Text', 'Entry']: #, 'Listbox', 'Label']:  # 
                r.bind_class(b, sequence='<Button-3>', func=self.rClicker, add='')
        except TclError:
            print ' - rClickbinder, something wrong' 
            pass

    def selLinkTbl(self):
        self.mb['text'] = self.tbl.get()

    def populateMenu(self):
        fname = self.txtDestMdb['text']
        #print fname
        self.mb.menu.delete(0, self.mb.menu.index('end'))
        self.tbl.set('')
        if os.path.isfile(os.path.normpath(fname)) and os.path.splitext(fname)[1] == '.mdb':
            self.validDestMdb = True
            self.mb['text'] = 'Select a table'
            try:
                cn = win32com.client.Dispatch(r"ADODB.Connection")
                cat = win32com.client.Dispatch(r"ADOX.Catalog")
                cn.Open(r'Provider=Microsoft.Jet.OLEDB.4.0;Data Source=' + fname)
                cat.ActiveConnection = cn
                for x in range(0, cat.Tables.Count):
                    #print tbl_name, cat.Tables.Item(x).Type
                    if cat.Tables.Item(x).Type == 'TABLE':
                        tbl_name = cat.Tables.Item(x).Name
                        self.mb.menu.add_radiobutton(label=tbl_name, value=tbl_name, variable=self.tbl, command=self.selLinkTbl)
                if self.mb['state'] == 'disabled':
                    self.mb['state'] = 'active'
                cat = None
                cn.Close()
                cn = None
            except:
                print 'exception in populateMenu'
        else:
            self.validDestMdb = False
            self.mb['state'] = 'disabled'
            
    def addDir(self):
        dirname = None
        dirname = tkFileDialog.askdirectory(title='Select directory',initialdir=self.lastDir)
        if dirname:
            self.txtMdbs.insert('end', dirname + ';\n')
            self.lastDir = dirname

    def addFiles(self):
        fnames = None
        fnames = tkFileDialog.askopenfilenames(title='Select files', initialdir=self.lastDir, filetypes=[('mdb','*.mdb')])
        for fname in fnames:
            self.txtMdbs.insert('end', fname + ';\n')
        if len(fnames) > 0:
            self.lastDir = os.path.split(fnames[0])[0]

    def selDestMdb(self):
        destMdb = None
        destMdb = tkFileDialog.askopenfilename(title='Select an mdb', initialdir=self.lastDir, filetypes=[('mdb','*.mdb')])
        if destMdb:
            self.txtDestMdb['text'] = os.path.normpath(destMdb)
            self.lastDir = os.path.split(destMdb)[0]
            self.populateMenu()

    def writeMsg(self, text):
        msg = text
        self.txtMsgs.insert('end', msg + '\n')
        self.txtMsgs.yview(MOVETO, '1.0')
        self.root.update_idletasks()

    def usage(self):
        txt = 'multLFRDB_qry.py - Multiple LFRDB query tool - v.' + self.version + '\n'
        txt = txt + '\n'
        txt = txt + 'Runs SELECT or UPDATE queries against a list of LFRDB Access database files.\n'
        txt = txt + '\n'
        txt = txt + '-Mdbs are specified in a semicolon-delimited list of files and/or directories.\n'
        txt = txt + 'All mdb files in specified directories are processed (non-recursive).\n'
        txt = txt + '-SQL statements can be pasted directly from Access.\n'
        txt = txt + '-Currently, "SELECT *" is not supported - field names must be listed explicity.\n'
        txt = txt + '"SELECT TOP" is not supported, and SQL aggregate functions are not supported.\n'
        txt = txt + '-Results from SELECT statements are written to a time-stamped table named\n'
        txt = txt + 'results_YYYYMMDDhhmmss in the specified destination mdb.\n'
        txt = txt + '-Optionally, a table in the destination mdb can be set as a link table. This\n'
        txt = txt + 'table will be linked in each LFRDB before exectuting the SQL statement. Links\n'
        txt = txt + 'will be removed when processing is complete.\n'
        txt = txt + '\n'
        txt = txt + 'This version is BETA. Backup all data before using!\n'
        tkMessageBox.showinfo('Usage', txt)

    def runQuery(self):
        def guiProcessing():
            self.root['cursor'] = 'watch'
            self.root.update_idletasks()
            self.top = ModalDialog(self.root)
            self.lblWait = Label(self.top, text='Processing, please wait...')
            self.btnOK = Button(self.top, text=' OK ', state='disabled', command = self.top.destroy)
            self.lblWait.grid(row=0)
            self.btnOK.grid(row=1)
            self.top.show()
            self.top['cursor'] = 'watch'
            self.top.update()
            self.top.focus_set()
            
        def guiReady():
            self.root['cursor'] = ''
            self.top['cursor'] = ''
            self.lblWait['text'] = 'Done. See messages below.'
            self.btnOK['state'] = 'active'
            self.top.focus_set()
        
        mdbListText = self.txtMdbs.get('1.0','end').replace('\n','').strip().rstrip(';')
        mdbList = mdbListText.split(';')
        entries = []
        for entry in mdbList:
            if os.path.isfile(os.path.normpath(entry)) and os.path.splitext(entry)[1] == '.mdb':
                if entry not in entries:
                    entries.append(os.path.normpath(entry))
            elif os.path.isdir(os.path.normpath(entry)):
                files = os.listdir(os.path.normpath(entry))
                for file in files:
                    if os.path.isfile(os.path.join(os.path.normpath(entry),file)) and os.path.splitext(file)[1] == '.mdb':
                        if os.path.join(os.path.normpath(entry),file) not in entries:
                            entries.append(os.path.join(os.path.normpath(entry),file))

        if len(entries) == 0:
            tkMessageBox.showinfo(self.title, 'no valid files or directories containing LFRDBs')
            return            
        g_sql = self.txtSQL.get('1.0','end').replace('\n',' ').replace('"','\'').replace(';','').strip()
        if g_sql[0:6].upper() not in ('SELECT','UPDATE'):
            tkMessageBox.showinfo(self.title, 'only SELECT and UPDATE statements are supported in this version')
            return
        p = re.compile('[zZ]\d\d_') # if g_sql contains actual zone numbers, replace with 'Z##'
        g_sql = p.sub('Z##_', g_sql)

        if g_sql[0:6].upper() == 'SELECT' and not self.validDestMdb:
            tkMessageBox.showinfo(self.title, 'destination mdb is required for a SELECT query')
            return
        if self.validDestMdb:
            dest_mdb = self.txtDestMdb['text']
            dest_tbl = 'results_' + datetime.now().strftime('%Y%m%d%H%M%S') # destination table name if one is needed    

        if self.tbl.get() != '':
            link_tbl = self.tbl.get() # optional table in dest_mdb to link in each LFRDB before running sql
            #print 'link table is', link_tbl
            cat = win32com.client.Dispatch(r'ADOX.Catalog')
            tbl = win32com.client.Dispatch(r'ADOX.Table')
        else:
            link_tbl = None

        cn = win32com.client.Dispatch(r'ADODB.Connection')
        
        guiProcessing()
        self.writeMsg('processing LFRDBs...')
        
        mdbs = []
        mdb_count = 0

        for file in entries:
            if not os.path.isfile(file):
                print file, 'is not a file'
                continue
            if os.path.splitext(file)[1] != '.mdb':
                self.writeMsg(file + ' is not a mdb')
                continue
            fname = os.path.split(file)[1]
##            if (fname[0:1].upper() != 'Z') or (not fname[1:3].isdigit()):
##                self.writeMsg('skipping ' + file + ' - not a LFRDB with "Z##_" file naming')
##                continue
            try:
                cn.Open(r'Provider=Microsoft.Jet.OLEDB.4.0;Data Source=' + file)
            except:
                self.writeMsg('could not open ' + file + ' - skipping this mdb')
                continue
            mdbs.append(file)
            mdb_count = mdb_count + 1

            if link_tbl: # link table if it does not already exist in this mdb
                cat.ActiveConnection = cn
                do_link = True
                for x in range(0, cat.Tables.Count):
                    if cat.Tables.Item(x).Name.upper() == link_tbl.upper():
                        self.writeMsg('table ' + link_tbl + ' already exists in ' + file + ' - link not added')
                        do_link = False
                if do_link:
                    try:
                        tbl.Name = link_tbl
                        tbl.ParentCatalog = cat
                        tbl.Properties.Item("Jet OLEDB:Create Link").Value = True
                        tbl.Properties.Item("Jet OLEDB:Link Datasource").Value = dest_mdb
                        tbl.Properties.Item("Jet OLEDB:Remote Table Name").Value = link_tbl
                        cat.Tables.Append(tbl)
                    except:
                        self.writeMsg('link table failed in ' + file + ' - aborting script')
                        tbl = None
                        cat = None
                        cn.Close()
                        cn = None
                        guiReady()
                        return

            z_num = fname[0:3].upper()
            z_sql = g_sql.replace('z##',z_num) # sql for this zone
            z_sql = z_sql.replace('Z##',z_num)
            
            # check for some Access reserved words that need brackets,
            # assuming these are used as field names
            p = re.compile(r'\bDate\b', re.IGNORECASE)
            z_sql = p.sub('[Date]', z_sql)
            p = re.compile(r'\bSECTION\b', re.IGNORECASE)
            z_sql = p.sub('[SECTION]', z_sql)
            p = re.compile(r'\bDescription\b', re.IGNORECASE)
            z_sql = p.sub('[Description]', z_sql)
            
            if z_sql[0:6].upper() == 'SELECT':
                if mdb_count == 1:
                    z_sql = z_sql.replace('FROM', 'INTO ' + dest_tbl + ' IN "' + dest_mdb + '" FROM')
                else:
                    i = z_sql.upper().find('FROM')
                    fields = z_sql[6:i].strip() # list of fields for INSERT INTO
                    if fields[0:12].upper() == 'DISTINCTROW ':
                        fields = fields[12:].strip()
                    if fields[0:9].upper() == 'DISTINCT ':
                        fields = fields[9:].strip()
                    if fields[0:4].upper() == 'ALL ':
                        fields = fields[4:].strip()
                    p = re.compile('\w*\.', re.IGNORECASE)
                    fields = p.sub('', fields) # remove 'Z##_tablename.' from field names
                    z_sql = z_sql.replace('SELECT', 'INSERT INTO ' + dest_tbl + ' (' + fields + ') IN "' + dest_mdb + '" SELECT')
            try:
                #print z_sql + '\n\n'
                cn.Execute(z_sql)
            except:
                self.writeMsg(z_sql)
                self.writeMsg('query failed on ' + file + ' - skipping this mdb')
                if link_tbl and do_link:
                    cat.Tables.Delete(link_tbl)
                cn.Close()
                continue
            if link_tbl and do_link:
                cat.Tables.Delete(link_tbl)
            cn.Close()

        self.writeMsg('')
        self.writeMsg('processed ' + str(mdb_count) + ' mdbs:')
        for mdb in mdbs:
            self.writeMsg(mdb)
        self.writeMsg('Execute SQL complete')
        self.writeMsg('')
        
        if link_tbl:
            cat = None
            tbl = None
        cn = None

        guiReady()        


if __name__ == '__main__':

    gui = Gui()
    mainloop()
