python main.py \
    --mode agent \
    --domain math \
    --dataset AIME24 \
    --rollout_concurrency 128 \
    --pass_k 3 \
    --model deepseek
    # --experience_file data/math/train/DAPO100/deepseek-chat/step_3/experiences.json



# Web
# python main.py \
#     --mode agent \
#     --domain web \
#     --dataset WebWalkerQA \
#     --experience_file data/web/train/AFM_web_RL_100/step_75/experiences.json \
#     --rollout_concurrency 128 \
#     --pass_k 3