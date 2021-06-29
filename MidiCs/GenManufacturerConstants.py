import pathlib
import requests
import pandas as pd


def main():
    response_text = requests.get("https://www.midi.org/specifications-old/item/manufacturer-id-numbers").text
    dfs = pd.read_html(response_text)
    for frame in dfs:
        frame.drop(0, inplace=True)
    dataset = pd.concat(dfs)
    dataset.drop(1, inplace=True)
    dataset.drop(dataset[dataset[0].apply(lambda x: "to" in str(x))].index, inplace=True)
    dataset.reset_index(inplace=True)
    dataset = dataset.drop('index', axis=1)
    dataset = dataset.rename(columns={0: 'id', 1: 'manufacturer'})
    dataset.drop(dataset[dataset['id'].isna()].index, inplace=True)
    dataset['id'] = dataset['id'].apply(lambda x: ([int(item[:-1], 16) for item in str(x).split()]))
    reserved = dataset[dataset['manufacturer'].apply(lambda x: str(x).lower() == "reserved")]['id']
    dataset.drop(dataset[dataset['manufacturer'].apply(lambda x: str(x).lower() == "reserved")].index, inplace=True)
    dataset['manufacturer'] = dataset['manufacturer'].apply(lambda x: str(x).replace(" ", ' '))
    dataset = dataset.drop_duplicates(subset='manufacturer')
    # print(reserved)

    def function(x):
        x = x.replace(".", "")
        x = x.replace(',', '')
        x = x.replace('(', '')
        x = x.replace(')', '')
        x = x.replace('"', '')
        x = x.replace("'", '')
        return x.upper()

    dataset['label'] = dataset['manufacturer'].apply(function)
    dataset['lsize'] = dataset['label'].apply(lambda x: len(x))
    print(dataset)
    max_len = dataset['lsize'].max() + max(dataset['id'].apply(lambda x: len(str(x)))) + 6
    result = ['# -*- coding: utf-8 -*-', "MANUFACTURER_ID = {"]
    for index, item in dataset.iterrows():
        # print(item)
        result.append(("    '" + item['label'] + "': " + str(item['id']) + ',' + ' ' * max_len)[:max_len + 1] + '# ' + item['manufacturer'])
    result.extend(['}'])
    with pathlib.Path("./MidiCs/ManufacturerId.py").expanduser().open("w") as file:
        file.writelines([item + '\n' for item in result])

    result = ['# -*- coding: utf-8 -*-', "MANUFACTURER_NAME = {"]
    # result.append('MANUFACTURER_NAME = {')
    for index, item in dataset.iterrows():
        result.append('    ' + (str(tuple(item['id'])) + ": '" + item['label'] + "'," + ' ' * max_len)[:max_len + 1] + '# ' + item['manufacturer'])
    result.append("}")
    # result.append('RESERVED_IDS = [')
    # for indey, item in reserved.iteritems():
    #     result.append('    ' + str(item))
    # result.append(']')
    # print("\n".join(result))
    with pathlib.Path("./MidiCs/ManufacturerName.py").expanduser().open("w") as file:
        file.writelines([item + '\n' for item in result])


if __name__ == "__main__":
    main()
