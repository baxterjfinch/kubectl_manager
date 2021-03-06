import os
import re
import subprocess, sys

class ApplicationForwarder:

    def __init__(self):
        self._namespace = 'testnet'
        self._pods = []
        self._pods_details = []
        self._chosen_pods = []
        self._forwarded_pods = []
        self._pids = []

    def get_pods(self):
        pods = 'kubectl get pods -n {0}'.format(self._namespace)
        result = subprocess.run(['kubectl', 'get', 'pods', '-n', self._namespace], stdout=subprocess.PIPE)

        x = result.stdout.decode('utf-8').splitlines()
        x.pop(0)

        for pod in x:
            line = re.split('\s+', pod)
            self._pods_details.append(line)
            self._pods.append(line[0])

    def get_pods_details(self):
        print("Pod Details:")

        for pod in self._pods_details:
            print(pod)

    #Unimplemented
    def choose_pods(self):
        print("\nChoose Pods To Forward")
        print("(i.e. 2, 3, 7, 14 -or- all)\n")

        for pod in self._pods:
            print("{0} - {1}".format(self._pods.index(pod), pod))

        self._chosen_pods = input("\n\n>> ")
        self.forward_pods()

    def forward_pods(self):
        if self._chosen_pods == "all" or self._chosen_pods == "All":
            print("\n\nForwarding All Pods...\n\n")
        else:
            print("\n\nForwarding pods: {0}".format(self._chosen_pods))

    def forward_custom_pods(self):
        kib = [s for s in self._pods if 'kibana' in s][0]
        hapi = [s for s in self._pods if 'hyperion-api' in s][0]
        hindexer = [s for s in self._pods if 'hyperion-indexer' in s][0]
        edata = [s for s in self._pods if 'elastic-data' in s][0]

        kf = 'kubectl port-forward {0} -n {1} 5601:5601 &'.format(kib, self._namespace)
        ha = 'kubectl port-forward {0} -n {1} 7770:7777 &'.format(hapi, self._namespace)
        hi = 'kubectl port-forward {0} -n {1} 7771:7777 &'.format(hindexer, self._namespace)
        ed = 'kubectl port-forward {0} -n {1} 8081:8081 &'.format(edata, self._namespace)
        es = 'kubectl port-forward svc/elasticsearch-es-http 9200:9200 &'

        result = subprocess.Popen(ha, shell=True)
        result2 = subprocess.Popen(hi, shell=True)
        result3 = subprocess.Popen(kf, shell=True)
        result4 = subprocess.Popen(ed, shell=True)
        result5 = subprocess.Popen(es, shell=True)

        self._forwarded_pods.append(kib)
        self._forwarded_pods.append(hapi)
        self._forwarded_pods.append(hindexer)
        self._forwarded_pods.append(edata)
        self._forwarded_pods.append('elasticsearch-es-http')

    def list_forwarded_pods(self):
        print("Forwarded Pods Are: {0}".format(self._forwarded_pods))

    def kill_forwarded_pods(self):
        cmds =['lsof -i :5601', 'lsof -i :7770', 'lsof -i :7771', 'lsof -i :8081', 'lsof -i :9200']

        for cmd in cmds:
            result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
            x = result.stdout.decode('utf-8').splitlines()

            if len(x) > 0:
                x.pop(0)
                line = re.split('\s+', x[0])
                subprocess.run('kill -9 {0}'.format(line[1]).split())

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, space):
        self._namespace = space
        print("\nNamespace set to {0}\n".format(self._namespace))
