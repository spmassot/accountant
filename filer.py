import pandas as pd
import xlrd
import re


def prep_files(files, files_type):
    return {
        'ups': prep_ups_files,
        'givens': prep_givens_files,
        'freight': prep_freight_files
    }.get(files_type, lambda x: x)(files)


def prep_ups_files(files):
    def prep_file(f, reg):
        xls = xlrd.open_workbook(f, on_demand=True)
        matched = [x for x in xls.sheet_names() if reg.match(x)]
        return pd.read_excel(
            input_file,
            sheetname=matched[0],
            parse_cols=89
        ).to_dict(orient='records')

    sought = re.compile(r'^\s*accruals*\s*$', re.I)
    return pd.concat([prep_file(f, sought) for f in files], ignore_index=True)


def prep_givens_files(files):
    def prep_file(f, reg):
        adjustments = re.compile(r'.*adjustment.*')
        xls = xlrd.open_workbook(f, on_demand=True)
        sheets = [x for x in xls.sheet_names() if reg.match(x)]
        adj_sheets = [x for x in sheets if adjustments.match(x)]
        flat_sheets = [x for x in sheets if x not in adj_sheets]
        flat_frames = [pd.read_excel(f,
                                     sheetname=mtch,
                                     header=7,
                                     converters={"ORDER #'s":str}
                                    ).dropna(thresh=12) for mtch in flat_sheets]
        adj_frames = [pd.read_excel(f,
                                    sheetname=mtch,
                                    header=7,
                                    converters={"ORDER #'s":str}
                                   ).dropna(thresh=4) for mtch in adj_sheets]
        return (
                pd.concat(flat_frames, ignore_index=True),
            pd.concat(adj_frmaes, ignore_index=True)
        )
    sought = re.compile(r'^(brampton|chesapeake|plainfield|reno|hope).*', re.I)
    flat_files = []
    adjustments = []
    for f in files:
        flat, adj = prep_file(f, sought)
        flat_files.append(flat)
        adjustments.append(adj)
    return (
        pd.concat(flat_files, ignore_index=True),
        pd.concat(adjustments, ignore_index=True)
    )


def prep_frieight_files(files):
    pass
