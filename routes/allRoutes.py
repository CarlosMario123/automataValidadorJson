from routes.autoJsonRoute import autoMataJson
from routes.indexRoute import indexRoute
def instanceRoute(app):
    app.register_blueprint(indexRoute)
    app.register_blueprint(autoMataJson)
