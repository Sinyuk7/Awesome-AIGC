# Complete Training Guide for FLUX.2 Klein on AI Toolkit

Last_Updated: 2026-03-31

## Overview

* Purpose: Distill the full training knowledge for building practical FLUX.2 Klein LoRAs in Ostris AI Toolkit, including model choice, dataset design, parameter logic, evaluation method, troubleshooting, and inference parity.
* Scope: Covers `FLUX.2 Klein 4B Base` and `FLUX.2 Klein 9B Base` LoRA training in AI Toolkit, the meaning of core settings, Base-specific sampling logic, dataset patterns for character/style/product LoRAs, VRAM planning, and post-training parity rules. Does not cover non-Klein model recipes or detailed installation SOPs.

## Core Concepts

* **FLUX.2 Klein**: A unified model family that supports both text-to-image generation and image editing. In practice, a Klein LoRA can affect both generation and editing workflows depending on dataset and caption design.
* **Base**: The non-distilled checkpoint intended for fine-tuning and LoRA training. AI Toolkit currently exposes only `FLUX.2 Klein 4B Base` and `FLUX.2 Klein 9B Base` for Klein training.
* **Distilled behavior**: A low-step inference behavior pattern. It is not the training target in the current AI Toolkit Klein workflow. Treating Base like Distilled during evaluation causes frequent misjudgment.
* **Size compatibility**: A 4B-trained LoRA only works meaningfully with 4B Base, and a 9B-trained LoRA only works meaningfully with 9B Base. Cross-size testing invalidates evaluation.
* **Training Steps**: Optimizer update duration. This is the training length control, not the preview denoising step count.
* **Sample Steps**: Denoising steps used when generating training previews or inference outputs. For Base Klein, low sample steps can make a good LoRA look weak or noisy.
* **Repeats per image**: The effective training dose per image, approximated by `repeats_per_image ≈ (S × B × G) / N`, where `S` is training steps, `B` is batch size, `G` is gradient accumulation, and `N` is image count. This is a key control variable for character likeness training.
* **Quantization**: A memory-saving mechanism used mainly to make 4B/9B training fit into available VRAM and sometimes improve practical stability under tight hardware budgets.
* **Regularization dataset**: A small general-domain dataset, usually low-weighted, added to reduce collapse or overfitting for narrow datasets such as a single character or product.
* **Inference parity**: Matching training samples at inference requires alignment of the whole pipeline, not only prompt and seed. Base model variant, scheduler semantics, resolution snapping, LoRA application mode, and required control inputs all matter.

## Consolidated Principles

* P1 [Critical]: Do not evaluate `Base` Klein with `Distilled`-style low step counts. For Base evaluation, use about `50` sample steps and guidance around `4`; otherwise weak/noisy previews may be a sampling artifact rather than a training failure.
* P2 [Critical]: Do not mix `4B` and `9B` between training and testing. LoRA validity depends on matching the exact Klein size and Base variant used during training.
* P3 [Critical]: Do not treat `Training Steps` and `Sample Steps` as the same variable. One controls learning duration; the other controls preview or inference quality.
* P4 [High]: Choose model size by stability budget before raw quality ambition. `4B Base` is the safer starting point for most users; `9B Base` can deliver stronger prompt fidelity and detail but has lower tolerance for aggressive memory-saving and unstable settings.
* P5 [High]: Optimize training dose intentionally. For character likeness, repeats per image is the primary training-dose metric; changing gradient accumulation without adjusting steps changes the effective dose.
* P6 [High]: Use clean data before aggressive tuning. Removing near-duplicates, keeping signal consistent, and aligning captions with the intended learned concept usually improves results more reliably than early hyperparameter complexity.
* P7 [High]: When 9B training destabilizes, reduce learning rate and rank before trying exotic fixes. A small regularization set and earlier checkpoint selection are preferred recovery moves.
* P8 [Normal]: Use training-preview parity as the evaluation baseline. If inference differs from AI Toolkit samples, first suspect pipeline mismatch rather than LoRA failure.

## Mechanisms & Logic

* Model selection logic:

  1. Start from task goal and hardware budget.
  2. If you need a practical and more stable starting path, prefer `4B Base`.
  3. If you have stronger VRAM headroom and can tolerate tighter stability margins, use `9B Base`.
  4. Keep the training and testing size identical throughout the workflow.
* Environment logic:

  1. Local AI Toolkit is suitable for users with a compatible NVIDIA GPU and willingness to manage their own environment.
  2. Cloud AI Toolkit is the lower-friction option for `9B Base`, larger datasets, and higher-resolution training.
  3. Workflow and UI are largely the same; the main difference is GPU location and available VRAM headroom.
* Dataset logic:

  1. **Character / likeness LoRA**:

     * Typical scale: `20–60` curated images.
     * Need variation in angle, lighting, expression, and focal behavior.
     * Captions should stay short and avoid over-describing facial micro-details.
     * A unique trigger token is recommended for controllable activation.
  2. **Style LoRA**:

     * Typical scale: `50–200` images.
     * Mix subjects so style is the only stable constant.
     * Captions should emphasize medium, palette, and lighting language.
     * Trigger word is optional but useful when explicit on/off control is desired.
  3. **Product / concept LoRA**:

     * Typical scale: `30–100` images.
     * Early-stage consistency in geometry and scale is helpful.
     * Captions should name the product and preserve key invariant attributes.
     * A trigger word is strongly recommended.
* Core configuration logic in AI Toolkit:

  1. **Job panel**:

     * Use a clear training name.
     * Use a unique trigger word for character and product LoRAs; style LoRAs may keep it optional.
  2. **Model panel**:

     * Choose `FLUX.2 Klein 4B Base` or `FLUX.2 Klein 9B Base`.
     * Use the official repository matching the selected size.
  3. **Quantization panel**:

     * Enable when VRAM is tight, especially on 9B.
     * If quantization errors appear, temporarily disable it to validate the training path, then re-enable.
  4. **Target panel**:

     * `Target Type`: `LoRA`.
     * `Linear Rank`: start `16` on 4B, expand to `32` only if clearly underfit; on 9B start at `16–32`, and prefer `16` when stability is uncertain.
  5. **Save panel**:

     * `Data Type`: `BF16` is the safe default.
     * Save cadence around `250–500` steps is practical.
  6. **Training panel**:

     * `Batch Size`: start at `1`.
     * `Gradient Accumulation`: `1–4` depending on VRAM.
     * `Learning Rate`: start around `1e-4`; reduce to `5e-5` if unstable.
     * `Steps`: for small datasets `2000–4000`; for mid-size datasets `3000–6000`; or compute from repeats-per-image for identity training.
     * For first runs, a smoke test around `1000` steps is recommended before a full rerun.
  7. **Regularization**:

     * Add a small low-weight regularization set when the dataset is narrow and 9B becomes unstable.
  8. **Datasets panel**:

     * `Default Caption` examples:

       * Character: `photo of [trigger]`
       * Style: `[trigger], watercolor illustration, soft edges, pastel palette`
       * Product: `product photo of [trigger], clean background, studio lighting`
     * `Caption Dropout Rate`: small values such as `0.05` can help in some setups.
     * `Cache Latents`: enable when available for speed.
     * Start with a single main resolution such as `1024`; add more buckets only when needed for robustness.
  9. **Sample panel**:

     * `Sample Every`: around `250–500`.
     * `Guidance Scale`: around `4`.
     * `Sample Steps`: around `50` for Base evaluation.
     * Keep seed fixed for checkpoint comparison.
     * Use `6–10` prompts close to real intended usage.
* High-likeness character training logic for `9B Base`:

  * Target training dose:

    * `50–90` repeats per image for normal identity learning.
    * `90–120` repeats per image for stronger likeness locking.
  * Compute steps with `S ≈ ceil(N × target_repeats / (B × G))`.
  * Lower gradient accumulation often gives more specific identity learning, but steps must be increased to preserve the same dose.
  * Starter settings:

    * `Batch Size`: `1`
    * `Gradient Accumulation`: `1`, or `2–4` if VRAM constrained
    * `LR`: `1e-4`, reduce to `5e-5` if collapse appears
    * `Rank`: `16`, move to `32` only when stable and underfit
    * `Resolution`: `1024`
    * `Default Caption`: `photo of [trigger]`
    * `Caption Dropout`: `0.05`
    * Preview sampling: Base-style, about `50` steps and guidance `4`
* Evaluation logic:

  1. Judge checkpoints only under Base-appropriate preview settings.
  2. If a checkpoint first improves and later degrades, stop and roll back to an earlier saved checkpoint.
  3. Treat weak/noisy outputs under `4–8` sample steps as invalid evidence for Base Klein quality.
* Inference parity logic:

  1. Align the exact base model repository and variant.
  2. Align width and height after any snapping rule.
  3. Align step count, guidance, and scheduler semantics.
  4. Align LoRA application mode such as adapter versus fuse or merge.
  5. For edit or I2V families, provide the same required control inputs.
  6. Treat runtime stack drift as a real variable when changing Diffusers, ComfyUI, CUDA, or PyTorch versions.

## Constraints

* Do not use `Distilled`-style low-step sampling to judge `Base` Klein. `4–8` step previews can falsely suggest poor training quality.
* Do not load a `4B` LoRA on `9B Base`, or a `9B` LoRA on `4B Base`. This breaks meaningful evaluation and can be misread as “LoRA has no effect.”
* Do not assume “can run inference” means “can train comfortably.” Training requires extra memory for optimizer state, activations, LoRA modules, and preview sampling.
* Do not push `9B Base` under aggressive VRAM-saving settings unless necessary. Community guidance in the material treats `9B + heavy memory pressure` as a common instability pattern.
* Do not increase gradient accumulation without revising steps if you are targeting a fixed repeats-per-image dose.
* Do not raise rank first when the model is unstable. Lower rank is a primary stabilization move; higher rank is for stable underfitting cases.
* Do not over-interpret a falling loss value if samples are being evaluated with the wrong Base sampling settings.
* Do not ignore license gating for `9B Base`. If download or access is denied, the documented fix is to accept the model license and add a Hugging Face read token in AI Toolkit settings.
* Hard boundaries and practical ranges:

  * `4B Base`: local training is realistic around `24GB` with conservative settings.
  * `9B Base`: treat `32GB+` as the comfortable local floor; cloud H100/H200 is the low-friction path for high-resolution and faster iteration.
  * Base evaluation default: around `50` sample steps and guidance `4`.
  * Common starter rank: `16`; expand toward `32` only when justified.
  * Common identity-training target: `50–90` repeats per image; `90–120` for stronger likeness emphasis.

## Derived Insights

* The highest-yield mistake to remove first is not bad hyperparameters but bad evaluation. In this material, many “LoRA is weak” diagnoses collapse once Base Klein is previewed at the correct step count.
* `4B Base` is the operational default, not merely the cheaper option. The distilled knowledge consistently frames it as the faster and more stable starting path, especially before committing to `9B` instability tradeoffs.
* For identity LoRAs, step count alone is the wrong abstraction. The actionable control variable is effective per-image exposure, which ties together dataset size, batch size, gradient accumulation, and total steps.
* The shortest safe workflow is:

  1. Start with clean data.
  2. Choose `4B Base` unless there is a strong reason for `9B`.
  3. Run a smoke test around `1000` steps.
  4. Evaluate only with Base-style sampling.
  5. Expand rank or duration only after stable evidence of underfitting.
  6. For deployment, match the training pipeline before blaming the LoRA.

# Appendix

## Conflict Register

* Conflict 1: `Sample steps ≈ 50` versus example YAML showing `sample_steps: 25`.

  * Type: Scope
  * Affects: Preview quality judgment
  * Resolution Hint: Treat `≈50` as the Base evaluation baseline for Klein guidance, while YAML values may reflect a specific user job or non-general example. Do not universalize example YAML over the Klein training guidance.
* Conflict 2: General training steps ranges versus formula-based steps for character likeness.

  * Type: Scope
  * Affects: How to decide total training duration
  * Resolution Hint: Use generic ranges such as `2000–6000` for broad first-pass training, but use the repeats-per-image formula when likeness strength is the optimization target.

## Assumptions

* A1: The current Klein training path in AI Toolkit is `Base-only`, because the materials state that AI Toolkit currently exposes only `FLUX.2 Klein 4B Base` and `FLUX.2 Klein 9B Base` in the model architecture selector.
* A2: The intended workflow is LoRA training for image-domain tasks, not full-model retraining, and the user wants reusable LoRA behavior in later generation or editing workflows.
* A3: Inference quality should be judged against AI Toolkit training samples only after base model, scheduler semantics, resolution handling, and LoRA application mode are aligned.

**Phase 6 — Report**

* Source materials used:

  * `Knowledge_Distillation_Protocol.md`
  * `Pasted text (2).txt` as the main FLUX.2 Klein training source
  * `123.txt` as the high-likeness 9B settings source
  * `Pasted text (3).txt` as the training-inference parity source
* Output result:

  * A single structured knowledge document centered on `Complete Training Guide for FLUX.2 Klein on AI Toolkit`.
* Module structure:

  * Overview
  * Core Concepts
  * Consolidated Principles
  * Mechanisms & Logic
  * Constraints
  * Derived Insights
  * Appendix with Conflict Register and Assumptions
* Exceptions and conflict notes:

  * Example YAML sample-step values differ from the general Klein Base evaluation recommendation.
  * Generic steps ranges and repeats-formula steps are both valid, but serve different scopes.
