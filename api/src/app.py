import cs348_api

if __name__ == "__main__":
    app = cs348_api.app.create_app()
    app.run(host = '0.0.0.0', debug=True, port = 6608)
