from app import create_app # This looks for 'create_app' in app/__init__.py

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)