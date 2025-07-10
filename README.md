<br />
<div align="center">
    <!-- <img src="" alt="Logo" width="80" height="80"> -->
  </a>

  <h1 align="center">fashioNER</h2>

  <p align="center">
    Named entity recognition (NER) and sentence analyzer.
  </p>

</div>



## About fashioNER
<!-- <img src=""> -->

<p>fashioNER is an natural language processing (NLP) and computational linguistic exploratory project developed to analyze sentences about fashion-related products. This NER is trained to identify ~100 common product names and creates a data report about the descriptive words that appear nearby. The use case is to analyze listings or information about products from a search engine page. </p>


<p> 
This NER is trained off of google search data and built from a "blank" spaCy English model. spaCy's pre-trained "en_core_web_lg" model was used to prepare the linguistic analysis.
</p>

### Built with


[![Jupyter Notebook][Jupyter Notebook]][jupyter-url]

[![spaCy][spaCy]][spaCy-url]


## Getting Started

### Prerequisites

**Python 3.13.3**

### Setup
<ol>
  <li>
  Please clone this repository onto your local machine
  </li>
  <li>
  Open the terminal and cd into the fashioNER directory.
  </li>
  <li>
  Set Up Virtual Environment
    <ol>
        <li>Create venv: run 
            <code>python -m venv .venv</code>
          </li>
          <li> Activate venv: 
          <ul>
          <li>Mac: 
          <code>source .venv/bin/activate</code>
          </li>
          <li>Windows: 
          <code>.venv\Scripts\activate</code>
          </li>
          </ul>
        </li>
    </ol>
    </li>
      <li>
      Install Requirements
        <ol>
          <li>Upgrade pip: run 
            <code>pip install --upgrade pip</code> 
          </li>
          <li>Install requirements: run 
            <code>pip install -r requirements.txt</code> 
          </li>
          <li>
            Wait for intallation (can take a few minutes).
          </li>
        </ol>
    </li>
  </li>
  <li>
  Run Application in Jupyter Notebook
  <ol>
  <li>
    Open Jupyter notebook: run <code>jupyter notebook</code>
  </li>
  <li>
    The browser should open with the program inside, if it does not, please go to: http://localhost:8888/tree 
  </li>
  <li>
  Click into the <b>/project</b> directory and open the notebook file: <b>Main.ipynb</b>
  </li>
  </ol>
  </li>
</ol>

## Usage
### Input: 
The program accepts plain text (not a file) or an HTML file as input - **must** specify which type the input is when initializing the ProductModel.

<img src="./assets/images/input.jpeg">

#### HTML file input
I recommend using the first page of a product search on Google. This NER was trained on Google queries.
I recommend saving the body text:
<img src="assets/images/google_example.jpeg" > 
<!-- variables -->

[Jupyter Notebook]: https://img.shields.io/badge/Jupyter%20Notebook-F37626?style=flat-square&logo=jupyter&logoColor=white
[jupyter-url]: https://jupyter.org/
[spaCy]: https://img.shields.io/badge/NLP%20with-SpaCy-blue
[spaCy-url]: https://spacy.io/