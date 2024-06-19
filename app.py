from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TMDB_API_KEY = '5a0316d325fa79bd1595723c01abbad7'

@app.route('/recommend', methods=['GET'])
def recommend():
    movie_name = request.args.get('movie')
    if not movie_name:
        return jsonify({'error': 'Please provide a movie name'}), 400

    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}'
    search_response = requests.get(search_url)
    search_data = search_response.json()

    if not search_data['results']:
        return jsonify({'error': 'Movie not found'}), 404

    movie_id = search_data['results'][0]['id']
    recommendations_url = f'https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}'
    recommendations_response = requests.get(recommendations_url)
    recommendations_data = recommendations_response.json()

    recommendations = []
    for movie in recommendations_data['results']:
        recommendations.append({
            'title': movie['title'],
            'overview': movie['overview'],
            'release_date': movie['release_date']
        })

    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
