# Data Consumer in the User Interface

This guide will help you navigate the main features of the Open Data Manager as a Data Consumer.

## Main Page

When you open ODM you will be taken to the start page or “Dashboard” as shown below:

![Main Page](quick-start-images/main-page.png)

## Browse Studies

As a Data Consumer, you can browse and explore various studies. 

To search and browse studies, click on the **“Browse studies”** button on the dashboard/start page.

![Browse Studies](quick-start-images/browse-studies.png)

## Search for Data

Apply filters to search for specific studies. For example, select filters using the criteria in the panel on the left, 
such as Data Class, Organism, etc.

!!! info "The exact filters you see may vary due to the data contained within your ODM system. Administrators can lock which facets are available for all users."

<figure markdown="span">
  ![Filters](quick-start-images/filters.png){ width="700" }
  <figcaption>Users can apply filters to refine their search, including Organism, Data Class, Organization Name, Study Type, Study Source, etc.</figcaption>
</figure>

The system's search functionality is designed to enhance user experience and efficiency by allowing users 
to look up specific keywords effortlessly. By entering terms such as **"bowel"**, users can quickly access a range 
of relevant studies. Additionally, the search bar is equipped with an intuitive autocomplete feature, 
which not only predicts and suggests potential search terms but also provides values from various ontologies. 
This ensures a more streamlined and accurate search process, making it easier to navigate through the available 
data and find pertinent information swiftly.

![Data Search](quick-start-images/search-data.png)

Use the search bar to find specific keywords, such as **"bowel"** to display relevant studies.
The autocomplete feature also suggests values from various ontologies.

## Select a Study

After applying the desired filters to narrow down your search results, you will see a list of studies 
that match your criteria. To delve deeper into a specific study, simply click on the corresponding icon. 
This action will open the study, allowing you to review its details and findings comprehensively.

![Select Study](quick-start-images/selet-study.png)

The study will open in a new tab, where the following tabs can be explored:
**Study:** Shows the study metadata.
**Samples:** Contains all the samples' metadata.
**Data:** Details of the files linked or attached to the study.

![Study Tabs](quick-start-images/study-tabs.png)

### Accession number

In addition, a unique accession number is automatically generated for each study in the ODM. 
The accession number allows you to identify the specific study and to further work with the study via API endpoints. 
Learn more about API endpoints and functionalities in the API User Guide.

![Accession](quick-start-images/accession.png)

Every study imported to the ODM contains a unique identifier named accession number. 
You can visualize the accession number on the Study tab, or you can copy the accession number 
by clicking on the top bar of the main page and selecting “copy accession”

## Visualize Data

To visualize the study data:

1. Click on **Explore**.
   ![Explore View](quick-start-images/explore-data.png)

2. Select an attribute to display. For example, "Age".
3. A plot will be created showing the values for the attribute "Age".
   ![Explore View](quick-start-images/explore-data-2.png)

4. To combine up to two attributes, such as "Age" and "Disease" simply select another attribute from the menu.
   ![Explore View](quick-start-images/explore-data-3.png)

5. To remove an attribute from your comparison click the :material-window-close: at the top right corner 
of the attribute in the list or use **Reset** option to remove all the attributes.
   ![Explore View](quick-start-images/explore-data-4.png)

6. The plot combining two attributes displays informative data, such as sample count, and minimal and maximum values.
   ![Explore View](quick-start-images/explore-data-5.png)

7. To export the plot in SVG or PNG formats, simply hover over the top right corner of the plot. A menu with three dots :material-dots-horizontal: will appear, allowing you to select the desired format for download. The available formats for downloading the plot are SVG and PNG.
   ![Explore View](quick-start-images/explore-data-export.png)

## Export Data

Export all the information contained in the study. Note that some studies may have restrictions.

1. Click on **Export**.
2. A window will open, and the file will be compressed.
3. Once compressed, you can download the folder containing all the data and metadata from the study.

!!! warning "If some externally stored data is inaccessible due to its removal from the original external storage (the link to the storage is invalid), the study cannot be exported."

![Export Data](quick-start-images/export-data.png)

By following these steps, you can efficiently browse, visualize, and export data as a Data Consumer using 
the Interface of Open Data Manager.
