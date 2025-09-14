# WeatherApp

A simple web application built using **Streamlit** to check weather, compare cities, and save favorite cities locally.

## Features

* **Single City Weather**

  * Enter a city name and get current weather details.
  * Save the city to favorites.

* **Compare Cities**

  * Compare weather of two cities side-by-side.

* **Favorites**

  * View all saved favorite cities.
  * Remove cities from favorites.
  * Favorites persist locally even after closing the app.

## Folder Structure

```
WeatherApp/
├── .gitignore
├── requirements.txt
├── app.py
├── config.py            # contains API key
├── utils/
│   └── weather_api.py   # fetch weather from API
├── static/
│   └── styles.css       # custom styling
└── favorites.json       # local storage for favorites
```

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone <repo_url>
   cd WeatherApp
   ```

2. Setup Environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:

   * **Windows PowerShell**

     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```

   * **Windows cmd**

     ```cmd
     .\.venv\Scripts\activate.bat
     ```

   * **Linux / Mac**

     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Add your API key:

   Create `.env` file in the project root:

   ```python
   API_KEY = "YOUR_API_KEY_HERE"
   BASE_URL = "YOUR_BASE_URL"
   ```

   > Make sure `config.py` is added to `.gitignore` to protect your API key.

6. Run the Application:

   ```bash
   streamlit run app.py
   ```

Local URL: [http://localhost:8501](http://localhost:8501)

```

## Usage

- **Single City Tab**: Enter a city, click **Get Weather**, and optionally add to favorites.  
- **Compare Cities Tab**: Enter two cities, click **Compare** to view side-by-side weather.  
- **Favorites Tab**: View and remove favorite cities; changes are saved locally.
```
