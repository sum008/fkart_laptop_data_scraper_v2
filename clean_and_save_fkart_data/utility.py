import requests

def get_base_token(bearer):
    # f37c8239d992ab304d31c9dcdd7158eadc98dd83
    url = "https://cloud.seatable.io/api/v2.1/dtable/app-access-token/"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {bearer}"
    }
    return requests.get(url, headers=headers).json()

def create_table(payload, base_uuid, bearer):
    url = f"https://cloud.seatable.io/dtable-server/api/v1/dtables/{base_uuid}/tables/"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {bearer}"
    }
    return requests.post(url, json=payload, headers=headers).json()

def insert_data_to_table(base_uuid, payload, bearer):
    url = f"https://cloud.seatable.io/dtable-server/api/v1/dtables/{base_uuid}/batch-append-rows/"
    # payload = {
    #     "table_name": "test_tbl",
    #     "rows": [{ "col1": "sdfsdfsd" }, { "col1": "aaaaaaa" }, { "col1": "ttttttt" }]
    # }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {bearer}"
    }
    return requests.post(url, json=payload, headers=headers).json()