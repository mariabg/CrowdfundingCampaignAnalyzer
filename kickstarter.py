import sys
import glob
import pandas as pd
import numpy as np
import pycountry
# import plotly
# import plotly.plotly as py
# plotly.tools.set_credentials_file(username='', api_key='')

def main ():
    # Data was obtained from https://webrobots.io/kickstarter-datasets/
    allFiles = glob.glob("kickstarterData/*.csv")
    frame = pd.DataFrame()
    arr = []
    for fl in allFiles:
        df = pd.read_csv(fl, index_col=None, header=0)
        arr.append(df)
    df = pd.concat(arr)

    df = cleanData(df)
    df = removeOutliers(df)
    df.to_csv('outputFiles/cleanedData.csv', encoding='utf-8')

    # Select an specific group, e.g. country and time range
    # df = df.loc[df['country'] == 'Spain']
    # df = df[df.deadline < '15-11-2017']
    # df = df[df.deadline > '15-11-2015']

    # Save only specific data, e.g. uploading to Carto
    # countrySuccMean = df.groupby(['countryName'])['success'].agg(['mean', 'count'])
    # countrySuccMean = countrySuccMean[countrySuccMean['count'] >= 10]
    # countrySuccMean.to_csv('outputFiles/cartoData.csv', header='true', encoding='utf-8')

    # Plots
    # categoryArray = ['technology', 'theater', 'games', 'film%20&%20video', 'publishing', 'music', 'art', 'photography']
    # scatterPlot(df, df['category'], 'goal', 'pledged', categoryArray, 'X', 'Y')
    # scatterPlot(df, df['length'], 'length', 'success', [0, 1], 'X', 'Y')
    # scatterPlot(df, df['length'], 'length', 'success', [0, 1], 'X', 'Y')

def scatterPlot (df, data, xAttrib, yAttrib, colouredBy, xTitle, yTitle):
    fig = {
        'data': [
            {
                'x': df[data==name][xAttrib],
                'y': df[data==name][yAttrib],
                'name': name, 'mode': 'markers',
            } for name in colouredBy
        ],
        'layout': {
            'xaxis': {'title': xTitle, 'type': 'log'},
            'yaxis': {'title': yTitle}
        }
    }
    output = 'scatterPlot_' + xAttrib + '_' + yAttrib
    py.plot(fig, filename=output)

def cleanData (df):
    # remove redundant data, add relevant missing data and organize it
    clean = df[['name', 'id','blurb', 'category', 'location', 'goal', 'static_usd_rate', 'usd_pledged', 'backers_count', 'launched_at', 'deadline', 'urls']].copy()
    clean['category'] = clean['category'].str.extract('.*\www.kickstarter.com/discover/categories/(.+?)/\.*', expand=True)
    clean['category'] = clean['category'].str.replace('film%20&%20video', 'film & video')
    clean['countryCode'] = clean['location'].str.extract('country":"(.+?)","url', expand=True)
    clean['countryName'] = clean.apply(lambda row: getCountryNames(row.countryCode), axis=1)
    clean['launched_at'] = pd.to_datetime(clean['launched_at'], unit='s')
    clean['deadline'] = pd.to_datetime(clean['deadline'], unit='s')
    clean['url'] = clean['urls'].str.extract('project":"(.+?)","rewards', expand=True)
    clean = clean.rename(columns = {'backers_count':'backers'})
    clean = clean.rename(columns = {'usd_pledged':'pledged'})
    clean['pledged'] = clean.pledged.round(decimals=2)
    clean = clean.rename(columns = {'goal':'nousd_goal'})
    clean['goal'] = clean.nousd_goal*clean.static_usd_rate
    clean['success'] = clean.apply(lambda row: successful(row.goal, row.pledged), axis=1)
    clean['length'] = (clean['deadline'] - clean['launched_at']).dt.days
    clean['launchedMonth'] = clean['launched_at'].dt.month
    clean = clean.drop('static_usd_rate', 1)
    clean = clean.drop('nousd_goal', 1)
    clean = clean.drop('location', 1)
    clean = clean.drop('countryCode', 1)
    clean = clean.drop('urls', 1)
    clean = clean.drop_duplicates(subset=None, keep='first')
    clean.dropna()
    return clean

def removeOutliers (clean):
    clean = clean[clean.goal > 1]
    clean = clean[clean.goal < 1000000]
    clean = clean[np.abs(clean.goal-clean.goal.mean())<=(3*clean.goal.std())]
    clean = clean[np.abs(clean.pledged-clean.pledged.mean())<=(3*clean.pledged.std())]
    clean = clean[np.abs(clean.backers-clean.backers.mean())<=(3*clean.backers.std())]
    return clean

def getCountryNames (code):
    for co in list(pycountry.countries):
        if code == co.alpha_2:
            return co.name
    return None

def successful (goal, pledge):
    if (goal > pledge):
        return 0
    else:
        return 1

if __name__ == '__main__':
    main()
