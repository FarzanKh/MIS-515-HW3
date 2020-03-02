# Movie Analytics    Farzan Khoobchehr     March 01, 2020
# OMDB API Key information:
# Here is your key: 7e722195
# Please append it to all of your API requests,
# OMDb API: http://www.omdbapi.com/?i=tt3896198&apikey=7e722195
import requests
import json
import xmltodict
import textblob
import matplotlib.pyplot as plt
import skimage.io
# import WordCloud

# DEFINING FUNCTIONS
def get_poster():
    movie_poster_url = omdb_data["root"]["movie"]["@poster"]
    movie_poster = skimage.io.imread(movie_poster_url)
    plt.imshow(movie_poster, interpolation = "bilinear")
    plt.axis("off")
    plt.show()


def get_background():
    print()
    movie_year = omdb_data["root"]["movie"]["@year"]
    movie_rated = omdb_data["root"]["movie"]["@rated"]
    movie_runtime = omdb_data["root"]["movie"]["@runtime"]
    movie_genre = omdb_data["root"]["movie"]["@genre"]
    movie_actors = omdb_data["root"]["movie"]["@actors"]
    movie_plot = omdb_data["root"]["movie"]["@plot"]
    print("Year:",movie_year)
    print("Rating:",movie_rated)
    print("Runtime:",movie_runtime)
    print("Genre:",movie_genre)
    print("Actors:",movie_actors)
    print("Plot:",movie_plot)
    print()


def get_reception():
    print()
    movie_awards = omdb_data["root"]["movie"]["@awards"]
    movie_metascore = omdb_data["root"]["movie"]["@metascore"]
    movie_imdb_rating = omdb_data["root"]["movie"]["@imdbRating"]
    print("Awards:",movie_awards)
    print("Metascore:",movie_metascore)
    print("IMDB Rating:",movie_imdb_rating)
    print()
    
    
def get_sentiment():
    response_2 = requests.get(imdb_url)
    if response_2:
        imdb_data = json.loads(response_2.text)   # parsing to json
        review_list = []  # creating a list to put all the review texts in it
        for line in imdb_data:                               
            review_list.append(line["Review text"])  #putting only the review texts into the list and exlude dates and number of stars
        review_string = ''.join(review_list)  # creating a variable to convert review_list to string - TextxBlob only accepts string.
        blob = textblob.TextBlob(review_string)  # creating a blob object from all the review text strings
        polarity_list = []
        subjectivity_list = []
        for sentence in blob.sentences:
            polarity_list.append(sentence.polarity)
            subjectivity_list.append(sentence.subjectivity)
        print()
        print("Average IMDb review polarity:",sum(polarity_list)/len(polarity_list))
        print("Average IMDb review subjectivity:",sum(subjectivity_list)/len(subjectivity_list))
        print()
    else:
        print("Sorry, the tool could not successfully load any IMDb reviews for this movie. Please try another analysis or movie.")

# def get_wordcloud():
#     response_2 = requests.get(imdb_url)
#     if response_2:
#         imdb_data = json.loads(response_2.text)
#     else:
#         print("Sorry, the tool could not successfully load any IMDb reviews for this movie. Please try another analysis or movie.")

print("Welcome to the movie analytics tool!")
repeat_blob = textblob.TextBlob("yes")
while repeat_blob.correct().lower() == "yes":
    try:
        movie_name = input("What movie would you like to analyze? ")
        omdb_url = "https://www.omdbapi.com/?r=xml&apikey=7e722195&t="+movie_name
        imdb_url = "https://dgoldberg.sdsu.edu/515/imdb/"+movie_name.lower()+".json"
        response_1 = requests.get(omdb_url)
        if response_1:
            omdb_data = xmltodict.parse(response_1.text)
            check_true = omdb_data["root"]["@response"]
            if check_true == "True":
                further_analyze_blob = textblob.TextBlob("yes")
                while further_analyze_blob.correct().lower() == "yes":
                    analysis_type_blob = textblob.TextBlob(input("What would you like to see \n (background/reception/poster/wordcloud/sentiment)? "))
                    if analysis_type_blob.correct().lower() == "background":
                        get_background()

                    elif analysis_type_blob.correct().lower() == "reception":
                        get_reception()
                    elif analysis_type_blob.correct().lower() == "poster":
                        get_poster()
#                     elif analysis_type_blob.correct().lower() == "wordcloud":
                        
                    elif analysis_type_blob.correct().lower() == "sentiment":
                        get_sentiment()
                    else:
                        print("Sorry, that analysis is not supported. Please try again.")
                    further_analyze_blob = textblob.TextBlob(input("Would you like to further analyze this movie(yes/no)? "))
            else:
                print("Sorry, we couldn't find information for this movie on OMDB")
        else:
            print("Sorry, we couldn't connect to the API")
    except:
        print("Sorry, we're having an issue. Please try again")
    repeat_blob = textblob.TextBlob(input("Would you like to analyze another movie(yes/no)? "))
    
    
    



