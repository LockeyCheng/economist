What Google searches and GDP can tell you about footballing success

Our model identifies what makes a country good at football—and who the outliers are

https://cdn.static-economist.com/sites/default/files/images/2018/06/articles/main/20180616_blp519.jpg

WITH the World Cup about to start, fans around the planet are squabbling over who has the best chance of winning it. The betting markets suggest that there is little to separate Brazil, Germany, Spain and France, who between them have roughly a 60% probability of victory. But 

 has tried to answer a more fundamental question: what makes a country good at football in the first place?

To do so, we built a statistical model that aims to identify the underlying sporting and economic factors that determine a country’s long-term footballing performance. We downloaded the results of all international games since 1990 (which have been 

 by Mart Jürisoo, a data scientist) and tested which variables have been correlated with the goal difference between teams.

We started with money. Stefan Szymanski, an economist at the University of Michigan who has built a similar model, has shown that wealthier countries tend to enjoy more sporting success. Football has plenty of rags-to-riches stars, but those who grow up in poor places face the greatest obstacles. In Senegal, for instance, coaches have to deworm and feed some players before they can train them. So we included GDP per capita at purchasing power parity in our model. Holding all other factors constant, having twice the wealth of your opponent was associated with scoring 0.2 goals more than them in a head-to-head fixture.

Then we tried to gauge football’s popularity. In 2006 FIFA, the sport’s governing body, asked national federations to estimate the number of teams and players, of any standard, in their countries. Between two otherwise identical competitors, having twice as many players as your opponent was worth about 0.2 goals, and twice the teams nearly 0.1 goals.

To these we added population figures, expecting bigger to mean better. Surprisingly, we found the opposite: for two countries similar in every other way, including their number of players—say Italy and Japan, both with nearly 5m footballers—the one with a bigger overall population (Japan, with 127m to Italy’s 61m) generally fared worse. Football is probably a lower priority in such places. After controlling for the pool of available talent, every 100m of population more than your opponent was penalised by about 0.1 goals per game.

We supplemented FIFA’s guesses with more recent data: the average rate at which people searched for football on Google between 2004 and 2018, relative to other team sports (such as rugby, cricket, American football, baseball, basketball and ice hockey). Football got 90% of Africa’s attention over that period, compared with 20% in America and just 10% in cricket-loving South Asia. With all else constant, having ten percentage points’ more Google interest in football than your opponent was worth 0.1 goals. We also included Olympic medals won per person to capture national enthusiasm for, and spending on, sports in general. Each additional medal gained per million people was worth 0.2 goals, after controlling for all other variables.

Next we accounted for home advantage, which is worth about 0.6 goals per game, and for strength of opposition. For example, Peru has conceded a deficit of nearly 0.2 goals per game, but its opponents have also been about 0.6 goals per game better than a median international side. So we gave Peru an adjusted goal difference of 0.4 goals per game more than a median country.

Finally, to reduce the distorting effect of hapless minnows like the Cayman Islands and Bhutan, we whittled down our results to the 126 countries that have played at least 150 matches since 1990.

Our model has its limitations. Its measures of interest and participation do not cover the whole period, so we cannot capture the effect of football’s changing popularity around the world. Using goal difference as a benchmark of success means that a match-winning goal in a World Cup final counts as much as the final score in an 8-0 thumping.

But even with these imperfections, our model can account for 40% of the differences between countries’ average goal margin over 28 years. More importantly, it can identify those national teams that have consistently performed at a higher level than their economic and sporting potential would suggest.

Uruguay was one of the biggest outliers, managing nearly a goal per game better than predicted. Brazil, Argentina, Portugal and Spain were all overachievers, as were many countries in west Africa and the Balkans. Surprisingly, China and many Middle Eastern teams have actually exceeded our model’s very low expectations.

In contrast Germany’s wealth, obsession with the sport, vast pool of players and excellent sporting infrastructure should have allowed it to dominate all other challengers by at least 0.4 goals per match. (That is not far from the 0.6 goals that mighty Bayern Munich have enjoyed over plucky Borussia Dortmund since 1990, winning 17 league titles to Dortmund’s 5.) In reality, the reigning world champions have merely been one of a handful of strong national teams.

Our model’s outliers and biggest improvers hold many valuable lessons for ambitious football officials around the world. You can read about them in this week’s 

.