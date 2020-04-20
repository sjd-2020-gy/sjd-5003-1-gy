# Agent / Environment Interaction
---
This application was contructed during the study of  
&emsp;&emsp;GEOG5003M - Programming for Geographical Information Analysis,  
&emsp;&emsp;University of Leeds.  

The application primarily takes one or more an "Agents" (sheep) and moves each around and interacts with a 300 x 300 raster (environment).  

A second set of "Agents" (Wolf) was introduced to hunt and kill the sheep.

A GUI front-end was added to allow defautls to be overridden.


---
### Contents of Repository

##### Application Files
* modelhome.py  
* modelmain.py  
* agentframework.py  
  
##### Execution Preparation
Copy all .py files (3) to folder of choice.


---
### Run Instructions

##### With GUI
At command prompt, enter:

&emsp;&emsp;***python modelhome.py***  


##### Without GUI
At command prompt, enter:

&emsp;&emsp;***python modelmain.py***  

with any or all of the following optional arguments:  

| --- | --- |  
| ***&#x2010;&#x2010;agents n*** | where n = Number of Agents (numeric) |  
| ***&#x2010;&#x2010;defaults x*** | where x = Use default Agent start locations (Y/N*) |  
| ***&#x2010;&#x2010;moves n*** | where n = Number of Agent & Wolf moves (numeric) |  
| ***&#x2010;&#x2010;distance n*** | where n = Distance considered to be a neighbour (numeric) |  
| ***&#x2010;&#x2010;wolves n*** | where n = Number of wolves in Wolf Pack (numeric) |  
| ***&#x2010;&#x2010;plotstart x*** | where x = Show starting location of Agents & Wolf Pack (Y/N*) |  
| ***&#x2010;&#x2010;dispagents x*** | where x = Display Agent summary data (Y/N*) |  
| ***&#x2010;&#x2010;dispwolves x*** | where x = Display Wolf summary data (Y/N*) |  
| ***&#x2010;&#x2010;dispparams x*** | where x = Display Parameter Data (Y/N*) |  

*Any other value will be treat as if a N


---
###### Author Details 
Name: To be advised after marking
Student Id: 201388212 
Course: Master of Science - Geographical Information Science  
Unit: GEOG5003M - Programming for Geographical Information Analysis (36393)  
Published Date: 20 April 2020

---
###### License Details 
URL: //https://sjd-2020-gy.github.io/sjd-5003-1-gy/license/
