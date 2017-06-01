import dataset
import config

# unicode mgmt
import sys
reload(sys)
sys.setdefaultencoding('utf8')

Db1 = dataset.connect(config.DB1)
Db2 = dataset.connect(config.DB2)

def get_nullable(string):
    if string == 'YES':
        return 'nullable'
    else:
        return ''

def get_vc_max(length):
    if length is None:
        return ''
    else:
        return str(length)

def get_schema(db):
    query = db.query("""SELECT table_name, column_name, data_type, character_maximum_length, is_nullable
                        FROM information_schema.columns 
                        WHERE table_schema = 'public' 
                        ORDER BY table_name, column_name;""")

    result = {}
    for x in query:
        if x['table_name'] not in result:
            result[x['table_name']] = {}
        result[x['table_name']][x['column_name']] = x['data_type'] + ' ' + get_vc_max(x['character_maximum_length']) + ' ' + get_nullable(x['is_nullable'])
    return result


db1_tables = get_schema(Db1)
db2_tables = get_schema(Db2)

if not all( x in db1_tables for x in db2_tables ):
    extra_tables = [x for x in db2_tables if x not in db1_tables]
    print('Tables in db2 not in db1', extra_tables)
elif not all ( x in db2_tables for x in db1_tables):
    extra_tables = [x for x in db1_tables if x not in db2_tables]
    print('Tables in db1 not in db2', extra_tables)
else:
    print('Tables match')


if all( len(db2_tables[x]) == len(db1_tables[x]) for x in db2_tables ):
    print('Columns match')
else:
    for x in db2_tables:
        extra_prod = [x + ":" + c + "(" + db2_tables[x][c] + ")" for c in db2_tables[x] if c not in db1_tables[x]]
        if ( len(extra_prod) > 0):
            print('Columns in db2_tables not in db1_tables', extra_prod)
        extra_qa = [ x + ":" + c + "(" + db1_tables[x][c] + ")" for c in db1_tables[x] if c not in db2_tables[x]]
        if ( len(extra_qa) > 0):            
            print('Columns in db1_tables not in db2_tables', extra_qa)

for t in [t for t in db2_tables if t in db1_tables]:
    for c in [c for c in db2_tables[t] if c in db1_tables[t]]:
        if ( db2_tables[t][c] != db1_tables[t][c] ):
            print("for column " + c + " data type in prod is " + db2_tables[t][c] + " and in qa is " + db1_tables[t][c])




