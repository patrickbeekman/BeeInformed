from bokeh.io import output_notebook, show, output_file, curdoc
from bokeh.layouts import row, column, widgetbox
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, HoverTool, Slider
from bokeh.palettes import Viridis
import geopandas as gpd
import pandas as pd
import json


class MapCreator:

    def __init__(self):
        self.gdf = self.load_states_data()
        self.colony_loss, self.all_years = self.load_colony_losses()
        self.geo_source = None
        self.slider = None
        self.loss_plot = None

    def load_states_data(self):
        # downloaded from: https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-1-states-provinces/
        shapefile = 'data/state_earth_data/ne_110m_admin_1_states_provinces_lakes.shp'
        gdf = gpd.read_file(shapefile)[['name', 'woe_label', 'postal', 'fips', 'geometry']]
        return gdf

    def load_colony_losses(self):
        # scraped from https://bip2.beeinformed.org/loss-map/
        losses_csv = 'data/total_winter_colony_losses.csv'
        colony_loss = pd.read_csv(losses_csv, header=0)
        colony_loss['YEAR'] = [int(x.split("/")[0]) for x in colony_loss['year']]
        all_years = colony_loss['YEAR'].unique()
        colony_loss = colony_loss.rename(columns={"total_loss(%)":"colony_loss"})
        return colony_loss, all_years

    def data_by_year(self, year):
        # merge and format datasets
        merged = self.gdf.merge(self.colony_loss[self.colony_loss['YEAR'] == year], left_on='name', right_on='state', how='left')
        merged.fillna("No data", inplace=True)
        merged_json = json.loads(merged.to_json())
        json_data = json.dumps(merged_json)
        return json_data

    def colony_loss_map(self):
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
        self.loss_plot = figure(title='Colony Loss in %d' % self.all_years.max(), plot_height=600, plot_width=950, toolbar_location=None, tools=[hover])
        self.loss_plot.xgrid.grid_line_color = None
        self.loss_plot.ygrid.grid_line_color = None

        #Add patch renderer to figure.
        self.geo_source = GeoJSONDataSource(geojson=self.data_by_year(self.all_years.max()))
        self.loss_plot.patches('xs', 'ys', source=self.geo_source, fill_color={'field': 'colony_loss', 'transform': color_mapper},
                  line_color='black', line_width=0.25, fill_alpha=1)  # Specify figure layout.
        self.loss_plot.add_layout(color_bar, 'below')

        self.slider = Slider(title='Year', start=self.all_years.min(), end=self.all_years.max(), step=1, value=self.all_years.max())
        self.slider.on_change('value', self.updated_plot_year)

        layout = column(self.loss_plot, widgetbox(self.slider))
        curdoc().add_root(layout)

    #update callback
    def updated_plot_year(self, attr, old, new):
        yr = self.slider.value
        new_data = self.data_by_year(yr)
        self.geo_source.geojson = new_data
        self.loss_plot.title.text = "Colony Loss in %d" % yr
