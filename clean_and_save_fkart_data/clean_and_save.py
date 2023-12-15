import pandas as pd

from utility import create_table, get_base_token, insert_data_to_table
import configparser



def extract_headers():
    header_set = set()
    for index in range(0, len(fkart_data)):
        cur_list = fkart_data.loc[index].to_list()[0]
        for cur_hearder_index in range(0, len(cur_list), 2):
            # print(cur_hearder_index)
            header_set.add(cur_list[cur_hearder_index])
    return header_set


def convert_json_to_dict():
    dict_list = []
    for index in range(0, len(fkart_data)):
        current_data = fkart_data.loc[index].to_list()[0]
        extracted_dict = {current_data[index]: current_data[index+1]
                          for index in range(0, len(current_data), 2)}
        dict_list.append(extracted_dict)
    # dict_list = dict(sorted(dict_list.items()))
    return dict_list


def final_correction(header_set, spec_dict):
    for index in range(0, len(spec_dict)):
        for header in header_set:
            if header not in spec_dict[index].keys():
                spec_dict[index][header] = None
    return spec_dict

def create_header_payload(header_list, table_name):
    payload = {"table_name": table_name, "columns": [{"column_type": "number", "column_name":"id"}]}
    for cur_header in header_list:
        payload["columns"].append({"column_type": "long-text", "column_name":cur_header})
    return payload
        


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("../flipkart_scraper_with_scrapy/config/token.config")
    fkart_data = pd.read_json(
        "../flipkart_scraper_with_scrapy/fkart_data_scraper/specs.jsonl", lines=True)
    dict_to_list = convert_json_to_dict()
    headers = extract_headers()
    dict_to_list = final_correction(
        header_set=headers, spec_dict=dict_to_list)
    
    bearer_token = config.get("bearer_token","token")
    table_name = config.get("table", "table_name")
    payload = create_header_payload(header_list=headers, table_name=table_name)
    res=get_base_token(bearer=bearer_token)
    create_tbl_res=create_table(payload=payload, base_uuid=res["dtable_uuid"], bearer=res["access_token"])
    payload = {
        "table_name": "fkart_laptop_data_tbl",
        "rows": dict_to_list
    }
    result=insert_data_to_table(base_uuid=res["dtable_uuid"], payload=payload, bearer=res["access_token"])
    print(result)
    # final_df = pd.DataFrame.from_dict(dict_to_list, orient="columns")
    # final_df.to_csv(".//converted_csv.csv", header=True, index=False)
