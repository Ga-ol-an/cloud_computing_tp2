from flask import Flask, request, jsonify
import pickle
import os


app = Flask(__name__)

# Note that the path to the file ("/path/to/model.pickle" in the example above) will need to be adjusted depending on whether your
# Flask front-end is running directly on the VM, inside the container, or using the Kubernetes shared volume (see below).
# app.model = pickle.load(open("/result/rules.pickle", "rb"))


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/recommend", methods=["POST"])
def recommend():
    VERSION = os.environ.get("VERSION", "1.0")
    NB_RECOMENDATION_SONGS = int(os.environ.get("NB_RECOMENDATION_SONGS", 3))
    
    input = request.get_json(force=True, silent=False)
    user_songs = input.get("songs", [])

    if user_songs is None or len(user_songs) == 0:
        return jsonify({'error': 'No songs provided.'}), 400

    with open("data/rules.pickle", "rb") as file:
        file_content = pickle.load(file)

    rules = file_content.get("rules", [])
    model_date = file_content.get("model_date", "unknown")

    possible_recommendations = []
    for antecedent, consequent, confidence in rules:
        if set(antecedent).issubset(set(user_songs)):
            for song in consequent:
              # If the song is not already in user's songs
                if song not in user_songs:
                    # If the song is already in possible recommendations
                    if song in [s for s, _ in possible_recommendations]:
                        # Update confidence if higher
                        for i in range(len(possible_recommendations)):
                            if possible_recommendations[i][0] == song and confidence > possible_recommendations[i][1]:
                                possible_recommendations[i] = (song, confidence)
                    else:
                      possible_recommendations.append((song, confidence))

    # print(possible_recommendations)

    #! Criar um if pra deixar a função recursiva, caso queira mais musicas recomendadas??

    # Filtrar as recomendações para as N mais confiantes
    recommendations = sorted(
        possible_recommendations,
        key=lambda x: x[1],
        reverse=True
    )[:NB_RECOMENDATION_SONGS]

    recommended_songs = [song for song, _ in recommendations]

    return jsonify({'songs': recommended_songs, 'version': VERSION, 'model_date': model_date})

if __name__ == '__main__':
    app.run()