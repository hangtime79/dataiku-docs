# Working with Microsoft R

  * [1. What is Microsoft R?](#1-intro)
  * [2. How to set up Microsoft R in Dataiku?](#2-setup)
  
This app note gives an overview of "Microsoft R" and its different flavors, and explains how to configure it for Dataiku. 

<a name="1-intro"></a>

## 1. What is Microsoft R?

Microsoft R is mostly built on top of the acquisition of Revolution Analytics, and is in fact an umbrella designing different products:

### 1.1: Microsoft R Open

As taken from the [official website](https://mran.microsoft.com/rro):

> Microsoft R Open is the enhanced distribution of R from Microsoft Corporation. 
> The current release (as of December 2018), Microsoft R Open 3.5.1, is based the statistical language R-3.5.1 and 
> includes additional capabilities for improved performance, reproducibility and platform support.
> <br/> 
> Just like R, Microsoft R Open is open source and free to download, use, and share.
> <br/>
> Microsoft R Open includes:
> <ul>
>   <li>The open source R language, the most widely used statistics software in the world</li>
>   <li>Compatibility with all packages, scripts and applications that work with R-3.5.1</li>
>   <li>The installation of many packages include all base and recommended R packages plus a set of specialized packages released by Microsoft Corporation to further enhance your Microsoft R Open experience</li>
>   <li>Support for Windows and Linux-based platforms</li>
> </ul>
> <br/>
> Plus these key enhancements:
> <ul>
>   <li>Multi-threaded math libraries that brings multi-threaded computations to R.</li>
>   <li>A high-performance default CRAN repository that provide a consistent and static set of packages to all Microsoft R Open users.</li>
>   <li>The checkpoint package that make it easy to share R code and replicate results using specific R package versions.</li>
> </ul>

### 1.2: Microsoft R Client

As taken from the [official website](https://docs.microsoft.com/en-us/machine-learning-server/r-client/what-is-microsoft-r-client):

> Microsoft R Client is a free, community-supported, data science tool for high performance analytics. 
> R Client is built on top of Microsoft R Open so you can use any open-source R package to build your analytics. 
> Additionally, R Client includes the powerful RevoScaleR technology and its proprietary functions to benefit from parallelization and remote computing.
> <br/>
> R Client allows you to work with production data locally using the full set of RevoScaleR functions, but there are some constraints. 
> Data must fit in local memory, and processing is limited to two threads for RevoScaleR functions.

This version of R is interesting as it includes RevoScaleR functions.

> The [RevoScaleR library](https://docs.microsoft.com/en-us/machine-learning-server/r-reference/revoscaler/revoscaler) is a collection of portable, 
> scalable, and distributable R functions for importing, transforming, and analyzing data at scale. You can use it for descriptive statistics, 
> generalized linear models, k-means clustering, logistic regression, classification and regression trees, and decision forests.
> Functions run on the RevoScaleR interpreter, built on open-source R, engineered to leverage the multithreaded and multinode architecture of the host platform.

### 1.3: Microsoft R Server (now Machine Learning Server)

As taken from the [official website](https://docs.microsoft.com/en-us/machine-learning-server/what-is-machine-learning-server):

> Microsoft Machine Learning Server is your flexible enterprise platform for analyzing data at scale, building intelligent apps, 
> and discovering valuable insights across your business with full support for Python and R. Machine Learning Server meets the needs of 
> all constituents of the process – from data engineers and data scientists to line-of-business programmers and IT professionals. 
> It offers a choice of languages and features algorithmic innovation that brings the best of open-source and proprietary worlds together.
> <br/>
> R support is built on a legacy of Microsoft R Server 9.x and Revolution R Enterprise products. Significant machine learning and 
> AI capabilities enhancements have been made in every release. Python support was added in the previous release. Machine Learning Server 
> supports the full data science lifecycle of your Python-based analytics.
> <br/>
> Additionally, Machine Learning Server enables operationalization support so you can deploy your models to a 
> scalable grid for both batch and real-time scoring.

Note that the proper wording in "Machine Learning Server", and that most of the initial RevoScaleR capabilities in R have been ported to Python with 
similar API's. 

### 1.4: R Services for SQL Server (2016 and beyond)

A last possibility is to use [R directly in SQL Server](https://docs.microsoft.com/fr-fr/sql/advanced-analytics/what-is-sql-server-machine-learning?view=sql-server-2017):

> SQL Server 2017 Machine Learning Services is an add-on to a database engine instance, used for executing R and Python code on SQL Server. 
> Code runs in an extensibility framework, isolated from core engine processes, but fully available to relational data as stored procedures, 
> as T-SQL script containing R or Python statements, or as R or Python code containing T-SQL.
> <br/>
> If you previously used SQL Server 2016 R Services, Machine Learning Services in SQL Server 2017 is the next generation of R support, 
> with updated versions of base R, RevoScaleR, MicrosoftML, and other libraries introduced in 2016.
> <br/>
> In Azure SQL Database, Machine Learning Services (with R) is currently in public preview.
> <br/>
> The key value proposition of Machine Learning Services is the power of its enterprise R and Python packages to deliver advanced 
> analytics at scale, and the ability to bring calculations and processing to where the data resides, eliminating the need to pull 
> data across the network.


<a name="2-setup"></a>

## 2. How to set up Microsoft R in Dataiku?
 
Dataiku can use these 2 flavors in lieu of regular "CRAN" R:

* Microsoft R Open
* Microsoft R Client

**In case of a fresh Dataiku install**:

* Download Dataiku and run installer
* Install dependencies for R:
```sudo -i "/PATH-TO-DATAIKU-INSTALLER/scripts/install/install-deps.sh" -without-java -without-python -with-r```

If you wish to use Microsoft R Open (MRO):

* Download and install MRO following [the documentation](https://mran.microsoft.com/documents/rro/installation)
* Make sure that MRO is now the default R installation on your server by starting the interpreter (type `R` and look for startup message)
* Run the R integration (```./bin/dssadmin install-R-integration```)

If you wish to use Microsoft R Client (MRC):

* Download and install MRC following [the documentation](https://docs.microsoft.com/en-us/machine-learning-server/r-client/install-on-linux)
* Make sure that MRC is now the default R installation on your server by starting the interpreter (type `R` and look for startup message)
* Run the R integration (```./bin/dssadmin install-R-integration```)

**In case of an existing Dataiku install with R integration**:

* Remove the existing R packages in *DSS_DATA_DIR*/R.lib (```cd DATAIKU_DATA_DIR/R.lib && rm -rf *```)
* Install MRO or MRC as described above
* Rerun R integration script (```./bin/dssadmin install-R-integration```)

**Important remarks:**

* The main issue is to make sure that your system picks up the right R version. To do so, simple check where the R interpreter points 
to by typing - for instance, `ls -la $(which R)`; then change or create a symbolic link to the proper R version. MRC usually starts 
from `/opt/microsoft/rclient/VERSION/bin/R/R` and MRO from `/opt/microsoft/ropen/VERSION/lib64/R/bin/R`. As an example, if you want to 
make MRO the default, you could use ```ln -sf /opt/microsoft/ropen/VERSION/lib64/R/bin/R /usr/bin/R```.

* If there is an pre-existing R integration, you may always want to remove all existing packages in `DSS_DATA_DIR/R.lib` and re-run the `install-R-integration` script 
to get the proper packages version. 

<hr/>

**What about the other flavors?**

* *ML Server* (R Server) has not been tested but is highly unlikely, or at least very cumbersome, to work with Dataiku as Microsoft R needs 
to be located on the same physical server as Dataiku. Even if connectivity could be established, it would be hard to handle Datasets. 

* *R Services for SQL Server* may be usable from Dataiku but has not been tested in details. Limitations are not known so it is advised not 
to try to use it from Dataiku.

