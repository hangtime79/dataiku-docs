#import "template.typ": *

#show: project.with(
  title: "Method for computing muticlass ROC AUC",
  authors: (
    (name: "Dataiku DSS", affiliation: "www.dataiku.com"),
  ),
  abstract: [
    This document explains the methodology implemented to compute the ROC AUC for multiclass classification models in Dataiku DSS.
  ],
  num: none
)

= General Formula
​
We define $"MROC"_"AUC"$ as an equivalent of $"ROC"_"AUC"$ for multiclass classification. \
Let $C$ be the number of classes,
​
$ "MROC"_"AUC" = 1/(C times (C - 1)) dot.c sum_(i=0)^(C-1) sum_(j=0, j eq.not i)^(C - 1) A(i,j) $

= Detail of how $A(i,j)$ is computed

== Input arrays

#grid(columns: (1fr, auto), gutter: 3em, [
  Let $y_"truth"$ be the array of ground truth class values (in ${0, dots, C - 1}$). It is of shape $(M, 1)$, i.e. $M$ rows and $1$ column:
],[ $
  y_"truth" = 
    lr(vec(3, 1, dots.v, 0) space.quad })
    #stack([$M$ rows,], v(0.5em), [values $in {0, dots, C - 1}$])
$])

#grid(columns: (1fr, auto), gutter: 3em, [
  Let $y_"probas"$ be the array of predicted probabilities. Each column $i$ corresponds to a class $i$, where values are probability estimates for the class $i$. It is of shape $(M, C)$, i.e. $M$ rows and $C$ columns:
],[$
  y_"probas" =
  lr(
    underbrace( mat(
      0.1,    0.9,    dots.h,    0      ;
      0.8,    0,      dots.h,    0.2    ;
      dots.v, dots.v, dots.down, dots.v ;
      0,      0,      dots.h,    0.7    ;
      0,      0.1,    dots.h,    0.9    ;
    ), #text(size: 1.5em)[$C "cols"$])
    space.quad },
    size: #(100% - 3em)
  ) M "rows"
$])

== $A(i,j)$ computation

For every pair of classes $i eq.not j$, let $L_(i,j)$ be the subset of rows of $y_"truth"$ where the ground truth is either $i$ or $j$.

$ L_(i,j) = lr({ k in {0, dots, M - 1} | y_("truth", k) = i "or" y_("truth", k) = j }) $

With $y_("truth", L_(i, j))$ and $y_("proba", L_(i, j))$ the corresponding arrays with only these rows
- Let $y_("truth", L_(i, j),"binarized")$ be a copy of $y_("truth", L_(i, j))$ with all values at $j$ set to $0$ and all at $i$ set to $1$
- Note $y_("probas", L_(i, j), "col" i)$ the column $i$ of $y_("probas", L_(i, j))$

$ A(i,j) = "ROC"_"AUC"(
  y_("truth", L_(i, j),"binarized"),
  y_("probas", L_(i, j), "col" i)
) $
with $"ROC"_"AUC"$ the usual binary classification ROC AUC metric.
