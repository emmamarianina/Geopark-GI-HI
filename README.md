# Geopark-GI-HI
Scripts and data of Msc thesis "A quantitative assessment of geodiversity and human influence in geoparks"

10-9-2020

Appendix III: digital appendix for Msc thesis Emma Polman "A quantitative assessment of geodiversity and human influence in geoparks", University of Amsterdam. 

This appendix contains:
1) geopark polygon shapefile
	a) folder--> "shapefile_geopark_areas" in zip file

2) model and data analysis Python scripts
	a) create and take random samples from GI and HI --> "Random_samples 1-3"
	b) import data to Python environment --> "import_results_for_data_analysis.py"
	c) data analysis and visualisation scripts --> all other .py files

3) tables with model results (all in zip file)
	a) results_GI_HI --> geodiversity index and human influence (change) stats for random samples and geoparks
	b) results_lithology --> number of grid cells for lithology types on continents and geoparks
	c) results_soils --> number of grid cells for soil types on continents and geoparks 


Python packages used: Numpy, ArcPy, Statsmodels, SciPy, Matplotlib, dbfread, pandas, glob, os & seaborn. For the use of the ArcPy module an ArcGIS license is required. 

Zonal stats for geoparks were calculated manually in ArcGIS pro with the "zonal stats to table" tool
Results_lithology and results_soils were calculated manually in ArcGIS Pro as well, see methods section workflow and tools used. 

NB. All relative pathnames are examples from my local environment and should be changed according to the user's local folder structure. Scripts are numbered according to the order in which they should be executed. 

