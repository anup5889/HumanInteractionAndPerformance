__author__ = 'anupdudani'
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import matplotlib.mlab as mlab


from Intial import joinSenderAggDetectedAgg,modificationOfBluetootDF

ParticipantsDF= pd.read_csv("data_for_task/Participants.csv")
TransactionsDF=pd.read_csv("data_for_task/Transactions.csv")
"""
def modificationOfTransactionDF():
    modifiedTransactionsDF=pd.merge(TransactionsDF,ParticipantsDF, left_on='assigned.to',right_on='badge.id')
    del modifiedTransactionsDF["badge.id"]
    return modifiedTransactionsDF
"""
modifiedTransactionsDF=pd.merge(TransactionsDF,ParticipantsDF, left_on='assigned.to',right_on='badge.id')
del modifiedTransactionsDF["badge.id"]
print modifiedTransactionsDF
modifiedTransactionsDF.columns

aggregatedDF=modifiedTransactionsDF.groupby( [ "assigned.to", 'complexity','team']).count().reset_index()
print aggregatedDF[aggregatedDF['assigned.to']==267]
print aggregatedDF.info()




def plotGraphs():
    plt.figure()
    sns.factorplot(x="assigned.to", y="assign.date", hue='team',\
                   data=aggregatedDF.groupby(['assigned.to','team']).sum().reset_index(),
                       kind='bar',size=6, palette="muted", legend_out=False)
    plt.xlabel("Badge ID")
    plt.ylabel("Number of Tasks completed in total")
    plt.title("Number of total tasks completed by an Employee")
    sns.factorplot(x="assigned.to", y="assign.date", hue='complexity', data=aggregatedDF,
               size=6, kind="bar", palette="muted",legend_out=False)
    plt.xlabel("Badge ID")
    plt.ylabel("Number of Tasks completed by complexity")
    plt.title("Number of tasks completed by an Employee")
    plt.show()
plotGraphs()
InteractionDF=joinSenderAggDetectedAgg()

#print InteractionDF.head()


def createScoreColumn():
    aggregatedDF['score']=aggregatedDF['complexity'].apply(lambda x: 3 if x=="Complex" else 2 \
        if x=="Advanced" else 1)
    aggregatedDF['score']=aggregatedDF['score']*aggregatedDF['assign.date']
    return aggregatedDF
aggregatedDF=createScoreColumn()
print aggregatedDF[aggregatedDF['assigned.to']==267]
print len(aggregatedDF), len(createScoreColumn())

#print aggregatedDF
print aggregatedDF[["assigned.to", "score"]]
#aggregatedDF
aggregatedDF=aggregatedDF.groupby( by=[ "assigned.to"])["score"].sum().reset_index()


JoinedInteractionPerformance=pd.merge(aggregatedDF,InteractionDF, left_on="assigned.to", right_on="ID")
JoinedInteractionPerformance=JoinedInteractionPerformance[JoinedInteractionPerformance["Team"]!='Pricing']
print JoinedInteractionPerformance.describe()
del JoinedInteractionPerformance["assigned.to"]
JoinedInteractionPerformance=JoinedInteractionPerformance[['ID','score', 'coes','coed','ACSD',]]
print JoinedInteractionPerformance.head()
print JoinedInteractionPerformance.info()
print JoinedInteractionPerformance.describe()   

"""
Hypothesis testing

Divided dataframe into two parts:
PeopleWhoInteractMore: The people who interact more times than avg interaction
PeopleWhoInteractLess: The people who interact less times than the avg interaction

"""
print "Score of employee with ID 293"
PeopleWhoInteractMore=JoinedInteractionPerformance[JoinedInteractionPerformance['ACSD']> \
                                                   JoinedInteractionPerformance.ACSD.mean()]
PeopleWhoInteractLess=JoinedInteractionPerformance[JoinedInteractionPerformance['ACSD']< \
                                                   JoinedInteractionPerformance.ACSD.mean()]

def plotHistogramOfDist():
    plt.figure()
    PeopleWhoInteractLess['score'].hist( bins=20, label='InteractLess') # your code here to plot a historgram for hourly entries when it is raining
    PeopleWhoInteractMore['score'].hist(bins=20, label='InteractMore') # your code here to plot a historgram for hourly entries when it is not raining
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.title("Histogram of Scores | People Interact More Vs People Who Interact Less")
    plt.legend()
    plt.show()
#plotHistogramOfDist()
print PeopleWhoInteractLess.describe()
print PeopleWhoInteractMore.describe()

result=scipy.stats.ttest_ind(PeopleWhoInteractMore['score'], PeopleWhoInteractLess['score'], equal_var=False)
print result

result2=scipy.stats.ranksums(PeopleWhoInteractMore['score'], PeopleWhoInteractLess['score'])
print result2

result3=scipy.stats.mannwhitneyu(PeopleWhoInteractMore['score'], PeopleWhoInteractLess['score'])
print result3


"Variance of the two populations are diff"
print "Variance of the two populations"
print PeopleWhoInteractLess['score'].var()
print PeopleWhoInteractMore['score'].var()


#df['color'] = df.Set.map( lambda x: 'red' if x == 'Z' else 'green')
