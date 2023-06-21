import cs348_api

app = cs348_api.create_app()

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True, port = 6608)
