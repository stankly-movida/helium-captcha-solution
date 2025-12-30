# 🤖 Helium + CapSolver: Python Web 自动化框架

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![CapSolver](https://img.shields.io/badge/CAPTCHA%20Solver-CapSolver-green)](https://www.capsolver.com/?utm_source=github&utm_medium=repo&utm_campaign=helium-capsolver)

**English** | [简体中文](README_CN.md)

## 🌟 项目概览

本项目提供了一个强大且易用的框架，用于集成 **Helium**（一个简化的 Selenium 封装库）与 **CapSolver**（一个由 AI 驱动的 CAPTCHA 解决服务）。

我们的目标是实现无缝、可靠的 Python Web 自动化，让您的脚本能够自动处理 **Cloudflare Turnstile** 和 **reCAPTCHA** 等现代验证码挑战，不再受阻。

### 核心特性

*   **简化自动化**：利用 Helium 人类可读的 API，例如 `click("提交")`，`write("文本", into="输入框")`。
*   **AI 驱动的验证码解决**：集成 CapSolver API，自动解决复杂的验证码挑战。
*   **可靠示例**：提供可直接运行的 reCAPTCHA v2、reCAPTCHA v3 和 Cloudflare Turnstile 示例代码。
*   **反检测最佳实践**：包含配置，让您的自动化浏览器更像人类用户。

## 🚀 快速开始

### 前置条件

*   Python 3.8+
*   一个 CapSolver API 密钥（[点击此处获取](https://dashboard.capsolver.com/dashboard/overview/?utm_source=github&utm_medium=repo&utm_campaign=helium-capsolver)）

### 安装步骤

1.  **克隆仓库：**
    ```bash
    git clone https://github.com/your-username/helium-capsolver-solver.git
    cd helium-capsolver-solver
    ```

2.  **安装依赖：**
    ```bash
    pip install -r requirements.txt
    ```

3.  **设置 API 密钥：**
    出于安全考虑，强烈建议将您的 CapSolver API 密钥设置为环境变量。

    ```bash
    # Linux/macOS
    export CAPSOLVER_API_KEY="YOUR_API_KEY"

    # Windows (Command Prompt)
    set CAPSOLVER_API_KEY="YOUR_API_KEY"
    ```
    您也可以直接修改示例文件中的 `CAPSOLVER_API_KEY` 变量。

## 💡 使用示例

所有核心示例代码位于 `src/` 目录下。

### 1. 核心验证码解决逻辑

`src/core_solver.py` 文件包含了与 CapSolver API 交互的可复用函数：`create_task`、`get_task_result` 和 `solve_captcha`。

```python
# src/core_solver.py (代码片段)
import time
import requests

CAPSOLVER_API = "https://api.capsolver.com"
CAPSOLVER_API_KEY = os.environ.get("CAPSOLVER_API_KEY", "YOUR_API_KEY") # 从环境变量读取

def solve_captcha(task_payload: dict) -> dict:
    """完成 CAPTCHA 解决工作流。"""
    # ... 实现细节 ...
    pass
```

### 2. 解决 reCAPTCHA v2

此示例演示了如何解决 reCAPTCHA v2 挑战，包括自动检测 Site Key 和使用底层 Selenium 驱动注入 Token。

**运行示例：**
```bash
python src/recaptcha_v2_solver.py
```

### 3. 解决 Cloudflare Turnstile

此脚本展示了如何解决 Cloudflare Turnstile 挑战，并将返回的 Token 注入到所需的表单字段中。

**运行示例：**
```bash
python src/turnstile_solver.py
```

### 4. 解决 reCAPTCHA v3 (基于分数)

对于基于分数的验证码，此示例展示了如何获取具有特定 Action 和最低分数的 Token。

**运行示例：**
```bash
python src/v3_solver.py
```

## ⚙️ 最佳实践

为最大化您的自动化成功率，请遵循以下建议：

1.  **使用反检测标志**：配置 Chrome 选项以禁用自动化标志（请参阅 `src/recaptcha_v2_solver.py` 中的示例）。
2.  **实现随机延迟**：在操作之间添加随机的 `time.sleep()` 调用来模拟人类行为。
3.  **健壮的错误处理**：始终使用 `try...except` 块并为 API 调用实现重试逻辑（请参阅 `src/core_solver.py`）。

## 🤝 贡献指南

我们欢迎社区贡献！请参阅我们的 [CONTRIBUTING.md](CONTRIBUTING.md) 文件，了解如何提交拉取请求、报告错误和提出功能建议。

## 📄 许可证

本项目采用 MIT 许可证授权 - 详情请参阅 [LICENSE](LICENSE) 文件。

---
*免责声明：本项目仅用于教育和道德自动化目的。请遵守您所交互网站的服务条款。*
*附注：在 [CapSolver](https://dashboard.capsolver.com/dashboard/overview/?utm_source=github&utm_medium=repo&utm_campaign=helium-capsolver) 注册时使用代码 **`HELIUM`** 可获得额外奖励积分！*
