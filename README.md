  <h3 align="center">Simple Rest API Assesment</h3>





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


This project is about creating an app that list the blob files inside an Azure Blob Storage Container.
The app will use an App registration(service principal) for authorization/authentication to the azure API.



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

Python
Helm
Docker

<!-- GETTING STARTED -->
## Getting Started

Follow the steps below to install the application on your Kubernetes cluster. 

### Prerequisites

In oder to deploy the application you must have
* a Kubernetes cluster you can access
* kubectl installed and a valid kubeconfig with which to connect to the cluster
* helm installed
* the azure service principal credentials, azure storage account url and azure Blob storage container name 

#### Creating the Azure resources
1. Login to your azure account via azure-cli:
	* install [azure-cli](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
	* [sign in with azure-cli](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli)
2. Create a Blob Storage 
	* create a resource group `az group create {rg-name} --location {location}`
	* create the blob `az storage account create --name  {storage-account} --resource-group  {resource-group} --location  {location} --sku Standard_ZRS --encryption-services blob`
	* create a container `az storage container create --account-name  {storage-account} --name  {container} --auth-mode login`
3. Create a service principal
	* create a service principal `az ad sp create-for-rbac --name {service-principal-name}`
		* note down the outputted credentials, will use them later
	* create a role `
	az role assignment create --assignee  {appId} --scope /subscriptions/{subscriptionName} --role  {roleName} `

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
- [ ] Deploy on top of OTOMI
- [ ] Update the app with functional swagger UI

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



