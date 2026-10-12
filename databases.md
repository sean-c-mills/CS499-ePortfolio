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

# Databases

## Enhancement Overview

For my third enhancement, I expanded how MongoDB is used in the Animal Shelter Dashboard by moving the rescue-profile information into the database instead of keeping it directly in the application. I also added validation, moved the database credentials into environment variables, and tested a compound index with the rescue searches to see whether it improved performance.

## Artifact Versions

### Original Artifact

[View the Original Animal Shelter Dashboard](https://github.com/sean-c-mills/CS499-ePortfolio/tree/main/artifacts/CS340%20Artifact%20Original)

### Enhanced Artifact

[View Enhancement Three: Databases](https://github.com/sean-c-mills/CS499-ePortfolio/tree/main/artifacts/CS340%20Artifact%20Enhancement%203%20-%20Databases)

## What Changed

The original dashboard used MongoDB to store the animal shelter records, but some application information was still stored directly in the Python code. This enhancement moved the rescue profiles into their own MongoDB collection so changes made through the configuration page remain available after the application is closed.

I also added validation in both the application and MongoDB, moved the database username and password into environment variables, and created a compound index for the rescue-search fields. I tested the index with 10,000 animal records to determine whether it actually improved the searches before keeping it in the final version.

## Enhancement Narrative

The artifact I selected is the Animal Shelter Dashboard that I originally created during my CS 340: Client Server Development course earlier in the Computer Science program. I have continued using this artifact throughout CS 499 because it gives me the opportunity to keep improving the same application from different areas of computer science instead of moving to a completely different project each time. The application uses Python and Dash to display animal shelter records that are stored in MongoDB, while a CRUD module handles the communication with the database. In the original version, MongoDB was mainly being used to store the animal records while some of the other information the application needed was still stored directly in the Python code. I selected this artifact for the Databases enhancement because there was already a working connection between the application and MongoDB, but I felt like the database could be doing more than it was at that point. The original design also had the MongoDB username and password directly in the source code and there were not really any database rules making sure the animal information matched what the dashboard expected.

For this enhancement, I moved the rescue-profile information into a separate MongoDB collection so the profiles are now stored in the database instead of only being part of the application. The breed, sex, and age requirements are pulled from the database when a rescue search is performed and I also connected the rescue-profile configuration page to MongoDB so any changes made there stay saved after the application is closed. Users can create profiles and make changes to existing ones or delete them if they are no longer needed. Before anything is saved, the application checks the profile information and I also added MongoDB validation so the database can reject a profile if the structure is wrong. I did something similar with the animal collection because the rescue searches and map depend on the age and location information being in the format the application expects.

This enhancement made progress toward Course Outcomes 3, 4, and 5. Course Outcome 3 applies because I wanted to actually test whether a compound MongoDB index would improve the rescue searches instead of just adding one and assuming it was helping. I used the same rescue queries that the dashboard uses and compared how MongoDB handled them before and after the index was added. Without the index, MongoDB examined all 10,000 animal documents for every rescue profile, while after adding it that dropped to 200 documents for Water Rescue, 272 for Mountain or Wilderness Rescue, and 389 for Disaster or Individual Tracking. The average query time also went from around 7.7 to 7.9 milliseconds without the index to around 0.9 to 1.4 milliseconds with it, so since the testing showed that it actually helped I decided to keep the index in the final version.

Course Outcome 4 is supported because MongoDB is now being used for more than just storing the original shelter records and the rescue-profile information is now part of the database too. The dashboard gets those requirements from MongoDB when it performs the rescue searches instead of having them stored directly in the application. I also made progress toward Course Outcome 5 because I moved the MongoDB connection information out of the source code and into environment variables, while also adding validation in the application and in MongoDB so bad information has less of a chance of being stored. Course Outcomes 1 and 2 were not the main focus of this enhancement and are demonstrated elsewhere in the ePortfolio through the code review, written communication, and discussion of collaboration.

One of the more useful things I learned from this enhancement was that database performance really needs to be tested based on how the application is actually searching the data. The rescue searches use exact matches for fields like animal type and sex along with an age range, while breeds are searched using case-insensitive regular expressions, so I did not want to just assume that putting every search field into an index was automatically going to be the best choice. After testing the compound index, MongoDB was able to cut down the number of animal documents it had to look through even though the breed filtering still had to be handled separately. This helped me understand indexes better because just seeing that a field is part of a search does not necessarily mean it belongs in the index, and the way the full query works matters more.

The biggest challenge was moving the rescue profiles into MongoDB because once I started doing that I realized it affected more parts of the application than just where the profiles were saved. The dashboard needed to get the profiles from the database and so did the configuration page, then I also had to change the callbacks and rescue-search services because those parts were still expecting the old profile information that was stored inside the application. The validation took some extra work too because I wanted the application to catch bad information before it was saved, but I still needed MongoDB to have its own rules in case something got to the database another way. This was probably the part that helped me understand the database work the most because one change to where the information is stored ended up changing how several other parts of the application worked with that information, so I had to keep going back through the project and making sure everything was still using the same data the same way. I received full credit on the completed enhancement and did not receive any corrective feedback, so I kept the implementation the same while preparing it for the final ePortfolio.

## Narrative Document

[Download the Original Databases Narrative](https://github.com/sean-c-mills/CS499-ePortfolio/raw/main/narratives/Enhancement%203%20-%20Databases%20Narrative.docx)

[Return to the ePortfolio Home Page](https://sean-c-mills.github.io/CS499-ePortfolio/)
