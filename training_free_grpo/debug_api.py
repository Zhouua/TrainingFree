"""诊断API调用问题的测试脚本"""
import argparse
import asyncio
import time
import os
from training_free_grpo.model_config import setup_model_env, get_supported_models
from training_free_grpo.llm import LLM

async def test_api_call(model_name: str = None):
    print("=" * 60)
    print("开始诊断API调用问题")
    print("=" * 60)
    
    # 设置模型环境
    if model_name:
        print(f"\n1. 设置{model_name}模型环境...")
        setup_model_env(model_name)
    else:
        print("\n1. 使用.env文件中的默认配置...")
        print(f"   UTU_LLM_MODEL: {os.getenv('UTU_LLM_MODEL', 'Not set')}")
        print(f"   UTU_LLM_BASE_URL: {os.getenv('UTU_LLM_BASE_URL', 'Not set')}")
    
    import os
    print(f"   UTU_LLM_MODEL: {os.getenv('UTU_LLM_MODEL')}")
    print(f"   UTU_LLM_BASE_URL: {os.getenv('UTU_LLM_BASE_URL')}")
    print(f"   UTU_LLM_API_KEY: {os.getenv('UTU_LLM_API_KEY')[:20]}..." if os.getenv('UTU_LLM_API_KEY') else "   UTU_LLM_API_KEY: None")
    
    # 创建LLM实例
    print("\n2. 创建LLM实例...")
    llm = LLM()
    
    # 测试简单调用
    print("\n3. 测试简单API调用...")
    test_prompt = "计算 2+2=?"
    print(f"   测试提示: {test_prompt}")
    
    start_time = time.time()
    try:
        # 同步调用
        print("   发送请求...")
        response = llm.chat(test_prompt, max_tokens=100, temperature=0.7)
        end_time = time.time()
        
        print(f"\n✅ API调用成功!")
        print(f"   响应时间: {end_time - start_time:.2f}秒")
        print(f"   响应内容: {response}")
        
    except Exception as e:
        end_time = time.time()
        print(f"\n❌ API调用失败!")
        print(f"   耗时: {end_time - start_time:.2f}秒")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {e}")
        import traceback
        print("\n完整错误堆栈:")
        print(traceback.format_exc())
        return False
    
    # 测试异步调用（模拟训练脚本的使用方式）
    print("\n4. 测试异步调用（模拟训练脚本）...")
    start_time = time.time()
    try:
        coro = asyncio.to_thread(llm.chat, test_prompt, temperature=0.7, max_tokens=100)
        response = await asyncio.wait_for(coro, timeout=60)
        end_time = time.time()
        
        print(f"\n✅ 异步调用成功!")
        print(f"   响应时间: {end_time - start_time:.2f}秒")
        print(f"   响应内容: {response}")
        
    except asyncio.TimeoutError:
        print(f"\n❌ 异步调用超时!")
        print(f"   超时时间: 60秒")
        return False
    except Exception as e:
        end_time = time.time()
        print(f"\n❌ 异步调用失败!")
        print(f"   耗时: {end_time - start_time:.2f}秒")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {e}")
        import traceback
        print("\n完整错误堆栈:")
        print(traceback.format_exc())
        return False
    
    # 测试并发调用
    print("\n5. 测试小规模并发调用（5个并发）...")
    start_time = time.time()
    
    async def single_call(idx):
        try:
            coro = asyncio.to_thread(llm.chat, f"计算 {idx}+1=?", temperature=0.7, max_tokens=50)
            response = await asyncio.wait_for(coro, timeout=60)
            return {"success": True, "idx": idx, "response": response}
        except Exception as e:
            return {"success": False, "idx": idx, "error": str(e)}
    
    tasks = [single_call(i) for i in range(5)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end_time = time.time()
    
    success_count = sum(1 for r in results if isinstance(r, dict) and r.get("success"))
    print(f"\n   并发调用完成: {success_count}/5 成功")
    print(f"   总耗时: {end_time - start_time:.2f}秒")
    
    for r in results:
        if isinstance(r, dict):
            if r.get("success"):
                print(f"   ✅ 任务{r['idx']}: {r['response'][:50]}...")
            else:
                print(f"   ❌ 任务{r['idx']}: {r['error']}")
        else:
            print(f"   ❌ 异常: {r}")
    
    if success_count < 5:
        print("\n⚠️ 并发调用存在失败，可能是速率限制问题")
        return False
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过! API配置正常")
    print("=" * 60)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="诊断API调用问题")
    parser.add_argument(
        "--model", 
        type=str, 
        default=None, 
        choices=get_supported_models(),
        help=f"模型选择 (可选: {', '.join(get_supported_models())})。如不指定，使用.env中的默认配置"
    )
    args = parser.parse_args()
    
    success = asyncio.run(test_api_call(args.model))
    if not success:
        print("\n建议:")
        print("1. 检查网络连接")
        print("2. 验证API Key是否有效")
        print("3. 检查对应模型的API服务状态")
        print("4. 尝试降低并发数: --rollout_concurrency 5")
        if args.model:
            print(f"5. 尝试其他模型: {', '.join([m for m in get_supported_models() if m != args.model])}")
