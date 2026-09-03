import os
import json
import random
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor


def chat(prompt, model, n=1, temperature=0.7, max_tokens=8, system=None):
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key or os.environ.get("AXON_STUB"):
        return _stub(prompt, n)
    return [_one(prompt, model, key, temperature, max_tokens, system) for _ in range(n)]


def chat_many(prompts, model, temperature=0.7, max_tokens=8, system=None, workers=8):
    """One call per prompt, issued concurrently, results in prompt order.

    The prompts inside a single step are independent of each other (k branch
    variants, or k probe forms), so firing them together changes nothing about
    the experiment and turns a k-deep serial chain into one round trip."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key or os.environ.get("AXON_STUB"):
        return [_stub(p, 1)[0] for p in prompts]
    if len(prompts) == 1:
        return [_one(prompts[0], model, key, temperature, max_tokens, system)]
    with ThreadPoolExecutor(max_workers=min(workers, len(prompts))) as pool:
        return list(pool.map(
            lambda p: _one(p, model, key, temperature, max_tokens, system), prompts))


def _one(prompt, model, key, temperature, max_tokens, system):
    messages = [{"role": "user", "content": prompt}]
    if system:
        messages.insert(0, {"role": "system", "content": system})
    body = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        },
    )
    for i in range(5):
        try:
            resp = json.loads(urllib.request.urlopen(req, timeout=60).read())
            return resp["choices"][0]["message"]["content"]
        except urllib.error.URLError:
            if i == 4:
                raise
            time.sleep(2 ** i)


def _stub(prompt, n):
    r = random.Random(prompt)
    return [r.choice(["A", "B", "C"]) for _ in range(n)]
