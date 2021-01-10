from project import app, socketio


if __name__ == "__main__":
    print("BabyMonitor Running")
    socketio.run(app, port=5000)
