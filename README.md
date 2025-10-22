# Training-Free GRPO

本项目基于 [Youtu-Agent Training-Free GRPO](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO) 进行改进和优化。

## 📖 原始项目

- **原始仓库**: [TencentCloudADP/youtu-agent (training_free_GRPO 分支)](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO)
- **论文**: [Training-Free Group Relative Policy Optimization (arXiv:2510.08191)](https://arxiv.org/abs/2510.08191)

关于 Training-Free GRPO 的详细原理、方法和基准测试结果，请参考原始仓库和论文。

## 🎯 遇到的问题与改进

### 问题 1: 缺少多模型支持

**问题描述**：
- 原始代码只支持使用 `.env` 文件配置的单一模型
- 无法方便地切换不同模型进行对比实验
- 多模型实验需要频繁修改环境变量

**改进方案**：
- ✅ 添加 `--model` 命令行参数，支持快速切换模型
- ✅ 实现 `model_config.py` 模块，统一管理多模型配置
- ✅ 支持模型列表：`deepseek`, `qwen`, `gemini`, `openai` 等
- ✅ 自动根据模型名称创建独立的结果目录

### 问题 2: API 速率限制导致训练中断

**问题描述**：
- 使用高并发（如 `rollout_concurrency=128`）时频繁触发 429 错误
- 不同 LLM 服务商有不同的速率限制（RPM/TPM）
- 训练中断后难以恢复，浪费 API 调用额度

**改进方案**：
- ✅ 降低默认并发数到 5-10，避免触发速率限制
- ✅ 添加智能重试机制，自动处理临时性 API 错误
- ✅ 完善断点续传机制，支持训练中断后无缝恢复
- ✅ 在文档中添加并发参数调优建议

### 问题 3: 模型间数据不一致

**问题描述**：
- 原始实现中每个模型都有独立的 epoch 数据目录
- 不同模型的训练数据顺序可能不同
- 难以进行公平的模型对比实验

**改进方案**：
- ✅ 重构目录结构，实现 **共享 epoch 数据 + 模型独立 step 数据**
- ✅ 所有模型使用相同的 `shuffled_data.jsonl`，确保数据一致性
- ✅ 每个模型维护独立的 rollouts 和 experiences
- ✅ 新的目录结构：
  ```
  data/{domain}/train/{experiment_name}/
  ├── epoch_0/
  │   └── shuffled_data.jsonl  # 所有模型共享
  ├── epoch_1/
  │   └── shuffled_data.jsonl
  ├── {model_name_1}/
  │   ├── stats.json
  │   ├── step_0/
  │   │   ├── rollout.jsonl
  │   │   └── ...
  │   └── step_1/
  │       └── experiences.json
  └── {model_name_2}/
      └── ...
  ```

### 问题 4: Token 限制导致生成不完整

**问题描述**：
- 不同模型有不同的 token 限制
- 固定的 `max_tokens` 可能不适用于所有模型
- 复杂问题可能因 token 限制而截断

**改进方案**：
- ✅ 添加 `--rollout_max_tokens` 参数，可根据模型调整
- ✅ 默认值设为 16384，适配大多数主流模型
- ✅ 支持针对不同任务动态调整 token 限制

## 🚀 快速开始

### 1. 环境设置

First, set up your Python environment and install the required dependencies in the project root.

```bash
# 克隆本仓库
git clone <your-repo-url>
cd youtu-agent

# 同步依赖
uv sync

# 激活虚拟环境
source ./.venv/bin/activate

# 升级 datasets 包
uv pip install --upgrade datasets
```

配置环境变量：

```bash
cp .env.example .env
```

编辑 `.env` 文件，添加您的 API Keys。**改进：现在支持配置多个模型**：

```ini
# DeepSeek API
UTU_LLM_TYPE=chat.completions
UTU_LLM_MODEL=deepseek-chat
UTU_LLM_BASE_URL=https://api.deepseek.com/v1
UTU_LLM_API_KEY=sk-xxx  # https://platform.deepseek.com/api_keys

# Qwen API (阿里云 DashScope)
QWEN_MODEL=qwen3-8b
QWEN_API_KEY=sk-xxx  # https://dashscope.console.aliyun.com/apiKey

# Gemini API
GEMINI_MODEL=gemini-2.0-flash-exp
GEMINI_API_KEY=xxx  # https://aistudio.google.com/app/apikey

# Web 搜索任务需要配置
SERPER_API_KEY=xxx
JINA_API_KEY=xxx
```

### 2. 运行训练

进入 `training_free_grpo` 目录运行训练脚本。

**主要参数**：
- `--mode`: 执行模式 (`prompt` 或 `agent`)
- `--model`: **[新增]** 模型选择 (`deepseek`, `qwen`, `gemini` 等)
- `--domain`: 任务领域 (`math` 或 `web`)
- `--experiment_name`: 实验名称
- `--dataset`: 数据集名称
- `--dataset_truncate`: 截断数据集到前 N 个样本
- `--epochs`: 训练轮数
- `--batchsize`: 批次大小
- `--grpo_n`: GRPO 组中的 rollout 数量
- `--rollout_concurrency`: **[改进]** 并发数（建议 5-10，避免速率限制）
- `--rollout_temperature`: LLM 温度参数
- `--rollout_max_tokens`: **[新增]** 最大 token 数
- `--task_timeout`: 任务超时时间（秒）

**示例 1：使用 Qwen 模型训练数学推理任务**

```bash
cd training_free_grpo

python train.py \
    --mode agent \
    --model qwen \
    --domain math \
    --experiment_name DAPO100 \
    --dataset DAPO-Math-17k \
    --dataset_truncate 100 \
    --epochs 5 \
    --batchsize 100 \
    --grpo_n 5 \
    --rollout_concurrency 5 \
    --rollout_temperature 0.7 \
    --rollout_max_tokens 16384 \
    --task_timeout 3600
```

**示例 2：使用 DeepSeek 模型训练**

```bash
python train.py \
    --mode agent \
    --model deepseek \
    --domain math \
    --experiment_name DAPO100 \
    --dataset DAPO-Math-17k \
    --dataset_truncate 100 \
    --epochs 5 \
    --batchsize 100 \
    --grpo_n 5 \
    --rollout_concurrency 5 \
    --rollout_temperature 0.7 \
    --task_timeout 3600
```

**示例 3：Web 搜索任务训练**

```bash
python train.py \
    --mode agent \
    --model qwen \
    --domain web \
    --experiment_name AFM_web_RL_100 \
    --dataset AFM_web_RL_100 \
    --epochs 3 \
    --batchsize 4 \
    --grpo_n 5 \
    --rollout_concurrency 5 \
    --rollout_temperature 0.7 \
    --task_timeout 1800
```

### 3. 运行评估

使用 `main.py` 脚本进行评估。

**主要参数**：
- `--mode`: 执行模式
- `--model`: **[新增]** 模型选择
- `--domain`: 任务领域
- `--experiment_name`: 实验名称
- `--experience_file`: 训练过程中保存的经验文件路径
- `--dataset`: 评估数据集
- `--rollout_concurrency`: 并发数
- `--rollout_max_tokens`: **[新增]** 最大 token 数
- `--pass_k`: Pass@k 指标
- `--task_timeout`: 超时时间

**示例 1：评估数学推理任务**

```bash
python main.py \
    --mode agent \
    --model qwen \
    --domain math \
    --experiment_name AIME24_test \
    --dataset AIME24 \
    --experience_file data/math/train/DAPO100/qwen3-8b/step_3/experiences.json \
    --rollout_concurrency 5 \
    --rollout_max_tokens 16384 \
    --pass_k 32
```

**注意**：经验文件路径现在包含模型名称，如 `data/math/train/DAPO100/{model_name}/step_X/experiences.json`

**示例 2：评估 Web 搜索任务**

```bash
python main.py \
    --mode agent \
    --model qwen \
    --domain web \
    --experiment_name WebWalkerQA_test \
    --dataset WebWalkerQA \
    --experience_file data/web/train/AFM_web_RL_100/qwen3-8b/step_3/experiences.json \
    --rollout_concurrency 5 \
    --pass_k 3
```

## 💡 使用建议

1. **并发控制**：建议从低并发（5-10）开始测试，避免触发 API 速率限制
2. **模型切换**：使用 `--model` 参数快速切换模型，无需修改 `.env` 文件
3. **断点续传**：训练支持自动断点续传，中断后可直接重新运行相同命令
4. **数据一致性**：共享的 epoch 数据确保不同模型使用相同的训练序列
5. **Token 优化**：根据模型能力调整 `--rollout_max_tokens` 参数

## 📂 目录结构（改进后）

```
data/{domain}/train/{experiment_name}/
├── epoch_0/
│   └── shuffled_data.jsonl       # 所有模型共享的 epoch 数据
├── epoch_1/
│   └── shuffled_data.jsonl
├── {model_name_1}/                # 模型 1 的独立数据
│   ├── stats.json
│   ├── step_0/
│   │   ├── rollout.jsonl
│   │   ├── single_rollout_summary.json
│   │   ├── single_query_critique.json
│   │   └── batch_update.json
│   └── step_1/
│       └── experiences.json
└── {model_name_2}/                # 模型 2 的独立数据
    └── ...
```

## 🔗 参考资源

- **原始仓库**: [TencentCloudADP/youtu-agent](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO)
- **论文**: [Training-Free Group Relative Policy Optimization (arXiv:2510.08191)](https://arxiv.org/abs/2510.08191)


```

