from flask import Flask, jsonify, request
from flask_cors import CORS
from library import Book, Library

app = Flask(__name__)
CORS(app)

lib = Library()  # loads books.json automatically on startup


@app.route("/", methods=["GET"])
def status():
    return jsonify({"status": "ok", "message": "Library API is running"})


@app.route("/books", methods=["GET"])
def get_books():
    # lib.books is a dict keyed by ISBN — iterate .values()
    return jsonify([book.to_dict() for book in lib.books.values()])


@app.route("/books", methods=["POST"])
def add_book():
    data = request.json or {}
    missing = [f for f in ("title", "author", "isbn") if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    book = Book(
        title=data["title"],
        author=data["author"],
        isbn=data["isbn"],
        pages=int(data.get("pages", 0)),
    )
    try:
        lib.add_book(book)
    except KeyError as e:
        return jsonify({"error": str(e)}), 409  # 409 Conflict

    return jsonify({"message": f"'{book.title}' added"}), 201


@app.route("/books/<path:title>", methods=["DELETE"])
def remove_book(title: str):
    # The frontend deletes by title, so find the ISBN first
    matches = lib.find_book(title)
    if not matches:
        return jsonify({"error": f"'{title}' not found"}), 404

    lib.remove_book(matches[0].isbn)  # remove_book uses ISBN internally
    return jsonify({"message": f"'{title}' removed"})


if __name__ == "__main__":
    app.run(debug=True)