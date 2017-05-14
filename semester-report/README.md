Semester Research Report
=======================

Adrian Law, Mark Bestavros, Tyrone Hou

Report written by Mark Bestavros

## Introduction
Over the past two semesters, we have been studying Data Mechanics: the study of how data moves through institutions and urban settings, and how we can use this data as part of algorithmic approaches to improve how cities function and operate. Specifically, we have been working under Andrei Lapets, developing optimizations for bus systems in Boston. This report will serve as an overview of the work we’ve done primarily in the Spring 2017 semester. 

### Summary of Existing Research
This semester’s work served as a direct continuation of our research project in Professor Lapets’ CS591: Data Mechanics for Pervasive Systems and Urban Applications course for Fall 2016. Many of the methods and algorithms applied in this semester’s research came directly from that project, so this section will serve as a brief summary and analysis of the research from last semester before elaborating on the expansions to that work this semester.

Last semester, we focused on improving the MBTA’s public bus system through two key optimizations: 

1. **Bus station placement optimization**: The routes that run through metropolitan Boston distribute stops across the city according to a variety of considerations. Ideally stop placement would take into account geographic population density and reduce the distance and amount of time it takes for a person to reach the closest bus stop. We use the k-means clustering algorithm to generate means corresponding to residential properties in Boston, and use those means to derive new optimal bus stop locations along a route. To ensure that the means lie along the original bus route, we first project all residential areas within 0.5 km of a route to the closest point on the route. We then map these points into a one dimensional space so that the k-means will only move means along the route, then map the means back into two dimensional space to get the locations of the optimal bus stops.

2. **Bus allocation optimization**: The second most important consideration in optimizing bus routes is the number of buses each route should be allocated. Using MBTA bus location data with estimates of their average speed and deviation, the average completion time of a route per bus plus the deviation of that time can be derived. Two metrics used to measure the allocation is the latency of the route (on average how long it takes for a stop to be serviced) and the inefficiency of the allocation (the probability that two bus schedules will overlap each other at some point).  Assuming that the distribution of completion time is normally distributed, and that buses will be sent out at equal intervals to maximize coverage, the formula for optimization is below:  

![Allocation Score Formula](https://raw.githubusercontent.com/tyronehou/course-2016-fal-proj/master/alaw_markbest_tyroneh/poster/optimalAllocationFormula.gif)

Total latency is simplified in that inter-stop distance is not calculated; rather, latency is the average interarrival time (completion time / k) multiplied by n, where n is the number of stops and k is the number of buses. Inefficiency can be measured by the total area of intersection of k normal distributions multiplied by the number of buses. Output in the collection OptimumAllocation stores the optimal number of buses for each route.

#### Stop Placement

![Sample Map of Route Coverage](https://raw.githubusercontent.com/tyronehou/course-2016-fal-proj/master/alaw_markbest_tyroneh/poster/mapSampleCoverage.png)

![K-Means Optimized Stops](https://raw.githubusercontent.com/tyronehou/course-2016-fal-proj/master/alaw_markbest_tyroneh/poster/KmeanStops.png)

We ran our algorithm on bus stops along Route 39: (Forest Hills Station - Back Bay Station via Huntington Ave.) The route provided us with a good distribution of residential points along the route, ensuring that the kmeans did not cluster points with too much bias. Our results showed that new stops moved along the route towards areas with more residential areas, which may indicate that the current stop placement is not optimal.

However, our algorithm did not take into account cases when the spread of residential areas near to a route was scarce. For example, many bus routes extending past the metropolitan Boston area had a very low distribution of residential points. This would bias our algorithm to shift most of the bus stops inwards, leaving the outer routes with no stops. Additionally, we want to minimize the amount of travel time for each rider, as well increase the connectivity of the bus system to other modes of public transit, e.g. the T and Hubway. Thus we would like to run our algorithm on weighted data points from commercial properties, T stop and Hubway station locations in Boston.

#### Bus Allocation

![Optimal Allocation Graph](https://raw.githubusercontent.com/tyronehou/course-2016-fal-proj/master/alaw_markbest_tyroneh/poster/optimalAllocation.png)

The results we found from the optimization algorithm did consistently correlate with the results from actual allocations of each route; those routes that generally had more buses running on them due to length or importance were generally allocated more buses by our algorithm. This is most likely due to the fact that the importance, length and ridership of a route were captured by the number of stops on a route and the average and deviation of completion time per bus on that route. 

However, our algorithm also consistently under-allocates the number of buses per route across all routes. The total number of buses that the algorithm chose to allocate was 401, nearly half as many as the actual active number of buses running on MBTA’s Boston routes (around 800). This suggests that our algorithm has shortfalls as a heuristic and should take into account other factors that we did not consider.


## Data Mechanics Continued
This semester, we elected to continue our research as a team working under Professor Lapets. A few weeks after presenting our poster from the class at Data Science Day 2017, we were fortunate enough to get in touch with several representatives from Boston Public Schools (BPS), who were interested in improving their bus routing and efficiency through a public “[Transportation Challenge.]( http://bostonpublicschools.org/transportationchallenge)” BPS notes in its [challenge criteria]( http://bostonpublicschools.org/cms/lib07/MA01906464/Centricity/Domain/2263/17.04.01%20BPS%20Transportation%20Overview%20Challenge%20v2.F.pdf) that the cost of school transit in Boston is astronomical: the transportation budget accounted for $110 million of the school system’s budget, and the cost per student is the second-highest in the US. While this is partly due to the complexity and irregularity of Boston’s roads, the lack of any meaningful optimization is probably the largest factor. 
To mitigate this, BPS wants the public to submit possible optimizations for their school bus routing. Since this seemed a natural application of our research, we decided to get involved. 

### Generating a “Fake” Dataset

As part of the challenge, parties need a dataset of students and schools to work with and test their optimizations against. Of course, due to privacy laws, releasing real student information is impossible without signing a non-disclosure agreement, but this limits the reach of the challenge. Ideally, they would have a randomized dataset that is representative of Boston’s students that allows for parties to experiment with solutions before submitting a request for real student data. Since we were collaborating directly with Boston Public Schools before the challenge started, they granted us early access to the dataset they planned on making publicly available for challenge participants. Unfortunately, their randomized data was just an Excel spreadsheet with names and addresses, and the distribution seemed to be completely random across the city:

< image of initial dataset visualization here >

A dataset that is non-representative of the actual student populations in Boston, such as this originally proposed dataset, would affect the submitted algorithms’ effectiveness in the real world. Additionally, we anticipated that many teams would be doing redundant work in converting the provided Excel spreadsheet to a better format like `GeoJSON`. After voicing these concerns to BPS, they agreed to collaborate with us on generating a better randomized dataset that would be provided to the public as part of the challenge once it kicked off.

To build this simulated student dataset, we used several publicly-available datasets derived from the Massachusetts census, along with key demographic information about students in Boston Public Schools and the existing residential dataset that we collected as part of our previous semester’s research. On a high level, our algorithm goes zipcode-by-zipcode and follows these steps:

1.	looks at the number of BPS students living in that zip and randomly assigns residential addresses as “student addresses” until the number of students matches up, and
2.	looks at the percentages of students in that zip that go to different schools, and randomly assigns schools to student addresses based on that distribution. 

From there, we assign any other necessary information (such as the household’s grade level, and the associated safe distance to walk as specified by BPS criteria) and the student’s bell time, which is randomly selected from the three possible times of 7:30, 8:30, and 9:30 to conform to the city-wide bell distribution (a roughly 40%-40%-20% split between the respective bell times). Finally, we store this data in the `GeoJSON` format, which is easily readable and more standardized among the data science community. (We also provide a function to output the dataset as an Excel spreadsheet.)

Looking at the resulting dataset, we notice a much tighter clustering: for the most part, students tend to go to schools nearby to them. This is what we would expect from a realistic dataset.

![New Randomized Student Dataset]( https://raw.githubusercontent.com/Data-Mechanics/bps-simulated-data/master/visualization.png)

### Developing a Candidate Algorithm for the Transportation Challenge

Once we had finished developing a randomized dataset for the Transportation Challenge, our focus shifted to actually developing a candidate solution to the problem at hand.

We consider the following optimization a “baseline;” that is, we expect to do better in future iterations. As-is, this is a naïve solution that should benchmark how well-optimized the current BPS bus system is.

The first step in our algorithm is finding optimal bus stops for the student body. As outlined above in the summary of existing research, we worked on a very similar problem during the Data Mechanics class in optimizing the MBTA’s bus stops, and we decided to apply that approach here. The process for generating bus stops is roughly as follows:

1.  Use k-means on the student dataset to generate potential stop locations, and
2.  assign students to the generated stops, following the constraints set out by BPS about student walking distance and neighborhood safety

This algorithm will work on any student dataset, though we test it on our randomized dataset.

Next, we need a graph representation of Boston's roads, which we generate using the `geoql` and `networkx` Python libraries. We use `geoql` to filter out roads that do not meet the bus stop criteria (ex. highways, or roads that are too narrow to fit buses), and `networkx` to find the largest connected segment.

Both these datasets, in addition to school coordinate information, are fed into the routing algorithm itself, which produces the desired bus routes. Before starting, we project the kmeans-generated bus stops onto the `networkx` graph as "stop nodes," giving us one dataset to work with that has all the necessary information to produce the routes. Once this is complete, the algorithm runs:

1. **Initialization:** every stop starts with at least one bus (up to as many needed to hold all students assigned to that stop). Total driven miles is equal to the length of all routes combined.
2. **Assignment:** For every route, individually test a merge with every other route and calculate a new potential route which combines both routes' stops, and the new route's potential distance and capacity is calculated
    * After each route potential is calculated, the route potential that reduces the total distance the most is accepted as the next update to the current state
3. Termination check: The total distance of all routes is calculated with the new potential route combination
    * If the new potential route would increase the total distance, then the algorithm terminates in the current state of routes without the new route
    * If the new potential route would cause a student to be on the bus longer than the maximum of 60 minutes, then the algorithm terminates in the current state of routes without the new route
4. Update: the current state is updated, and the combined route replaces the two original routes for the next iteration

When this algorithm finishes running, it will output all bus routes and stops from start to end, with total drive distance minimized.

### Conclusion

With no good way to test our algorithm in practice short of deploying it for a few days in the City of Boston, we really don't know how well our algorithm will stack up to the existing system in BPS. However, our advisor, Andrei Lapets, is currently working independently on an evaluation tool for submissions to the Transportation Challenge, so we should at least have some metric for how well we end up doing relative to other proposed solutions. 

The most obvious candidate for future research is the routing algorithm. As mentioned before, what we have now is a baseline, and we really only worked seriously with one graph algorithm. We anticipate that applying more advanced techniques and digging deeper into graph theory could easily yield major improvements. In addition, the generated student dataset could also be improved for future transportation challenges. Some of the assumptions we made in making the dataset were naive; for example, we assume that only one student maximum lives in every household. This assumption held because the number of students was less than the total number of residences for every zip code, but an enriched dataset that takes into account the relative proportions of multi-student households would undoubtedly provide a more accurate picture of the City of Boston's students for researchers to play with.

Much of the code for this research project is hosted in private repositories; if you are interested in having a look at our work, please let us know.
