# Homer postgresql subscription data handling
## Objective: To load and manage data from json file to postgresql database

#### Python code features:
<ul>
    <li> Create table into datbase </li>
    <li> Load data from Json file</li>
    <li> Insert records into postgresql database</li>
    <li> Featch records/fetch subscription frequencies from database</li>
    <li> Maintain atomicity of transactions</li>
</ul>

#### Assumptions made in porject developement:
<ul>
    <li> User has at least taken trial subscription i.e. subscription list can not be empty</li>
    <li> At one time, user can not be on both trial and paid subscription</li>
</ul>

#### Project flow:
<ul>
    <li> data.json :  Data which needs to process and insert in database</li>
    <li> db_credentials.ini :  Postgresql datbase credential for developement or production team</li>
    <li> Homer_db.py :  Python code to manage connection, cursor, transactions of a database</li>
    <li> homer_logs.log :  Log file to track, report or debug the code execution</li>
    <li> homer_test.py :  Main file to handle the code execution: It calls methods to create table, insert records and fetch user counts</li>
    <li> log_config.ini :  Log configuration file</li>
    <li> subscription.py : Handles fetch, insert and create query management </li>
    <li> util.py : It implements business logic to convert json data as per database format</li>
</ul>

#### Code execution steps

<ul>
    <li> Install require project dependencies - ignore if already installed</li>
    <li> Change datbase auth credentials in db_credentials.ini file</li>
    <li> Run homer_test.py - It will create table and insert records into database</li>
    <li> Run fetch_subscription_count() of homer_test.py to fetch subscription frequencies</li>
</ul>

#### User distribution based on subscription:
<strong>`{'Active Trial': 0, 'Expired Trial': 2, 'Active Subscription': 0, 'Expired Subscription': 3}` </strong>