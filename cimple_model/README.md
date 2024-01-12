### Model Objective
Given an input X for e.g. `user_id` , `act`, `obj` the model should be able to map the input to a suitable datamodel as well as to a normalised field name. Example:
- when u input `user_id` to the model, it should output `authentication` as the top suggested datamodel, followed by `data_access`. 
- The model should also be able to output the correct normalised field name `user`

Technically most ML model can be used, but we selected LogisticRegression as we need to return multiple suggestions to the frontend. The suggestions can then be sorted based on the probability returned by the model, this can be seen in `inference.py`

### Future roadmap
When we have more training data, CIMple can even be more powerful by training word embeddings. This way, we can handle any unseen input X as it can be mapped to previously seen words/tokens in the dataset.

In the long run when LLM is democratized, the process to do automated CIM mapping would be even simpler by making use of LLM's ability to semantically understand logs and datamodel names. Intuitively, an intelligent LLM model can understand what type of log it is, the fields to be mapped, and the suitable datamodel mapping. 