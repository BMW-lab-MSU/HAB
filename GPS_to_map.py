import plotly.express as px
import pandas as pd
from plotly.offline import plot
directory = "/media/flint/Elements/HAB/Flight_23/"
df = pd.read_csv(directory+"GPS_DATA.csv")
types = ['open-street-map', 'white-bg', 'carto-positron', 'carto-darkmatter', 'stamen-terrain', 'stamen-toner', 'stamen-watercolor']


color_scale = [(0, 'blue'), (1,'orange')]

fig = px.scatter_mapbox(df, 
                        lat="Latitude", 
                        lon="Longitude", 
                        hover_name="UTC", 
                        hover_data=["UTC", "Altitude[m]"],
                        color="Altitude[m]",
                        color_continuous_scale=color_scale,
                        
                        zoom=15, 
                        height=800,
                        width=800)

fig.update_layout(mapbox_style=types[0])

fig.show()
plot(fig)