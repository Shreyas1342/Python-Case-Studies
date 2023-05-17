"""
@author: Shreyas_Chaudhari
"""
import os
import pandas as pd
import matplotlib.pyplot as plt


def read_file(file_dir = r"C:\Users\Shreyas_Chaudhari\Desktop\Python_assignment\Assignment_2"):
    file_path = os.path.join(file_dir,'movie_meta_data.csv')
    imdb = pd.read_csv(file_path)
    imdb.fillna('unknown',inplace = True)
    return imdb
#Q1
#a-Top/bottom n percentile movies according to metascore

#Filter for movies with specified genre and non-missing metascore & user rating ,top and bottom n movies and percentiles
def metascore_movies(imdb,genre, n):
    
    genre_data = imdb[imdb['genres'].str.contains(genre, na=False)]
    genre_data = genre_data[genre_data['metascore'] != -1]   
    top_n = genre_data['metascore'].quantile(1 - n / 100)
    bottom_n = genre_data['metascore'].quantile(n / 100)    
    top_n_movies = genre_data[genre_data['metascore'] >= top_n].sort_values(by='metascore', ascending=False)[['genres', 'title', 'metascore']]
    bottom_n_movies = genre_data[genre_data['metascore'] <= bottom_n].sort_values(by='metascore', ascending=False)[['genres', 'title', 'metascore']]    
    return top_n_movies, bottom_n_movies
 


#b-Top/bottom n percentile movies according to ‘number of imdb user votes’
def imdb_user_rating_movies(imdb,genre, n):
    
    genre_data = imdb[imdb['genres'].str.contains(genre, na=False)]
    genre_data = genre_data[genre_data['imdb user rating'] != -1]
    top_n = genre_data['imdb user rating'].quantile(1 - n / 100)
    bottom_n = genre_data['imdb user rating'].quantile(n / 100)
    top_n_movies = genre_data[genre_data['imdb user rating'] >= top_n].sort_values(by='imdb user rating', ascending=False)[['genres', 'title', 'imdb user rating']]
    bottom_n_movies = genre_data[genre_data['imdb user rating'] <= bottom_n].sort_values(by='imdb user rating', ascending=False)[['genres', 'title', 'imdb user rating']]
    return top_n_movies, bottom_n_movies




#=======================================================================================================================

#Q2
#Q2Movies who have won an Oscar in a particular year. For example, get the year as a
#parameter to your function and return all the movies that won an Oscar in that year

def get_oscar_winners(imdb,year):
    # Filter the dataframe to include only non-null rows with Oscar wins
    oscar_winners = imdb[(imdb['awards'].notnull()) & (imdb['awards'].str.contains('Oscar'))]
    oscar_winners['oscar_year'] = oscar_winners['awards'].str.extract(r"(?<=Oscar\s)(.*?)(?=\,)")
    oscar_winners['oscar_year'] = oscar_winners['oscar_year'].astype(str)
    # Get the list of movie titles
    year =str(year)
    result = oscar_winners.loc[oscar_winners['oscar_year'] == year,['title','oscar_year']]
    return result


#=======================================================================================================================

#Q3.Anayze and return n movies wit highest lowest budget.

imdb.fillna('unknown',inplace =True)
def sort_movies_using_budget(imdb,n,order = 'Top'):
    unknown_df = imdb['budget'] != 'unknown'
    df = imdb[unknown_df]
    df['currency'] = df['budget'].str.replace('\d+', '').str.replace(',', '').str.replace('[\[\](){}]+', '').str.replace('(estimated)', '').str.replace('$','USD')
    df['budget'] = df['budget'].str.replace(r'\D+', '').astype(int)
    df ['budget_usd'] = False
    exchange_rates = {'USD ':1, 'GBP ':1.37, 'EUR ':1.17, 'CAD ':0.79, 'INR ': 0.014 , 'AUD ': 0.73 , 'FRF ':0.1708, 'HUF ':0.0033, 'DKK ': 0.16, 'CNY ':0.15}
    for index,row in df.iterrows():
        if df.loc[index,'currency'] in exchange_rates.keys():
            df.loc[index,'budget_usd'] = df.loc[index,'budget'] * exchange_rates[row['currency']]
    if order == 'Top':
       return df.sort_values(by = 'budget_usd',ascending = False)[:n]
    elif order == 'Bottom':
       return df.sort_values(by = 'budget_usd')[:n]
    else:
        print('Invalid Input')
        


#=======================================================================================================================

#Q4.which countries have highest number of movies release in each year

# Group the movies by year and country and count the number of movies in each group, explode the countries and sorting.
def get_highest_movie_releases_by_country(imdb,year, n):
    
    movies_by_year_and_country = imdb[['year','title','countries']]   
    movies_by_year_and_country = movies_by_year_and_country.assign(countries= movies_by_year_and_country ["countries"].str.strip().str.split(", ")).explode("countries")  
    movies_by_year_and_country = movies_by_year_and_country[movies_by_year_and_country['year'] == year]
    movies_by_year_and_country  =  movies_by_year_and_country.groupby('countries')['title'].count().reset_index()
    movies_by_year_and_country = movies_by_year_and_country.sort_values(by= 'title', ascending=False)
    highest_movies_by_year = movies_by_year_and_country.head(n)    
    return highest_movies_by_year


#=======================================================================================================================

#Q5 Analyze if there any relationship between the any imdb user rating and number of awards recieved.

# count the number of awards and plot a scatter plot of the two variables
def scatter_plot(imdb):
    imdb['num_awards'] = imdb['awards'].str.count(',') + 1
    plt.scatter(imdb['imdb user rating'], imdb['num_awards'])
    plt.xlabel('IMDb User Rating')
    plt.ylabel('Number of Awards')
    plt.show()
    plt.savefig(r"C:\Users\Shreyas_Chaudhari\Desktop\Python_assignment\Assignment_2\Que5_scatter_plot.jpg")
    corr_coeff = imdb['imdb user rating'].corr(imdb['num_awards'])
    corr_coeff_df = pd.Series(corr_coeff)
    return corr_coeff_df



#=======================================================================================================================

#Q6 Return AKAs of a specified movie in a specified region
#Strip whitespace, split the 'akas' column and take specified movie in akas column to iterate.
def Movie_AKAs(imdb,movie, region):
    imdb['akas'] = imdb['akas'].astype(str).str.strip().str.split(', ')
    movie_data = imdb.loc[imdb['title'] == movie, 'akas']
    akas = []
    for element in movie_data:
        for aka in element:
            if region in aka:
                akas.append(aka.replace(region, '').replace('()', '').replace('\\','').strip())
    if not akas:
        return f"No AKAs found for '{movie}' in '{region}'"
    else:
        return pd.Series(akas)


#=======================================================================================================================

#Q7 Movies released on ,before or after a given year(take year as parameter)
#put conditons on year and flter the it with titles.
def movies_by_release_year(imdb,year, option):
    year_filter = {
        'on': imdb['year'] == year,
        'before': imdb['year'] < year,
        'after': imdb['year'] > year}
    movies_df = imdb.loc[year_filter[option], 'title']
    if movies_df.empty:
        print(f"No movie released {option} {year}.")
    else:
        return movies_df


#=======================================================================================================================

#Q8 Director who has made most number of oscar winning awards.
#Splitting the directors column
#checked awards column for oscar,explode directoes award and groupby directors and take max()
def oscar_winning_director(imdb):
    imdb['directors'] = imdb['directors'].str.split(',')
    oscar_winners = imdb[imdb['awards'].str.contains('Oscar', na=False)]
    oscar_winners_exploded = oscar_winners.explode('directors')
    director_count = oscar_winners_exploded.groupby('directors').size().to_dict()
    most_oscar_winning_director = max(director_count, key=director_count.get)
    print(f"{most_oscar_winning_director} : {director_count[most_oscar_winning_director]}")
    return pd.Series(most_oscar_winning_director)


def main():
    
    imdb = read_file()
    
    folder_path = r"C:\Users\Shreyas_Chaudhari\Desktop\Python_assignment\Assignment_2"
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    #Q1 a.
    top_movies_by_metascore, bottom_movies_by_metascore = metascore_movies(imdb,'Action', 30)
    
    top_movies_by_metascore.to_csv(os.path.join(folder_path,'Que1_a_top.csv'),index = False)
    top_movies_by_metascore.to_json(os.path.join(folder_path,'Que1_a_top.json'),orient='records')
    
    bottom_movies_by_metascore.to_csv(os.path.join(folder_path,'Que1_a_bottom.csv'),index = False)
    bottom_movies_by_metascore.to_json(os.path.join(folder_path,'Que1_a_bottom.json'),orient='records')
    
    #Q1 b.
    top_movies_by_imdb_user_rating, bottom_movies_by_imdb_user_rating = imdb_user_rating_movies(imdb,'Action', 30)
    
    top_movies_by_imdb_user_rating.to_csv(os.path.join(folder_path,'Que1_b_top.csv'),index = False)
    top_movies_by_imdb_user_rating.to_json(os.path.join(folder_path,'Que1_b_top.json'),orient='records')

    
    bottom_movies_by_imdb_user_rating.to_csv(os.path.join(folder_path,'Que1_b_bottom.csv'),index = False)
    bottom_movies_by_imdb_user_rating.to_json(os.path.join(folder_path,'Que1_b_bottom.json'),orient='records')
    
    #Q2   
    oscar_winners = get_oscar_winners(imdb,1979)
    oscar_winners.to_csv(os.path.join(folder_path,'Que2.csv'),index = False)
    oscar_winners.to_json(os.path.join(folder_path,'Que2.json'),orient='records')
    
    #Q3
    sorted_movies_by_budget = sort_movies_using_budget(imdb,10,'Top')
    sorted_movies_by_budget .to_csv(os.path.join(folder_path,'Que3.csv'),index = False)
    sorted_movies_by_budget .to_json(os.path.join(folder_path,'Que3.json'),orient='records')
    
    #Q4
    highest_movies_by_year = get_highest_movie_releases_by_country(imdb,2001,5)
    highest_movies_by_year.to_csv(os.path.join(folder_path,'Que4.csv'),index = False)  
    highest_movies_by_year.to_json(os.path.join(folder_path,'Que4.json'),orient='records') 
        
    #Q5
    coeff = scatter_plot(imdb)
    coeff.to_csv(os.path.join(folder_path,'Que5.csv'),index = False)      
    coeff.to_json(os.path.join(folder_path,'Que5.json'),orient='records') 
       
    #Q6
    akas= Movie_AKAs(imdb,'Body Bags', 'United States')
    akas.to_csv(os.path.join(folder_path,'Que6.csv'),index = False)
    akas.to_json(os.path.join(folder_path,'Que6.json'),orient='records')
    
    #Q7
    movies_release=movies_by_release_year(imdb,2020, 'after')
    movies_release.to_csv(os.path.join(folder_path,'Que7.csv'),index = False)
    movies_release.to_json(os.path.join(folder_path,'Que7.json'),orient='records')
    
    #Q8
    Most_oscar= oscar_winning_director(imdb)
    Most_oscar.to_csv(os.path.join(folder_path,'Que8.csv'),index = False)
    Most_oscar.to_json(os.path.join(folder_path,'Que8.json'),orient='records')



if __name__ == '__main__':
    main()
