from bs4 import BeautifulSoup as soup
import requests
import re
import pandas as pd


top_100_url = 'https://www.imdb.com/list/ls009668704/'

page = requests.get(top_100_url)
html = soup(page.content, 'html')

films = html.findAll("div",{"class":"lister-item mode-detail"})

Movie_Names = []
Descriptions = []
Release_Dates = []
Director_Names = []
Ratings = []
Durations = []
Actors_list = []
Filming_Dates = []

movie_codes = []

for film in films :

    Movie_name = film.find("h3",{"class":"lister-item-header"}).a.text
    Description = film.find("p",{"class":""}).text.strip()
    # Could be fetched from the movie page
    Release_Date = film.find("span",class_="lister-item-year text-muted unbold").text.replace("(","").replace(")","")
    try:
        Director_Name = film(text=re.compile(r'Director:'))[0].find_next().text
    except:
        Director_Name = film(text=re.compile(r'Directors:'))[0].find_next().text

    Rating = film.find("span",class_ = "ipl-rating-star__rating").text
    Duration = film.find("span",class_="runtime").text
    Actors = []
    Actors.append(film(text=re.compile(r'Stars:'))[0].find_next().text)
    Actors.append(film(text=re.compile(r'Stars:'))[0].find_next().find_next().text)
    Actors.append(film(text=re.compile(r'Stars:'))[0].find_next().find_next().find_next().text)
    Actors.append(film(text=re.compile(r'Stars:'))[0].find_next().find_next().find_next().find_next().text)
    movie_code = film.a['href'][7:-1]

    Movie_Names.append(Movie_name)
    Descriptions.append(Description)
    Release_Dates.append(Release_Date)
    Director_Names.append(Director_Name)
    Ratings.append(Rating)
    Durations.append(Duration)
    Actors_list.append(Actors)
    movie_codes.append(movie_code)

for movie_code in movie_codes:
    url = "https://www.imdb.com/title/" + movie_code + "/locations?ref_=ttfc_ql_5"
    page_movie = requests.get(url)
    html1 = soup(page_movie.content, 'html')
    try:
        filming_dates = html1.find("section",{"id":"filming_dates"}).find("li",class_="ipl-zebra-list__item").text.strip()
    except:
        filming_dates = "N/A"
    Filming_Dates.append(filming_dates)

data = {
    'Movie_Names' : Movie_Names,
    'Descriptions': Descriptions,
    'Release_Dates' : Release_Dates,
    'Director_Names': Director_Names,
    'Ratings' : Ratings,
    'Durations' : Durations,
    'Actors_list' : Actors_list,
    'Filming_Dates' : Filming_Dates,
}

labels = list(range(1,101))

df = pd.DataFrame(data,labels)


