<div class="portfolio-header">
  <h1>Sean Mills | CS-499 ePortfolio</h1>
  <p>Southern New Hampshire University</p>
</div>

<nav class="portfolio-nav">
  <a href="https://sean-c-mills.github.io/CS499-ePortfolio/">Home</a>
  <a href="https://sean-c-mills.github.io/CS499-ePortfolio/#professional-self-assessment">Self-Assessment</a>
  <a href="https://sean-c-mills.github.io/CS499-ePortfolio/#code-review">Code Review</a>
  <a href="https://sean-c-mills.github.io/CS499-ePortfolio/software-design.html">Software Design &amp; Engineering</a>
  <a href="https://sean-c-mills.github.io/CS499-ePortfolio/algorithms-data-structures.html">Algorithms &amp; Data Structures</a>
  <a href="https://sean-c-mills.github.io/CS499-ePortfolio/databases.html">Databases</a>
</nav>

# Software Design and Engineering

## Enhancement Overview

For my first enhancement, I reorganized the Animal Shelter Dashboard so the interface and the processing behind its features were separated into different parts of the application. I also separated general animal browsing from rescue searches and added a separate page for managing rescue-profile settings. This made the project easier to follow and gave me a better structure to build on during the later enhancements.

## Artifact Versions

### Original Artifact

[View the Original Animal Shelter Dashboard](https://github.com/sean-c-mills/CS499-ePortfolio/tree/main/artifacts/CS340%20Artifact%20Original)

### Enhanced Artifact

[View Enhancement One: Software Design and Engineering](https://github.com/sean-c-mills/CS499-ePortfolio/tree/main/artifacts/CS340%20Artifact%20Enhancement%201%20-%20Software%20Design%20and%20Engineering)

## What Changed

The original project relied heavily on the Jupyter Notebook and dashboard callbacks to handle both the interface and application logic. For this enhancement, I separated the application into different modules so the dashboard could focus on displaying information and receiving user input while service modules handled the processing behind those actions.

I also separated general animal browsing from rescue-candidate searches and added a rescue-profile configuration page. This gave the application a clearer structure and provided a foundation for the algorithm and database enhancements that followed.

## Enhancement Narrative

The artifact I selected is the Animal Shelter Dashboard that I originally worked on in CS 340: Client Server Development. The application uses Python and Dash to display animal shelter records stored in MongoDB, while a CRUD module handles communication with the database. The original dashboard allowed users to filter animals for specialized rescue work and then view the results through the interface. I selected this artifact because it already demonstrated software development skills, but the original version placed too much responsibility inside the Jupyter Notebook and dashboard callbacks. The rescue requirements were also hardcoded directly into the filtering logic, which made the program harder to maintain if those requirements needed to change later.

For this enhancement, I reorganized the application so different parts of the program have clearer responsibilities. The dashboard now focuses on displaying information and receiving input, while separate service modules handle the processing behind those actions. Database access remains separated through the CRUD module, which helps keep the application structure a lot easier to follow. I also separated general animal browsing from the rescue-candidate search, and users can now browse animals by type, while the rescue side continues to use the rescue categories. The main difference is that those rescue requirements now come from rescue profiles instead of being hardcoded directly into the callback. Those profiles can now also be reviewed and changed through a separate configuration page, which should make future updates much easier to do without placing more logic inside the dashboard itself.

The enhancement made progress toward several course outcomes. The strongest progress was toward the outcome involving the design and evaluation of computing solutions because I had to reconsider how the different parts of the application should all work together. The best example of this was the rescue-profile management. My original plan was to include this functionality with the normal dashboard, but while implementing it I noticed there was a potential problem because general users shouldn’t just be able to change the requirements used for rescue searches. I separated that functionality from the normal dashboard and moved it to a configuration page instead.

I did not implement authentication during this enhancement because I wanted to keep the work within its intended scope. I also made great progress toward the outcome involving computing techniques by using modular Python files and Dash routing to improve the structure of the application. The collaboration outcome is supported by keeping rescue requirements in a consistent profile structure. Persistent storage and sharing of that information was intentionally left for the database enhancement that followed.

The biggest takeaway from this enhancement was that improving an existing program isn’t always limited to following the original plan exactly. Some of my design problems became more noticeable once I started separating the application into smaller parts. I had to decide where processing should happen and how profile information should move through the application. I also had to figure out how the normal dashboard should differ from the configuration functionality. Moving the original files into a new project structure also caused some temporary import and file-location problems, which required me to verify that each module was being loaded from the right location. These challenges helped me understand why separation of responsibilities is important in software design. The enhancement kept the original functionality while giving the application a structure that made it easier for me to continue building on it during the later enhancements.

## Narrative Document

[Download the Software Design and Engineering Narrative](narratives/Enhancement%201%20-%20Software%20Design%20and%20Engineering%20Narrative.docx)

[Return to the ePortfolio Home Page](./)
