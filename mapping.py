#%%
from bokeh.io import output_notebook, show, output_file, curdoc
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
import geopandas as gpd
import pandas as pd
import json

#%%

shapefile = 'data/state_earth_data/ne_110m_admin_1_states_provinces_lakes.shp'
losses_csv = 'data/total_winter_colony_losses.csv'

# load datasets
gdf = gpd.read_file(shapefile)[['name', 'woe_label', 'postal', 'fips',  'geometry']]
colony_loss = pd.read_csv(losses_csv, header=0)

# merge and format datasets
merged = gdf.merge(colony_loss[colony_loss['year'] == '2016/17'], left_on='name', right_on='state')
merged_json = json.loads(merged.to_json())
json_data = json.dumps(merged_json)
geo_source = GeoJSONDataSource(geojson=json_data)

# create color maps
palette = brewer['YlGn'][8]
# reverse so darkest is highest
palette = palette[::-1]
color_mapper = LinearColorMapper(palette=palette, low=0, high=40)
#Create color bar.
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500, height=20,
                     border_line_color=None, location=(0, 0), orientation='horizontal')

#Create figure object.
p = figure(title='Colony Loss in 2016', plot_height=600, plot_width=950, toolbar_location=None)
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

#Add patch renderer to figure.
p.patches('xs', 'ys', source=geo_source, fill_color={'field': 'total_loss(%)', 'transform': color_mapper},
          line_color='black', line_width=0.25, fill_alpha=1)  # Specify figure layout.
p.add_layout(color_bar, 'below')#Display figure inline in Jupyter Notebook.

curdoc().add_root(row(p, width=800))

print(gdf.shape)