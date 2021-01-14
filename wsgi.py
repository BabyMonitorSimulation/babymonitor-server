from project import app, socketio


if __name__ == "__main__":
    port = 5000
    print(f"BabyMonitor Running in {port}")
    socketio.run(app, port=port)
