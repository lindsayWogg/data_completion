import polars as pl
from geoloc import get_geoloc_geopy,get_geoloc_opencagedata
from image_search import search_pixabay_images




def transform():
    file_path='/home/lindsay/Documents/DEVELOPPEMENT/Python/data_completion/src/main/python/files/sample-data-for-data-scrapping.xlsx'
    df=pl.read_excel(file_path,sheet_name='Resort Data')
    print(df)
    df_geoloc=pl.DataFrame()
    for row in df.iter_rows(named=True):
        print(f"country: {row['country']}, state_province: {row['state_province']}")
        if get_geoloc_geopy(f"{row['Title']}"):
            coords=get_geoloc_geopy(f"{row['Title']}")
        else:
            coords = get_geoloc_opencagedata(row['country'], row['state_province'])
        
        
        links=str(', '.join(map(str, search_pixabay_images(f"{row['country']} {row['state_province']}")))).replace(',', '\n')
        print(coords)
        df_temp=pl.DataFrame({'Title':row['Title'],'country':row['country'],'state_province':row['state_province'],'Zip':coords[2],'URL':links,'Latitude':str(coords[0]),'Longitude':str(coords[1])}).with_columns(Zip=pl.col('Zip').cast(str))
        print(df_temp)
        df_geoloc=pl.concat([df_geoloc,df_temp])
        print(df_geoloc)
    df_source=df.select(['Title','country','state_province','location','location_2','altitute','altotute_from','altitite_to','aski_area','no_of_lifts','continent','star_rating','Ski_Resort_ID'])
    df_final=df_source.join(df_geoloc,how='left',on=['Title','country','state_province',])
    df_final.write_excel('/home/lindsay/Documents/DEVELOPPEMENT/Python/data_completion/src/main/python/outputs/Data_completed.xlsx')
if __name__=="__main__":
    transform()