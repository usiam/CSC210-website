import pandas as pd
from urdine import db
from urdine.models import User, Post, Hall, Station, Food
df = pd.read_csv('urdine/data/Hall.csv')

for i in range(len(df)):
 hall = Hall(name=df['name'][i])
 db.session.add(hall)
 db.session.commit()