import pandas as pd
import re
# file.csv path
file_csv = 'input.csv'

def extract_number(text):
    text = text.rsplit(",")[0]
    pattern = re.compile(r'\d+')
    result = "".join(pattern.findall(text))
    return result
# reads a csv file and creates a DataFrame

df = pd.read_csv(file_csv)

df.drop_duplicates(keep="first")
df.drop_duplicates(subset=["Title","N_Rooms","Square_meters","Floors","BathRooms","Neighborhood"],keep="first") #drops duplicates


df  = df[~(df["Price"]=="Prezzo su richiesta")] # deletes all property auction 


df["Floors"] = df["Floors"].replace("T","0") # formats floors transforming them in numbers
df["Floors"] = df["Floors"].replace("S - T","-1")
df["Floors"] = df["Floors"].replace("R","0")

df["Price"] = df["Price"].apply(lambda x : extract_number(x))  # cleans Price column extracting only the numerical data
df['Price'].fillna(0, inplace=True)  # fills missing values with 0
df["Price"] = df["Price"].astype(int)  # converts price column into Integer

df['Neighborhood'] = df["Neighborhood"].str.replace(r'[^\w\s,]',",", regex = True)   # cleans Neighborhood column extracting only the Neighborhood
df["Neighborhood"] = df["Neighborhood"].apply(lambda x: ', '.join(x.split(', ')[:-1]))
df.loc[df["Neighborhood"] == "Cinecitt,, Quadraro", "Neighborhood"] = df.loc[df["Neighborhood"] == "Cinecitt,, Quadraro", "Neighborhood"].str.replace(",", "à", 1)


condition = (df["Title"].str.contains("Albergo")) | (df["Title"].str.contains("Palazzo")) #deletes all hotels and buildings
df = df[~condition] 


df.to_csv("output.csv", index = False)


print(df.tail(100))  # Stampa le prime righe del DataFrame
