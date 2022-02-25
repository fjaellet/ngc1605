# TOPCAT analysis of NGC 1605

This is a supplementary document for our Research Note on NGC 1605.

This document is structures as follows:
1. Classical manual cluster analysis with [TOPCAT](https://www.star.bris.ac.uk/~mbt/topcat/) (for example see [this tutorial](https://www.cosmos.esa.int/web/gaia-users/archive/use-cases#ClusterAnalysisGUI))
2. Analysing NGC 1605 assuming that it is a double cluster (as suggested by [Camargo 2021](https://ui.adsabs.harvard.edu/abs/2021ApJ...923...21C/abstract))

## 1. Classical manual analysis

We follow the typical steps of a manual analysis using [TOPCAT](https://www.star.bris.ac.uk/~mbt/topcat/): 
1. select a reasonable circular region around the cluster (say, 10 arcmin):
![selecting a smaller sky region](/im/topcat_step1.png "selecting a smaller sky region")

2. select the peak in proper-motion space:
![select a region around the obvious peak in the proper-motion diagram](/im/topcat_step2.png "select the peak in proper-motion space")

3. weed out stars with incompatible parallaxes:
![weed out stars with incompatible parallaxes](/im/topcat_step3.png "weed out stars with incompatible parallaxes")

4. look at the colour-magnitude diagram:
![look at the colour-magnitude diagram](/im/topcat_step4.png "look at the colour-magnitude diagram")

## 2. Assuming NGC 1605 is in fact a double cluster?

We follow the same steps, but now for NGC 1605a/b separately:

To know what we should look for, we start from Fig. 1 of Camargo (2021):
![Camargo 2021, Fig. 1](/im/camargo2021_fig1.png "Camargo 2021, Fig. 1")

We make a manual selection on the sky:
![selecting sub-clusters](/im/topcat_step1ab.png "selecting sub-clusters")

But then we immediatley see that the 2 manually "sub-clusters" (apart from being heavily contaminated by the field) overlap in proper-motion space and in the CMD: hence they cannot be considered separate entities:

We make a manual selection on the sky:
![Proper-motion diagram](/im/topcat_step2_ab.png "Proper-motion diagram")

![Zoom into proper-motion diagram](/im/topcat_step2zoom_ab.png "Zoom into proper-motion diagram")

![CMD](/im/topcat_step4_ab.png "CMD")

All this is only easily visible thanks to the exquisite data quality of Gaia...

This work presents results from the European Space Agency (ESA) space mission Gaia. Gaia data are being processed by the Gaia Data Processing and Analysis Consortium (DPAC). Funding for the DPAC is provided by national institutions, in particular the institutions participating in the Gaia MultiLateral Agreement (MLA). The Gaia mission website is [https://www.cosmos.esa.int/gaia](https://www.cosmos.esa.int/gaia). The Gaia archive website is [https://archives.esac.esa.int/gaia](https://archives.esac.esa.int/gaia).

