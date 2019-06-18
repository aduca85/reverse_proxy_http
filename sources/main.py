import server
import yaml
import cProfile

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


if __name__ == '__main__':
    #cProfile.run('main()')
    main()