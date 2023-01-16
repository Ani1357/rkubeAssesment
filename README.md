
  <h3 align="center">Simple Rest API Assesment</h3>
  <a name="readme-top"></a>




<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents:</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


This project is about creating an simple python app that list the blob files inside an Azure Blob Storage Container.
The app will use an App registration(service principal) for authorization/authentication to the azure API. The app will expose an endpoint where a REST API will be served.



### Built With

List any major frameworks/libraries used:

[Flask](https://flask.palletsprojects.com/en/2.2.x/) web framework
[Azure Python SDK](https://learn.microsoft.com/en-us/azure/developer/python/sdk/azure-sdk-overview) for communicating with Azure's API
[Flasgger](https://github.com/flasgger/flasgger) for the Swagger UI

<!-- GETTING STARTED -->
## Getting Started

Follow the steps below to install the application on your Kubernetes cluster. 

### Prerequisites

In oder to deploy the application you must have
* a Kubernetes cluster you can access (see **Creating the Azure resources** section)
* [kubectl installed](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) and a valid kubeconfig with which to connect to the cluster
* [helm installed](https://helm.sh/docs/intro/install/)
* the azure service principal credentials, azure storage account url and azure Blob storage container name (see **Creating the Azure resources** section)

#### Creating the Azure resources
1. Login to your azure account via azure-cli:
	* install [azure-cli](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
	* [sign in with azure-cli](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli)
2. Create a Blob Storage 
	* create a resource group 
		```bash
		# Set Resource Group Name 
		RGNAME="rkubes-rg"
		# Set Region (Location) or any other location
		LOCATION="westeurope"
		# Create Resource Group
		az group create -n $RGNAME -l $LOCATION
		```
	* create the blob 
		```bash
		#Set Storage Account Name.
		SA_NAME="rkubesblobstorage" # Must be globaly unique. If already in use try adding a random number as a suffix (ex. SA_NAME="rkubesblobstorage${RANDOM}")
		az storage account create --name  $SA_NAME --resource-group $RGNAME --location  $LOCATION --sku Standard_ZRS --encryption-services blob
		```
	* create a container 
		```bash
		# Set container name
		CONTAINER_NAME="democontainer"
		az storage container create --account-name $SA_NAME --name  $CONTAINER_NAME --auth-mode login
		```
3. Create a service principal
	* create a service principal 
		```bash
		# Set the service principal name
		SP_NAME="rkubesapp-sp"
		az ad sp create-for-rbac --name $SP_NAME
		 ```
		* note down the outputted credentials, will use them later
	* create a role 
		```bash
		# Get the blob storage resource id
		SA_ID=$(az storage account list --query "[?name=='${SA_NAME}'].id" -otsv)
		# Set AZURE_CLIENT_ID. It was outputed in Step 3.1 when creating the Service principal
		# It can also be printed via az cli as showed below
		AZURE_CLIENT_ID=$(az ad app list --query "[?displayName=='${SP_NAME}'].appId" -otsv)
		# Set the role name
		ROLE_NAME='rkubes_app_role'
		az role assignment create --assignee $AZURE_CLIENT_ID --scope $SA_ID --role $ROLE_NAME ```
4. Create the AKS Cluster: 

	```bash
	# Set Resource Group Name 
	AKS_RGNAME=otomi
	# Create Resource Group
	az group create -n $RGNAME -l $LOCATION
	# Set Cluster name
	NAME=quickstart
	CLUSTER_NAME=otomi-aks-$NAME
	
	# Create AKS cluster
	az aks create --name $CLUSTER_NAME \
	--resource-group $AKS_RGNAME \
	--location $LOCATION \
	--vm-set-type VirtualMachineScaleSets \
	--nodepool-name otomipool \
	--node-count 1 \
	--node-vm-size Standard_F8s_v2 \
	--kubernetes-version 1.23.8 \
	--enable-cluster-autoscaler \
	--min-count 1 \
	--max-count 3 \
	--max-pods 100 \
	--network-plugin azure \
	--network-policy calico \
	--outbound-type loadBalancer \
	--uptime-sla \
	--generate-ssh-keys
	```
5. Configure kubectl 
	```bash
	# Get the kubeconfig
	az aks get-credentials --overwrite-existing --admin -g $AKS_RGNAME -n $CLUSTER_NAME
	# Test it
	kubectl get ns 
	# It should show the default k8s namespaces
	```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation


1. Add the helm repo
	* `helm repo add redkubes https://ani.al/charts` 
2. Update the helm repo
   * `helm repo update`
3. Create a values file to configure the app
	* run this command to create a values file called myvalues.yaml  `helm show values rkubesapp/rkubesapp > myvalues.yaml`
	* edit the myvalues.yaml file by updating the desired values. The  app needs this values to work: 
	`azureClientID, azureClientSecret, azureTenantID, storageAccountUrl,containerName `
4. Install the helm chart `helm install rkubes rkubesapp/rkubesapp -f myvalues.yaml`

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

The app will will create a service of type clusterIP. One way to access the app is by port-forwarding the service to a local port by running `kubectl port-forward services/rkubes-rkubesapp 8080:80`. Now the app is reachable through `localhost:8080`. Browse `localhost:8080/files` to get the list of file inside the azure container.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] MVP Python Rest API
- [x] Docker image uploaded to docker hub
- [x] Helm chart created
- [x] Helm repository created
- [x] Helm chart available publicly
- [x] Deployed and tested in Azure
	- [x] Write a AKS installation guide 
- [ ] Deploy and test on minikube
	- [ ] Write a minikube installation guide
- [x] Deploy on top of OTOMI
- [x] Update the app with functional swagger UI

See the [open issues](https://github.com/Ani1357/rkubeAssesment/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - ani.argjiri@gmail.com

Project Link: [https://github.com/Ani1357/rkubeAssesment](https://github.com/Ani1357/rkubeAssesment)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
