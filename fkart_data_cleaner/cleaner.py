import pandas as pd


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
            # print(spec_dict[index])
            if header not in spec_dict[index].keys():
                spec_dict[index][header] = None
            # else:
            #     spec_dict[index][header] = None
        # spec_dict[index] = dict(sorted(spec_dict[index].items()))
    return spec_dict


if __name__ == "__main__":
    fkart_data = pd.read_json(
        "C:/Users/sk464/Documents/flipkart_scraper_with_scrapy/fkart_data_scraper/specs.jsonl", lines=True)
    dict_to_list = convert_json_to_dict()
    final_headers = extract_headers()
    # print(type(dict_to_list[0]))
    # dict_to_list = final_correction(
    #     header_set=final_headers, spec_dict=dict_to_list)
    print(final_headers)
    # print(len(dict_to_list))
    # print(dict_to_list[1])
    # dict_to_list = dict(sorted(dict_to_list.items()))
    # final_df = pd.DataFrame.from_dict(dict_to_list, orient="columns")
    # final_df.to_csv(".//converted_csv.csv", header=True, index=False)

    # ddd = pd.read_csv(".//converted_csv.csv")
    # print(ddd.head())

# print(fkart_data.reset_index()["specs"])
