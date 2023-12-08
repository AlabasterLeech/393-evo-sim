# Cellvolution
A small zero-player evolution simulator. Semester long group project for CSDS 393 at CWRU in Fall '23. The project began with a software requirement specification document followed by a design document, neither of which are on GitHub. Design and implementation stems from what was outlined and decided in those two documents.

To run Cellvolution, simply run __main__.py found in the src folder. Additionally, all source code for the project can be found in that folder. The other folders in the directory have self explanatory names and contain the testing code and the assests for Cellvolution.

A detailed user manual on operating Cellvolution can be found by clicking the 'Tutorial' button on the main menu or by opening the tutorial.txt file in the assets folder.

Status of bugs and SRS omissions:
There are no currently outstanding bugs and two omissions from the SRS:
- Allowing the user to define and add new survival functions
- Allowing the user to edit the genomes of individual organisms
These two features ended up being too complex to implement for the version of Cellvolution for this project given the time we had. A significant portion of this complexity came from the fact that both of these features give the user significant access to the underlying code of Cellvolution and the safeguards we would have had to develop to prevent the user from inadvertantly breaking the program with either of these features would have been too large a time sink for the project.

Issue tracking and version control were done through git and GitHub and the repository can be viewed at https://github.com/AlabasterLeech/393-evo-sim