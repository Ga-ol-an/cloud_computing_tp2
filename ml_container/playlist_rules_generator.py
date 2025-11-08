from fpgrowth_py import fpgrowth
import pandas as pd
import pickle
import os
import ssl
import time
from datetime import datetime

def generate_playlist_rules():
  # Define the variables below based on the env values set in the Kubernetes deployment file
  MIN_SUPPORT_RATIO=float(os.getenv("MIN_SUPPORT_RATIO", "0.1"))
  MIN_CONFIDENCE=float(os.getenv("MIN_CONFIDENCE", "0.1"))
  DATASET_ADDRESS=os.getenv("DATASET_ADDRESS", "https://homepages.dcc.ufmg.br/~cunha/hosted/cloudcomp-2023s2-datasets/2023_spotify_ds1.csv")

  df = pd.read_csv(DATASET_ADDRESS)

  # itemset_list = df.groupby('pid')['track_name'].apply(list).to_list()
  
  itemset_list = (
        df.dropna(subset=["pid", "track_name"])
          .astype({"pid": str, "track_name": str})
          .groupby("pid", sort=False)["track_name"]
          .apply(lambda s: s.dropna().astype(str).drop_duplicates().tolist())
          .tolist()
    )

  # freqItemSet, rules = fpgrowth(itemset_list, MIN_SUPPORT_RATIO, MIN_CONFIDENCE)
  _, rules = fpgrowth(itemset_list, MIN_SUPPORT_RATIO, MIN_CONFIDENCE)

  print("Generated Playlist Rules:")
  for rule in rules:
      print(f" - {rule}")

  metadata = {
      "rules": rules,
      "model_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  }

  # os.makedirs('result', exist_ok=True)
  with open('data/rules.pickle', 'wb') as file:
      pickle.dump(metadata, file)
      
  # Keep in loop so the container doesn't stop right after generating the model
  while True:
      print("Playlist rules generated and saved to 'data/rules.pickle'. Pod still running in loop.")
      time.sleep(10)  # Sleep for 10 seconds
      
if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    generate_playlist_rules()