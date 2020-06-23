# Curative COVID-19 Test Returns Portal

A lightweight returns portal to service Curative Inc. COVID-19 test returns.
- Return shipping labels powered by [ShipEngine API](https://www.shipengine.com/ "ShipEngine Homepage")

To run this locally you will need to download `pipenv` so you can easily pull the projects dependencies.
- [Install Pipenv](https://pipenv.pypa.io/en/latest/install/ "Install Pipenv")
    - Once you have installed `pipenv` you will need to run the following commands.
    ```bash 
    pipenv install
    ```
    - That will pull all necessary dependencies and you can run the project by running `pipenv shell` to start the python virtual environment.
    - *Start the Server:*
    ```bash
    python run.py
    ```
    - Visit [http://localhost:5005/](http://localhost:5005/ "Curative Returns Portal - Local")