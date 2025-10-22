import argparse

from utu.config import ConfigLoader, EvalConfig


def parse_eval_config() -> EvalConfig:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_name", type=str, default="ww", help="Configuration name for evaluation.")
    parser.add_argument("--exp_id", type=str, default=None, help="Experiment ID.")
    parser.add_argument("--agent_model", type=str, default=None, help="Agent model.")
    parser.add_argument("--dataset", type=str, default=None, help="Dataset.")
    parser.add_argument("--dataset_type", type=str, default=None, help="Dataset type.")
    parser.add_argument("--concurrency", type=int, default=None, help="Test concurrency.")
    parser.add_argument("--judge_concurrency", type=int, default=None, help="Judge concurrency.")
    args = parser.parse_args()

    config = ConfigLoader.load_eval_config(args.config_name)
    if args.exp_id:
        config.exp_id = args.exp_id
    if args.agent_model:
        config.agent.model.model_provider.model = args.agent_model
    if args.dataset:
        config.data.dataset = args.dataset
    if args.dataset_type:
        config.data.type = args.dataset_type
    if args.concurrency:
        config.concurrency = args.concurrency
    if args.judge_concurrency:
        config.judge_concurrency = args.judge_concurrency
    return config
