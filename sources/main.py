import server
import yaml
import cProfile
import os

def read_config(config_file):
    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
    return cfg

def main():
    config_file = 'config.yaml'
    cfg = read_config(config_file)
    server_address = (cfg['proxy']['listen']['address'], int(cfg['proxy']['listen']['port']))
    upstream_addresses = []
    for service in cfg['proxy']['services']:
        for key, value in service.items():
            if key == 'hosts':
                upstreams = value
            elif key == 'strategy':
                load_balancer_strategy = value
    for upstream in upstreams:
        addr = (upstream['address'], int(upstream['port']))
        upstream_addresses.append(addr)

    service = server.Server()
    service.run(server_address, upstream_addresses, load_balancer_strategy)

def main_k8s():
    server_address = (os.environ['SERVER_ADDRESS'], int(os.environ['SERVER_PORT']))
    load_balancer_strategy = os.environ['LOAD_BALANCER_STRATEGY']
    upstream_one_address = (os.environ['UPSTREAM_ONE_ADDRESS'], int(os.environ['UPSTREAM_ONE_PORT']))
    upstream_two_address = (os.environ['UPSTREAM_TWO_ADDRESS'], int(os.environ['UPSTREAM_TWO_PORT']))
    upstream_addresses = [upstream_one_address, upstream_two_address]

    service = server.Server()
    service.run(server_address, upstream_addresses, load_balancer_strategy)


if __name__ == '__main__':
    if os.environ['K8S'] == 'true':
        main_k8s()
    else:
        main()
    #cProfile.run('main()')

    