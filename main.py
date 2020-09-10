from forwarder_class import ApplicationForwarder
from platform_requester import PlatformRequester

app = ApplicationForwarder()
app.get_pods()

plat = PlatformRequester()
plat.access_token = ""

def main(app, plat):
    action = input("start, stop, list, forwarded, set_namespace, get_namespace, help >> ")

    if action == "start":
        app.forward_custom_pods()
        main(app, plat)

    elif action == "stop":
        app.kill_forwarded_pods()
        main(app, plat)

    elif action == "list" or action == "l":
        app.get_pods_details()
        main(app, plat)

    elif action == "forwarded" or action == "f":
        app.list_forwarded_pods()
        main(app, plat)

    elif action == "get_namespace" or action == "getn":
        print(app.namespace)
        main(app, plat)

    elif action == "set_namespace"or action == "setn":
        namespace = input("\nEnter namespace >> ")
        app.namespace = namespace
        main(app, plat)

    elif action == "help" or action == "h":
        print("Help me")
        main(app, plat)

    else:
        main(app, plat)

if __name__ == "__main__":
    main(app, plat)
