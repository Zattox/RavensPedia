<!--Installation-->
## Installation
1. Cloning the repository

```git clone https://github.com/Zattox/RavensPedia.git```

2. Installation of poetry
 
The installation process is described [here](https://www.jetbrains.com/help/pycharm/poetry.html#install-poetry)

3. Installing dependencies
 
Go to the project folder, then write in the terminal ```poetry install```

4. Creating Environment variables

Create a ```.env``` file in the root folder of the project and enter your environment variable values: ```FACEIT_BASE_URL``` и ```FACEIT_API_KEY```

5. Getting FACEIT_BASE_URL
   
There are different versions of the API, and the code describes how to interact with version 4 ```https://open.faceit.com/data/v4/matches```, more details [here](https://docs.faceit.com/docs/data-api/data/#tag/Matches/operation/getMatchStats)

6. Getting FACEIT_API_KEY
   
Getting the API_KEY is described [here](https://developers.faceit.com/docs/auth/api-keys)
