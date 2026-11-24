# 18.3 Sentiment analysis - naive Bayes Bernoulli

- Section: 18.3
- Asset class: Cryptocurrencies
- Harness status: **not testable: other data not available** - needs a text or sentiment feed and a trained classifier.

## Description (paper)

Social media sentiment analysis based strategies have been used in stock trading 230

and also applied to cryptocurrency trading. The premise is to use a machine learning classification scheme to forecast, e.g., the direction of the BTC price movement based on tweet data. This entails collecting all tweets containing at least one keyword from a pertinent (to BTC price forecasting) learning vocabulary V over some timeframe, and cleaning this data. 231 The resultant data is then further processed by assigning a so-called feature ( *M -vector) X i to each tweet labeled by i = 1 ,..., N, where N is the number of tweets in the dataset. Here M = \| V \| is the number of keywords in the learning vocabulary V. So, the components of each vector X i are X ia, where *a = 1 ,..., M labels the words in V. Thus, if the word w a ∈ V labeled by a is not present in the tweet T i labeled by i, then X ia = 0. If w a is present in T i, then we can set X ia = 1 or X ia = n ia, where n ia counts the number of times w a appears in T i. In the former case (which is what we focus on in the following) we have a Bernoulli probability distribution, while in the latter case we have a multinomial distribution.

Next, we need to build a model that, given the N feature vectors X i, predicts one out of a preset number K of outcomes (so-called classes) C α, α = 1 ,..., K. E.g., we can have K = 2 outcomes, whereby BTC is forecasted to go up or down, which can be used as the buy/sell signal. Alternatively, as in the ANN strategy in Subsection 18.2, we can have K quantiles for the normalized returns b *R ( *t). Etc. This then defines our trading rules. Once the classes C α are chosen, a simple way to forecast them is to build a model for conditional probabilities P ( *C α \| X 1 ,..., X N). Here, generally, P ( *A \| B) denotes the conditional probability of A occurring assuming *B is true. Pursuant to Bayes' theorem, we have

P(A\|B) = P(B\|A) P(A)

P ( B ) (538)

where P ( *A) and P ( *B) are the probabilities of A and B occurring independently of each other. So, we have

P(C\alpha|X1,..., XN) = P(X1,..., XN|C\alpha) P(C\alpha)

P ( X 1,..., X N ) (539)

Note that P ( *X 1 ,..., X N) is independent of C α and will not be important below. Now, P ( *C α) can be estimated from the training data. The primary difficulty is in

estimating P ( *X 1 ,..., X N \| C α). Here a simplification occurs if we make the "na¨ıve" conditional independence assumption (hence the term "na¨ıve Bayes"), i.e., that, given the class C α, for all i the feature X i is conditionally independent of every other feature X j, j = 1 ,..., N ( *j ̸ = i):

P(Xi|C\alpha, X1,..., Xi−1, Xi+1,..., XN) = P(Xi|C\alpha) (540) Then Eq. (539) simplifies as follows:

$$ P(C\alpha|X1,..., XN) = \gamma P(C\alpha) $$

N Y $$ i=1 $$

The conditional probabilities P ( *X i \| C α) can be estimated using the conditional probabilities P ( *w a \| C α) for the M words w a in the learning vocabulary V: $$ P(Xi|C\alpha) = $$

M Y $$ a=1 $$ ia\alpha (543)

Qiaα = P(wa|C\alpha), $$ Xia = 1 $$ (544) Qiaα = 1 −P(wa|C\alpha), $$ Xia = 0 $$ (545)

The conditional probabilities P ( *w a \| C α) can simply be estimated based on the occurrence frequencies of the words w a in the training data. Similarly, the probabilities *P ( *C α) can be estimated from the training data. 232 So, if we set the forecasted value *C pred of the outcome to that with the maximum P ( *C α \| X 1 ,..., X N), then pred = argmax C\alpha\in{1,...,K}P(C\alpha)

N Y $$ i=1 $$

M Y $$ a=1 $$

[P(wa|C\alpha)]Xia[1 −P(wa|C\alpha)]1−Xia (546)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 18.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
