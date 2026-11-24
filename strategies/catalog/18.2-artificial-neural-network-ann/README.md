# 18.2 Artificial neural network (ANN)

- Section: 18.2
- Asset class: Cryptocurrencies
- Harness status: **not testable: intraday ML** - trains a neural network on intraday (15-minute) indicators; the harness is daily and stdlib-only.

## Description (paper)

This strategy uses ANN to forecast short-term movements of BTC based on input technical indicators. In ANN we have an input layer, an output layer, and some

1988\], \[Caskey, 1991\], \[D'Este, 2014\], \[Fass and Francis, 2004\], \[Maaravi and Levy, 2017\], \[McCants, 2007\], \[Shackman and Tenney, 2006\], \[Zhou et al, 2016\]. 218 Blockchain is a distributed ledger, which keeps a record of all transactions. It is a sequential chain of blocks, which are linked using cryptography and time-stamping, containing transaction records. No block can be altered retroactively without altering all subsequent blocks, which renders blockchain resistant to data modification by its very design. For a blockchain maintained by a large network as a distributed ledger continuously updated on a large number of systems simultaneously, collusion of the network majority would be required for a nefarious modification of blockchain.

number of hidden layers. So, in this strategy the input layer is built using technical indicators. 221 E.g., we can use (exponential) moving averages ((E)MAs), (exponential) moving standard deviations ((E)MSDs), relative strength index (RSI), 222 etc. More concretely, we can construct the input layer as follows (see, e.g., \[Nakano, Takahashi and Takahashi, 2018\]). Let P ( *t) be the BTC price at time t, where *t = 1 , 2 ,... is measured in some units (e.g., 15-minute intervals; also, t = 1 is the most recent time). Let:

$$ R(t) = $$ *P ( *t) *P ( *t + 1) − 1 (521) $$ eR(t, T1) = R(t) −R(t, T1) $$ (522) $$ R(t, T1) = 1 $$ *t + *T 1 X $$ t′=t+1 $$ *R ( *t ′) (523) $$ bR(t, T1) = $$ e *R ( *t, T 1 ) \sigma(t, T1) (524) $$ [\sigma(t, T1)]2 = $$ *T 1 − 1 *t + *T 1 X $$ t′=t+1 $$ \[ e *R ( *t, T 1 )\] 2 (525)

So: R ( *t) is the return from t + 1 to t; R ( *t, T 1 ) is the serial mean return from t + T 1 to t +1, i.e., over T 1 periods, where T 1 can be chosen to be long enough to provide a reasonable estimate for the volatility (see below); e *R ( *t, T 1 ) is the serially demeaned return; σ ( *t, T 1 ) is the volatility computed from t + T 1 to t + 1; and b *R ( *t, T 1 ) is the normalized (serially demeaned) return. Below, for notational simplicity we will omit the reference to the T 1 parameter and will use b *R ( *t) to denote the normalized returns.

Next, we can define EMAs, EMSDs and RSI as follows: 223 $$ EMA(t, \lambda, \tau) = 1 −\lambda $$ 1 −\lambda\tau t+\tau X $$ t′=t+1 $$ *t ′ − t − 1 b *R ( *t ′) (526) $$ [EMSD(t, \lambda, \tau)]2 = 1 −\lambda $$ \lambda −\lambda\tau t+\tau X $$ t′=t+1 $$ λt′−t−1 [ bR(t′) −EMA(t, λ, \tau)]2 (527)

$$ RSI(t, \tau) = $$ \nu+(t, \tau) \nu+(t, \tau) + \nu−(t, \tau) (528) $$ \nu\pm(t, \tau) = $$ t+\tau X $$ t′=t+1 $$ max(± bR(t′), 0) (529)

Here: τ is the moving average length; λ is the exponential smoothing parameter. 224

221 Thus, in spirit, it is somewhat similar to the single-stock KNN trading strategy discussed in Subsection 3.17, which utilizes the k-nearest neighbor (KNN) algorithm (as opposed to ANN).

The input layer can then be defined as consisting of, e.g., b *R ( *t), EMA( *t, λ a , τ a), EMSD( *t, λ a , τ a), and RSI( *t, τ ′*

*a ′), where a = 1 ,..., m, a ′ = 1 ,..., m ′. The values τ a can, e.g., be chosen to correspond to 30 min, 1 hr, 3 hrs and 6 hrs (so m = 4; see fn. 224 for the values of λ a). The values τ ′ a ′ can, e.g., be chosen to correspond to 3 hrs, 6 hrs and 12 hrs (so m ′ = 3). There is no magic bullet here. These values can be chosen based on out-of-sample backtests keeping in mind, however, the ever-present danger of over-fitting various free parameters (see below), including τ a, λ a and τ ′*

*a ′. The output layer can be constructed as follows. Let the objective be to forecast which quantile the future normalized return will belong to. Let the number of quantiles be K. Thus, for the values of t corresponding to the training dataset *D train, 225 we have the normalized returns b *R ( *t), t ∈ D train. Let the ( *K − 1) quantile values of b *R ( *t), t ∈ D train, be q α, α = 1 ,..., ( *K − 1). For each value of t, we can define the supervisory K -vectors S α ( *t), α = 1 ,..., K, as follows:         

$$ S1(t) = 1, $$ $$ bR(t) \leqq1 $$ $$ S\alpha(t) = 1, $$ $$ q\alpha−1 \leqbR(t) < q\alpha, $$ 1 < \alpha < K $$ SK(t) = 1, $$ $$ qK−1 \leqbR(t) $$ $$ S\alpha(t) = 0, $$ otherwise (530)

The output layer can then be a nonnegative K -vector p α ( *t), whose elements are interpreted as the probabilities of the future normalized return to be in the α -th quantile. So, we have

K X $$ \alpha=1 $$ $$ p\alpha(t) = 1 $$ (531)

The output layer is constructed from the input layer as some nonlinear function thereof with some number of parameters to be determined via training. In ANN we have L layers labeled by ℓ = 1 ,..., L, where ℓ = 1 corresponds to the input layer, and ℓ = L corresponds to the output layer. At each layer we have N ( *ℓ) nodes and the corresponding N ( *ℓ) -vectors *⃗X ( *ℓ) with components X ( *ℓ) $$ i(ℓ), i(ℓ) = 1,..., N (ℓ):226 $$ ( *ℓ) $$ i(ℓ) = h(ℓ) $$

*i ( *ℓ) ( *⃗Y ( *ℓ) ) , ℓ = 2 ,..., L (532) ( *ℓ) $$ i(ℓ) = $$ *N ( *ℓ − 1) X $$ j(ℓ−1)=1 $$ ( *ℓ)

*i ( *ℓ) *j ( *ℓ − 1) X ( *ℓ − 1) *j ( *ℓ − 1) + B ( *ℓ) *i ( *ℓ) (533)

Here: *⃗Y ( *ℓ) is an N ( *ℓ) -vector with components Y ( *ℓ) $$ i(ℓ), i(ℓ) = 1,..., N (ℓ); X(1) $$

*i (1) are the input data (for each value of t, i.e., b *R ( *t), EMA( *t, λ a , τ a), EMSD( *t, λ a , τ a), and RSI(t, \tau ′ *a ′) - see above); X ( *L)

*i ( *L) are the output data p α ( *t) (i.e., N ( *L) = K and the index

225 Ideally, when computing the quantiles, an appropriate number d 1 of the values of t = *t d , t d − 1 ,..., t d − d 1 +1, d = \| D train \|, should be excluded to ensure that all the EMA, EMSD and RSI values are computed using the required numbers of datapoints.

( *L) is the same as α); the unknown parameters A ( *ℓ)

*i ( *ℓ) *j ( *ℓ − 1) (the so-called weights) and ( *ℓ)

*i ( *ℓ) (the so-called bias) are determined via training (see below); and there is much arbitrariness in terms of picking the values of N ( *ℓ) and the so-called activation functions h ( *ℓ)

*i ( *ℓ). A possible choice (out of myriad others) is as follows (see, e.g., \[Nakano, Takahashi and Takahashi, 2018\]): 227 ( *ℓ) $$ i(ℓ)(⃗Y (ℓ)) = max $$  ( *ℓ) *i ( *ℓ) , 0  , ℓ= 2,..., L −1 (ReLU) (534)

( L )

i(L)(⃗Y (L)) = Y (L) *i ( *L)  

N ( L ) X $$ j(L)=1 $$

( L ) *j ( *L)   *− 1 (softmax) (535)

I.e., ReLU is used at the hidden layers (and the algorithm moves onto the next layer only if some neurons are activated (fired) at layer ℓ, i.e., at least some Y ( *ℓ)

i(ℓ) > 0), and softmax is used at the output layer (so that we have the condition (531) by construction). Further, to train the model, i.e., to determine the unknown parameters, some kind of error function E (we suppress its variables) must be minimized, e.g., the so-called cross-entropy (see, e.g., \[de Boer et al, 2005\]):

E = −

X *t ∈ D train*

K X $$ \alpha=1 $$ S\alpha(t) ln(p\alpha(t)) (536)

To minimize E, one can, e.g., use the stochastic gradient descent (SGD) method, which minimizes the error function iteratively until the procedure converges. 228

Finally, we must specify the trading rules. There are a number of possibilities here depending on the number of quantiles, i.e., the choice of K. A reasonable trading signal is given by: Signal = (

Buy , iff $$ max(p\alpha(t)) = pK(t) $$ Sell , iff $$ max(p\alpha(t)) = p1(t) $$ (537)

Therefore, the trader buys BTC if the predicted class is p K ( *t) (the top quantile), and sells if it is p 1 ( *t) (the bottom quantile). This trading rule can be modified. E.g., the buy signal can be based on the top 2 quantiles, and the sell signal can be based on the bottom 2 quantiles (see, e.g., \[Nakano, Takahashi and Takahashi, 2018\]). 229

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 18.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
