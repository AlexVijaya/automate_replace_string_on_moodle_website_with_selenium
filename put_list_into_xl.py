def put_list_into_xl_func(inner_list_of_tuple_of_link_and_code,path_to_file):

    import openpyxl
    import os
    from openpyxl import Workbook
    os.chdir(path_to_file)
    #print ( path_to_file )
    #print ( os.path.join ( path_to_file , 'http_to_https_results.xlsx' ) )
    # print('/media/alex/新加卷/OBS_Recordings_T/Data_science/Python/My_python_programs/IOYU/http_to_https')
    if os.path.exists ( os.path.join ( path_to_file , 'http_to_https_results.xlsx' ) ):
        print ( 'file http_to_https_results.xlsx already exists' )
        wb = openpyxl.load_workbook ( os.path.join ( path_to_file , 'http_to_https_results.xlsx' ) )
        ws = wb.active

    else:
        print ( 'file http_to_https_results.xlsx does not exist. I am gonna create it' )
        wb = Workbook ()
        ws = wb.active
        wb.save ( filename = 'http_to_https_results.xlsx' )


    for row_counter , row_value in enumerate ( inner_list_of_tuple_of_link_and_code ):
        for column_counter , cell_value in enumerate ( inner_list_of_tuple_of_link_and_code[row_counter] ):
            # print (inner_list_of_tuple_of_link_and_code[row_counter][column_counter])
            ws.cell ( row = row_counter + 1 , column = column_counter + 1 ).value =\
                inner_list_of_tuple_of_link_and_code[row_counter][column_counter]
            # time.sleep (1)
    wb.save ( filename = 'http_to_https_results.xlsx' )

