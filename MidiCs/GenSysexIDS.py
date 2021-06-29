import requests
import pandas as pd


def main():
    response_text = requests.get("https://www.midi.org/specifications-old/item/table-4-universal-system-exclusive-messages").text
    df = pd.read_html(response_text)[0]
    df.drop(index=0, inplace=True)
    idx = df[df[0].apply(lambda x: 'Real Time' in str(x))].index[1]
    non_rt = df[df.index < idx]
    rt = df[df.index > idx]
    non_rt.drop(index=1, inplace=True)
    non_rt.rename(columns={0: 'subID1', 1: 'subID2', 2: 'garbage', 3: 'description'}, inplace=True)
    non_rt.drop(index=2, inplace=True)
    non_rt = non_rt.reset_index()
    non_rt.drop(['index', 'garbage'], axis=1, inplace=True)
    non_rt['subID1'] = non_rt['subID1'].apply(lambda x: int(x, 16))
    non_rt['subID2'] = non_rt['subID2'].astype(int, errors='ignore')
    rt = rt.reset_index()
    # print(non_rt)
    for index, row in non_rt.iterrows():
        if row['subID1'] == "":
            print('++++')
        print(row)
    # print(rt)


if __name__ == "__main__":
    main()