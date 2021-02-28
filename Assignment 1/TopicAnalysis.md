# Topic Analysis
This document contains a description of the methodology used to do topic
analysis on the twitter dataset using the Latent Dirichlet Allocation
model. Hereafter, the results of the analysis, combined with a critical look at
the limitations, but also opportunities for future work, are reported.

## Methodology

### Dataset
The dataset used in this analysis contained a list of documents, where each
document is represented as a list of sanitized tweets. The sanitization process
of tweets is described in a seperate section of this paper [REFERENCE].
Due to the large number of documents, a subset of the dataset was used as
main source. This subset is reduced to 2000 documents. Also, documents that
contain no tokens or tokens that have a length shorter than three are not
used in the final analysis.

### Modeling
After the dataset setup, a model is chosen. Two different LDA models are used,
the LdaModel model provided by the `gensim` library, and the LdaMallet model.
The LdaMallet model is a model that wraps around the default LdaModel model
using a different algorithm, videlicet Mallet's algorithm. Sources claim that
Mallet's model performs better, which is tested in the next section.

### Testing and tuning
Before the model can be tuned, tests are run first. The results of these
tests should give a better insight into choosing suitable values for
the hyperparameters of the models. A model's coherence is used as indication
to how well a model performs.
Each model is trained iteratively over a list of numbers, where each number
represents *k* number of topics. The results of the iteration are shown in
figure [REFERENCE]. This figure shows the coherence scores in relation to
the number of topics. It also shows that Mallet's model shows the highest
overal coherence scores. Based on this figure, further topic modelling is
done using the LdaMallet model with a value *k* of 20 as the number of topics.

### Plotting
Using the best model, the topics can be plotted in a graph to get an 
illustrative view of the model. 
Each bubble on the left-hand side plot represents a topic. The larger the 
bubble, the more prevalent that topic is. A good topic model will have fairly 
big, non-overlapping bubbles scattered throughout the chart instead of being 
clustered in one quadrant.
A model with too many topics, will typically have many overlaps, small sized
bubbles clustered in one region of the chart.
This plot of a model trained using the optimal parameters mentioned earlier,
is shown in figure [REFERENCE].

### Results
Using the plot in figure [REFERENCE], you can see that the topics are not 
overlapping. This implies that all topics are seperated from each other. 
However, analysing the top contributer tokens of each topic, certain topics
look similar. This can mean different things. Either there are too many
topics or the documents are so complex that the topics may look closely
related but are not. 
To see if the topics are able to prove themselves useful, two new datasets
are introduced: a subset of tweets recorded in the first seven days of the
main dataset, and a subset of tweets recorded in the last seven days of the
main dataset.
If a shift in time results into models showing topics that are significantly
different, these models can lead to different insights or give a better
understanding of the data.
Figure [REFERENCE] and figure [REFERENCE] show the plots of the newly
created models. One can argue that the top contributers to each topic have
not changed much. However, the rest of the words did change. For example,
take "trump" and "hillary". The topics where those contribute the most,
contain different words between the models (i.e. first and last week).

### Future
The final trained models can be used to group messages. This grouping
technique, in combination with data labeled per state, sentiment groups, or
any other demographic metric, can possibly lead to interesting insights
into the subject groups or main dataset.
