from forwarder_class import ApplicationForwarder

app = ApplicationForwarder()
app.get_pods()

def main(app):
    action = input("start, stop, list, forwarded, set_namespace, get_namespace, help >> ")

    if action == "start":
        app.forward_custom_pods()
        main(app)
    elif action == "stop":
        app.kill_forwarded_pods()
        main(app)
    elif action == "list" or action == "l":
        app.get_pods_details()
        main(app)
    elif action == "forwarded" or action == "f":
        app.list_forwarded_pods()
        main(app)
    elif action == "get_namespace" or action == "getn":
        app.get_namespace()
        main(app)
    elif action == "set_namespace"or action == "setn":
        app.set_namespace()
        main(app)
    elif action == "help" or action == "h":
        print("Help me")
        main(app)
    else:
        main(app)
    # os.system("echo Hello from the other side!")

if __name__ == "__main__":
    main(app)
