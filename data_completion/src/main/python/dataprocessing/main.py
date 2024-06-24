import polars as pl

def data_transaform():
    #extract
    file_path='/home/lindsay/Documents/DEVELOPPEMENT/Python/data_completion/src/main/python/files/Copy of Resorts_Database_Schema_Aligned_5.xlsx'
    output_path='/home/lindsay/Documents/DEVELOPPEMENT/Python/data_completion/src/main/python/outputs/'
    df_res=pl.read_excel(file_path,sheet_name='Resorts').rename({'id':'resort_id','location':'location_id'})
    df_img=pl.read_excel(file_path,sheet_name='Images')
    df_rat=pl.read_excel(file_path,sheet_name='Ratings')
    df_num=pl.read_excel(file_path,sheet_name='Numerics')
    df_gen=pl.read_excel(file_path,sheet_name='Generics')
    df_types=pl.read_excel(file_path,sheet_name='Types')
    df_loc=pl.read_excel(file_path,sheet_name='Locations').rename({'id':'location_id'}).select(['location_id','address','city','continent_id','country','state','continent','state_id'])
    df_coun=pl.read_excel(file_path,sheet_name='Countries').rename({'code':'country_code','name':'country','id':'country_id'})
    df_cont=pl.read_excel(file_path,sheet_name='Continents').rename({'code':'continent_code','name':'continent_name'})
    df_states=pl.read_excel(file_path,sheet_name='States').rename({'id':'state_id','name':'state_name'})
    df_coms=pl.read_excel(file_path,sheet_name='Comments')
    
    #transform
    df_res_loc=df_res.join(df_loc,how='left',on='location_id')
    df_res_loc_states=df_res_loc.join(df_states,how='left',on='state_id')
    df_res_loc_states_cont=df_res_loc_states.join(df_cont,how='left',on='continent_id')
    df_res_loc_states_cont_count=df_res_loc_states_cont.join(df_coun,how='left',on='country')#Location and coordinates data generation
    
    df_coms_grouped=df_coms.group_by(['comment','author']).agg(scores=pl.col('comment').count())#scores for different attributes based on customer reviews
    
    df_res_loc_states_cont_count.write_excel(output_path+'Location_and_coordinates_data_generation.xlsx')
    df_coms_grouped.write_excel(output_path+'scores_based_on_customer_reviews.xlsx')
    
if __name__=="__main__":
    data_transaform()