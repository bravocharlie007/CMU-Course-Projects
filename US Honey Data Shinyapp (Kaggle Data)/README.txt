Extracted Salient Features from honey production data in US states and displayed them in an interactive shiny web app including a chloropleth map and tidyverse graphs among others.

1) honeydata.csv is the raw kaggle dataset

2) init_statedata perfoms modifications on honeydata.csv and outputs a .csv file called states.dat that contains the geographic
delimitations of each US state along with Honey production statistics per state.

3) ui generates the desired user interface of our shiny app.

4) server hosts the server, loads the states.dat csv file and draws all graphs including the Chloropleth map

5) CHLOROPLETH_MAP is init_statedata with a small part of server and does not bring anything else to the table
