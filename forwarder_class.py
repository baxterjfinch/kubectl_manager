import os
import re
import subprocess, sys

class ApplicationForwarder:

    def __init__(self):
        self.namespace = 'testnet'
        self.pods = []
        self.pods_details = []
        self.chosen_pods = []
        self.forwarded_pods = []
        self.pids = []

    def get_pods(self):
        pods = 'kubectl get pods -n {0}'.format(self.namespace)
        result = subprocess.run(['kubectl', 'get', 'pods', '-n', self.namespace], stdout=subprocess.PIPE)
        x = result.stdout.decode('utf-8').splitlines()
        x.pop(0)

        for pod in x:
            line = re.split('\s+', pod)
            self.pods_details.append(line)
            self.pods.append(line[0])

        # print("Active Pods: {0}".format(self.pods))
        # print("Details: {0}".format(self.pods_details))

    def get_pods_details(self):
        print("Pod Details:")

        for pod in self.pods_details:
            print(pod)

    def choose_pods(self):
        print("\nChoose Pods To Forward")
        print("(i.e. 2, 3, 7, 14 -or- all)\n")

        for pod in self.pods:
            print("{0} - {1}".format(self.pods.index(pod), pod))

        self.chosen_pods = input("\n\n>> ")
        self.forward_pods()

    def forward_pods(self):

        if self.chosen_pods == "all" or self.chosen_pods == "All":
            print("\n\nForwarding All Pods...\n\n")
        else:
            print("\n\nForwarding pods: {0}".format(self.chosen_pods))

    def forward_custom_pods(self):
        kib = [s for s in self.pods if 'kibana' in s][0]
        hapi = [s for s in self.pods if 'hyperion-api' in s][0]
        hindexer = [s for s in self.pods if 'hyperion-indexer' in s][0]

        kf = 'kubectl port-forward {0} -n {1} 5601:5601 &'.format(kib, self.namespace)
        ha = 'kubectl port-forward {0} -n {1} 7770:7777 &'.format(hapi, self.namespace)
        hi = 'kubectl port-forward {0} -n {1} 7771:7777 &'.format(hindexer, self.namespace)

        result = subprocess.Popen(ha, shell=True)
        result2 = subprocess.Popen(hi, shell=True)
        result3 = subprocess.Popen(kf, shell=True)

        self.forwarded_pods.append(kib)
        self.forwarded_pods.append(hapi)
        self.forwarded_pods.append(hindexer)

    def list_forwarded_pods(self):
        print("Forwarded Pods Are: {0}".format(self.forwarded_pods))

    def kill_forwarded_pods(self):
        cmds =['lsof -i :5601', 'lsof -i :7770', 'lsof -i :7771']

        for cmd in cmds:
            result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
            x = result.stdout.decode('utf-8').splitlines()
            if len(x) > 0:
                x.pop(0)
                line = re.split('\s+', x[0])
                subprocess.run('kill -9 {0}'.format(line[1]).split())

    def set_namespace(self):
        namespace = input("\nEnter namespace >> ")
        self.namespace = namespace
        print("\nNamespace set to {0}\n".format(self.namespace))

    def get_namespace(self):
        print("\nNamespace set to {0}\n".format(self.namespace))
