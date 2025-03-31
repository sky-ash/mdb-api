# MdB API Microservice
> 2025-03-31, Distributed Systems

---

A Python microservice using FastAPI that acts as a wrapper to the external mdb-data API, allowing you to search German Bundestag members (MdB) by name.
Includes:

- Development using FastAPI and Python
- Local deployment
- Dockerized deployment
- Kubernetes deployment w/ Minikube  
- Centralized config via `.env` file 

---

- [Getting Started](#getting-started)
  - [Important Notes](#important-notes)
  - [Prerequisites](#prerequisites)
  - [Installing Prerequisites](#installing-prerequisites)
- [Deployment](#deployment)
  - [Setup](#0-setup)
  - [Local Deployment](#1-local-deployment-using-python-virtual-environment)
  - [Docker Deployment](#2-docker-deployment)
  - [Kubernetes Deployment](#3-kubernetes-deployment)
- [API Testing](#api-testing)
    - [Health Check](#0-health-check)
    - [Successful response (200 OK)](#1-successful-response-200-ok)
    - [No results (204 No Content)](#2-no-results-204-no-content)
    - [Invalid API key (401 Unauthorized)](#3-invalid-api-key-401-unauthorized)
    - [Timeout simulation (504 Gateway Timeout)](#4-timeout-simulation-504-gateway-timeout)


---

## 🚀 Getting Started
### Imporant Notice
- This Project has been tested on **Windows 11** and **Arch Linux**
  Should also work on **macOS** — use the Linux instructions.
- For Windows Users: If using PowerShell and you encounter `ExecutionPolicy` errors, try"

    ```shell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    ```

- for the simplest experience, run all commands in **CMD** or a bash-like terminal (e.g. Git Bash, WSL).

---

### Prerequisites
- Git (optional – needed if cloning instead of downloading)
- Python 3.8+ (with `pip` and `venv`)
- Docker
- Minikube and `kubectl` (for Kubernetes Deployment)
- Something to access the REST API, like `curl` or Postman


#### Verify installation

```bash
python --version
pip --version
docker --version
minikube version
kubectl version --client
curl --version
git --version
```

if any of the commands return an error, the tool is not installed or not in the PATH.

---

### Installing Prerequisites

#### **Windows** 

<details><summary>using <strong>winget</strong></summary>

```shell
winget install Python.Python Git.Git Docker.DockerCLI cURL.cURL Kubernetes.minikube Kubernetes.kubectl
```
</details>

<details><summary>using <strong>chocolatey</strong></summary>

```shell
choco install python git docker-cli curl minikube kubernetes-cli
```
</details>

---

#### **macOS** 

<details><summary>using <strong>homebrew</strong></summary>

```bash
brew install python git docker curl
```
</details>

---

#### **Linux** 

<details><summary>using <strong>pacman</strong></summary>

```bash
sudo pacman -S python git docker curl minikube kubectl
```
</details>

<details><summary>using <strong>apt</strong></summary>

```bash
sudo apt-get install python3 python3-pip git docker.io curl
```
</details>


---

## ⚙️ Deployment

### Setup

#### 1. Clone or download

 - Clone the repository from GitHub and `cd` into the folder:


    ```bash
    git clone https://github.com/sky-ash/mdb-api.git
    cd mdb-api
    ```

    Or download the ZIP, extract it, and `cd` into the folder manually.

---

#### 2. Set up your `.env` file

 - Create a `.env` file in the project root. 

    To use the provided [`template.env`](./template.env) as a base:

    ```bash
    mv template.env .env
    ```

 - Write your API key to access the mdb-data service in the `.env` file:

    ```bash
    MDB_DATA_READ_TOKEN=<your_api_key> 
    ```

    Simply replace `<your_api_key>` with the token you received for the mdb-data service.

 - The default values for local deployment (defined in `env.py`, see [here](./app/env.py)) can also be found in the `template.env` file:

    ```bash
    MDB_API_HOST=0.0.0.0
    MDB_API_PORT=8002
    RESPONSE_TIMEOUT=2
    MDB_DATA_BASE_URL=http://127.0.0.1:8001
    ```

    You can uncomment and modify them here if needed.

 - When deploying as a container, the default value for `MDB_DATA_BASE_URL` will be overwritten by the `Dockerfile` (see [here](./Dockerfile))

    ```Dockerfile 
    ENV MDB_DATA_BASE_URL="http://mdb-data:8001"
    ```

    This is the URL needed inside the container, as it will not be able to access the host machine directly.
    
> The other variables are also read from the `.env`, including the API key.
    So you only have to set it once for all kinds of deployment.


<details><summary><b>Environment Variables: Overview</b></summary>
<table>
    <thead>
        <tr>
            <th>Variable</th>
            <th>Required?</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>MDB_DATA_READ_TOKEN</td>
            <td>yes</td>
            <td>The read token for the mdb-data service</td>
        </tr>
        <tr>
            <td>MDB_API_HOST</td>
            <td>optional</td>
            <td>The host address the API will listen on</td>
        </tr>
        <tr>
            <td>MDB_API_PORT</td>
            <td>optional</td>
            <td>The port the API will listen on</td>
        </tr>
        <tr>
            <td>RESPONSE_TIMEOUT</td>
            <td>optional</td>
            <td>The timeout in seconds for the API to wait for a response from mdb-data</td>
        </tr>
        <tr>
            <td>MDB_DATA_BASE_URL</td>
            <td>optional</td>
            <td>The base URL of the mdb-data service (where the mdb-api gets its raw data from)</td>
        </tr>
    </tbody>
</table>
</details>


---

### Local Deployment (with Python)

#### 1. Start the `mdb-data` backend

- This service acts as a backend, providing the data for the API.


    ```bash
    docker network create dhbw
    docker run --name mdb-data -dp 8001:8001 \
      --network dhbw --env DELAY=0 haraldu/mdb-data:1
    ```

    The network `dhbw` will contain both the `mdb-data` and `mdb-api` containers, allowing them to communicate with each other.
    
> The `--env DELAY=0` flag sets the delay of the responses from the mdb-data service to 0 seconds.
    You can increase this value to simulate a slow connection and test the API's timeout functionality.

#### 2. Create a virtual environment and install dependencies

- Create a new virtual environment and activate it:

    <details><summary>using<strong> Windows</strong></summary>

    ```shell
    python -m venv .venv
    .venv\Scripts\activate
    ```

    </details>
    <details><summary>using<strong> Linux</strong> or <strong> macOS</strong></summary>

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

    </details>

---

- Install the required dependencies:

    ```bash
    pip install --no-cache-dir -r requirements.txt
    ```
    The `--no-cache-dir` flag is optional, but ensures that the latest versions of the packages are installed.

#### 3. Run the Python microservice

- launch the API using the following command:

    ```bash
    python -m app.main
    ```
    
    This executes a `uvicorn` command specified in [`main.py`](./app/main.py) file, which starts the FastAPI server.

    The API is now running and listening on the specified host and port, e.g.: [http://127.0.0.1:8002](http://localhost:8002))  




> You will be redirected to the [`'/redoc'`](http://localhost:8002) page, which shows the API documentation using ReDoc.
You can also access the Swagger UI at [`/docs`](http://localhost:8002/docs).

---

### Docker Deployment


---



#### 1. Remove existing containers and networks

- Remove any existing containers and networks that may interfere with the deployment.

    <details><summary><strong>you can use this command</strong></summary>

    ```bash
    docker stop mdb-data
    docker rm mdb-data
    docker stop mdb-api
    docker rm mdb-api
    docker network rm dhbw
    ```

    This will remove any existing containers and networks with the same names, enxuring all the following steps work as expected.

    </details>

> Recommended if you have previously deployed the containers and are following the instructions again.



---



#### 2. Build the image

```bash
docker build -t mdb-api .
```


---



#### 3. Start `mdb-data` service

```bash
docker network create dhbw

docker run --name mdb-data -dp 8001:8001 \
  --network dhbw \
  --env DELAY=0 \
  haraldu/mdb-data:1
```


---


#### 4. Run `mdb-api` container

```bash
docker run --name mdb-api -dp 8002:8002 \
  --network dhbw \
  --env-file .env \
  mdb-api
```

- Uses the same `.env` file from local development
> API is now available at [http://localhost:8002](http://localhost:8002)



---



### Deployment with Kubernetes (Minikube)

---

#### 1. Remove existing containers & deployments

##### Containers & Networks

> use the same command as in the previous section to remove existing containers and networks.

<details><summary>Remove container artifacts and existing networks</summary>

```
docker stop mdb-data
docker rm mdb-data
docker stop mdb-api
docker rm mdb-api
docker network rm dhbw
```

</details>


##### Existing Deployments 

```
kubectl delete -f deployment/
kubectl delete -f mdb-data-service/deployment/
```


#### 2. Launch Minikube

- make sure minikube is running
- if not, launch it

    ```
    minikube start
    ```

#### 3. Build & Load Image

- build mdb-api image from the `Dockerfile` 

    ```bash
    docker build -t mdb-api .
    ```

    now load the image into `minikube` (once it is running):

    ```bash
    minikube image load mdb-api:latest
    ```
#### 4. Deployment

- apply the deployment files to the minikube cluster

    ```
    kubectl apply -f deployment/
    kubectl apply -f mdb-data-service/deployment/
    ```
    - files for the mdb-api:            [`deployment/`](./deployment/)  
    - files for the mdb-data-service:   [`mdb-data-service/deployment/`](./mdb-data-service/deployment/) 


#### 5. Check Status & Open API in Browser


- check if the pods are running

    ```
    kubectl get pods
    ```
    you should see the following output:

    ```
    NAME                        READY   STATUS    RESTARTS   AGE
    mdb-api-<id>                1/1     Running   0          1m
    mdb-data-<id>               1/1     Running   0          1m
    ```

    Wait until both pods are in the `Running` state.

- open the API documentation in browser by running:

    ```
    minikube service mdb-api
    ``` 

---


## 🧪 API Testing

You can test the MDB-API service using any HTTP client like Postman, or use `curl` to follow along with the examples below.


> 💡 On Windows CMD, don't use single quotes – use double quotes:
> ```cmd
> curl -i "http://localhost:8002/api/v1/getByName?name=scholz"
> ```
> The examples below all use this pattern. On Linux, you can use both single and double quotes.

---

#### 0. Health Check

This endpoint lets you verify that the API service is running:

```bash
curl "http://localhost:8002/health"
```

Expected response:

```json
{"status":"UP"}
```

---

#### 1. Successful response (200 OK)

```bash
curl "http://localhost:8002/api/v1/getByName?name=scholz"
```

Example output:

```json
[{"id":"7506","titel":"Olaf Scholz, Bundeskanzl."}]
```

✔ Works for names with one or multiple matches (e.g. `Lindner`, `Gysi`, `Riexinger`)

---

#### 2. No results (204 No Content)

```bash
curl -i "http://localhost:8002/api/v1/getByName?name=doesnotexist"
```

Response:

```
HTTP/1.1 204 No Content
```

---

#### 3. Invalid API key (401 Unauthorized)

To simulate this:

1. Open your `.env` file
2. Replace the real token with a fake one like:

   ```env
   MDB_DATA_READ_TOKEN=INVALID_TOKEN
   ```

3. Restart the service

Now try:

```bash
curl -i "http://localhost:8002/api/v1/getByName?name=scholz"
```

Expected output:

```
HTTP/1.1 401 Unauthorized
{"detail":"Error 401: Invalid credentials"}
```

---

#### 4. Timeout simulation (504 Gateway Timeout)

To test this, start the `mdb-data` container with an artificial delay:

```bash
docker run --name mdb-data -dp 8001:8001 \
  --network dhbw \
  --env DELAY=5 \
  haraldu/mdb-data:1
```

Make sure the delay exceeds your `RESPONSE_TIMEOUT` (default is 2 seconds). Then restart `mdb-api` and test again:

```bash
curl -i "http://localhost:8002/api/v1/getByName?name=scholz"
```

Expected output:

```
HTTP/1.1 504 Gateway Timeout
{"detail":"Error 504: Gateway timeout"}
```

