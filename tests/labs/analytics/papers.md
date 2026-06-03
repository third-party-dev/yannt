
- [TrojAI Literature Review](https://github.com/usnistgov/trojai-literature)

- [TOP: Backdoor Detection in Neural Networks via Transferability of Perturbation](https://arxiv.org/pdf/2103.10274)

- [Scalable Backdoor Detection in Neural Networks](https://arxiv.org/pdf/2006.05646)

- [STRIP: A Defence Against Trojan Attacks on Deep Neural Networks](https://arxiv.org/pdf/1902.06531)

- [Fingerprinting Deep Learning Models via Network Traffic Patterns in Federated Learning](https://arxiv.org/pdf/2506.03207)

- [FLARE: A Wireless Side-Channel Fingerprinting Attack on Federated Learning](https://arxiv.org/pdf/2512.10296)

- [A Fingerprint for Large Language Models](https://arxiv.org/pdf/2407.01235)

- [LLMs Have Rhythm: Fingerprinting Large Language Models Using Inter-Token Times and Network Traffic Analysis](https://arxiv.org/html/2502.20589v1)

- [A Fingerprint Scheme for Deep Neural Network Models Based on Adversarial Samples](https://dl.acm.org/doi/10.1145/3689236.3689266)

- [Intrinsic Fingerprint of LLMs: Continue Training is NOT All You Need to Steal A Model!](https://arxiv.org/abs/2507.03014)

Claude Things:

1. Why sigmoid mid-network is architecturally meaningful (the legitimate uses)

  - **Gated Linear Units (GLU)** — [Dauphin et al. (2017), "Language Modeling with Gated Convolutional Networks" (arXiv:1612.08083, ICML 2017)](https://arxiv.org/abs/1612.08083), introduced the GLU as a component-wise product of two linear projections, one of which is first passed through a sigmoid function. This is the canonical legitimate use of a mid-network sigmoid: it's always paired with a parallel linear branch and acts as a learned soft gate. [Shazeer (2020), "GLU Variants Improve Transformer" (arXiv:2002.05202)](https://arxiv.org/abs/2002.05202), extended this to SwiGLU/GEGLU used in LLaMA, PaLM, and most modern LLMs.

  - Unsure why this citation was used: [The Fingerprint of Architecture - Sketch-Based Design Methods for Researching Building Layouts Through the Semantic](https://www.researchgate.net/publication/241186084_The_Fingerprint_of_Architecture_-_Sketch-Based_Design_Methods_for_Researching_Building_Layouts_Through_the_Semantic)
  
  - **Highway Networks** — [Srivastava, Greff & Schmidhuber (2015) (arXiv:1505.00387, NeurIPS 2015)](https://arxiv.org/abs/1505.00387) introduced highway networks, which employ a transform gate and carry gate using sigmoid functions to determine whether information should be transformed and passed forward or carried through unchanged. . This is the other major legitimate use: sigmoid mid-network as an information routing mechanism across depth.
  
  - **Mixture of Experts gating** — In MoE architectures, a gating network takes input data and calculates a set of weights determining the contribution of each expert, ensuring the most relevant experts are assigned more weight for a given input. ["Sigmoid Gating is More Sample Efficient than Softmax Gating in Mixture of Experts" (arXiv:2405.13997)](https://arxiv.org/abs/2405.13997). Sigmoid-based gating here literally performs routing between sub-networks.
  
  Therefore: **every major use of sigmoid mid-network in the literature involves information routing or gating**.

2. Why unexpected ops in unusual positions are a forensic red flag (the security angle)

  - The backdoor/trojan literature is where the *suspicious* side lives, but it focuses on activation patterns and weight distributions rather than op-position specifically:

    > Hidden features trained into a model are only activated by specific trigger inputs, causing the model to produce unexpected behaviour — while behaving normally on clean inputs. [(Li et al., arXiv:1909.02742)](https://arxiv.org/abs/1909.02742)

The forensic implication — that unusual op placement can reveal hidden routing — comes from combining these two observations: (a) sigmoid mid-network is the canonical architectural primitive for conditional routing, and (b) hidden behaviours in trojaned models require some form of conditional computation.


```python
# Sigmoid mid-network without a parallel branch (no GLU/highway skip structure)
# is anomalous because legitimate uses always involve paired branches:
#   - GLU: sigmoid(Wx) ⊗ Vx  [Dauphin et al. 2017, arXiv:1612.08083]
#   - Highway: H(x)·T(x) + x·(1-T(x))  [Srivastava et al. 2015, arXiv:1505.00387]
# An isolated sigmoid without this structure warrants inspection — it may be
# a gating/routing primitive whose purpose is not self-evident from the graph alone.
```
