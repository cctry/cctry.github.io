---
title: 'Weight sharing in GPT'
date: 2025-03-21
permalink: /posts/2025/03/weight-sharing-in-gpt/
tags:
  - LLM
---

One caveat of the GPT model is that it uses the same matrix for both word embedding and decoding. 

As shown in the paper, the token embedding matrix $W_e$ is used again to multiply with $h_n$ to get the logits for the next token.![](/images/posts/GPT2.png)

This can also be seen in the code snippet from the official [GPT2 repository](https://github.com/openai/gpt-2/blob/9b63575ef42771a015060c964af2c3da4cf7c8ab/src/model.py#L171C9-L171C58):
```python
# word embedding
wte = tf.get_variable('wte', [hparams.n_vocab, hparams.n_embd], 
                      initializer=tf.random_normal_initializer(stddev=0.02))
... # model forward pass
h = norm(h, 'ln_f')
h_flat = tf.reshape(h, [batch*sequence, hparams.n_embd])
# hidden states to token logits
logits = tf.matmul(h_flat, wte, transpose_b=True) 
```

Actually, this is from the orginal *Attention is all you need* paper, where this techniques is adopted from the paper [Using output embedding to improve language models](https://aclanthology.org/E17-2025.pdf). 

The word embedding matrix ($W_e$) is a $[\text Vocab, D]$ matrix where each row represents the embedding of each token. The decode matrix $W_d$ is a $[\text Vocab, D]$ matrix multiplied to the hidden state vector $h$ with transpose to get the logits, 
$$\text logits = h \cdot W_d^T$$

The logits are passed to a softmax layer and then to a cross entropy loss function to compute the loss. Therefore, the gradient of $W_d$ is computed as 
$$\frac{\partial L}{\partial W} = (p - y)h^T,$$
where  $p$ is the probability after the softmax; $y$ is  the label (one hot).

Inside the $p-y$ vector, only at the position of correct token ($i$) is negative: $p_i-1$, others are positive $p_j-0$.
Therefore, when performing gradient descent on the $i^{th}$ row of $W$, we have
$$W_i = W_i - \eta(p_i-y_i)h^T$$

Since $p_i-y_i$ is negative, the $h$ is added to $W_i$. As a result, the updated $W_i$ will be in the middle of the original $W_i$ and $h^T$. As the pretraning proceeds, $W_i$ becomes closer to $h^T$.

$h$ is a contextualized representation of the next token. Multiplying $h$ with $W_d$ is to compute the cosine similarity of every token's representation in $W_d$ with $h$. Assuming the model is overfitting, it should give the correct token directly. This means that the $h$ should be identical to the $i^{th}$ row of $W_d$.

Now, we have seen an interesting analogy. Both the row $i$ in $W_e$ and $W_d$ are the representation of the toeken $i$. Therefore, it is reasonable to reuse $W_e$ as $W_d$. 

Given this practice, we can have another interesting observation. The GPT's output $h$ is essentially a weighted sum of all possible tokens' embeddings. That is to say, the GPT exactly knows its task is to generate the next token based on all previous tokens.
