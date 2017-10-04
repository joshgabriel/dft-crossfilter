<p align="center"><sup><strong>
DFT-CROSSFILTER
</strong></sup></p>
The Dft-Crossfiltering is a web platform that provides crossfiltering capabilities to users.
The aim of this platform is to support a dft benchmark data exposed to collaborators.
* **[SETUP](SETUP.md)** – setup instructions.
* **[LICENSE](LICENSE)** – the license.

# The platform components
UPDATED APP AND COMPLETE PACKAGE IS IN THE CompleteApp folder

## benchmark-db
Mongodb database for managing the dft data.
The models are design for ease of access from the API but also from the frontend.
It might be subjected to regular changes.

## benchmark-api
A python flask REST service that exposes the database access to the frontend.
The api endpoints have been organized to allow an ease for sending HTTP requests from
the frontend.

## benchmark
A python library for easily loading csv files by name without extension.
Not sure if this will not be deleted.

## bokeh apps 
bokeh apps prec_analysis and crossfiler_app which serve the frontend 
providing all the user interactive visualization. It makes calls to the api to
obtain the data.

## benchmark-precision
Library of python and R modules for the precision analysis.
