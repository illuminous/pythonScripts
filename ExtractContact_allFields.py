import win32com.client

DEBUG = 0

class MSOutlook:
    def __init__(self):
        self.outlookFound = 0
        try:
            self.oOutlookApp = \
                win32com.client.gencache.EnsureDispatch("Outlook.Application")
            self.outlookFound = 1
        except:
            print "MSOutlook: unable to load Outlook"
        
        self.records = []


    def loadContacts(self, keys=None):
        if not self.outlookFound:
            return

        # this should use more try/except blocks or nested blocks
        onMAPI = self.oOutlookApp.GetNamespace("MAPI")
        ofContacts = \
            onMAPI.GetDefaultFolder(win32com.client.constants.olFolderContacts)

        if DEBUG:
            print "number of contacts:", len(ofContacts.Items)

        for oc in range(len(ofContacts.Items)):
            contact = ofContacts.Items.Item(oc + 1)
            if contact.Class == win32com.client.constants.olContact:
                if keys is None:
                    # if we were't give a set of keys to use
                    # then build up a list of keys that we will be
                    # able to process
                    # I didn't include fields of type time, though
                    # those could probably be interpreted
                    keys = []
                    for key in contact._prop_map_get_:
                        if isinstance(getattr(contact, key), (int, str, unicode)):
                            keys.append(key)
                    if DEBUG:
                        keys.sort()
                        print "Fields\n======================================"
                        for key in keys:
                            print key
                record = {}
                for key in keys:
                    record[key] = getattr(contact, key)
                if DEBUG:
                    print oc, record['FullName']
                self.records.append(record)


if __name__ == '__main__':
    if DEBUG:
        print "attempting to load Outlook"
    oOutlook = MSOutlook()
    # delayed check for Outlook on win32 box
    if not oOutlook.outlookFound:
        print "Outlook not found"
        sys.exit(1)
    fields = ['Account','Anniversary','AssistantName','AssistantTelephoneNumber',
           'Attachments','BillingInformation','Birthday','Body','Body','Body','Business2TelephoneNumber',
           'BusinessAddress','BusinessAddressCity','BusinessAddressCountry','BusinessAddressPostalCode',
           'BusinessAddressPostOfficeBox','BusinessAddressState','BusinessAddressStreet','BusinessFaxNumber',
           'BusinessHomePage','BusinessTelephoneNumber','CallbackTelephoneNumber','CarTelephoneNumber',
           'Categories','Children','Companies','CompanyMainTelephoneNumber','CompanyName',
           'ComputerNetworkName','ConversationTopic','CreationTime','CustomerID',
           'Department','Email1Address','Email2Address','Email3Address',
           'FileAs','FirstName',
           'FTPSite','FullName','Gender','GovernmentIDNumber','Hobby','Home2TelephoneNumber',
           'HomeAddress','HomeAddressCity','HomeAddressCity','HomeAddressCountry','HomeAddressCountry','HomeAddressPostalCode',
           'HomeAddressPostalCode','HomeAddressPostOfficeBox','HomeAddressPostOfficeBox','HomeAddressState','HomeAddressState',
           'HomeAddressStreet','HomeAddressStreet','HomeFaxNumber','HomeTelephoneNumber','Importance','Importance','Initials',
           'InternetFreeBusyAddress','ISDNNumber','JobTitle','Journal','Language','LastModificationTime','LastName',
           'Links','MailingAddress','ManagerName','MessageClass','MiddleName',
           'Mileage','MobileTelephoneNumber','NickName','NoAging','OfficeLocation','OrganizationalIDNumber',
           'OtherAddress','OtherAddressCity','OtherAddressCountry','OtherAddressPostalCode',
           'OtherAddressPostOfficeBox','OtherAddressState','OtherAddressStreet','OtherFaxNumber','OtherTelephoneNumber',
           'OutlookInternalVersion','OutlookVersion','PagerNumber','Parent','PersonalHomePage',
           'PrimaryTelephoneNumber','Profession','RadioTelephoneNumber',
           'ReferredBy',
           'ReminderOverrideDefault','ReminderPlaySound','ReminderSet','ReminderSoundFile','ReminderTime',
           'Sensitivity','Sensitivity','Size','Spouse',
           'Subject','Suffix','TelexNumber','Title','TTYTDDTelephoneNumber',
           'UnRead','User1','User2','User3','User4','WebPage']
##    fields = ['FullName',
##                'CompanyName', 
##                'MailingAddressStreet',
##                'MailingAddressCity', 
##                'MailingAddressState', 
##                'MailingAddressPostalCode',
##                'HomeTelephoneNumber', 
##                'BusinessTelephoneNumber', 
##                'MobileTelephoneNumber',
##                'Email1Address',
##                'Body'
##                ]

    if DEBUG:
        import time
        print "loading records..."
        startTime = time.time()
    # you can either get all of the data fields
    # or just a specific set of fields which is much faster
    #oOutlook.loadContacts()
    oOutlook.loadContacts(fields)
    if DEBUG:
        print "loading took %f seconds" % (time.time() - startTime)

    print "Number of contacts: %d" % len(oOutlook.records)
f = open('c:/working/Outlook/marketingContacts_20150319.csv', 'w')
biglist = ['Account','Anniversary','AssistantName','AssistantTelephoneNumber',
           'Attachments','BillingInformation','Birthday','Body','Body','Body','Business2TelephoneNumber',
           'BusinessAddress','BusinessAddressCity','BusinessAddressCountry','BusinessAddressPostalCode',
           'BusinessAddressPostOfficeBox','BusinessAddressState','BusinessAddressStreet','BusinessFaxNumber',
           'BusinessHomePage','BusinessTelephoneNumber','CallbackTelephoneNumber','CarTelephoneNumber',
           'Categories','Children','Companies','CompanyMainTelephoneNumber','CompanyName',
           'ComputerNetworkName','ConversationTopic','CreationTime','CustomerID',
           'Department','Email1Address','Email2Address','Email3Address',
           'FileAs','FirstName',
           'FTPSite','FullName','Gender','GovernmentIDNumber','Hobby','Home2TelephoneNumber',
           'HomeAddress','HomeAddressCity','HomeAddressCity','HomeAddressCountry','HomeAddressCountry','HomeAddressPostalCode',
           'HomeAddressPostalCode','HomeAddressPostOfficeBox','HomeAddressPostOfficeBox','HomeAddressState','HomeAddressState',
           'HomeAddressStreet','HomeAddressStreet','HomeFaxNumber','HomeTelephoneNumber','Importance','Importance','Initials',
           'InternetFreeBusyAddress','ISDNNumber','JobTitle','Journal','Language','LastModificationTime','LastName',
           'Links','MailingAddress','ManagerName','MessageClass','MiddleName',
           'Mileage','MobileTelephoneNumber','NickName','NoAging','OfficeLocation','OrganizationalIDNumber',
           'OtherAddress','OtherAddressCity','OtherAddressCountry','OtherAddressPostalCode',
           'OtherAddressPostOfficeBox','OtherAddressState','OtherAddressStreet','OtherFaxNumber','OtherTelephoneNumber',
           'OutlookInternalVersion','OutlookVersion','PagerNumber','Parent','PersonalHomePage',
           'PrimaryTelephoneNumber','Profession','RadioTelephoneNumber',
           'ReferredBy',
           'ReminderOverrideDefault','ReminderPlaySound','ReminderSet','ReminderSoundFile','ReminderTime',
           'Sensitivity','Sensitivity','Size','Spouse',
           'Subject','Suffix','TelexNumber','Title','TTYTDDTelephoneNumber',
           'UnRead','User1','User2','User3','User4','WebPage']
for item in biglist:
    
    f.write(item+',')
f.write('\n')
for i in range(len(oOutlook.records)):
    for x in biglist:
        try:
            column = "%s" %oOutlook.records[i][x]
            column = "".join(column.splitlines())
            column = column.replace(',','')
            f.write(column).encode('utf-8').strip()
            
            
        except:
            f.write(',')
    f.write(str(i)+'\n')
        
    
##    contact = "%s" % oOutlook.records[i]['FullName']
##    company = "%s" % oOutlook.records[i]['CompanyName']
##    company =company.replace(',','')
##    address = "%s" % oOutlook.records[i]['MailingAddressStreet']
##    address = "".join(address.splitlines())
##    address = address.replace(',','')
##    city = "%s" % oOutlook.records[i]['MailingAddressCity']
##    state = "%s" % oOutlook.records[i]['MailingAddressState']
##    zipcode = "%s" % oOutlook.records[i]['MailingAddressPostalCode']
##    homephone = "%s" % oOutlook.records[i]['HomeTelephoneNumber']
##    businessphone= "%s" % oOutlook.records[i]['BusinessTelephoneNumber']
##    mobilphone = "%s" % oOutlook.records[i]['MobileTelephoneNumber']
##    notes = "%s" % oOutlook.records[i]['Body']
##    notes = "".join(notes.splitlines())
##    notes = notes.replace(',','')
##    email = "%s" % oOutlook.records[i]['Email1Address']
##
##    output = ((contact+','+company+','+address+','+city+','+state+','+zipcode+','+homephone+','+businessphone+','+mobilphone+','+notes+','+email)).encode('utf-8').strip()
##    f.write(output+'\n')
##f.close()


    
    
