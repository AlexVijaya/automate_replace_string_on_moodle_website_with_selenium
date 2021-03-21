def drop_duplicates_and_prune_to_200 ():
    import os
    import pandas as pd

    path_to_file="/media/alex/新加卷/OBS_Recordings_T/Data_science/Python/My_python_programs/IOYU/http_to_https"
    dirname=os.path.dirname(path_to_file)
    os.chdir(dirname)

    workbook_location=os.path.join(path_to_file,"http_to_https_results_with_https_sheet.xlsx")
    pd.set_option("display.max_columns",10)
    pd.set_option("display.width",1500)
    pd.set_option ( "max_colwidth" , 500 )
    pd.set_option ( "display.colheader_justify" , "left" )

    results_df=pd.read_excel(workbook_location,sheet_name = "link to page, https, code")
    #print (results_df)
    results_df_with_dropped_duplicates=results_df.drop_duplicates()
    results_df_with_dropped_duplicates_200 = results_df_with_dropped_duplicates[(results_df_with_dropped_duplicates["status_code (200 is good)"]>=200) & (results_df_with_dropped_duplicates["status_code (200 is good)"]<=300)]
    #print("len(results_df_with_dropped_duplicates_200.index)=",len(results_df_with_dropped_duplicates_200.index))
    only_200_df=[]
    for i in range(0,len(results_df_with_dropped_duplicates_200.index)):
        only_200_df.append(results_df_with_dropped_duplicates_200.iloc[i]["on this page a buggy http occurred"])


    results_df_with_dropped_duplicates_200.to_excel(os.path.join(path_to_file, 'https_with_dropped_duplicates.xlsx'), index = False)
    #drop_duplicates ()
    return (only_200_df)