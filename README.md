# Training-Free GRPO

本项目基于 [Youtu-Agent Training-Free GRPO](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO) 进行改进和优化。

## 📖 原始项目

- **原始仓库**: [TencentCloudADP/youtu-agent (training_free_GRPO 分支)](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO)
- **论文**: [Training-Free Group Relative Policy Optimization (arXiv:2510.08191)](https://arxiv.org/abs/2510.08191)

关于 Training-Free GRPO 的详细原理、方法和基准测试结果，请参考原始仓库和论文。

## ！！！评测结果
<img width="3224" height="442" alt="image" src="https://github.com/user-attachments/assets/24d45d14-682f-4f3c-bc7c-88c12c5b28fb" />
根据issues反馈，说明是按照avg_reward获得结果，但是根据个人评测，论文结果难以信服


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

### 问题 5: 评测数据管理混乱

**问题描述**：
- 原始代码中每个模型的评测结果存储在独立文件中
- 重复评测会覆盖之前的结果，丢失历史数据
- 难以对比不同模型在相同数据集上的表现
- 无法追溯评测的配置和时间信息

**改进方案**：
- ✅ **共享 rollout 机制**：所有模型使用相同的 `rollouts.jsonl`，确保公平对比
- ✅ **追加式统计记录**：每次评测追加到统计文件而非覆盖，保留完整历史
- ✅ **时间戳和配置追踪**：记录评测时间、使用的经验文件、Pass@K 参数等
- ✅ **标准化路径结构**：`data/{domain}/eval/{dataset}/rollouts.jsonl` 和 `{model_name}_stats.json`
- ✅ **性能趋势分析**：可通过历史记录观察模型在不同训练阶段的性能变化

**新的评测目录结构**：
```
data/{domain}/eval/{dataset}/
├── rollouts.jsonl              # 所有模型共享的 rollout 数据
├── deepseek-chat_stats.json    # DeepSeek 的统计历史（数组格式）
├── qwen3-8b_stats.json         # Qwen 的统计历史
└── gemini-2.0-flash_stats.json # Gemini 的统计历史
```

**统计文件格式示例**：
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

### 问题 6: 断点续传数据不兼容

**问题描述**：
- 修改 `grpo_n` 参数后无法继续训练
- rollout 文件长度不匹配导致 `AssertionError`
- 必须删除已有数据重新开始，浪费计算资源

**改进方案**：
- ✅ **智能数据扩展**：当新数据更多时自动扩展 rollout 列表
- ✅ **安全截断机制**：当新数据更少时自动截断
- ✅ **部分验证**：仅对重叠部分进行问题一致性校验
- ✅ **友好错误提示**：明确指出数据不匹配的原因和解决方案

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

### 2. 测试 API 连接

**在运行训练之前，强烈建议先测试 API 是否正常工作**，避免训练过程中因 API 问题而卡住。

我们提供了诊断脚本 `debug_api.py` 来测试 API 连接和并发性能：

```bash
cd training_free_grpo

# 测试 Qwen 模型（推荐）
python debug_api.py --model qwen

# 测试 DeepSeek 模型
python debug_api.py --model deepseek

# 测试 Gemini 模型
python debug_api.py --model gemini

# 测试 OpenAI 模型
python debug_api.py --model openai

# 使用 .env 文件中的默认配置
python debug_api.py

# 查看帮助信息
python debug_api.py --help
```

**测试内容**：
1. ✅ **简单 API 调用测试** - 验证 API Key 和网络连接
2. ✅ **异步调用测试** - 模拟训练脚本的调用方式
3. ✅ **并发调用测试** - 测试 5 个并发请求，检查速率限制

**成功输出示例**：
```
============================================================
开始诊断API调用问题
============================================================

1. 设置qwen模型环境...
✓ Model configured: qwen
  - Model: qwen3-8b
  - Base URL: https://dashscope.aliyuncs.com/compatible-mode/v1
  - API Key: ********84dd

2. 创建LLM实例...

3. 测试简单API调用...
   测试提示: 计算 2+2=?
   发送请求...
[LLM] API call successful, received 9 characters

✅ API调用成功!
   响应时间: 0.60秒
   响应内容: 2 + 2 = 4

4. 测试异步调用（模拟训练脚本）...
✅ 异步调用成功!
   响应时间: 0.36秒

5. 测试小规模并发调用（5个并发）...
   并发调用完成: 5/5 成功
   总耗时: 1.2秒

============================================================
✅ 所有测试通过! API配置正常
============================================================
```

**常见问题排查**：
- ❌ **连接超时**: 检查网络是否能访问对应的 API 地址
- ❌ **认证失败**: 验证 API Key 是否正确配置
- ❌ **速率限制**: 考虑降低训练时的 `--rollout_concurrency` 参数
- ❌ **模型不存在**: 检查 `.env` 中配置的模型名称是否正确

### 3. 运行训练

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
    --domain web \
    --experiment_name AFM_web_RL_100 \
    --dataset AFM_web_RL_100 \
    --epochs 3 \
    --batchsize 4 \
    --grpo_n 5 \
    --rollout_concurrency 128 \
    --rollout_temperature 0.7 \
    --task_timeout 1800
    --model qwen
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

### 4. 运行评估

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

**示例 1：评估数学推理任务（使用训练的经验）**

```bash
cd training_free_grpo

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

**示例 2：基线评估（无经验）**

```bash
python main.py \
    --mode agent \
    --model qwen \
    --domain math \
    --dataset AIME25 \
    --rollout_concurrency 5 \
    --pass_k 32
```

**示例 3：对比不同训练阶段**

```bash
# 评测 step 1
python main.py --model deepseek --dataset AIME25 \
  --experience_file data/math/train/DAPO100/deepseek-chat/step_1/experiences.json \
  --pass_k 32

# 评测 step 2
python main.py --model deepseek --dataset AIME25 \
  --experience_file data/math/train/DAPO100/deepseek-chat/step_2/experiences.json \
  --pass_k 32

# 评测 step 3
python main.py --model deepseek --dataset AIME25 \
  --experience_file data/math/train/DAPO100/deepseek-chat/step_3/experiences.json \
  --pass_k 32
```

所有评测结果会追加到 `data/math/eval/AIME25/deepseek-chat_stats.json`，方便查看性能提升趋势。

**示例 4：多模型对比评测**

```bash
# 评测 DeepSeek
python main.py --model deepseek --dataset AIME25 \
  --experience_file data/math/train/DAPO100/deepseek-chat/step_3/experiences.json

# 评测 Qwen（使用相同的 rollout 数据）
python main.py --model qwen --dataset AIME25 \
  --experience_file data/math/train/DAPO100/qwen3-8b/step_3/experiences.json

# 评测 Gemini
python main.py --model gemini --dataset AIME25 \
  --experience_file data/math/train/DAPO100/gemini-2.0-flash/step_3/experiences.json
```

所有模型共享 `data/math/eval/AIME25/rollouts.jsonl`，确保公平对比。

**示例 5：评估 Web 搜索任务****

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

### 训练建议

1. **并发控制**：建议从低并发（5-10）开始测试，避免触发 API 速率限制
2. **模型切换**：使用 `--model` 参数快速切换模型，无需修改 `.env` 文件
3. **断点续传**：训练支持自动断点续传，中断后可直接重新运行相同命令
4. **数据一致性**：共享的 epoch 数据确保不同模型使用相同的训练序列
5. **Token 优化**：根据模型能力调整 `--rollout_max_tokens` 参数
6. **GRPO 参数调整**：支持修改 `grpo_n` 后继续训练，系统会自动调整数据结构

### 评测建议

1. **共享 Rollout**：多个模型评测同一数据集时会自动共享 rollout，节省成本
2. **历史追踪**：评测结果会追加保存，不会覆盖历史记录
3. **基线对比**：先运行无经验的基线评测，再运行有经验的评测，对比提升效果
4. **阶段对比**：评测不同训练阶段（step_1, step_2, step_3）观察性能变化
5. **统计查看**：查看 `{model_name}_stats.json` 了解完整评测历史

## 📂 目录结构（改进后）

### 训练数据结构

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

### 评测数据结构

```
data/{domain}/eval/{dataset}/
├── rollouts.jsonl              # 所有模型共享的 rollout 数据
├── deepseek-chat_stats.json    # DeepSeek 的评测历史（数组格式）
├── qwen3-8b_stats.json         # Qwen 的评测历史
└── gemini-2.0-flash_stats.json # Gemini 的评测历史
```

**统计文件示例** (`{model_name}_stats.json`)：
```json
[
  {
    "timestamp": "2025-10-22 20:07:15",
    "experience_file": "none",
    "pass_k": 1,
    "avg_reward": 0.45,
    "Pass@1": 0.45
  },
  {
    "timestamp": "2025-10-22 23:29:18",
    "experience_file": "data/math/train/DAPO100/deepseek-chat/step_3/experiences.json",
    "pass_k": 32,
    "avg_reward": 0.583,
    "Pass@32": 1.0
  }
]
```

## 🔗 参考资源

- **原始仓库**: [TencentCloudADP/youtu-agent](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO)
- **论文**: [Training-Free Group Relative Policy Optimization (arXiv:2510.08191)](https://arxiv.org/abs/2510.08191)
- **详细文档**: [training_free_grpo/README.md](training_free_grpo/README.md)

## 📋 更新日志

### v2.0.0 (2025-10-22)

**新增功能**:
- ✅ 多模型支持 (`--model` 参数)
- ✅ 模型配置管理模块 (`model_config.py`)
- ✅ 共享 rollout 评测机制
- ✅ 追加式统计记录（带时间戳）
- ✅ 断点续传支持 `grpo_n` 参数动态调整
- ✅ 详细的 `training_free_grpo/README.md` 文档

**优化改进**:
- 🔧 评测路径从 `experiment_name` 改为 `dataset`
- 🔧 统计文件从单次结果改为历史记录数组
- 🔧 更友好的错误提示和参数说明

**Bug 修复**:
- 🐛 修复断点续传时 rollout 数据长度不匹配的问题
- 🐛 修复多次评测时统计结果被覆盖的问题



