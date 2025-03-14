
To create a new study in the Open Data Manager, follow these steps:

1. Click on **Create new study**: Start by selecting the option to create a New Study on the main dashboard (a) or from 
the menu in the top left corner, then click on “Create a New Study” (b).
2. **Assign a Name**: Give your study a descriptive name to identify it easily.
3. **Select the Template**: Choose the template you want to use for your study. Templates define the metadata structure 
and validation rules for your study. You can create your own template, and there is no limit on the number of templates you can use.

!!! tip "Understanding Templates"
    For more information about what a template is and how it works, refer to 
    the [Key Concepts section](../key-concepts/key-concepts.md)). This section provides definitions and details about templates, including how to 
    create and edit them. Explore the [Templates section](../doc-odm-user-guide/template-editor.md) if you require more information or need detailed guidance.

![create-study.gif](../doc-odm-user-guide/doc-odm-user-guide/gifs/create-study.gif)

## Explore Study Details

Once you click on **Create**, a new study will be automatically created, and you will be redirected to it. Here, you can explore the various tabs and features that are available.

The study will open in a new tab, where the following tabs can be explored:

* **Study**: Study refers to the foundational framework for a research project. It includes essential details such as the study's objective, hypotheses, experimental design, and statistical methods. The Study tab serves as the starting point for data organization, setting the stage for all subsequent data collection and analysis activities.
* **Samples Metadata**: Samples Metadata refers to the detailed information about the biological samples used in the study. This includes critical attributes such as tissue type, disease status, treatment conditions, and other relevant biological descriptors. Accurate documentation of sample metadata is crucial for reproducibility and for understanding the context and variability of the data.
* **+More:** The **+More** tab offers the possibility to upload and link **Libraries/Preparations.** This optional tab in ODM is used to document the methods and protocols for sample preparation, as well as the libraries generated from these samples. This can include details about sequencing libraries, reagent batches, and preparation protocols. Including this information helps in understanding the provenance and quality of the data, which is essential for data interpretation and reproducibility.
* **Data**: The Data section encompasses the actual raw or processed experimental data generated from the study. This includes primary outputs such as sequence reads, imaging data, or any other type of experimental measurement. Proper organization and annotation of this data are critical for subsequent data analysis, sharing, and long-term storage.
* **Explore:** This is a visualization tool. In this section, you can select up to two features from the sample metadata tab to create a graphical representation.

![study-tabs.gif](doc-odm-user-guide/gifs/study-tabs.gif)

## Accession number

In addition, a unique accession number is automatically generated for each study in the ODM. The accession number allows 
you to identify the specific study and to further work with the study via API endpoints.

![study-accession.gif](doc-odm-user-guide%2Fgifs%2Fstudy-accession.gif)

## Edit Study Metadata

* To edit the details of your study, select a tab and click on **Edit** at the bottom left of the page.

* Select the feature you want to edit, for example, **Study Source**. Type the new value for the field.

* Click **Publish** to save the changes. You can customize the name for the version you are updating by clicking the **Publish** button at the bottom of the screen. A new window will pop up, allowing you to customize the version name. 

![study-edit.gif](doc-odm-user-guide%2Fgifs%2Fstudy-edit.gif)
