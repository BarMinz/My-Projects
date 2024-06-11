import pandas as pd

url = 'https://docs.google.com/spreadsheets/d/1wU1346u_6U1VV9pxPRyRtv7OBucfnErKDUiUqWTwzSQ/export?format=csv&gid=0'

if __name__ == '__main__':
    read_file = pd.read_csv(url)
    read_file.to_excel(input("Enter a path to store the new file: "), index=False, header=True)