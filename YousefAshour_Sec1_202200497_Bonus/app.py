from flask import Flask, jsonify
from routes.books import library_bp
from flasgger import Swagger

app = Flask(__name__)

app.register_blueprint(library_bp, url_prefix= "/books")

swagger = Swagger(app, template_file="LMS.yaml")

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "resource not found"}), 404

@app.route("/api-docs")
def api_docs():
    return jsonify({"message": "Swagger documentation is available at /apidocs"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)