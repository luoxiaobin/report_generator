"""
Created on 2020/05/23

@author: kevin
"""
#!/usr/bin/python
import openpyxl
from openpyxl import Workbook  
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment,  numbers
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.utils import get_column_letter
from openpyxl.reader.excel import load_workbook

import logging, time, configparser, os

# Setup logger
logger = logging.getLogger(__name__)


def write_to_excel(report_name, data, excel_file_name):
    
    try:
        logger.info(f"start generating excel file {excel_file_name}..")

        wb = Workbook()  
        ws = wb.active  

        ws.merge_cells('a1:y1')
        ws['A1'] = f"{report_name}"
        cell = ws['A1']
        cell.font = Font(size =20, bold=True)
        cell.alignment = Alignment(horizontal="left", vertical="center")

        row_count = 0
        for rec in data:
            ws.append(list(rec))
            row_count = row_count + 1
        
        wb.save(f"{excel_file_name}")  
        logger.info(f"Total {row_count} records inserted into excel file")

        # doing formatting of the excel
        wb = load_workbook(filename = f"{excel_file_name}") 

        ws = wb["Sheet"]
        
        for col in range(1, 26):
            cell = ws.cell(column=col, row=2) 
            cell.font = Font(bold=True)

        for row in range(2, row_count+2):
            cell=ws.cell(column=1, row=row)
            cell.alignment = Alignment(horizontal="center", vertical="center")

            cell=ws.cell(column=2, row=row)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell=ws.cell(column=4, row=row)
            cell.alignment = Alignment(horizontal="center", vertical="center")

            cell=ws.cell(column=8, row=row)
            cell.alignment = Alignment(horizontal="center", vertical="center")

            cell=ws.cell(column=9, row=row)
            cell.number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1
            
            cell=ws.cell(column=10, row=row)
            cell.number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1

            cell=ws.cell(column=11, row=row)
            cell.number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1

            cell=ws.cell(column=12, row=row)
            cell.number_format = u'#,##0.0000;'

            cell=ws.cell(column=13, row=row)
            cell.number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1

            cell=ws.cell(column=21, row=row)
            cell.alignment = Alignment(horizontal="center", vertical="center")

            cell=ws.cell(column=24, row=row)
            cell.alignment = Alignment(horizontal="center", vertical="center")

        #for col in range(ws.min_column, ws.max_column + 1):
        for col in range(1,26):
            ws.column_dimensions[get_column_letter(col)].auto_size = True        

        wb.save(f"{excel_file_name}")  

        logger.info(f"Excel file has been formatted")
    
    except (Exception) as error:
        logger.warning("Something wrong in appending value to excel:")
        print(error)


if __name__ == '__main__':

    ExcelFileName = "test.xlsx"
    ExcelFileName_FullPath = os.path.dirname(os.path.realpath(__file__)) + "\\" + ExcelFileName

    data = [["col1 row1", "col2 row1","col2 row1"],
            ["col1 row2", "col2 row2","col2 row2"]]

    write_to_excel(data,  ExcelFileName_FullPath)
