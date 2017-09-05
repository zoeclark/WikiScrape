# WikiScrape
### This application returns
1) The 50 most frequent wikipedia pages associated with a given seed wikipedia page: 
  User inputs a Wikipedia page and a recursion level, application goes to every pages that page links to, and every page that  page links to, and so on, until the depth of recursion reaches the recursion level selected.   I am trying to solve a problem I encounter when reading technical wikipedia pages: I can't begin to understand the page  without first understanding some of articles the pages links me to. This application suggests a starting point. 

2) The 50 best paths through the wikipedia pages associated with the seed wikipedia page:
  The application treats the wikipedia URLs as observable variables and the URLs parent (the page it came from) as a "hidden"  variable and uses a hidden Markov Model (AKA Naive Bayes) to guess the best paths through the associated pages, starting  with the seed page. I often find wikipedia "worm holes" where one interesting page leads to another and so on, and I wanted this application to guess the best lines of inquiry. 


### To Run:<br />
<p> Script takes 2 arguments from the command line: 1 = URL, 2 = recursion level. If the 3rd argument is 'one paragraph,' the script will only read the first paragraph of the wiki pages, not the full article. </p>

**Example**: ```python wikiScrape.py https://en.wikipedia.org/wiki/Post-postmodernism 3 one paragraph``` <br />
**Run Time:**
Running the application with a recursion level of 2 takes on average 5 minutes with a solid connection. A recursion level of 3 takes me on  average 25 minutes. Ideally, a multi-threaded program would make multiple queries at the same time, but I don't want to step on Wikipedia's toes. 
  
### Algorithm Notes:  <br />
<p> The application tracks all the best "bigrams" (pairs of wiki URLs and parent wiki URLs). Then the algorithm then examines the 5 most likely paths back to seed URL from the bigram and selects the longest path. For a given "bigram," the top 5 paths back to the seed URL are  typically multiple linear representations of the same cyclic information, so the longer the path, the more complete the (linear) representation of the cycle. I hope to return the information visually one day. A classic HMM would not use the most frequently occurring bigrams like I did; it would use the conditional probability of the bigram (the url and parent url) based on the unigram (just the url) I chose not to do this because the problem isn't interested in a probability distribution over the different paths, it just wants the most frequently occurring paths.</p> 
