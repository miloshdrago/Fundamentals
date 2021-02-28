# Hey guys these three methods all do exactly the same thing
# there is no noticable performance difference
# only thing is that the short version looks nicer

# good old loop

sent_list = []

t_size = tweets['sanitized_text'].shape[0]
start=datetime.datetime.now()

print("I am going to classify %d tweets!" % t_size)
number = 0

for t in tweets['sanitized_text']:
    starttime=datetime.datetime.now()
    foo = classifier.classify(extract_features(t))
    sent_list.append(foo)
    number+= 1
    
    if number % 1000 == 0:
        t_size -= number
        print("%d tweets classified!" % number)
        print("Classification rate is %d tweets in %s seconds" % (number, str(datetime.datetime.now()-starttime)))
        print("%d tweets left to go!" % (t_size))
        print("Last classification was: %s\n" % foo)
        number = 0

print("This took : %s" % str(datetime.datetime.now()-start) )

# same thing using .map()

starttime=datetime.datetime.now()    
print("Classifying %d tweets at %s" % (tweets.shape[0], starttime))
tweets['sentiment'] = tweets['sanitized_text'].map(lambda a: classifier.classify(extract_features(a)))
print("This took %s " % str(datetime.datetime.now() - starttime))

# same thing using .apply()

starttime=datetime.datetime.now()    
print("Classifying %d tweets at %s" % (tweets.shape[0], starttime))
tweets['sentiment'] = tweets['sanitized_text'].apply(lambda a: classifier.classify(extract_features(a)))
print("This took %s " % str(datetime.datetime.now() - starttime))
