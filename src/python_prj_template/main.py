from python_prj_template.opensearch.client import Client

if __name__ == "__main__":
    client = Client()
    client.read_config("./config.toml")
    client.create_client()
    # print(client.client.info())