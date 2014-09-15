if __name__ == '__main__':
    from FlaskBlueprints import app, config
    app.run(port=config.PORT, debug=config.DEBUG)