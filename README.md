# community

![Header](/docs/_static/images/header.png)

## About

* This repository is a static django website;
* It uses the [GCI private API](https://developers.google.com/open-source/gci/resources/downloads/TaskAPISpec.pdf)
* __Attention:__ This repository only re-publishes publicly available information
* Uses IGitt, supporting both GitHub & GitLab

## Deploy Netlify on your fork :

Following are the steps to deploy netlify on your forked ``community`` repository :

- Signup on [netlify](https://app.netlify.com/).
- Click on **New site from Git**.
- Choose **Git provider (Github) >** Choose a repository **< username >/community**.
- Branch to deploy **master**.
- Basic build settings :
  * Set Build command to **.ci/build.sh**.
  * Set Publish directory to **public**.
  * Click on **Show advanced >** **New variable** to add the `environment variables`.

After that to set the ``environment variables`` :

- Put **GH_TOKEN** in `Key` column and your generated `GitHub Access Token`
  in `Value` column.
- Similarly add other `variables` like **OH_TOKEN, GL_TOKEN** if needed.
- Click on **Deploy Site** to deploy the site.
