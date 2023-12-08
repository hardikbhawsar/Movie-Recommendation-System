import csv
from pyswip import Prolog

def create_prolog_facts(csv_path, prolog_path):
    facts = []
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if all(row.values()):
                fact = 'film("{}","{}","{}",{},"{}",{},{},"{}","{}","{}","{}",{},{}, "{}",{}).'.format(
                    row['name'], row['rating'], row['genre'], row['year'], row['released'],
                    row['score'], row['votes'], row['director'], row['writer'], row['star'],
                    row['country'], row['budget'], row['gross'], row['company'], row['runtime']
                )
                facts.append(fact)
    
    with open(prolog_path, 'w', encoding='utf-8') as prolog_file:
        for fact in facts:
            prolog_file.write(fact + '\n')

def consult_prolog_file(prolog, dataset_file_path):
    prolog.consult(dataset_file_path)

def execute_query(prolog, query):
    query_result = list(prolog.query(query))
    print("--------------------------------------------------")
    return query_result

def print_query_result(query_result, key_name):
    print("Query Result:")
    for result in query_result:
        value = result[key_name].decode('utf-8') if isinstance(result[key_name], bytes) else result[key_name]
        print(f"{value}")
    print("--------------------------------------------------")


# Define paths
csv_file_path = "Dataset/dataset.csv"
prolog_file_path = "Dataset/dataset.pl"
dataset_file_path = "Dataset/dataset.pl"

# Create Prolog facts and write to the dataset1.pl file
create_prolog_facts(csv_file_path, prolog_file_path)
print("Prolog facts have been written to dataset1.pl.")

# Initialize Prolog
prolog = Prolog()

# Consult the Prolog file to load the facts
consult_prolog_file(prolog, dataset_file_path)

# User menu loop
while True:
    # User menu
    print("\nChoose an option:")
    print("1. Filter movies by genre")
    print("2. Filter movies by IMDb rating")
    print("3. Filter movies for pet")
    print("4. Filter top 10 rated movies of a particular genre")
    print("5. Filter movies of an Actor/Actress")
    print("6. Filter movies of a director")
    print("7. Filter movies of a country")
    print("8. Filter movies for runtime")
    print("9. Filter movies depending on age")
    print("10. Filter movies depending on your mood")
    print("11. Filter top 10 IMDb movies similar to the given movie")
    print("12. Filter top 10 hit movies depending on their gross income")
    print("0. Exit")
    print("--------------------------------------------------")
    
    user_choice = input("Enter your choice : ")
    print("--------------------------------------------------")

    if user_choice == "1":
        # Query for user-defined genre
        print("Genre: Comedy, Action, Biography, Drama, Horror, Animation, Adventure, Biography, Crime, Pet, Mystery")
        user_genre = input("Enter the genre to search: ")
        genre_query = 'film(X, _, "{}", _, _, _, _, _, _, _, _, _, _, _, _)'.format(user_genre)
        print(f"Executing genre query: {genre_query}")
        genre_result = execute_query(prolog, genre_query)
        print_query_result(genre_result, 'X')

    elif user_choice == "2":
        # Query for movies with IMDb rating > user-defined rating
        user_imdb_rating = float(input("Enter the IMDb rating to search (e.g., 8.0): "))
        rating_query = 'film(X, _, _, _, _, Score, _, _, _, _, _, _, _, _, _), Score > {}.'.format(user_imdb_rating)
        print(f"Executing rating query: {rating_query}")
        rating_result = execute_query(prolog, rating_query)
        print_query_result(rating_result, 'X')

    elif user_choice == "3":
        # Query for movies with the genre "Pet"
        pet_query = 'film(X, _, "Pet", _, _, _, _, _, _, _, _, _, _, _, _)'
        print(f"Executing genre query for 'Pet' movies: {pet_query}")
        pet_result = execute_query(prolog, pet_query)
        print_query_result(pet_result, 'X')

    elif user_choice == "4":
        # Query for user-defined genre
        print("Genre: Comedy, Action, Biography, Drama, Horror, Animation, Adventure, Biography, Crime, Pet, Mystery")
        user_genre1 = input("Enter the genre to search top 10 imdb movies: ")
        top10_genre_query = 'film(X, _, "{}", _, _, Y, _, _, _, _, _, _, _, _, _)'.format(user_genre1)
        print(f"Executing genre query: {top10_genre_query}")
        top10_genre_result = execute_query(prolog, top10_genre_query)
        # print_query_result(genre_result, 'X')
        sorted_results = sorted(top10_genre_result, key=lambda x: x['Y'], reverse=True)
        # Take the top 10 results
        top_10 = sorted_results[:10]
        # Print 'X' values of the top 10 'Y' values
        print("Top 10 Movies:")
        for entry in top_10:
            movie_name = entry['X'].decode('utf-8') if isinstance(entry['X'], bytes) else entry['X']
            print(f"{movie_name} - {entry['Y']}")
        print("--------------------------------------------------")
        
    if user_choice == "5":
        # Query for user-defined genre
        actor = input("Enter the name of Actor/Actress: ")
        actor_query = 'film(X, _, _, _, _, _, _, _, _, "{}", _, _, _, _, _)'.format(actor)
        print(f"Executing genre query: {actor_query}")
        actor_result = execute_query(prolog, actor_query)
        print_query_result(actor_result, 'X')

    if user_choice == "6":
        # Query for user-defined genre
        director = input("Enter the name of Director: ")
        director_query = 'film(X, _, _, _, _, _, _, "{}", _, _, _, _, _, _, _)'.format(director)
        print(f"Executing genre query: {director_query}")
        director_result = execute_query(prolog, director_query)
        print_query_result(director_result, 'X')

    if user_choice == "7":
        # Query for user-defined genre
        region = input("Enter the region: ")
        region_query = 'film(X, _, _, _, _, _, _, _, _, _, "{}", _, _, _, _)'.format(region)
        print(f"Executing genre query: {region_query}")
        region_result = execute_query(prolog, region_query)
        print_query_result(region_result, 'X')

    elif user_choice == "8":
        # Query for movies with runtime in a user-defined range
        user_min_runtime = int(input("Enter the minimum runtime (in minutes): "))
        user_max_runtime = int(input("Enter the maximum runtime (in minutes): "))
        runtime_query = 'film(X, _, _, _, _, _, _, _, _, _, _, _, _, _, Runtime), {} =< Runtime, Runtime =< {}.'.format(user_min_runtime, user_max_runtime)
        print(f"Executing runtime query: {runtime_query}")
        runtime_result = execute_query(prolog, runtime_query)
        print_query_result(runtime_result, 'X')

    elif user_choice == "9":
        # Input: user's age
        user_age = int(input("Enter your age: "))
        # Classify appropriate movie certificate based on age
        if user_age < 13:
            user_certificate = 'G'
        elif user_age < 17:
            user_certificate = 'PG-13'
        elif user_age < 18:
            user_certificate = 'R'

        # Query for movies based on determined certificate
        certificate_query = 'film(X, "{}", _, _, _, _, _, _, _, _, _, _, _, _, _).'.format(user_certificate)
        print(f"Executing certificate query: {certificate_query}")
        certificate_result = execute_query(prolog, certificate_query)
        print_query_result(certificate_result, 'X')

    elif user_choice == "10":
        #Input: User's mood
        user_mood = input("Enter your mood (happy/sad): ").lower()
        # Query movies based on user's mood
        if user_mood == "happy":
            mood_query = 'film(X, _, _, _, _, Y, _, _, _, _, _, _, _, _, _), member(Genre, ["Action", "Adventure"]), film(X, _, Genre, _, _, Y, _, _, _, _, _, _, _, _, _).'
        elif user_mood == "sad":
            mood_query = 'film(X, _, "Comedy", _, _, Y, _, _, _, _, _, _, _, _, _).'
        else:
            print("Invalid mood. Please enter 'happy' or 'sad'.")
            continue 
        print(f"Executing mood query: {mood_query}")
        mood_result = execute_query(prolog, mood_query)   
        mood_sorted_results = sorted(mood_result, key=lambda x: x['Y'], reverse=True)
        top_10_mood = mood_sorted_results[:10]
        # Print movie's name of the top 10 imdb values
        print("Top 10 Movies:")
        for entry in top_10_mood:
            movie_name_mood = entry['X'].decode('utf-8') if isinstance(entry['X'], bytes) else entry['X']
            print(f"{movie_name_mood} - {entry['Y']}")

    elif user_choice == "11":
        # Filter top 10 IMDb movies of the same genre and country as a given movie
        user_movie_name = input("Enter the name of the movie: ")

        # Query to get the genre and country of the given movie
        movie_info_query = 'film("{}", _, Genre, _, _, _, _, _, _, _, Country, _, _, _, _).'.format(user_movie_name)
        movie_info_result = execute_query(prolog, movie_info_query)

        if not movie_info_result:
            print(f"Movie '{user_movie_name}' not found.")
            continue

        genre = movie_info_result[0]['Genre'].decode('utf-8')
        country = movie_info_result[0]['Country'].decode('utf-8')

        # Query top 10 IMDb movies of the same genre and country
        top_movies_query = 'film(X, _, "{}", _, _, Score, _, _, _, _, "{}", _, _, _, _), Score > 7.0.'.format(genre, country)
        print(f"Executing top movies query: {top_movies_query}")
        top_movies_result = execute_query(prolog, top_movies_query)
        print_query_result(top_movies_result[:10], 'X')

    elif user_choice == "12":
        # Filter top 10 grossing movies
        top_grossing_query = 'film(X, _, _, _, _, _, _, _, _, _, _, _, Gross, _, _)'
        print(f"Executing top grossing query: {top_grossing_query}")
        top_grossing_result = execute_query(prolog, top_grossing_query)
        print_query_result(top_grossing_result, 'X')

        gross_sorted_results = sorted(top_grossing_result, key=lambda x: x['Gross'], reverse=True)
        top_10_gross = gross_sorted_results[:10]
        # Print movie name of the top 10 gross values
        print("Top 10 Movies:")
        for entry in top_10_gross:
            movie_name = entry['X'].decode('utf-8') if isinstance(entry['X'], bytes) else entry['X']
            print(f"{movie_name} - Gross Income: $ {entry['Gross']}")
        print("--------------------------------------------------")

    elif user_choice == "0":
        print("Exiting the program. Goodbye!")
        break

