from forwarder_class import ApplicationForwarder

app = ApplicationForwarder()
app.get_pods()
app.get_pods_details()

def main(app):
    action = input("start, stop, list, help >> ")

    if action == "start":
        app.forward_custom_pods()
        main(app)
    elif action == "stop":
        app.kill_forwarded_pods()
        main(app)
    elif action == "list":
        app.list_forwarded_pods()
        main(app)
    elif action == "help":
        print("Help me")
        main(app)
    else:
        main(app)
    # os.system("echo Hello from the other side!")

if __name__ == "__main__":
    main(app)
