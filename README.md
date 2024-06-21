# Proof of Concept: A Community-Based Collaborative Federated Learning Development and Automation Framework

> **_Please note:_** This project utilizes Federated Learning source code based on the repository mentioned in the Acknowledgments section.

## Description:

- This project provides a virtual research environment for community-based collaborative Federated Learning.
- Our FL workflows include 12 training rounds of federated learning based on MNIST dataset.
- Since we focus on Decentralized Federated learning scenario, our CWL workflow randomly selects one of the clients to act as the aggregator for each training round, updating the global model from the received client weights.

## Federation Structure :

- Federation structure in this demo:

  - Clients: We have used Github actions to create docker images and terraform templates (Clients fodler) to create client nodes and to deploy the docker containers, or we assume all clients participating in the Federated Learning experiments are running the necessary docker dontainers. In our demo we used AWS EC2 instances, GCP Compute Engine and Private Cloud Virtual Machines to represent FL client nodes.

  - Communication server: This is a simple server used by the client docker containers to send their availability and participate in the FL experiments. The server is created with the following terraform template : `Actions_workflow/main.tf`. Before that ensure to create a communication server docker image from `docker_compose_files/decentralized_compose.yml` based on your communication server architecture (x86 or ARM).

## Architecture

![architecture_final](https://github.com/anandanlk/community_based_fl/blob/master/Architecture.jpg)

## Video demonstration

## Using this demo: https://github.com/anandanlk/community_based_fl/blob/master/Demo/Demo.mp4

> **_Please note:_** We are not responsible for any use or misuse of the code or its consequences. For example we are not responsible for any expenses if you are using your own AWS or GCP account while using this demo nor for any security concerns.

- Changes needed:

  - Creating docker images for client training based on `Dockers_source_code/client_training`, `Dockers_source_code/client_registration` and `Dockers_source_code/communication_server` and pushing them to your own docker hub to be used in the experiments, or use our Github action workflows.
  - Change the docker compose file `docker_compose_files/decentralized_compose.yml` with the name of your docker images
  - Change the terraform template of the communication server based on your own aws configuration and your own name for the `Dockers_source_code/communication_server` docker image created.

- FL clients state before running the experiment:

  - Clients that want to participate in the FL experiments should be running the docker compose file `docker_compose_files/decentralized_compose.yml` and also have created an empty weight file in their directory with `.pt` extension.

- Experiment Setup:
  Assuming you have already forked/cloned the Git repository. The data, 'client_centralized_compose.yml' and 'client_compose.yml' files are available at https://github.com/anandanlk/Compose. This will be automatically pulled to clients when using our Terraform templates or GitHub actions workflows.

  Option1: If you are creating communication server(Template is available in the Actions folder) and docker images yourself then you can keep the git repository as it is. Ensure to create docker images for both x86 and ARM based architecture. You can create the images for both architecture in a single machine using Docker buildx. Same docker image name can hold both images and no need to create two images.

  Option2: If you are want to use the provided GitHub Action workflows to create Communicaiton server and to update 'client_register_test' docker then follow this step.
  Seperate the 'decentralised_fl' and 'fl_portal' folder contents directly(without the folders fl_portal and decentralised_fl) into two git repositories to ensure the .github/workflows from 'decentralised_fl' are in the root directory of the Git repository. Ensure both repositories are under the same root directory in your machine. The Github action workflow will take care of creating docker images for both architecture x86 and ARM.

  anyname (Main directory)
  \folder1 (Git Repo 1 - fl_portal contents)
  \folder2 (Git Repo 2 - decentralised_fl contents)

1. FL Portal Setup
   1.1 Install Python 3.12 and create virtual environment
   1.2 Install the requirements for the backend (pip install -r requirements.txt)
   1.3 Install npm for the backend project
   1.4 Install MongoDB and configure it in fl_portal\backend\config\config.py
   1.5 start the frontend and backend using ./bstart.sh and ./fstart.sh (Ensure required permissions)
   1.4 Jupyter Lab Extension setup
   1.4.1 Install npm
   1.4.2 Build (npm run build)
   1.4.3 jupyter labextension install .
   1.4.4 jupyter lab build
   1.4.5 jupyter labextension enable communityfl
   Note: Once Communication server is up and running, update the communicaiton server IP in fl_portal\backend\config\config.py

2. Decentralised FL Setup
   2.1. Create the following github actions secrets in based on your AWS account:

   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - DOCKER_PASSWORD
   - DOCKER_USERNAME

   For GCP, Install required CLI as per the instruction from GCP. You can also use any other cloud providers.

   2.2. Replace tags based on your dockerhub name in the following github actions workflows: `decentralised_fl/.github/workflows/Create Docker Client Decentralised.yml`, `decentralised_fl/.github/workflows/Create Communication Server and update Registration Docker.yml`

3.3 Terraform templates are in the Clients Folder

3.4 Run 'Create Client Decentralised Docker.yml' github action to create 'client_decentralized' docker. (or) Create on your own for both x86 and ARM architecture.

3.5 Run Create 'Create Communication Server and update Registration Docker.yml' github action to create 'communication server' and also to create or update 'client_register_test' docker with Communication IP. If the client_registration_test docker already running in client, this action will trigger watchtower docker and that will update the client_registration_test docker in client. terraform template to create the communication server is under the 'Actions' folder. Change the configurations as required.

Experiment:

1. Update the newly created communicaiton server IP in fl_portal\backend\config\config.py
2. Launch Jupyter Lab
3. Click on the communityfl portal
4. Register and login to the portal
5. Discover Clients
6. The newly created clients IPs will appear in this page (This might take some time, wait for the client dockers to up and run)
7. Click Initiate FL button and wait for the results.

## Acknowledgements

This project uses code from the following sources:

- A Kontomaris, Chronis (2023) CWL-FLOps: A Novel Method for Federated Learning Operations at Scale [https://github.com/CWL-FLOps/DecentralizedFL-CWL]

- Shaoxiong Ji. (2018, March 30). A PyTorch Implementation of Federated Learning. Zenodo. [http://doi.org/10.5281/zenodo.4321561](http://doi.org/10.5281/zenodo.4321561)
