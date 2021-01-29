from app_pack import app

application = app

if __name__ == "__main__":
    #application.debug = True
    port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0', port=port)
