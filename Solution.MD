
<!-- ABOUT THE PROJECT -->
## About The Project


This is a simple REST API built with flask and MongoDB.

### Infrastructure decisions
  * Options considered:
    * SQL (any flavor)
    * NoSql databases
      * MongoDb
      * Cassandra
      * DynamoDB
  * SQL:
    * Great database for ACID compliance. (we don't need it for this application)
    * Vertical scaling 
    * This limits regional availability and requires replication of the database which is complex
    * Some flavors have inbuilt support for NoSql storage.
  * NoSql
    * MongoDb
      * Acid properties across documents.
      * Easy modelling and querying.
      * Horizontal scaling, with high availability.
      * Platform-agnostic (self hosted and managed).
      * Supports joins, multiple ranges etc .
      * Json based storage
    * Cassandra
      * Read optimized database.
      * Strict query first approach, to support additional queries a new model and rebuild is required.
      * Extremely high availability is possible with the right configurations for the right use cases.
      * Platform-agnostic (self hosted and managed)
      * Key-value storage.
    * DynamoDB
      * Heavy dependencies on AWS.(vendor locked)
      * Strict key-value store
      * Could become very expensive relatively soon
      * Not a lot of room for optimization, too few metrics.

  #### Decision
  I decided to use mongoDb as a backend store for multiple reasons, it provided an easy interface to work with.
  It's extremely flexible for any other use cases that might come in the future, which on production it always does.
  I have prior experience with it. 

  P.S: Any SQL database would have been a strong second with regards to other NoSql databases considered as most of them are key-value based strict databases. 

#### Code base structure
The code base tries to follow a strict separation of concerns principal.
The system is divided into 3 layers:
* View layer: responsible for dealing with request and response logic
* Service layer: complex business logic goes here, although there were not a lot
* I/O layer: Abstracts away any database or other form of I/O from the rest of the system.
  * This allows us to change the database / models while maintaining the same interface to the service layer


### Prerequisites

Make sure you are using a virtual env and have docker installed on the machine. 
cd into the root directory of this repository and run the following commands. 

NOTE: The script is meant for one time run. 
Please ensure the file sharing is for the folder of the project and subfolder is enabled,
such that mongo can retain state. 
For steps on how to do this, please search for "docker file sharing + {your os, windows / mac/ linux}
* docker
  ```
  docker-compose up -d 
  ```
* load data (please ensure to run in a virtual env)
  ```
  pip install -r requirements.txt
  python load_data_script.py
  ```
* Done, the test API should be available on localhost:5000/

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- EXAMPLES -->
## Buddywise API Documentation
### Employee Endpoints
#### Get Common Friends
Returns the common friends between two employees.

Request
```
GET /employee/get-common-friends
```


##### Query Parameters
```
emp1_id - ID of the first employee. Required.
emp2_id - ID of the second employee. Required.
```
##### Example Request
```http request
GET /employee/get-common-friends?emp1_id=1&emp2_id=2
```


##### Response
* employee_details - Details of both employees.
  * {employee_id} - Details of an employee with the given ID.
    * Name - The name of the employee.
    * Age - The age of the employee.
    * Phone - The phone number of the employee.
    * Address - The address of the employee.
    * common_friends - The list of IDs of the common friends between the two employees. 


##### Example Response
```json
{
    "employee_details": {
        "1": {
            "Name": "John",
            "Age": 30,
            "Phone": "1234567890",
            "Address": "123 Main St"
        },
        "2": {
            "Name": "Jane",
            "Age": 25,
            "Phone": "9876543210",
            "Address": "456 Elm St"
        }
    },
    "common_friends": ["3"]
}
```

#### Get Employee Details
Returns the details of a single employee.

##### Request
```http request
GET /employee/{id}
```

###### Path Parameters
id - ID of the employee to retrieve. Required.

###### Example Request
```http request
GET /employee/1
```

###### Response
* name - The name of the employee.
* age - The age of the employee.
* company - The name of the company the employee belongs to.
* fruits - The list of fruits the employee likes.
* vegetables - The list of vegetables the employee likes.

```json
{
    "name": "John",
    "age": 30,
    "company": "foo",
    "fruits": ["apple", "banana"],
    "vegetables": ["carrot"]
}

```


### Companies
Get all companies
```http request
GET /company/
```
Returns a list of all companies.

##### Response
```json
{
    "companies": ["1", "2"]
}

```

Get company by ID

```http request
GET /company/<company_id>
```
Returns the company with the specified ID.

##### Response
```json
{
    "name": "foo"
}
```

Get employees of a company
```http request
GET /company/<company_id>/employees
```
Returns a list of employees who work for the specified company.

##### Response
```json
{
    "employees": ["1", "2"]
}
```




```
