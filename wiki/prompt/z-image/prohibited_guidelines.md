# z-image Prompt Construction Prohibited Guidelines

Last_Updated: 2025-03-05

## Overview [Required]

- Purpose: Define prohibited practices, invalid operations, and constraint violations when constructing prompts for z-image
- Scope: Covers prompt syntax bans, model mechanism limitations, content generation failures / Does not cover LoRa training, ComfyUI node parameters, model architecture details, safety filtering

## Core Concepts [Required]

- **z-image**: A few-step distilled text-to-image model that does not rely on classifier-free guidance during inference. z-image-turbo refers to the same model architecture.
- **Negative Prompt Invalidity**: z-image does not use negative prompts at all. The negative prompt input box in UI is ignored by the model.
- **Prompt Enhancer (PE)**: An upstream LLM-based template used to expand brief prompts into detailed descriptions before feeding to z-image.
- **Meta Tags**: Quality descriptors like "8K", "masterpiece", "best quality" that have no effect on z-image output.

## Consolidated Principles [Required]

- P1 [Critical]: Negative prompts are completely non-functional
  - z-image ignores negative_prompt input entirely
  - Any content placed in negative prompt boxes has zero effect on generation
  
- P2 [Critical]: CFG scale settings are invalid
  - guidance_scale values do not affect output quality or prompt adherence
  - Official pipeline uses guidance_scale = 0.0
  
- P3 [High]: Metaphorical language is prohibited in final prompts
  - Poetic expressions, similes, and figurative descriptions degrade output quality
  - z-image requires concrete, visualizable descriptions only
  
- P4 [High]: Meta tags are prohibited
  - Terms like "8K", "masterpiece", "best quality", "highly detailed" are banned
  - These tokens provide no quality enhancement for z-image
  
- P5 [High]: Tag-based prompting is invalid
  - Comma-separated tag lists ("1girl, red hair, blue eyes") perform worse than natural language
  - Tag-based syntax from Pony/SDXL models does not translate effectively
  
- P6 [Normal]: Vague descriptions are prohibited
  - Generic terms like "cute anime girl" produce inconsistent results
  - Lack of specificity causes unpredictable output variation
  
- P7 [Normal]: Output token count must not fall below 256 tokens
  - Prompts with fewer than 256 tokens produce suboptimal results
  - Context: z-image trained on detailed captions; short prompts lack sufficient conditioning signal
  
- P8 [Normal]: Negation phrases are prohibited outside extreme cases
  - Pattern "no X", "without X", "no XXX" is banned in standard prompting
  - Must use positive antonyms instead of negation
  - Context: z-image lacks CFG mechanism to process negative constraints effectively

## Constraints [Conditional]

### C1: Prohibited Prompt Syntax

- Metaphors and figurative language
  - "poetic sunset" → invalid
  - "dreamlike atmosphere" → invalid
  - "ethereal beauty" → invalid
  
- Emotional and subjective descriptors
  - "mysterious vibe" → invalid
  - "hopeful mood" → invalid without concrete visual specification
  
- Meta quality tags
  - "8K", "4K", "HD", "high resolution" → invalid
  - "masterpiece", "best quality", "ultra detailed" → invalid
  - "award winning" → invalid

- Negation-based descriptions (non-extreme cases)
  - "no light" → invalid; use "dark" or "dim lighting" instead
  - "no people" → invalid; use "empty scene" or "uninhabited" instead
  - "no watermark" → invalid; use "clean image" or omit entirely
  - "without text" → invalid; use "plain background" or "text-free" instead

### C2: Prohibited Model Interactions

- Using negative_prompt parameter
  - Context: Any negative prompt input is discarded by z-image pipeline
  - Ban boundary: All attempts to use negative prompts are ineffective
  
- Using guidance_scale for quality control
  - Context: CFG is not used in z-image inference
  - Ban boundary: guidance_scale values other than 0.0 serve no purpose

### C3: Prohibited Prompt Structures

- Tag list format
  - "1girl, solo, long hair, red eyes, school uniform" → invalid structure
  - Context: z-image responds to natural language, not comma-separated tags
  
- Brief vague prompts
  - "a beautiful girl" → insufficient detail
  - "cute character" → insufficient detail
  - Context: Short prompts under 30-40 words produce generic outputs

- Token count exceeding 512 without parameter adjustment
  - Prompts > 512 tokens get truncated at default max_sequence_length
  - Context: 600-1000 word prompts require max_sequence_length=1024 setting

- Mixed style control modifiers
  - Pony Diffusion score tags combined with natural language descriptions → invalid
  - SDXL weight syntax like "(keyword:1.2)" → invalid
  - Context: z-image optimized for natural language, not tag-based modifiers

- Unverified reasoning mode attempts
  - Using Qwen3-4B-Thinking as direct text encoder in ComfyUI → invalid
  - Expecting reasoning node functionality in ComfyUI → invalid
  - Context: Official reasoning not yet implemented in community tools

### C4: Prohibited Output Behaviors (from PE template constraints)

- Deviation from original user intent
  - PE must not alter core subject, count, action, state, IP names, colors, text
  
- Outputting content beyond the final prompt
  - PE must not output explanations, commentary, or wrapper text
  - Only the processed prompt string is allowed in output

## Mechanisms & Logic [Conditional]

### Why Negative Prompts Are Invalid

- z-image is a few-step distilled model
- Distillation removes the classifier-free guidance pathway
- Without CFG, there is no mechanism to subtract negative influence
- Inference uses only the positive text conditioning

### Why CFG Scale Is Invalid

- Standard diffusion: CFG compares conditional vs unconditional predictions
- z-image: No unconditional prediction path exists
- guidance_scale parameter has no mathematical target to modify
- Setting guidance_scale > 0 provides no quality benefit

### Why Metaphorical Language Fails

- z-image processes text through Qwen3-4B tokenizer
- Abstract concepts lack concrete visual anchors in training data
- Metaphors introduce ambiguity where the model requires specificity
- Result: Model improvises unpredictably or ignores metaphorical elements

### Why Tag-Based Prompting Fails

- z-image training used natural language captions
- Tag-based datasets (Danbooru-style) were not the primary training source
- Model attention mechanism optimized for sentence structure, not token lists
- Tag dilution: Multiple short tags compete for attention vs focused description

### Quality Degradation Triggers

- Steps < 8: Artifact increase
- Prompt words < 30: Detail deficiency
- Mixed style modifiers: Model confusion
- Token truncation: Loss of latter prompt descriptions
