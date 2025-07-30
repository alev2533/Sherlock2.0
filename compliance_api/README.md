# Sherlock Compliance API

## Index

1. [General Description](#general-description)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Environment Configuration](#environment-configuration)
5. [Local Deployment](#local-deployment)
6. [Deployment on Azure](#deployment-on-azure)
7. [Automated Deployment with GitHub Actions](#automated-deployment-with-github-actions)
8. [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)
9. [Additional Resources](#additional-resources)

## General Description

Sherlock is a solution developed for the Compliance team that uses web scraping to compile a list of news articles about potential clients and their shareholders. The articles found are processed with GenAI to identify potential reputational risks, generate recommendations, and consolidate these findings into a report.

The application allows:
- Uploading Excel files with information about entities to investigate
- Searching multiple news sources
- Analyzing results with GenAI to identify risks
- Generating consolidated reports in Excel format

## Prerequisites

### 1. Azure Account
- **Active Subscription**: Required to access Azure services.
- **Necessary Resources**:
  - Azure Function App (Plan type: Flex Consumption)
  - Azure OpenAI Service
  - Azure AI Document Intelligence

### 2. GitHub Account
- **Repository**: To host the source code.
- **Permissions**: Required to configure GitHub Actions.

### 3. Development Environment
- **Python 3.11**: Main programming language.
- **VS Code**: Code editor with extensions for Python, Azure Functions, Azure Account, and GitLens.

### 4. Necessary Tools
- **Git**: Version control.
- **Azure CLI**: Command-line interface to manage Azure resources.
- **Azure Functions Core Tools**: Tools to develop and test functions locally.

## Project Structure

1. **API Backend (FastAPI + Azure Functions)**
   - Serverless architecture with RESTful endpoints integrated with Azure.

2. **Azure OpenAI Services**
   - GPT-4o and text-embedding-ada-002 models for natural language processing.

3. **Free PyPDF Service**
   - Extracts content from PDF documents. No subscription required.

4. **Azure AI Document Intelligence**
   - OCR for scanned documents. Requires an Azure account and active subscription.

5. **ScrapingBee**
   - Distributed and efficient web scraping. Requires an account and subscription to access its services.

### API Endpoints

- **`/search`**: Performs a Google search given a string and returns an array of results of type GoogleSearch with up to 10 items.
- **`/scraping`**: Extracts content from a URL and returns it as part of an object of type GoogleSearch.
- **`/read-pdf`**: Extracts content from a PDF using PyPDF and Document Intelligence conditionally and returns it as part of an object of type GoogleSearch.
- **`/analyze`**: Calls AI models GPT-4o and text-embedding-ada-002 to interpret a piece of content and returns the interpretation as part of an object of type GoogleSearch.

## Environment Configuration

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/compliance_api.git
   cd compliance_api
   ```

2. **Set up virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install --no-cache-dir --upgrade -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp env_template.txt .env
   ```

   Required variables:
   ```env
   # ScrapingBee
   SCRAPINGBEE_API_KEY=""
   SCRAPINGBEE_NB_RESULTS="10"
   SCRAPINGBEE_COUNTRY_CODE="pe"
   SCRAPINGBEE_LANGUAGE="es"
   SCRAPINGBEE_NFPR="True"
   
   # Azure OpenAI
   AZURE_OPENAI_API_KEY=""
   AZURE_OPENAI_API_ENDPOINT=""
   AZURE_OPENAI_API_VERSION="2024-02-15-preview"
   AZURE_OPENAI_MODEL_1_DEPLOYMENT_NAME=""
   AZURE_OPENAI_MODEL_2_DEPLOYMENT_NAME=""
   AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME="text-embedding-ada-002"
   AZURE_OPENAI_CHAT_TEMPERATURE=0.2
   AZURE_OPENAI_CHAT_COMPLETION_CHOICES=1
   AZURE_OPENAI_CHAT_PRESENCE_PENALTY=0
   AZURE_OPENAI_CHAT_TOP_P=0.1
   
   # Document Intelligence
   DOCUMENT_INTELLIGENCE_ENDPOINT=""
   DOCUMENT_INTELLIGENCE_API_KEY=""
   ```

## Local Deployment

1. **Run the application locally**:
   ```bash
   python main.py
   ```

2. **Verify functionality**:
   - Access `http://localhost:8000` to verify that the API is running.

## Deployment on Azure

### Creating a Function App on Azure

#### Option A: From Azure Portal

1. **Access and Start**:
   - Go to [Azure Portal](https://portal.azure.com)
   - Search for "Function App" and click "+ Create"

2. **Basic Configuration**:
   - Subscription: [Your subscription]
   - Resource Group: Choose a name for your resource group
   - Name: Choose a name for your Function App
   - Publish: Code
   - Runtime Stack: Python 3.11
   - Region: East US
   - Operating System: Linux
   - Plan: Flex Consumption

#### Option B: From Azure CLI

1. **Create base resources**:
   ```bash
   az group create --name <resource-group-name> --location eastus
   az storage account create --name <storage-account-name> --location eastus --resource-group <resource-group-name> --sku Standard_LRS
   az functionapp create --name <function-app-name> --storage-account <storage-account-name> --resource-group <resource-group-name> --consumption-plan-location eastus --runtime python --runtime-version 3.11 --functions-version 4 --os-type Linux
   ```

   Make sure to replace `<resource-group-name>`, `<storage-account-name>`, and `<function-app-name>` with your preferred names.

## Automated Deployment with GitHub Actions

This section describes how to set up a CI/CD pipeline using GitHub Actions to automate the deployment of the Sherlock Compliance application on Azure Functions. This process ensures that every time a push is made to the main branch, the application is automatically deployed to Azure.

> 📚 **Official Documentation**: [Use GitHub Actions with Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-github-actions)

### Credential Setup

To configure automated deployment, it is necessary to establish the appropriate authentication credentials. The following steps are required:

1. **Prepare the Code**:
   ```bash
   git init
   git add .
   git commit -m "Initial version"
   git branch -M main
   git remote add origin https://github.com/your-username/compliance_api.git
   git push -u origin main
   ```
   > 📚 **Official Documentation**: [Introduction to Git](https://git-scm.com/doc)

2. **Configure GitHub Actions**:
   - In the Azure Portal, navigate to your **Function App**.
   - Go to **Deployment Center**.
   - Select **GitHub** as the deployment source.
   - Connect your GitHub repository.
   - Select the `main` branch for deployment.
   > 📚 **Official Documentation**: [Configure GitHub Actions in Azure](https://learn.microsoft.com/en-us/azure/app-service/deploy-github-actions)

3. **Set up Environment Variables**:
   - In the Azure Portal, navigate to **Function App > Configuration**.
   - Add the necessary environment variables from your `.env` file.

### Example Workflow for GitHub Actions

Below is an example workflow for the automated deployment of the application:

```yaml
# Docs for the Azure Web Apps Deploy action: https://github.com/azure/functions-action
# More GitHub Actions for Azure: https://github.com/Azure/actions
# More info on Python, GitHub Actions, and Azure Functions: https://aka.ms/python-webapps-actions

name: Build and deploy Python project to Azure Function App

on:
  push:
    branches:
      - main
  workflow_dispatch:

env:
  AZURE_FUNCTIONAPP_PACKAGE_PATH: '.' # set this to the path to your web app project, defaults to the repository root
  PYTHON_VERSION: '3.11' # set this to the python version to use (supports 3.6, 3.7, 3.8, 3.11)

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python version
        uses: actions/setup-python@v1
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Create and start virtual environment
        run: |
          python -m venv venv
          source venv/bin/activate

      - name: Install dependencies
        run: pip install -r requirements.txt

      # Optional: Add step to run tests here

      - name: Zip artifact for deployment
        run: zip release.zip ./* -r

      - name: Upload artifact for deployment job
        uses: actions/upload-artifact@v3
        with:
          name: python-app
          path: |
            release.zip
            !venv/

  deploy:
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: 'Production'
      url: ${{ steps.deploy-to-function.outputs.webapp-url }}

    steps:
      - name: Download artifact from build job
        uses: actions/download-artifact@v3
        with:
          name: python-app

      - name: Unzip artifact for deployment
        run: unzip release.zip

      - name: 'Deploy to Azure Functions'
        uses: Azure/functions-action@v1
        id: deploy-to-function
        with:
          app-name: '<your-function-app-name>' # Replace with your Function App name
          slot-name: 'Production'
          package: ${{ env.AZURE_FUNCTIONAPP_PACKAGE_PATH }}
          publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }} # Ensure this secret is set in GitHub
          scm-do-build-during-deployment: true
          enable-oryx-build: true
```

### Details to Replace:
- **`<your-function-app-name>`**: Replace this placeholder with the name of your Function App in Azure.
- **`AZURE_FUNCTIONAPP_PUBLISH_PROFILE`**: Ensure this secret is set in GitHub with your Function App's publish profile.

## Monitoring and Troubleshooting

### Log Review

1. **View logs in real-time**:
   ```bash
   az functionapp logs tail -g <resource-group-name> -n <function-app-name>
   ```

2. **Configure Application Insights**:
   - Review performance metrics and set up alerts.

## Additional Resources

### Official Documentation
- [Azure Functions Python](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Azure OpenAI](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Document Intelligence](https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/)
- [ScrapingBee API](https://www.scrapingbee.com/documentation/)
- [PyPDF Documentation](https://pypdf.readthedocs.io/en/latest/)

### Guides and Tutorials
- [Deploy to Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)
- [CI/CD with GitHub Actions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-how-to-github-actions)
- [Best Practices](https://docs.microsoft.com/en-us/azure/azure-functions/functions-best-practices)

### Tools
- [VS Code](https://code.visualstudio.com/)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/)
- [Postman](https://www.postman.com/)
- [Azure Storage Explorer](https://azure.microsoft.com/features/storage-explorer/)
