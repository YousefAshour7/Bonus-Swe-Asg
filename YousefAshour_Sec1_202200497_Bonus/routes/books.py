from flask import Blueprint, request, jsonify
from middleware.auth import authenticate_token

library_bp = Blueprint("books", __name__)

books = []

@library_bp.before_request
def before_request():
    result = authenticate_token()
    if result:
        return result


@library_bp.route("/", methods= ["GET"])
def get_books():
    return jsonify(books)


@library_bp.route("/", methods= ["POST"])
def creat_book():
    book = {
        "title": request.json.get("title"),
        "Author": request.json.get("Author"),
        "Published_Year": request.json.get("Published_Year"),
        "ISBN": request.json.get("ISBN"),
        "Genre": request.json.get("Genre", None)
    }

    if not all([book["title"], book["Author"], book["Published_Year"], book["ISBN"]]):
        return jsonify({"error": "Missing required fields"}), 400

    books.append(book)
    return jsonify(book), 201

@library_bp.route("/<string:ISBN>", methods= ["PUT"])
def update_book(ISBN):
    book = next((i for i in books if i["ISBN"] == ISBN), None)
    if book is None:
        return jsonify({"error": "item not found"}), 404

    book["title"] = request.json.get("title", book["title"])
    book["Author"] = request.json.get("Author", book["Author"])
    book["Published_Year"] = request.json.get("Published_Year", book["Published_Year"])
    book["Genre"] = request.json.get("Genre", book["Genre"])
    return jsonify(book), 200

@library_bp.route("/<string:ISBN>", methods= ["DELETE"])
def delete_book(ISBN):
    global books
    books = [i for i in books if i["ISBN"] != ISBN]
    return '', 204


@library_bp.route("/search", methods=["GET"])
def search_books():
    author = request.args.get("Author", None)
    published_year = request.args.get("Published_Year", None)
    genre = request.args.get("Genre", None)

    filtered_books = books

    if author:
        filtered_books = [i for i in filtered_books if i["Author"].lower() == author.lower()]
    if published_year:
        filtered_books = [i for i in filtered_books if str(i["Published_Year"]) == str(published_year)]
    if genre:
        filtered_books = [i for i in filtered_books if genre.lower() in (i.get("Genre") or "").lower()]

    return jsonify(filtered_books), 200
