# Training notes (after session-distill)

This skill only builds **SFT JSONL**. It does not train weights.

## Dataset format

Each line:

```json
{"messages":[{"role":"system","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

Compatible with:

- **Qwen** SFT (ChatML) via LLaMA-Factory / ms-swift / Firefly
- **Unsloth** (`FastLanguageModel.get_chat_template` + `train_on_responses_only`)
- **Axolotl** (`chat_template` / ShareGPT conversion)
- **Hugging Face TRL** `SFTTrainer` with a chat template tokenizer

Optional `meta` fields may need stripping for strict loaders:

```python
# strip meta if needed
import json
with open("in.jsonl") as f, open("clean.jsonl","w") as o:
    for line in f:
        obj = json.loads(line)
        o.write(json.dumps({"messages": obj["messages"]}, ensure_ascii=False) + "\n")
```

## Suggested base models

| Goal | Starting point |
|------|----------------|
| Strong general coding chat | `Qwen2.5-Coder-7B-Instruct` or `Qwen2.5-14B-Instruct` |
| Smaller / local GPU | `Qwen2.5-3B-Instruct` or `Qwen2.5-Coder-3B-Instruct` |
| Latest Qwen3 family | Matching `*-Instruct` checkpoint from Hugging Face |

Start from an **Instruct** checkpoint unless you know you need base + full SFT. Instruct + light LoRA on your pairs is usually enough to teach *your* project style without destroying general ability.

## Minimal LoRA path (Unsloth-style sketch)

1. Install Unsloth for your CUDA/torch stack.
2. Load e.g. `unsloth/Qwen2.5-Coder-7B-Instruct`.
3. Load `~/.grok/fine-tunes/*.jsonl` with a messages chat template.
4. Train LoRA (r=16–64), 1–3 epochs, low LR (~1e-4 to 2e-4 for LoRA).
5. Eval on held-out pairs: troubleshooting questions from a session you did **not** train on.

## Quality tips

- Prefer **50–500 high-quality pairs** over thousands of noisy ones.
- Balance archetypes: plan / implement / test / debug.
- Re-run `/session-distill` on more project sessions as you build; append to `corpus-sft.jsonl`.
- Always review a sample of lines before training.

## Safety

- Datasets may still contain business logic or private paths after redaction of keys — treat `fine-tunes/` as private.
- Do not upload corpus files to public model hosts without review.
