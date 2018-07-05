import pandas as pd
import xlrd
import numpy as np
import os
import sqlite3 as db
from datetime import date
from ipywidgets import Textarea, Button, HBox, VBox, Text
from IPython.display import display, clear_output

def main(b, path_name = '/mnt/c/Users/Sean/Desktop/AudioVox/UPS/'):
    '''Does all the juice'''
    clear_output()
    schema = load_schema()
    with db.connect('freight.db') as conn:
        zed = [engine(x, conn, schema, path_name) for x in os.listdir(path_name)]
    print('Done')

def engine(some_file, conn, schemm, filepath):
    '''Takes a single file, pulls the relevant sheet, and inserts into the db'''
    print(some_file,)
    if check_exists(conn, some_file):
        print('is already in the database')
    else:
        errs = import_data_too(
            pull_sheet(filepath+some_file), conn, schemm, filepath+some_file
        )
        conn.cursor().execute('''INSERT INTO log VALUES (?,?)''', (date.today(), some_file))
        conn.commit()
        print('has been successfully imported with {} errors.'.format(errs))

def import_data_too(in_df, conn, schema, file_name):
    '''Tries a bulk insert of a dataframe, with recursion in the case of errors'''
    def _recursive_insert(conn, d_frame, schem, err_count=0, all_errors=[]):
        try:
            d_frame.to_sql('invoice', conn, if_exists='append', index=True, dtype=schem)  # should variable-ize table name
        except BaseException as e:
            if len(d_frame) == 1:
                err_count += 1
                all_errors.append(dict(d_frame.iloc[0]).update({'Error':str(e)}))
            else:
                error_count, all_errors = _recursive_insert(
                    conn,
                    d_frame[:len(d_frame)//2],
                    schem, err_count,
                    all_errors
                )
                error_count, all_errors = _recursive_insert(
                    conn,
                    d_frame[len(d_frame)//2:],
                    schem, err_count,
                    all_errors
                )
        return err_count, all_errors

    error_count, all_errors = _recursive_insert(conn, in_df, schema)
    conn.commit()
    if error_count > 0:
        pd.DataFrame(all_errors).to_csv(file_name[:-5]+'_errors.csv')

    return error_count

def check_exists(con_obj, filename):
    '''Checks the log table for filename, returns bool'''
    exec_sql = 'SELECT * FROM log WHERE inv_name="{}"'.format(filename)
    return pd.read_sql(exec_sql, con_obj).empty != True

def pull_sheet(input_file):
    '''Takes a full filename (path included), returns a dataframe of the relevant sheet.
    Assumes we want 00000726XC or 00000255QU worksheets'''
    xls = xlrd.open_workbook(input_file, on_demand=True)
    sought = ['Accruals', 'accruals', 'ACCRUALS', 'Accrual', 'accrual', 'ACCRUAL']
    matched = [x for x in xls.sheet_names() for y in sought if y in x][0]
    subject = pd.read_excel(input_file, sheetname=matched, parse_cols=89)
    return subject

def load_schema():
    '''Returns a dictionary of "colum name":"dtype" for the UPS invoices'''
    with open('/mnt/c/Users/Sean/Repos/audioVox/freight-automation/invoice_schema.txt') as f:
        return {x.split('=')[0]:x.split('=')[1].replace('\n','') for x in f}

run = Button(description='Run', button_style='Success')
run.on_click(main)
display(run)

base_qry = """
select
sum([Net Amount]) as 'Sum of Net Amount',
[Tracking Number]
from invoice
where date([Transaction Date]) between
date('2018-05-01') and date('2018-05-31')  --change the dates
group by [Tracking Number]
"""

# Query the Database below

from ipywidgets import Textarea, Button, HBox, VBox, Text
from IPython.display import (display, clear_output)
import sqlite3 as db

QRY = Textarea(placeholder='Enter SQL to be executed', value=base_qry)
QRY.layout.width = '40%'
QRY.layout.height = '300px'
BUTTN = Button(description='Execute', button_style='primary')
RENDR = Button(description='Write Results to file', button_style='info')
WHR = Text(placeholder='Name the file', value='/mnt/c/Users/Sean/Desktop/AudioVox/')
WHR.layout.width = '50%'

def on_sql_sub(b):
    clear_output()
    if 'UPDATE' in QRY.value.upper() or 'DELETE' in QRY.value.upper():
        print('This tool is for Read-only use.')
    else:
        with db.connect('freight.db') as conn:
            try:
                x = pd.read_sql_query(QRY.value, conn)
            except pd.io.sql.DatabaseError as e:
                print(e)
            except BaseException as f:
                conn.commit()
            else:
                display(x)
                if b.description == 'Write Results to file':
                    x.to_csv(WHR.value)

display(HBox([QRY, VBox([RENDR, BUTTN]), WHR]))
BUTTN.on_click(on_sql_sub)
RENDR.on_click(on_sql_sub)

filepath = '/mnt/c/Users/Sean/Desktop/AudioVox/FRTDDP/'
thirteens = [x for x in os.listdir(filepath) if 'DDPB13' in x]
fourteens = [x for x in os.listdir(filepath) if 'DDPB14' in x]

thirteens_books = [pd.read_excel(filepath+book, sheetname=None) for book in thirteens]
fourteens_books = [pd.read_excel(filepath+book, sheetname=None) for book in fourteens]

thirteens_dfs = []
for b in thirteens_books:
    for k,v in b.items():
        thirteens_dfs.append(v)

fourteens_dfs = []
for b in fourteens_books:
    for k,v in b.items():
        fourteens_dfs.append(v)

'''
thirteens_books = [v for k,v in b.items() for b in thirteens_books]
fourteens_books = [v for k,v in b.items() for b in fourteens_books]
'''
df_13 = pd.concat(thirteens_dfs, ignore_index=True)
df_14 = pd.concat(fourteens_dfs, ignore_index=True).drop_duplicates(subset='Tracking Number')

ups_df = pd.read_csv(WHR.value, usecols=['Sum of Net Amount','Tracking Number'])

merged_ups_df = ups_df.merge(df_14, how='left', on='Tracking Number')

merged_ups_df.head()

merged_ups_df = merged_ups_df.groupby('Pick Ticket', as_index=False).sum()
merged_ups_df = merged_ups_df[['Sum of Net Amount','Pick Ticket']]
merged_ups_df['Pick Ticket'].to_csv('/mnt/c/Users/Sean/Desktop/AudioVox/ups_pick_tickets.csv')

merged_ups_df.to_csv('/mnt/c/Users/Sean/Desktop/AudioVox/ups_amt_by_pt.csv')

df_13 = df_13.groupby('Pick Ticket', as_index=False).sum()

more = merged_ups_df.merge(df_13, how='left', on='Pick Ticket')
more = more.drop_duplicates(subset='Pick Ticket', keep='first')
more = more.set_index('Pick Ticket')

df_13.to_csv('/mnt/c/Users/Sean/Desktop/AudioVox/FRTDDP/FRTDDPB13_05.csv')

more.to_csv('/mnt/c/Users/Sean/Desktop/AudioVox/ups_data.csv')

