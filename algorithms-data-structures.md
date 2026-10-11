# Algorithms and Data Structures

## Animal Shelter Dashboard

The Animal Shelter Dashboard was originally created in my CS 340: Client Server Development course. This enhancement focuses on improving how eligible rescue candidates are ranked after they pass the existing rescue requirements.

## Artifact Versions

### Original Artifact

[View the Original Animal Shelter Dashboard](https://github.com/sean-c-mills/CS499-ePortfolio/tree/main/artifacts/CS340%20Artifact%20Original)

### Enhanced Artifact

[View Enhancement Two: Algorithms and Data Structures](https://github.com/sean-c-mills/CS499-ePortfolio/tree/main/artifacts/CS340%20Artifact%20Enhancement%202%20-%20Algorithms%20and%20Data%20Structures)

## What Changed

The original rescue search treated every animal that passed the requirements the same once the results were displayed. For this enhancement, I added a suitability score based on the animal's age and breed so eligible rescue candidates could be compared after they qualified.

I also added two approaches for organizing the results. A bounded priority queue is used when the user requests the top 10 or top 20 candidates, while full sorting is used when all eligible animals need to be returned. I tested both approaches with increasingly larger datasets to compare their performance and verify that they returned the same top candidates.

## Enhancement Narrative

The artifact I selected is the Animal Shelter Dashboard that I originally created during my CS 340: Client Server Development course earlier in the Computer Science program. The application uses Python and Dash to display animal shelter records stored in MongoDB, while a CRUD module handles communication with the database. In the original version, users could select a rescue type and the dashboard would filter the animal records according to requirements such as breed, age, and sex. Although this worked just fine for finding animals that qualified, every animal that passed the filter was treated the same once the results were displayed. I selected this artifact for the Algorithms and Data Structures enhancement because the existing filtering process already gave me a group of acceptable candidates, which made it possible to focus on how those candidates could be compared and organized after they qualified. Instead of just replacing the original rescue search, I wanted to build on it by giving the application a better way to identify which eligible animals were the stronger matches.

For this enhancement, I added a suitability score that is calculated after an animal passes the existing rescue requirements. The score uses age and breed information that is already stored with each animal, with up to 50 points coming from how close the animal’s age is to the middle of the accepted range and up to 50 points coming from how closely its breed matches one of the preferred breeds. After the scores are calculated, the dashboard can organize the candidates in two different ways depending on what the user wants to see. When the user selects the top 10 or top 20 candidates, a bounded priority queue keeps track of the strongest results as each animal is evaluated, while selecting all eligible animals uses a full sorting approach because every result needs to be returned anyway. I also added the suitability score to the rescue table so the ranking is visible for the user instead of only happening in the background.

This enhancement made the strongest progress toward Course Outcomes 3 and 4. Course Outcome 3 applies because I had to design and compare two ways of solving the same ranking problem while considering the tradeoffs between them. A full sort generally requires O(n log n) time, while maintaining only the strongest k candidates with a priority queue requires approximately O(n log k). Instead of assuming the priority queue would automatically perform better, I tested both approaches with the same candidate records at increasing dataset sizes and confirmed that they returned the same top 10 animals each time. The results also supported Course Outcome 4 because I was able to use Python and a priority queue to improve the way the application organizes rescue candidates while still keeping the original search process in place.

One of the more useful things I learned from this enhancement was that the theoretical complexity of an algorithm doesn’t always show up clearly when the complete application is being timed. The end-to-end results for the full sort and priority queue stayed very close because both methods still had to calculate every suitability score and prepare the animal records before the actual ranking took place. Because of this, I also tested only the selection portion after the scores had already been calculated, which made the difference between the two approaches easier to see. At 100 records the priority queue was slightly slower, but as the amount of data increased it became more efficient, and at 10,000 records the selection took about 1.97 milliseconds compared with about 2.73 milliseconds for the full sort. This showed me that the priority queue was better suited to the top-k problem as the dataset grew, but it also showed why the performance of one algorithm shouldn’t be separated from the other work the application has to do.

The biggest challenge was deciding how to rank the eligible animals without making the suitability score seem more accurate than it really is. The original shelter data includes the information needed to compare age and breed, but it doesn’t contain an established formula for deciding which qualified dog would be the best rescue candidate. Because of this, I treated the score as an application-specific way to compare the information that was already available instead of claiming that it measures real rescue ability. I also needed to make sure that both of these ranking approaches gave the same results before their performance could be compared, seeing as a faster method wouldn’t be useful if it changed which animals were selected. Working through those decisions helped me understand that improving an algorithm involves more than just choosing the option with the better expected time, because the results still have to make sense for the problem the application is trying to solve.

## Narrative Document

[Download the Original Algorithms and Data Structures Narrative](https://sean-c-mills.github.io/CS499-ePortfolio/narratives/Enhancement%202%20-%20Algorithms%20and%20Data%20Structures%20Narrative.docx)

[Return to the ePortfolio Home Page](https://sean-c-mills.github.io/CS499-ePortfolio/)
