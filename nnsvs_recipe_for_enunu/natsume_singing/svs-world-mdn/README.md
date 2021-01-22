# natsume_singing/svs-world-mdn
This recipe makes use of Recurrent Mixture Density Networks for duration/acoustic model and optimized for ENUNU.

- timelag model: FeedForwardNet num\_layers 2, hidden\_dim 128
- duration model: RMDN, num\_gaussians 4, num\_layers 2, hidden\_dim 256
- acoustic model: RMDN with mlpg(dim-wise), num\_gaussians ,4 num\_layers 2, hidden\_dim 256
