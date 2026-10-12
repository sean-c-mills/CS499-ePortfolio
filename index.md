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

## Professional Self-Assessment

Welcome to my CS-499 ePortfolio. When I first started the Computer Science program, my main goal was to become a computer programmer because I wanted to work with software and eventually build applications of my own. That goal hasn’t really changed, but the program has shown me that there are other areas of computer science that also interest me. Courses that involved databases especially made me realize that I enjoy working with data and understanding how that information is stored and used by an application. Because of this, software development is still the main area I want to pursue, but I’m also interested in positions where programming and database work overlap. I also became more comfortable learning new languages as I went through the program because I started with C++ and Java, while later courses had me working with Python or JavaScript instead. Some courses focused more on how an application should be designed and others made me think more about what was happening with the data, so I got used to having to learn something different depending on the project.

The way I think about my career has also changed because finishing my degree won’t mean I’m done learning. Technology is going to keep changing, so I know I will have to keep learning new tools even after I start working in the field. I have also started caring more about understanding why a solution works instead of only getting it to work, which is something I want to carry with me when I start working in the field.

A lot of my school projects were completed individually, so most of my experience actually working as part of a team has come from my job in online grocery at Walmart. Everyone has their own work to complete, but we still depend on each other because orders have to keep moving even when priorities change or something goes wrong. If somebody falls behind or there is a problem with an order, that can affect other people too, so communication matters even when everyone isn’t doing the exact same job. Learning about Agile and Scrum during the program reminded me of some of that because software development can also involve different people working on different parts of the same goal and having to adjust when requirements change. I haven’t worked on a professional software team yet, but I do think my work experience has helped me understand why people need to communicate and be able to rely on each other when their work is connected. In software development, I think the same idea applies because developers and stakeholders need clear information from each other before they can make decisions about what should change or how a problem should be handled.

Communication was also something I worked on throughout the program because knowing how to write code is only part of the job if somebody else eventually has to understand what I did. In CS 230, I had to think about what a client was asking for and explain how I thought the software should be designed, which was different from just being given a programming problem and trying to get the right output. The code review in CS 499 was another example because I had to go back through an application I already created and explain what it did before talking about what I wanted to change.

I also had to explain why I thought those changes were worth making instead of just showing the code after I finished it. This helped me a lot with the communication outcome because it made me think more about the person who is going to read or listen to what I am explaining, and readable code and comments also matter for the same reason. I also learned that the amount of technical detail I use should depend on whether I am explaining something to another developer or to somebody who mainly needs to understand what the software is supposed to accomplish.

Data structures and algorithms became another area where I noticed that the way I looked at a problem changed as I went through the program. In CS 300, the ABCU Course Planner made me compare different ways of organizing course information and think about how that choice could affect what the program needed to do later. Earlier in the program I probably would have cared mostly about whether I could get the program to return the right answer, but I started paying more attention to how the solution was getting there too. I used that again during the capstone when I compared full sorting with a bounded priority queue instead of just assuming the priority queue would be better because of its expected complexity. I tested both approaches with as many as 10,000 records and found that the difference was easier to see when I looked at the ranking part by itself. That helped me understand the outcome involving the design and evaluation of computing solutions because sometimes the approach that looks better on paper still needs to be tested in the actual program before deciding if it really makes sense.

Software engineering and databases ended up being two of the areas I enjoyed the most. In CS 465, I worked on a full-stack application and got to see how JavaScript and Angular worked with the server side of the application, while MongoDB was being used to store the information. CS 340 gave me more experience with MongoDB, but this time I was using Python and Dash and had to work with CRUD operations as part of the application. These courses made it easier for me to understand that the different pieces aren’t really separate once the application starts getting larger because a change in one place can affect something somewhere else.

During the capstone I also tested a compound MongoDB index instead of just adding one and assuming it would help. Without the index, MongoDB examined all 10,000 animal records for each rescue search, while after adding it the searches only needed to examine a few hundred records depending on the rescue profile. I think that was a good example of how the program changed the way I approach things because I wanted to see whether the database change actually helped before deciding to keep it.

Security was something I didn’t think about as much when I first started creating programs, but it became more noticeable when I went back through older work. The Animal Shelter Dashboard had the MongoDB username and password directly in the source code, and there also weren’t many rules at the database level stopping bad information from being stored. When I worked on the database enhancement, I moved the connection information into environment variables and added validation in the application, while MongoDB also checks the information before storing it.

Earlier in the project I also moved the rescue-profile settings away from the normal dashboard because it didn’t make sense for changing those requirements to be treated the same as just looking through the animal records. I still wouldn’t call the application a complete secure production system because I didn’t add authentication, but the project made me think more about security while I was building something instead of only looking for problems at the end. That is probably the biggest change in how I think about the security outcome.

The three enhancements in this ePortfolio all use the same Animal Shelter Dashboard, which I think gives a better picture of my growth than using three unrelated projects would have. The Software Design and Engineering enhancement came first and reorganized the application so I wasn’t continuing to put more processing inside the notebook and callbacks. The Algorithms and Data Structures enhancement built on that by adding the rescue-candidate ranking and comparing two different ways of handling the results. After that, the Database enhancement moved the rescue-profile information into MongoDB so changes could be saved and used again, while I also added validation and changed how the database connection information was handled. Using the same application for all three made it easier for me to see how the different areas of computer science connect because changing the structure of the application affected what I could do later with the algorithms and database. The technical sections that follow show each stage of that progression along with the original artifact and the narrative explaining the work.

Putting the ePortfolio together also helped me see and explain my strengths more clearly because I could look at my earlier work next to the capstone version and compare how I approached the same application before and after the enhancements. Overall, I think the program has prepared me better to enter the field and work in software development because I’m more comfortable looking at an existing application and figuring out what needs to change, but I also know there is still going to be a lot I have to learn once I start working in the field.

[Download the Professional Self-Assessment](https://github.com/sean-c-mills/CS499-ePortfolio/raw/main/self-assessment/Professional%20Self-Assessment.docx)

## Code Review

This code review examines the original Animal Shelter Dashboard developed in my CS 340: Client Server Development course. The review discusses the application's existing functionality, identifies areas for improvement, and explains my planned enhancements in software design and engineering, algorithms and data structures, and databases.

[Watch my Code Review on YouTube](https://www.youtube.com/watch?v=bpVfyD-QywY)

## Software Design and Engineering

For my first enhancement, I reorganized the Animal Shelter Dashboard so the interface and the processing behind its features were separated into different parts of the application. I also separated general animal browsing from rescue searches and added a separate page for managing rescue-profile settings. This makes the project easier to follow and gave me a better structure to build on during the later enhancements.

[View the Software Design and Engineering Enhancement](https://sean-c-mills.github.io/CS499-ePortfolio/software-design.html)

## Algorithms and Data Structures

For my second enhancement, I added a suitability scoring system so eligible rescue candidates could be ranked instead of all of them being treated the same after they passed the rescue requirements. I also compared a bounded priority queue with full sorting and tested both approaches with larger datasets to see how their performance changed as the amount of data increased.

[View the Algorithms and Data Structures Enhancement](https://sean-c-mills.github.io/CS499-ePortfolio/algorithms-data-structures.html)

## Databases

For my third enhancement, I expanded how MongoDB is used in the Animal Shelter Dashboard by moving the rescue-profile information into the database instead of keeping it directly in the application. I also added validation, moved the database credentials into environment variables, and tested a compound index with the rescue searches to see whether it improved performance.

[View the Databases Enhancement](https://sean-c-mills.github.io/CS499-ePortfolio/databases.html)
