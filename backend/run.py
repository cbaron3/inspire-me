from server import app

if __name__ == "__main__":
    # Need to use false so apscheduler doesnt run jobs twice
    app.run(host='0.0.0.0', port=5000, use_reloader=False)