# AWS Assisted Pipeline for Research Participant Management
## Final Project, Large Scale Computing Spring 2021
## Max Kramer
---

### Table of Contents

|Section|
|---|
|[Problem Description](#problem-description)|
|[Pipeline Overview](#pipeline-overview)|
|[Addressing the Problem](#addressing-the-problem)|
|[Limitations](#limitations)|


### Problem Description

My work in the BrainBridge lab during COVID-19 has highlighted the importance of online data collection protocols for psychological research. The existence of platforms like Amazon Mechanical Turk and Prolific has created an alternative method for researchers to collect participant data. While these platforms are increasingly popular for data collection, they require training in AMT’s online environment and are not fully customizable. This extends to both the formatting of online experiments as well as data handling procedures. While AMT’s environment is well suited to the deployment of actual tasks, it is not as well suited to the “ingest” of participants into a study. 

The ingest of participants is usually an arduous task for researchers, especially for studies that require a large participant base. Collecting certain demographic information, determining if someone can be included in a study based on certain features, and managing communications usually involves a carefully orchestrated effort between researchers, lab managers, and IRBs. The protocol for preparing participants to enter a study is also a key focus of Institutional Review Boards (IRBs) who monitor ongoing research at Universities to ensure compliance with ethical standards and the law. While IRBs do have protocols in place for both in-lab and online experiments, there is not always perfect agreement between what the online platforms require and what the IRB deems appropriate. 

The overarching goal of my project is to develop a software pipeline that is flexible and customizable, allowing either experiments in the lab or participants on their devices to provide contact and demographic information, receive communications from experimenters (including critical IRB documents), and provide information for experiments such as Ecological Momentary Assessment (EMA) paradigms. It is my hope that this pipeline enables researchers with little to no python programming experience to leverage large-scale computing techniques to automate as much of the ingest as possible. This pipeline has the added benefit of customizability, which can be critical in settings where experimental designs are not often repeated or the guidelines by which one selects participants changes.

### Overview of the Pipeline

#### Ingest - [Script](https://github.com/lsc4ss-s21/final-project-aws-participant-ingest-pipeline/blob/master/participant_ingest.py)

The first phase of the pipeline is `participant_ingest.py`, a basic python script that allows a researcher to upload participant data to a CSV file, which is then pushed to a private Amazon S3 bucket. This script depends only on `boto3`, a python API for Amazon Web Services that handles the uploading of data to S3 in preparation for the other stages of the pipeline which exist inside of the AWS ecosystem. The script uses python’s `argparse` library to decide between one of two possible uploading mechanisms.

Supplying the command : `python3 participant_ingest.py -m` 

Engages the manual upload mode, which will prompt the user to enter the number of participants they wish to enter and then prompt for whatever details are contained within the **FIELDS** constant.

If the user instead does not supply the `-m` flag, the system will enter automatic upload mode, which takes a premade CSV file and either creates the ingest_output.csv file or amends new data to it before pushing the data to S3. 

#### Acceptance/Rejection Filtering - [Interactive Notebook]()

The notebook `Data_filtering.ipynb` serves as the second stage of the pipeline. This interactive notebook begins by engaging a boto3 client for both S3 (data) and SNS (communication). After reading in the output from the ingest python script, the notebook utilizes the `Ipywidget` package, an interactive graphical element library to allow for selective filtering of the dataset based on constraints. By identifying certain rows that meet those constraints, one can filter which participants will enter the study and which will not. The added benefit of SNS allows the researcher to then extract the email or phone number from the participants to either inform them of their acceptance or rejection into the study. 

#### IRB Informed Consent Distribution - [Notebook](https://github.com/lsc4ss-s21/final-project-aws-participant-ingest-pipeline/blob/master/Participant_Contact.ipynb)

The final stage of the pipeline is `Participant_IRB.ipynb`, which is another interactive notebook that allows for the communication of IRB informed consent forms to participants. After initializing boto3 clients and reading in the output from the prior notebook, the notebook uses SNS to subscribe each accepted participant to a given SNS channel based on their indicated preferred language. The use of multiple SNS topics allows for the translation of IRB informed consent forms into the preferred language automatically using AWS translate. The notebook loads in a file `IRB.txt` that can be filled with a given IRB consent form and then translates the form into each preferred language that is present in the dataset. The notebook ends by publishing a message containing the translated IRB form in the correct language to each accepted participant, sending on both the email and SMS channels. The form contains response information for either giving or refusing consent to participate in the study. 

### Addressing the Problem

This pipeline should allow for a relatively customizable and flexible environment for the ingest of participants into research studies. The composable and expandable infrastructure of AWS allows for easy expansion in the case of a high number of participants. The main advantage of utilizing this pipeline over a built-in solution on a platform like AMT or Prolific is the customizable nature of python code. The pipeline contains very few dependencies and relatively straightforward programming. The use of S3 could be overcome with local storage if a researcher prefers not to have their data handled by a third party or if an IRB forbids it for a given study due to the presence of Personally Identifiable Information (PII). This approach also has the potential to be distributed easily to researchers via github and requires minimal training. In smaller experiments, the entire pipeline can be completed in a matter of minutes, while any complicated operations are handled cleanly by AWS with only a minimal amount of python coding required.

### Limitations 

While the pipeline has advantages over AMT, there are definitely drawbacks. While the ingest script does not take long to process even tens of thousands of participants (approximately 0.08 seconds for 10,000 participants, due to speed of dictionary operations in python), the subscription and publication of messages via SNS will take proportionately longer when there are a large number of participants. This could likely be improved in the future using some form of parallelization across multiple EC2 instances, but was not implemented in this project due to time constraints. Another potential pipeline component that did not make it before the deadline was to have a dashboard for visualizing summary data from the demographic information collected by the ingest script. This dashboard could also take advantage of Ipywidgets to create interactive visualizations that could serve as the first step in statistical analysis of research findings. 

