from bokeh.io import output_notebook, show, output_file, curdoc
from bokeh.layouts import row, column, widgetbox
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, HoverTool, Slider
from bokeh.palettes import Viridis
import geopandas as gpd
import pandas as pd
import json

# downloaded from: https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-1-states-provinces/
shapefile = 'data/state_earth_data/ne_110m_admin_1_states_provinces_lakes.shp'
# scraped from https://bip2.beeinformed.org/loss-map/
losses_csv = 'data/total_winter_colony_losses.csv'

# load datasets
gdf = gpd.read_file(shapefile)[['name', 'woe_label', 'postal', 'fips',  'geometry']]
colony_loss = pd.read_csv(losses_csv, header=0)
colony_loss['YEAR'] = [int(x.split("/")[0]) for x in colony_loss['year']]
all_years = colony_loss['YEAR'].unique()
colony_loss = colony_loss.rename(columns={"total_loss(%)":"colony_loss"})


def data_by_year(year):
    # merge and format datasets
    merged = gdf.merge(colony_loss[colony_loss['YEAR'] == year], left_on='name', right_on='state', how='left')
    merged.fillna("No data", inplace=True)
    merged_json = json.loads(merged.to_json())
    json_data = json.dumps(merged_json)
    return json_data

# create color maps
palette = Viridis[8]
# reverse so darkest is highest
palette = palette[::-1]
color_mapper = LinearColorMapper(palette=palette, low=0, high=100, nan_color='#d9d9d9')
#Create color bar.
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500, height=20,
                     border_line_color=None, location=(0, 0), orientation='horizontal')

#Hover tool
hover = HoverTool(tooltips=[('State', '@state'), ("Winter colony loss (%)", '@colony_loss'), ('Num Colonies', '@colonies')])

#Create figure object.
p = figure(title='Colony Loss in %d' % all_years.max(), plot_height=600, plot_width=950, toolbar_location=None, tools=[hover])
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

#Add patch renderer to figure.
geo_source = GeoJSONDataSource(geojson=data_by_year(all_years.max()))
p.patches('xs', 'ys', source=geo_source, fill_color={'field': 'colony_loss', 'transform': color_mapper},
          line_color='black', line_width=0.25, fill_alpha=1)  # Specify figure layout.
p.add_layout(color_bar, 'below')

#update callback
def updated_plot_year(attr, old, new):
    yr = slider.value
    new_data = data_by_year(yr)
    geo_source.geojson = new_data
    p.title.text = "Colony Loss in %d" % yr

slider = Slider(title='Year', start=all_years.min(), end=all_years.max(), step=1, value=all_years.max())
slider.on_change('value', updated_plot_year)

layout = column(p, widgetbox(slider))
curdoc().add_root(layout)

print(gdf.shape)
