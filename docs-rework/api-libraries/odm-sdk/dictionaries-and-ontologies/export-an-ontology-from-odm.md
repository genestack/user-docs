---
diataxis: how-to
tab: api-libraries
---

# Export an ontology from ODM

This guide explains how to retrieve the source file of an ontology (dictionary) that is loaded in ODM.

## Steps

1. From the Dashboard, open the Template Editor.

   ![Template Editor in Dashboard](../../../assets/tools/odm-sdk/terminal/dictionaries-and-ontologies/exporting-ontologies-from-odm/1.png)

2. You will see all available templates.

   ![All templates](../../../assets/tools/odm-sdk/terminal/dictionaries-and-ontologies/exporting-ontologies-from-odm/2.png)

3. To review the ontologies associated with a particular template, open it by clicking on its title.

   ![Open template](../../../assets/tools/odm-sdk/terminal/dictionaries-and-ontologies/exporting-ontologies-from-odm/3.png)

4. You will see all attributes in the template, including those linked to dictionaries. Note the accession of the dictionary you want to export (for example, `GSF000026`).

5. Navigate to the File Manager using the direct link `[your_host]/ui/files`.

6. Enter the dictionary accession in the search field and click the search button. The results include both templates that use the dictionary and the dictionary file itself.

   ![Search results](../../../assets/tools/odm-sdk/terminal/dictionaries-and-ontologies/exporting-ontologies-from-odm/7.png)

   To find the dictionary file specifically, look at the **Type** column and identify the row with type **Dictionary**.

   ![Dictionary type in results](../../../assets/tools/odm-sdk/terminal/dictionaries-and-ontologies/exporting-ontologies-from-odm/8.png)

7. Click the more menu on the dictionary row to open the context menu, then click **More info**.

   ![More info](../../../assets/tools/odm-sdk/terminal/dictionaries-and-ontologies/exporting-ontologies-from-odm/9.png)

8. In the details panel, click the link in the **Data URL** attribute to download the source file.

   ![Data URL](../../../assets/tools/odm-sdk/terminal/dictionaries-and-ontologies/exporting-ontologies-from-odm/10.png)

   Alternatively, follow the link in the description to go to the original source.

   ![Source link](../../../assets/tools/odm-sdk/terminal/dictionaries-and-ontologies/exporting-ontologies-from-odm/11.png)

## Related

- [About dictionaries and ontologies](about-dictionaries.md)
