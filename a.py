import ssl
import json
from urllib.request import urlopen

import numpy as np
import pandas as pd

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.express.colors as pc


ssl._create_default_https_context = ssl._create_unverified_context

# File Authentication
@st.cache_data
def load_json():
    try:
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            return json.load(response)
    
    except json.decoder.JSONDecodeError as error:
        st.write("Failed to load JSON data - Check Interntet Connection or Server Data Fetch Request:", error)
        st.write("")
        
        print("Failed to load JSON data - Check Interntet Connection or Server Data Fetch Request:", error)
        print("")
    

# Data Frame Creation
@st.cache_data
def load_data():
    # sdoh_path = r"C:\Users\dcedr\Documents\dashboard_codes\sdoh.csv"
    sdoh_path = "sdoh.csv"
    return pd.read_csv(sdoh_path, dtype={"COUNTYFIPS":str, "STATEFIPS":str}, low_memory=False)
    

# Columns and Labels to use in "SDOHs Dropdown Menu"
sdoh_options = ["ACS_PCT_HH_PUB_ASSIST",      # poverty
                "ACS_TOT_CIVIL_EMPLOY_POP",   # employment
                "ACS_PCT_LT_HS",              # education
                "ACS_PCT_UNINSURED",          # insurance_coverage
                "HIFLD_MIN_DIST_UC"]          # healthcare_access
                # "ACS_PCT_GRANDP_NO_RESPS"]  # extended_family
    
labels_for_counties = [
    "Percentage of Families with Public Income or Food Asssitance ",                  # poverty
    "Number of Employed Civilians (Thousands) ",                                      # employment
    "Percentage of People with Less Than High School Education (Ages 25 and over) ",  # education
    "Percentage of People without Health Insurance Coverage ",                        # insurance_coverage
    "Miles to Nearest Urgent Care "]                                                  # healthcare_access
    # "Pct. Children Living with Grandparent, Not Responsible"]                       # extended_family
    
# Descriptions to display extra information to users
descriptions_for_counties = [
    "Percentage of Families that receive Public Assistance Income or Food Stamps/SNAP (Supplemental Nutrition Assistance Program).",  # poverty
    "Number (Thousands) of Employed Civilians (Ages 16 and over).",                                                                   # employment
    "Percentage of People With Less Than a High School Education (Ages 25 and over).",                                                # education
    "Percentage of People Without Health Insurance Coverage.",                                                                        # insurance_coverage
    "Distance in Miles to the Nearest Urgent Care Center (based on ZIP Codes)."]                                                      # healthcare_access
    # "Percentage of Children living with their Grandparent, that is not responsible for them."]                                      # extended_family  

sdoh_colors = ['color_ACS_PCT_HH_PUB_ASSIST', 'color_ACS_TOT_CIVIL_EMPLOY_POP', 'color_ACS_PCT_LT_HS',
               'color_ACS_PCT_UNINSURED', 'color_HIFLD_MIN_DIST_UC', 'color_ACS_PCT_GRANDP_NO_RESPS']

sdoh_tickvals=[3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000, 
               11000000, 12000000, 13000000, 14000000, 15000000, 16000000, 17000000]


dict_sdohLabels = dict(zip(sdoh_options, labels_for_counties))    
dict_sdohDescriptions = dict(zip(sdoh_options, descriptions_for_counties))
dict_sdohColors = dict(zip(sdoh_options, sdoh_colors))



# Columns and Labels to use in "Labs Menu"
lab_options = ["albumin_urine", "bun", "creatinine_serum", "creatinine_urine"]

labels_for_dots = ["Average of Albumin Urine lab test ", 
                   "Average of Blood Urea Nitrogen lab test ", 
                   "Average of Creatinine Serum lab test ", 
                   "Average of Creatinine Urine lab test "]

lab_colors = ["color_albu_urine", "color_bun", "color_crea_serum", "color_crea_urine"]

lab_dticks = [5, 2, 0.1, 15]


dict_labLabels = dict(zip(lab_options, labels_for_dots))
dict_labColors = dict(zip(lab_options, lab_colors))
dict_labsDticks = dict(zip(lab_options, lab_dticks))



# Dictionary with all labels
dict_Labels = {**dict_labLabels, **dict_sdohLabels}
dict_Labels["COUNTY"] = "County "



########################################
# --DASHBOARD APPLICATION START LINE-- #
########################################

st.set_page_config(layout="wide",
                   page_title="PR Kidney Disease-SDOH",
                   page_icon=":test_tube:",
                   menu_items={"Get help":"mailto:dylan.cedres@upr.edu",
                               "Report a Bug":"mailto:dylan.cedres@upr.edu",
                               "About":"Dashboard with Kidney Disease Lab Data and Social Determinants of Health Indices"})


counties = load_json()  # Puerto Rico's Map Information
sdoh = load_data()      # SDOHs and Labs Data


### Dashboard Main Title ###
title_buff, title2 = st.columns([0.28, 0.72])
# title1, title_buff, title2 = st.columns([0.20, 0.30, 0.50])

# with title1:
    # Application's Main Title (LEFT)
    # st.subheader("Kidney Disease Lab Test / Social Determinants of Health (SDoH)")
    # st.title("Dashboard: Social Determinants of Health and Kidney Disease Lab Data")
    # st.header("Dashboard: Social Determinants of Health and Kidney Disease Lab Data")

with title2:
    # Application's Main Title (CENTER)
    st.subheader("**Kidney Disease Lab Test / Social Determinants of Health (SDoH) - Puerto Rico**", anchor=False)
    

    
### Dropdown Menus and SDoHs Descriptions ###
col1, col2 = st.columns([0.175, 0.835], gap="medium")

with col1:
    st.markdown(body="")
    st.markdown(body="")
    st.markdown(body="##### Select the Kidney lab test")
    
    # Labs Menu
    lab_selection = st.selectbox(key="current_lab",
                                 label="**Select the Kidney lab test**", 
                                 label_visibility="collapsed",
                                 options=lab_options,
                                 index=0,
                                 format_func=lambda y: dict_labLabels[y])
                                 # format_func=lambda y: str(lab_options.index(y)+1) + ". " + dict_labLabels[y])
    st.markdown(body="")
    st.markdown(body="")
    st.markdown(body="")
    st.markdown(body="")
    
    # SDOHs Menu
    st.markdown(body="##### Select the SDOH")
    sdoh_selection = st.selectbox(key="current_sdoh",
                                  label="**Select the SDOH**", 
                                  label_visibility="collapsed",
                                  options=sdoh_options, 
                                  index=0, 
                                  format_func=lambda x: dict_sdohLabels[x])
                                  # format_func=lambda x: str(sdoh_options.index(x)+1) + ". " + dict_sdohLabels[x])
    
    st.markdown(body="")
    sdoh_description = st.markdown(body=dict_sdohDescriptions[sdoh_selection],
                                  help=dict_sdohLabels[sdoh_selection])



# Dictionary for ticks information
arange = np.arange(start=0.0, stop=1.01, step=0.05882352941176471)
sdoh_describe = sdoh[sdoh_selection].describe(percentiles=arange)
sdoh_describe.pop("50%")
percentiles_vals = sdoh_describe[7:-1].values

sdoh_ticktexts=(np.rint(percentiles_vals)).astype(int)


### Puerto Rico Choropleth Map containing Counties with SDOH Data ###
mapp = px.choropleth(data_frame=sdoh,                                        # dataframe to use
                     geojson=counties,                                       # establishes coordinates of Puerto Rico to trace its map
                     locations="COUNTYFIPS",                                 # determines considered locations, used for plot traces and updates
                     labels=dict_Labels,                                     # labels for labs and sdohs
                     hover_name="COUNTY",                                    # counties names
                     # hover_data={sdoh_selection:True, "COUNTYFIPS":False}, # info contained in counties
                     hover_data={lab_selection:":.1f", sdoh_selection:":.0f",
                                 "COUNTYFIPS":False},
                     # color=dict_sdohColors[sdoh_selection],                # counties color intensities
                     # color_continuous_scale=pc.sequential.Purples,         # color scale for color intensities
                     # range_color=[0.35, 1],                                # min and max color intensities for counties
                     )      
                     
# Geographical Map Design
mapp.update_geos(scope="world",                         # sets section of world map
                 fitbounds=False,                       # removes mapping of locations with geojson coordinates, same as <fitbounds> in px.choropleth(...)
                 visible=False,                         # removes all other countries and continents, same as <basemap_visible> in px.choropleth(...)
                 center=dict(lat=18.155, lon=-66.255),  # sets center coordinates of the figure's map projection
                 bgcolor="#f5f5f5",                     # background color name: "whitesmoke"
                 projection_scale=195,                  # sets the map's initial zoom and projection type
                 showframe=False,                       # shows the border lines of the map's plot box
                 )

# Map's Figure Layout
mapp.update_layout(autosize=False,                                      # allows custom size
                   margin=dict(autoexpand=True, r=0, t=0, l=0, b=0),    # figure's boundaries, distance from the plot's borders to the container's borders
                   
                   width=1200,                                          # map horizontal size/length, same as <width> in px.choropleth(...)
                   height=600,                                          # map vertical size/length, same as <height> in px.choropleth(...)
                                      
                   paper_bgcolor="#f5f5f5",                             # application background color
                   # paper_bgcolor="indigo",
                   
                   dragmode=False,                                      # disables dragging of the map figure
                   modebar=dict(color="#303030", 
                                activecolor="#d303fc", 
                                bgcolor="#f5f5f5",
                                remove=["zoomIn", "zoomOut", "select",  # disables modebar's options 
                                        "lasso", "pan", "reset"]),
                   
                   # title=dict(                       # Main Title Design
                   #     automargin=True,              
                   #     pad=dict(t=0, l=0, b=0, r=0),  
                   #     x=0.50,                        
                   #     y=0.90, 
                   #     xref="paper", 
                   #     yref="paper", 
                   #     xanchor="center",
                   #     yanchor="top",
                   #     text="Puerto Rico<br>", 
                   #     "SDOHs-Kidney Disease",       
                   #     font=dict(color="purple", family="Rockwell", size=16)), 
                   
                   
                   showlegend=False,
                   # legend=dict(                       # Legend Design 
                   #    x=0.60, 
                   #    y=-0.175,
                   
                   #    bgcolor="#f5f5f5",              # legend background color
                   #    bordercolor="black",            # legend border lines color
                   #    borderwidth=0.75,               # legend border lines thickness 
                   #    
                   #    entrywidth=1,                   # space between symbols and labels
                   #    entrywidthmode="pixels",        # determines unit of measurement
                   #    itemwidth=30,                   # size of symbols inside the legend
                   #    traceorder="reversed",
                   #    
                   #    title=dict(side="top",                                  # legend's title text properties
                   #               text="Legend",                   
                   #               font=dict(color="black", family="Rockwell", size=14)))
                   #    font=dict(color="black", family="Rockwell", size=13),   # legend's labels text properties
                   )

# Map's Traces Properties
mapp.update_traces(visible=True,
                   name=dict_sdohLabels[sdoh_selection],                # new name of symbol
                   z=sdoh[dict_sdohColors[sdoh_selection]],
                   # z=sdoh[sdoh_selection],
                   # zauto=False,                                       # allows custom inferior/superior limits & midpoint
                   # zmin=sdoh[sdoh_selection].min(),
                   # zmax=sdoh[sdoh_selection].max(),     
                   
                   marker=dict(line=dict(color="#303030", width=1.5), opacity=0.925),
                   
                   showscale=True,
                   autocolorscale=False,
                   colorscale=pc.sequential.Purples,
                   reversescale=False,

                   
                   showlegend=False,                     # allows to be shown in the legend
                   legendrank=1,                         # first symbol in the legend
                   legendwidth=10,                       # width of legend box
                   
                   colorbar=dict(
                       orientation="h",                  # sets the colorscale bar to be drawn horizontaly
                       outlinecolor="black",             # sets the color of the bar's borders
                       outlinewidth=1.05,                # sets thickness of the borders' lines
                       
                       x=0.725,
                       y=0.025,                    
                       
                       thickness=13,                     # thickness size of the bar
                       len=0.40,                         # length of the bar                       
                       
                       title=dict(
                           side="bottom",
                           text=dict_sdohLabels[sdoh_selection],
                           font=dict(color="#303030", family="Rockwell", size=10)),   
                       
                       tickmode="array",
                       tickvals=sdoh_tickvals,
                       ticktext=sdoh_ticktexts,
                       # tickformat=".0f",
                       # ticksuffix="%",
                       ticks="inside",
                       tickwidth=1.35,
                       ticklen=3.5,
                       tickcolor="black",
                       tickfont=dict(color="#303030", family="Rockwell", size=9))
                  )




# Puerto Rico Scattergeo Map containing County Coordinate with Lab Data
# Counties without lab data: Añasco, Florida, Hormigueros, Las Marías, and Orocovis
dots = px.scatter_geo(data_frame=sdoh,
                      lat="lat",
                      lon="lon",
                      fitbounds="locations",
                      labels=dict_Labels,                                          # labels for labs and sdohs
                      hover_name="COUNTY",                                         # title of the dots' hoverboxes
                      hover_data={lab_selection:":.1f", sdoh_selection:":.0f",     # information contained inside dots
                                  "lat":False, "lon":False}
                      # color="creatinine_serum",                                  # dots color intensities
                      # color_continuous_scale=pc.sequential.Oranges,              # color scale for color intensities
                      # range_color=[0.30, 1.0],                                   # min and max color intensities for dots 
                      # opacity=0.75,                                              # transparency level for dots 
                      )

# Dot's Figure Layout
dots.update_layout(margin=dict(r=0, t=0, l=0, b=0),
                   autosize=False,                   # allows custom size                   
                   showlegend=False)                        

# Map's Traces Properties 
dots.update_traces(showlegend=False,                                      # allows to be shown in the legend
                   legendrank=2,                                          # second symbol in the legend
                   name=dict_labLabels[lab_selection],                    # sets the trace name in the legend and on datum hover 
                   
                   hoverlabel=dict(align="left",                          # sets text to be aligned to the left
                                   # bgcolor="darkorange",                # hoverbox background color
                                   bordercolor="black"),                  # hoverbox edges color
                   
                   # selected_marker=dict(opacity=1, size=10),
                   marker=dict(
                       size=9,                                            # size of dots, same as <size> in px.scatter_geo(...)
                       line=dict(width=1.25, color="#303030"),            # dots borders line thickness & color
                       
                       color=sdoh[dict_labColors[lab_selection]],         # determines color intensities
                       opacity=0.90,
                       cauto=False,                                       # allows custom inferior/superior limits & midpoint
                       cmin=sdoh[lab_selection].min(),
                       cmax=sdoh[lab_selection].max(),
                       
                       showscale=True,                                    # displays scale values-to-color-intensities
                       autocolorscale=False,                              # allows custom colorscale
                       colorscale="Oranges",                              # determines color scale for color intensities
                       reversescale=False,                                # reverses bright and dark values
                       
                       colorbar=dict(
                           orientation="h",                               # sets the colorscale bar to be drawn horizontaly
                           outlinecolor="black",                          # sets the color of the bar's borders
                           outlinewidth=1.05,                             # sets thickness of the borders' lines
                           
                           x=0.275,
                           y=0.025,                      
                           
                           thickness=13,                                   # thickness size of the bar
                           len=0.40,                                       # length of the bar
                           
                           title=dict(
                               side="bottom",
                               text=dict_labLabels[lab_selection],
                               font=dict(color="#303030", family="Rockwell", size=10)), 
                           
                           tickmode="linear",
                           tick0=0,
                           dtick=dict_labsDticks[lab_selection],
                           # tickformat=".1f",
                           ticks="inside",
                           tickwidth=1.30,
                           ticklen=4,
                           tickcolor="black",
                           tickfont=dict(color="#303030", family="Rockwell", size=9)))          
                   )



# Combines the Dots Traces of the Scattergeo Map with the Counties Traces of the Choropleth Map, 
# based on Puerto Rico's Coordinates.
mapp.append_trace(dots.data[0], row="all", col="all")


with col2:
    # Display the plot and all its traces
    st.plotly_chart(mapp,
                    use_container_width=True,
                    config={"displayModeBar":"hover",  # Sets the mode bar to appear only when the mouse is inside the plot
                            "displaylogo":False,       # Removes the Plotly-Dash logo from appearing in the mode bar options
                            "scrollZoom":False})
    
# if sdoh_selection:
#     st.toast(body="Current SDOH  %s" % dict_sdohLabels[sdoh_selection], icon="⚕️")
        
# if lab_selection:
#     st.toast(body="Current Lab " + dict_labLabels[lab_selection], icon="🧪")