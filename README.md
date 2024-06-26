# indirect_prompt_injection_with_resume
Demonstration of Indirect-prompt-injection using a resume as an example.
This repository contains a web service that uses AI to determine whether an uploaded CV is good or not.

By creating a CV in some way and inducing the judgement result in white text in the CV, even a CV with no content can be judged as excellent.

<details>
<summary>Japanese</summary>
履歴書を例にした Indirect-prompt-injection のデモです。
このレポジトリでは、アップロードされた履歴書が優れているかどうかを AI によって判定する Web サービスが含まれています。

何かしらの方法で、履歴書を作成し、履歴書の中に白文字で判定結果を誘導することで、内容のない履歴書であっても優れたものであると判定させることができます。
</details>

## Requirements
- Python >= 3.10
- Poetry
- Anthropic API Key from [here](https://console.anthropic.com)

## Installation Python modules
```bash
$ git clone https://github.com/pacificbelt30/indirect_prompt_injection_with_resume
$ cd indirect_prompt_injection_with_resume
$ poetry install
```

## Run frontend server
```
$ cd front
$ poetry run python -m http.server 2000
```

## Run backend server
```
$ cd back
$ export ANTHROPIC_API_KEY=XX-XXXXXXXXXXXX 
$ poetry run uvicorn main:app --reload
```

## Reference
[https://kai-greshake.de/posts/inject-my-pdf/](https://kai-greshake.de/posts/inject-my-pdf/)
[https://embracethered.com/blog/posts/2023/ai-injections-direct-and-indirect-prompt-injection-basics/](https://embracethered.com/blog/posts/2023/ai-injections-direct-and-indirect-prompt-injection-basics/)
