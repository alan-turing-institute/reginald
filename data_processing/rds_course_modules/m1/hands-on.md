# Module 1: Hands-on session
## Introduction
In this hands-on session we will simulate a real-world scoping scenario:
- Participants are divided in groups.
- Each group will be a small data science team for the rest of the session. 
- Each team is paired with a helper who will act as a Principal Investigator (PI), i.e., a lead researcher who is seeking funding for a new project and wants the data science team to participate in it. 
- Each group will receive a short research proposal from the PI. 
- Teams need to go through the provided materials to conduct the scoping, including technical and ethical aspects. 

The activity consists of three phases:

## Phase 1: Setup, initial contact and discussion 

### **Schedule**
- 20 mins setup (in groups)
- 35 mins collaborative activity (exploration of materials and discussion, in groups)

****

### **Teams should follow these steps during Phase 1:**
1. Setup a GitHub repo for each group following the guidance in Lesson 1.4.

2. Ensure that all participants have access to it.

3. Prepare a scoping project board (decide the flow that better captures the scoping process you aim to conduct).

4. Go through all the received materials (you can follow up with the PI if something is not clear from the beginning).

5. To get a better understanding of the project, it might be necessary to:

    a. explore the dataset. 

    b. examine the dataset's documentation. 

    c. do an initial general literature search. To simplify this step, you can just look at [the paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3678208/) we used as an inspiration for the hands-on activities.

    We suggest to split your team into sub-groups to address these three points in parallel.
    
6. Create issues in the repo covering the scoping questions you want to discuss with the PI (see Module 1.2). You should ideally have at least one issue dedicated to each of the questions in your project scoping board. Start filling them in based on your initial exploration and the information you received from the PI. You will have a chance to speak with the PI in the second phase.

7. Additionally, if you notice anything interesting in the dataset that should be discussed during scoping you should make others in the group aware of it. You can:

    a. Create a new issue in your repo describing your observation or idea.
    
    b. or (if you wrote some code as part of your exploration) make a pull request to the main branch of the repo higlighting what you have found. 

****

### **The initial PI contact**

>15th of November 2021
>
>Subject: Request for collaboration
>
>
> Dear Research Engineering Group,
I am reaching out for scoping a potential collaboration. Social inequalities in health have been described across a range of European countries. While it is well-known in the literature that the higher the social class, the lower the prevalence/incidence of health problems, no study has attempted to explain social inequalities in health for Europe as a whole. To address this, I am setting up a project proposal for a large-scale study using promptly available data (European Quality of Life Time Series, freely available [online](https://ecommons.cornell.edu/handle/1813/87445)) and deep learning techniques. I envision a 2-year project answering the call “Personal Stories, Healing Nations” employing 1 full-time Post-Doctoral researcher covering the social science parts of the study and (potentially) in collaboration with your team for the technological parts. We are hoping to submit by Dec 1st, so we would be keen to establish the costs for this digital component by Nov 28. 
>
> While I am fairly new to big-data (and, I have to admit, I have my reservations), I believe a well-designed project with these sources might be able to rewrite our understanding of social inequalities in health in Europe (and even beyond) during the last two decaces, a period involving a series of major socio-economical and political events, ça va sans dire. Its impact will be relevant for the general public and could potentially even suggest actions to governments.
>
>
>Your Sincerely,
>
>Professor J. Doe


## Phase 2: Technical Questions (40 mins in group + 20 mins together)

## **Schedule**
- 40 mins collaborative activity (scoping, in groups)
- 20 mins presentation (all together)

****

## **Teams should follow these steps during Phase 2:**
1. After having explored the materials and prepared some initial questions in Phase 1, you can start an iterative conversation with the PI to reach an answer to the scoping questions questions listed below. This should consist of a series of discussions and further exploration of the data, any documentation you found and other literature. The PI will be available for you whenever you want during Phase 2.
2. You should document your discussions in the GitHub project board, trying to answer the questions as clearly as possible. You can do this all together or by splitting your team into sub-groups. Use the issues you created in Phase 1 and create new ones when new ideas come up.
3. After documenting the converstations and answers, one representative of the team will be asked to present your main conclusions in the common room.

We list here some main scoping questions we presented in Lesson 1.2

### The goal

1. What is the broad challenge we are trying to solve?

2. What is the specific research question? How does it translate to a data science problem?

### The data

3. Is data available? Can I legally use it? Is it appropriate for the research question?

### The expectations

4. What are the stakeholders' expectations?

5. What is in-scope and out-of-scope?

6. How does the output of the project look like and how is it going to be used?

### Success

7. What metrics do we use to measure the success of the project?

8. What is the expected impact? Is it realistic?

### Other questions

9. What about computational resources and timelines?


## Phase 3: Ethical Discussion (30 mins in groups, then 30 mins together)

### **Schedule**
- 40 mins collaborative activity (EDI discussion, in groups)
- 20 mins presentation (all together)

****

### **Teams should follow these steps during Phase 3:**
As a final step in the scoping activity, we want to examine questions relating to equality diversity and inclusion with the PI. Follow these steps:
1. Discuss with the PI any EDI questions you might have about the project goals, the data, the impact or other topics you consider important or controversial. The PI will be available throughout Phase 3.
2. You should document your discussions in the GitHub project board, similarly to Phase 2. You can do this all together or by splitting your team into sub-groups. 
3. After documenting the converstations and conclusions, one representative of the team will be asked to present your them in the common room.

Think about the following questions as a starting point but please approach this discussion with an open and investigative spirit. We would love to hear your insights!
- In this project we focus on the goal of studying health outcomes. Do the data contain the right type of information to do that (explore the dataset, the paper and the documentation)? 
- To what extent can we understand the relationship between health and social factors with this dataset? What claims can we make?
- Given the importance of understanding and explaining health outcomes, what does the PI plan to do to share the information publicly and achive positive societal impact?
- Is it important to make the work reproducible?
