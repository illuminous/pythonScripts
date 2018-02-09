from database.util import Conn
from config.cfg import Config
from sclass_objects import DbRow as Obj

cfg = Config()

def load_map():
    # loads database rows into a dictionary (map)  
    # map key = bps_cd|lifeform_cd
    # map value = list of db_row objects  - append objects for each SClass
    
    manual_mode = cfg.val("manual_mode")

    if manual_mode:
        return fetch_dict_manually()
    else:
        return fetch_dict_dynamically()

def fetch_dict_dynamically():
    
    dbm = {}
    groupnames = {}
    print 'loading database...'
    
    conn = Conn(cfg.val("mdb_file"))
    conn.Open()

    sql="""Select * from q_sclass_rules;""" 
    
    rs = conn.get_rs(sql)
    
    while not rs.EOF:
        bps_cd = rs.Fields.Item(0).Value
        groupname = rs.Fields.Item(1).Value
	if not groupnames.has_key(bps_cd):
	    groupnames[bps_cd] = groupname
        sclass_cd = rs.Fields.Item(2).Value
        lf_cd = rs.Fields.Item(3).Value 
        mincov = int(rs.Fields.Item(4).Value)
        maxcov = int(rs.Fields.Item(5).Value)
        minht = rs.Fields.Item(6).Value
        maxht = rs.Fields.Item(7).Value
        evt = rs.Fields.Item(8).Value
        obj = Obj(bps_cd, sclass_cd, lf_cd, mincov, maxcov, minht , maxht)
        load_db_row(dbm, obj)
        rs.MoveNext()
    
    rs.Close()
    conn.Close()
   
    return dbm,groupnames

def fetch_dict_manually():

    dbm = {}
    
    # columns: bps_cd, sclass_cd, lform_cd, min_cov, max_cov, min_ht, max_ht

    # loop through db rows...

    # 1st loop

    obj = Obj(10090, 1, 100, 103, 109, 101 , 108)

    load_db_row(dbm, obj)

    # 2nd loop...

    obj = Obj(10090, 2, 100, 104, 108, 101, 107)

    load_db_row(dbm, obj)

    # 3rd loop...
    
    #obj = Obj(10090, 3, 103, 104, 109, 109, 111)

    #load_db_row(dbm, obj)
    
    # 4th loop...
    #obj = Obj(10091, 4, 100, 103, 109, 108, 111)
    
    #load_db_row(dbm, obj)

    
    # end loop

    return dbm

def load_db_row(dbm, obj):
  
    if dbm.has_key(obj.id):
        dbm[obj.id].append(obj)
    else:
        dbm[obj.id] = [obj]
    
        
