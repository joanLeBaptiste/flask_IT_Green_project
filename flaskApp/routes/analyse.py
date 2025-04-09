from flask import Blueprint, render_template, request

bp = Blueprint('analyse', __name__, url_prefix='/analyse')

MODELS = {
    'GPT-3.5': 0.35,
    'GPT-4': 1.2,
    'Stable Diffusion': 2.5,
    'Claude': 0.8,
    'Mistral': 0.6
}

TYPES = {
    'Texte': 1,
    'Image': 5,
    'Vidéo': 20
}

@bp.route('/', methods=['GET', 'POST'])
def analyse():
    result = None
    if request.method == 'POST':
        modele = request.form.get('modele')
        requete = request.form.get('type_requete')
        quantite = int(request.form.get('quantite', 0))

        emission = MODELS.get(modele, 0) * TYPES.get(requete, 0) * quantite
        result = round(emission, 2)

    return render_template('analyse.html', result=result, models=MODELS.keys(), types=TYPES.keys())
