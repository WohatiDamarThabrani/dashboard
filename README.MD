# Ecommerce Dashboard
## Setup Environment - Anaconda
conda create --name main-ds python=3.11.0 
conda activate main-ds  
pip install -r requirements.txt  

## Setup Environment - Shell/Terminal  
mkdir proyek_analisis_data  
cd proyek_analisis_data  
pipenv install  
pipenv shell  
pip install -r requirements.txt  

## Run streamlit app  
streamlit run dashboard/dashboard.py

