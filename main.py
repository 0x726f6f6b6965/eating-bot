import app

if __name__ == "__main__":
    a = app.create_app()
    a.run(port=5002,debug=True)