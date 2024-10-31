import pandas as pd
import duckdb
import gzip
import glob
import pathlib
import shutil

datadir = "/home/danjo/scenarios/ume/matsim/output/"

flist = [p.name for p in pathlib.Path(datadir).iterdir() if (p.is_file() & p.name.endswith(".gz"))]
tablenames = [p[0:-7] for p in flist]
allstatements = []
con = duckdb.connect()

for f in flist:
    f_csv = f[0:-3]
    tablename = f_csv[0:-4]
    with gzip.open(datadir + f, 'rb') as f_in:
        with open(datadir + f_csv, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    tbl_create = f"create table {tablename} as select * from read_csv('{datadir + f_csv}');"
    allstatements.append(tbl_create + '\n')
    con.sql(tbl_create)

j_create = f'select "FROM" as orig, "TO" as dest, VALUE as {tablenames[0]} from {tablenames[0]};'
allstatements.append(j_create + '\n')
joined = con.sql(j_create)

for tn in tablenames[1:]:
    n_create = f'select "FROM" as orig, "TO" as dest, VALUE as {tn} from {tn};'
    allstatements.append(n_create + '\n')
    nexttable = con.sql(n_create)
    j_create = f"select joined.*, {tn} from joined full outer join nexttable on joined.orig = nexttable.orig and joined.dest = nexttable.dest;"
    allstatements.append(j_create + '\n')
    joined = con.sql(j_create)


con.sql("select * from joined order by orig, dest;").to_parquet(datadir + "matsim_los.parquet")
con.sql("select * from joined order by orig, dest;").to_csv(datadir + "matsim_los.csv")

allstatements.append(f"copy (select * from joined order by orig, dest) to {datadir}matsim_los.parquet (format parquet);\n")
outfile = open(datadir + 'create_statements.txt', 'w')
outfile.writelines(allstatements)
outfile.close()