# Training-Free GRPO

训练无关的组相对策略优化 (Group Relative Policy Optimization) 框架，支持多模型、多领域的 AI Agent 训练与评测。

## 📋 目录

- [功能特性](#功能特性)
- [目录结构](#目录结构)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [训练流程](#训练流程)
- [评测流程](#评测流程)
- [数据管理](#数据管理)

## ✨ 功能特性

### 多模型支持
- ✅ 支持 DeepSeek、Qwen、Gemini、OpenAI 等主流 LLM
- ✅ 通过 `--model` 参数快速切换模型
- ✅ 自动从 `.env` 文件读取模型配置和 API Key
- ✅ 训练和评测结果按模型隔离存储

### 多领域任务
- ✅ **Math**: 数学问题求解
- ✅ **Web**: 网页搜索任务

### 断点续传
- ✅ 训练过程支持中断后继续
- ✅ 自动跳过已完成的样本
- ✅ 支持修改 `grpo_n` 参数后继续训练

### 评测优化
- ✅ 所有模型共享 rollout 数据，节省计算成本
- ✅ 每个模型的统计结果独立保存
- ✅ 追加式统计记录，带时间戳和配置信息
- ✅ 完整保留评测历史，方便对比分析

## 📁 目录结构

```
training_free_grpo/
├── data/                           # 数据存储目录
│   ├── {domain}/train/            # 训练数据
│   │   └── {experiment}/          # 实验名称
│   │       ├── epoch_{X}/         # 共享的 epoch 数据
│   │       │   └── shuffled_data.jsonl
│   │       └── {model_name}/      # 模型特定数据
│   │           ├── step_{X}/
│   │           │   ├── rollout.jsonl
│   │           │   └── experiences.json
│   │           └── stats.json
│   └── {domain}/eval/             # 评测数据
│       └── {dataset}/             # 数据集名称
│           ├── rollouts.jsonl     # 共享 rollout (所有模型)
│           ├── {model_name}_stats.json  # 模型统计结果
│           └── ...
├── math/                          # 数学领域
│   ├── dataset.py                 # 数据集加载
│   ├── verify.py                  # 答案验证
│   ├── prompts.py                 # 提示词模板
│   └── experience.py              # 经验更新
├── web/                           # 网页领域
│   └── ...
├── model_config.py                # 模型配置管理
├── train.py                       # 训练脚本
├── main.py                        # 评测脚本
├── run.sh                         # 训练启动脚本
└── eval.sh                        # 评测启动脚本
```

## 🚀 快速开始

### 1. 环境配置

在 `.env` 文件中配置模型 API Key：

```bash
# DeepSeek
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_API_KEY=sk-xxxxx

# Qwen
QWEN_MODEL=qwen3-8b
QWEN_API_KEY=sk-xxxxx

# Gemini
GEMINI_MODEL=gemini-2.0-flash
GEMINI_API_KEY=xxxxx

# OpenAI
OPENAI_MODEL=gpt-4o
OPENAI_API_KEY=sk-xxxxx
```

### 2. 训练

使用 DeepSeek 模型训练：

```bash
python train.py \
    --mode agent \
    --model deepseek \
    --domain math \
    --experiment_name DAPO100 \
    --dataset DAPO-Math-17k \
    --dataset_truncate 100 \
    --epochs 3 \
    --batchsize 100 \
    --grpo_n 5 \
    --rollout_concurrency 10 \
    --rollout_temperature 0.7 \
    --task_timeout 1800
```

或使用快捷脚本：

```bash
bash run.sh
```

### 3. 评测

使用 DeepSeek 模型评测：

```bash
python main.py \
    --mode agent \
    --model deepseek \
    --domain math \
    --dataset AIME25 \
    --experience_file data/math/train/DAPO100/deepseek-chat/step_3/experiences.json \
    --rollout_concurrency 128 \
    --pass_k 32
```

或使用快捷脚本：

```bash
bash eval.sh
```

## ⚙️ 配置说明

### 模型选择参数

通过 `--model` 参数选择模型提供商：

| 参数值 | 说明 | 从 .env 读取 |
|--------|------|-------------|
| `deepseek` | DeepSeek 模型 | `DEEPSEEK_MODEL`, `DEEPSEEK_API_KEY` |
| `qwen` | 阿里云通义千问 | `QWEN_MODEL`, `QWEN_API_KEY` |
| `gemini` | Google Gemini | `GEMINI_MODEL`, `GEMINI_API_KEY` |
| `openai` | OpenAI GPT | `OPENAI_MODEL`, `OPENAI_API_KEY` |

### 训练参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--mode` | 推理模式 (agent/prompt) | `agent` |
| `--model` | 模型提供商 | 从 `.env` 读取 |
| `--domain` | 任务领域 (math/web) | 必填 |
| `--experiment_name` | 实验名称 | 必填 |
| `--dataset` | 数据集名称 | 必填 |
| `--dataset_truncate` | 截断数据集 | `None` |
| `--epochs` | 训练轮数 | `2` |
| `--batchsize` | 批次大小 | `64` |
| `--grpo_n` | GRPO 组大小 | `5` |
| `--rollout_concurrency` | 并发数 | `5` |
| `--rollout_temperature` | 温度参数 | `0.7` |
| `--rollout_max_tokens` | 最大 tokens | `16384` |
| `--task_timeout` | 任务超时 (秒) | `3600` |

### 评测参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--mode` | 推理模式 (agent/prompt) | `agent` |
| `--model` | 模型提供商 | 从 `.env` 读取 |
| `--domain` | 任务领域 (math/web) | 必填 |
| `--dataset` | 数据集名称 (如 AIME25) | 必填 |
| `--experience_file` | 经验文件路径 | `None` |
| `--rollout_concurrency` | 并发数 | `5` |
| `--pass_k` | Pass@K 指标 | `1` |
| `--rollout_max_tokens` | 最大 tokens | `16384` |
| `--task_timeout` | 任务超时 (秒) | `3600` |

## 🔄 训练流程

### 1. 数据流程

```mermaid
graph LR
    A[加载数据集] --> B[Epoch 洗牌]
    B --> C[批次划分]
    C --> D[添加经验]
    D --> E[GRPO 复制]
    E --> F[Rollout]
    F --> G[经验更新]
    G --> C
```

### 2. 目录结构

训练采用分层目录结构：

- **共享数据**: `data/{domain}/train/{experiment}/epoch_{X}/`
  - 所有模型共用同一个 epoch 的洗牌数据
  
- **模型数据**: `data/{domain}/train/{experiment}/{model_name}/step_{X}/`
  - 每个模型的 rollout 和经验独立存储

### 3. 断点续传

训练支持中断后继续：

1. 自动检测已完成的 step
2. 加载已有的 rollout 数据
3. 跳过已完成的样本
4. 继续未完成的训练

## 📊 评测流程

### 1. 共享 Rollout 设计

```
data/math/eval/AIME25/
├── rollouts.jsonl              # 所有模型共享
├── deepseek-chat_stats.json    # DeepSeek 统计
├── qwen3-8b_stats.json         # Qwen 统计
└── gemini-2.0-flash_stats.json # Gemini 统计
```

**优势**：
- ✅ 节省计算成本（避免重复生成 rollout）
- ✅ 公平对比（所有模型使用相同测试样本）
- ✅ 结果隔离（每个模型统计独立）

### 2. 追加式统计记录

统计文件格式 (JSON 数组)：

```json
[
  {
    "timestamp": "2025-10-22 20:07:15",
    "experience_file": "none",
    "pass_k": 1,
    "avg_reward": 0.45,
    "Pass@1": 0.45,
    "avg_tool_call": 7.2
  },
  {
    "timestamp": "2025-10-22 23:29:18",
    "experience_file": "data/math/train/DAPO100/deepseek-chat/step_3/experiences.json",
    "pass_k": 32,
    "avg_reward": 0.583,
    "Pass@32": 1.0,
    "avg_tool_call": 8.9
  }
]
```

**特性**：
- ✅ 保留完整评测历史
- ✅ 时间戳记录
- ✅ 配置信息追溯
- ✅ 性能趋势分析

### 3. 多模型对比

使用不同模型评测同一数据集：

```bash
# 评测 DeepSeek
python main.py --model deepseek --dataset AIME25 \
  --experience_file data/math/train/DAPO100/deepseek-chat/step_3/experiences.json

# 评测 Qwen (使用相同的 rollout)
python main.py --model qwen --dataset AIME25 \
  --experience_file data/math/train/DAPO100/qwen3-8b/step_3/experiences.json

# 评测 Gemini
python main.py --model gemini --dataset AIME25 \
  --experience_file data/math/train/DAPO100/gemini-2.0-flash/step_3/experiences.json
```

## 📈 数据管理

### 训练数据结构

```
data/math/train/DAPO100/
├── epoch_0/
│   └── shuffled_data.jsonl       # 所有模型共享
├── epoch_1/
│   └── shuffled_data.jsonl
├── deepseek-chat/                # DeepSeek 模型数据
│   ├── step_0/
│   │   ├── rollout.jsonl
│   │   └── critiques/
│   ├── step_1/
│   │   ├── rollout.jsonl
│   │   └── experiences.json
│   └── stats.json
└── qwen3-8b/                     # Qwen 模型数据
    ├── step_0/
    └── ...
```

### 评测数据结构

```
data/math/eval/
├── AIME25/
│   ├── rollouts.jsonl            # 共享 rollout
│   ├── deepseek-chat_stats.json  # DeepSeek 统计
│   └── qwen3-8b_stats.json       # Qwen 统计
└── MATH500/
    ├── rollouts.jsonl
    └── ...
```

## 🔧 高级功能

### 1. 修改 GRPO 参数后继续训练

系统会自动检测并调整 rollout 数据：

```bash
# 原始训练 (grpo_n=5)
python train.py --grpo_n 5 --experiment_name exp1

# 修改参数后继续 (grpo_n=10)
python train.py --grpo_n 10 --experiment_name exp1
# ✅ 自动扩展 rollout 数据
```

### 2. 评测不同训练阶段

对比不同 step 的性能：

```bash
# Step 1
python main.py --dataset AIME25 \
  --experience_file data/math/train/DAPO100/deepseek-chat/step_1/experiences.json

# Step 2
python main.py --dataset AIME25 \
  --experience_file data/math/train/DAPO100/deepseek-chat/step_2/experiences.json

# Step 3
python main.py --dataset AIME25 \
  --experience_file data/math/train/DAPO100/deepseek-chat/step_3/experiences.json
```

所有结果会追加到同一个统计文件，方便对比。

### 3. 无经验基线测试

```bash
# 基线 (无经验)
python main.py --dataset AIME25

# 有经验
python main.py --dataset AIME25 \
  --experience_file data/math/train/DAPO100/deepseek-chat/step_3/experiences.json
```

## 📝 更新日志

### v2.0.0 (2025-10-22)

**新增功能**:
- ✅ 多模型支持 (DeepSeek/Qwen/Gemini/OpenAI)
- ✅ 模型配置管理模块 (`model_config.py`)
- ✅ 训练和评测支持 `--model` 参数
- ✅ 共享 rollout 评测机制
- ✅ 追加式统计记录 (带时间戳)
- ✅ 断点续传支持 `grpo_n` 参数变化

**优化改进**:
- 🔧 评测数据路径从 `experiment_name` 改为 `dataset`
- 🔧 统计文件格式从单个字典改为列表 (支持历史记录)
- 🔧 更友好的错误提示信息

**Bug 修复**:
- 🐛 修复断点续传时 rollout 长度不匹配的问题
- 🐛 修复重复评测时统计结果被覆盖的问题

## 📄 许可证

遵循项目主许可证。
