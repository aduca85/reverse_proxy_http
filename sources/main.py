import server
import yaml

def read_config(config_file):
    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
    return cfg

if __name__ == '__main__':
    config_file = 'config.yaml'
    cfg = read_config(config_file)
    server_address = (cfg['server']['host'], int(cfg['server']['port']))
    upstreams_addresses = []
    for key, value in cfg.items():
        if key == 'upstreams':
            for _, address in value.items():
                upstream_address = (address['host'], int(address['port']))
                upstreams_addresses.append(upstream_address)
    
    server = server.Server()
    server.run(server_address, upstreams_addresses)