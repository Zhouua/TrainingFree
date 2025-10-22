import time
import openai
from utu.utils import EnvUtils

class LLM:
    def __init__(self):
        EnvUtils.assert_env(["UTU_LLM_TYPE", "UTU_LLM_MODEL", "UTU_LLM_BASE_URL", "UTU_LLM_API_KEY"])
        self.model_name = EnvUtils.get_env("UTU_LLM_MODEL")
        self.client = openai.OpenAI(
            api_key=EnvUtils.get_env("UTU_LLM_API_KEY"),
            base_url=EnvUtils.get_env("UTU_LLM_BASE_URL"),
        )

    # def chat(self, messages_or_prompt, max_tokens=16384, temperature=0, max_retries=3, return_reasoning=False):
    def chat(self, messages_or_prompt, max_tokens=8192, temperature=0, max_retries=3, return_reasoning=False):
        for retry_idx in range(max_retries):
            try:
                print(f"[LLM] Attempt {retry_idx + 1}/{max_retries}: Calling {self.model_name}...")
                if isinstance(messages_or_prompt, str):
                    messages = [{"role": "user", "content": messages_or_prompt}]
                elif isinstance(messages_or_prompt, list):
                    messages = messages_or_prompt
                else:
                    raise ValueError("messages_or_prompt must be a string or a list of messages.")

                # Build kwargs for API call
                kwargs = {
                    "model": self.model_name,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }
                
                # For Qwen models via DashScope, disable thinking for non-streaming calls
                # This is required by the API
                base_url = EnvUtils.get_env("UTU_LLM_BASE_URL") or ""
                if "dashscope" in base_url:
                    kwargs["extra_body"] = {"enable_thinking": False}
                
                print(f"[LLM] Sending request to API...")
                response = self.client.chat.completions.create(**kwargs)
                response_text = response.choices[0].message.content.strip()
                print(f"[LLM] API call successful, received {len(response_text)} characters")

                if return_reasoning:
                    # Check if reasoning_content exists (only for o1 models)
                    reasoning = getattr(response.choices[0].message, 'reasoning_content', None)
                    return response_text, reasoning
                return response_text

            except Exception as e:
                error = f"[LLM] ERROR (attempt {retry_idx + 1}/{max_retries}): {type(e).__name__}: {e}"
                print(error)
                import traceback
                print(traceback.format_exc())
                if retry_idx < max_retries - 1:
                    print(f"[LLM] Retrying in 10 seconds...")
            time.sleep(10)
        print(f"[LLM] FAILED after {max_retries} retries")
        return None