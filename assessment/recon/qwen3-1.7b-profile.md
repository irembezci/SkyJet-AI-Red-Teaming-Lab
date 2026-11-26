# Model Recon Profile: Qwen3 1.7B

## Target Identification

| Attribute | Value |
|---|---|
| Model Family | Qwen3 |
| Model | Qwen3-1.7B |
| Runtime | Ollama |
| Local Model Tag | `qwen3:1.7b` |
| Parameter Count | 1.7B |
| Quantization | Q4_K_M |
| Model Type | Dense causal language model |

## Model Capabilities

- Instruction following
- Reasoning
- Coding
- Multilingual capabilities
- Thinking and non-thinking modes
- Tool-oriented capabilities

## Context Window

- Model-card context length: 32,768 tokens
- Runtime context configuration: Not yet verified

## Potentially Relevant Security Characteristics

| Characteristic | Testing Consideration |
|---|---|
| Small model size | Evaluate instruction-following and adversarial robustness |
| Multilingual capability | Compare responses across languages |
| Reasoning capability | Evaluate responses to conflicting and adversarial instructions |
| Context capacity | Investigate context manipulation and long-context behavior |
| Quantization | Evaluate the deployed model configuration rather than assuming equivalence to the original model |

## Recon Status

- [x] Model identified
- [x] Model family identified
- [x] Runtime identified
- [x] Quantization identified
- [x] Preliminary capabilities documented
- [x] Runtime configuration verified
- [ ] Relevant security research reviewed

## Runtime Configuration

| Attribute | Observed Value |
|---|---|
| Runtime | Ollama |
| Architecture | Qwen3 |
| Parameters | 2.0B |
| Context Length | 40,960 tokens |
| Embedding Length | 2,048 |
| Quantization | Q4_K_M |
| Template | go_template |
| Tool Capability | Supported |
| Thinking Capability | Supported |
| Thinking Levels | false, true |
| Default Thinking Mode | Enabled |
| Temperature | 0.6 |
| Top-k | 20 |
| Top-p | 0.95 |
| Repeat Penalty | 1 |

### Security-Relevant Observations

- Tool capability is supported at the model level; application-level tool access remains to be verified.
- Thinking capability is enabled by default in the reported configuration.
- The context window may be relevant to long-context and context-manipulation testing.
- Testing will target the deployed quantized model configuration.
- Temperature and sampling parameters will be considered when evaluating test reproducibility.

### Verification Source

Runtime configuration obtained using:

`ollama show qwen3:1.7b`


## Sources

- https://huggingface.co/Qwen/Qwen3-1.7B
- https://ollama.com/library/qwen3:1.7b
- https://arxiv.org/abs/2505.09388

*This profile contains preliminary model information. Runtime-specific characteristics and security implications remain subject to further investigation.*


