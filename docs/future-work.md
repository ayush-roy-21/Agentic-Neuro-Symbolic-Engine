# Deliberately out of scope

Named here on purpose — these were considered and cut for stated
reasons, not silently dropped. Worth lifting close to verbatim into
the final report; examiners read explicit scoping as maturity, not as
a gap.

- **Training the transformer via DE/PSO instead of backprop.**
  Population-based search needs a full forward pass per individual,
  per generation — at transformer parameter counts that's orders of
  magnitude more compute than backprop for the same result, and worse
  on a CPU-only laptop specifically. DE/PSO here is used only to tune
  a handful of signal-blend weights, not the model itself.

- **A literal production execution/settlement system.** "Settlement
  finality" is a specific term from real clearing systems and
  blockchain consensus — it means a transaction is guaranteed
  irreversible. Nothing here settles a real transaction. What's built
  is a simulated order-matching engine, in Rust, compiled to WASM for
  a genuinely browser-independent demo — an accurate and still
  impressive claim.

- **A fully novel SDE-transformer architecture.** Built by composing
  an existing tool (torchsde's differentiable SDE solvers) with a
  standard forecasting transformer, rather than inventing new
  architecture mathematics — the latter is an open research problem
  (see the neural-SDE literature), not a semester-scoped one.

- **Full SHAP coverage across every model in the pipeline.** SHAP on a
  sequence transformer means many masked forward passes per
  explanation — expensive even with a GPU, worse on CPU. Applied
  instead to the smaller sentiment classifier; the transformer's
  forecasts use attention-weight visualization and Integrated
  Gradients instead.
