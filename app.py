def find_top_confirmed(n = 15):

    import pandas as pd
    corona_df=pd.read_csv("Covid-19.csv")
    by_country = corona_df.groupby('State/UTs').sum()[['Active']]
    cdf = by_country.nlargest(n, 'Active')[['Active']]
    return cdf

cdf=find_top_confirmed()
pairs=[(country,confirmed) for country,confirmed in zip(cdf.index,cdf['Active'])]


import folium
import pandas as pd
corona_df = pd.read_csv("Covid-19.csv")
corona_df=corona_df[['Latitude','Longitude','Active']]
corona_df=corona_df.dropna()

m=folium.Map(location=[11.7401,92.6586],
            tiles='Stamen toner',
            zoom_start=8)

def circle_maker(x):
    folium.Circle(location=[x[0],x[1]],
                 radius=float(x[2]),
                 color="red",
                 popup='Active cases:{}'.format(x[2])).add_to(m)
corona_df.apply(lambda x:circle_maker(x),axis=1)

html_map=m._repr_html_()

from flask import Flask,render_template, request


app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html",table=cdf, cmap=html_map,pairs=pairs)

@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        State = int(request.form["State"])

        return render_template("home.html",data=State,table=cdf, cmap=html_map,pairs=pairs)
    return render_template("home.html",table=cdf, cmap=html_map,pairs=pairs)

if __name__=="__main__":
    app.run(debug=True)

