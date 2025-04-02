# AIMGAF - Productivity Measurement and Gamification System

This project is a proof-of-concept designed to explore employee productivity in a factory setting can be measured and translated into a reward system. The project comprises three main components:

1. Dataset Generator – Generates employee performance data based on defined metrics.

2. Linear Programming – Uses generated productivity data to determine optimal task allocation.

3. Gamification – Creates leaderboards to reward efficiency and qualitative factors of employees.

## Installation

To set up the system, install the required dependencies:

```bash	
pip install -r requirements.txt
```

### Dependencies

- `holidays`
- `numpy`
- `pandas`
- `plotly`
- `plotly-express`
- `PuLP`
- `streamlit`
- `streamlit-lottie`


## Running the Application
Start the application using Streamlit:
```bash
streamlit run 1_Getting_Started.py
```

## Usage Guide
All of the functionality is accessible through the Streamlit interface with a home page that provides guidance on how to use the system. Regardless, a usage guide is included in here as well.
 
The application is divided into three main sections, each corresponding to a different module of the system. The following steps outline the process of using the application:

1. Generating a Dataset
   - Navigate to the Dataset Generator page.

   - Set the number of employees, equipment capacity, and operation difficulty.

   - Click Generate Dataset.

   - View and manage datasets in the interface.

2. Linear Programming Optimization

   - Navigate to the Linear Programming page.

   - Define work hour constraints for employees.

   - Click Build Dataframe to prepare data.

   - Click Solve LP Model to optimize allocation.

   - View results including task assignments and efficiency.

3. Gamification & Leaderboards

   - Navigate to the Gamification page.

   - Set leaderboard weight parameters.

   - Define Points per Star for productivity rankings.

   - Generate leaderboards by clicking Create Leaderboards.

   - View the global, productivity, and qualitative leaderboards.


## About

This project was developed during an internship at INOV as part of AIMGAF (Análise e Implementação de um Mecanismo de Gamification).