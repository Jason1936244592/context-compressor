#!/usr/bin/env python3
"""
Context Compressor - 对话上下文压缩主脚本

Usage:
    python compress.py < input.json > output.json
    python compress.py --analyze < input.json
    python compress.py --dry-run < input.json
"""

import json
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class ContextCompressor:
    """对话上下文压缩器"""
    
    def __init__(self, threshold_tokens: int = 50000, compression_ratio: float = 0.7):
        self.threshold = threshold_tokens
        self.target_ratio = compression_ratio
        self.recent_turns = 20  # 保留最近 N 轮完整对话
        
    def analyze(self, history: List[Dict]) -> Dict:
        """分析对话历史"""
        total_tokens = self.count_tokens(history)
        turn_count = len(history) // 2
        
        # 识别关键内容
        key_moments = self.identify_key_moments(history)
        code_blocks = self.extract_code_blocks(history)
        configs = self.extract_configs(history)
        todos = self.extract_todos(history)
        
        # 识别用户偏好
        preferences = self.extract_preferences(history)
        
        return {
            "total_tokens": total_tokens,
            "turn_count": turn_count,
            "key_moments_count": len(key_moments),
            "code_blocks_count": len(code_blocks),
            "configs_count": len(configs),
            "todos_count": len(todos),
            "preferences_count": len(preferences),
            "exceeds_threshold": total_tokens > self.threshold,
            "compression_recommendation": self.get_compression_recommendation(total_tokens)
        }
    
    def compress(self, history: List[Dict], strategy: str = "auto") -> Tuple[List[Dict], Dict]:
        """
        执行压缩
        
        Args:
            history: 对话历史
            strategy: 压缩策略 (auto/aggressive/conservative)
            
        Returns:
            (compressed_history, report)
        """
        if len(history) <= self.recent_turns * 2:
            # 对话太短，不需要压缩
            return history, {"status": "skipped", "reason": "对话太短，无需压缩"}
        
        # 分层压缩
        recent_turns = min(self.recent_turns, len(history) // 2)
        recent = history[-recent_turns * 2:]  # 保留最近 N 轮完整对话
        
        middle_start = max(0, len(history) - recent_turns * 2 - 60)
        middle = history[middle_start:-recent_turns * 2] if middle_start > 0 else []
        old = history[:middle_start] if middle_start > 0 else []
        
        # 生成摘要
        summary = self.generate_summary(old, middle)
        
        # 合并结果
        compressed = [summary] + middle[-20:] + recent if middle else [summary] + recent
        
        # 生成报告
        before_tokens = self.count_tokens(history)
        after_tokens = self.count_tokens(compressed)
        saved_tokens = before_tokens - after_tokens
        saved_ratio = saved_tokens / before_tokens if before_tokens > 0 else 0
        
        report = {
            "status": "success",
            "before_tokens": before_tokens,
            "after_tokens": after_tokens,
            "saved_tokens": saved_tokens,
            "saved_ratio": f"{saved_ratio:.1%}",
            "before_turns": len(history) // 2,
            "after_turns": len(compressed) // 2,
            "preserved": {
                "recent_turns": recent_turns,
                "code_blocks": len(self.extract_code_blocks(compressed)),
                "configs": len(self.extract_configs(compressed)),
                "todos": len(self.extract_todos(compressed))
            }
        }
        
        return compressed, report
    
    def generate_summary(self, old: List[Dict], middle: List[Dict] = None) -> Dict:
        """生成对话摘要"""
        messages = old + (middle if middle else [])
        
        if not messages:
            return {
                "role": "system",
                "content": "## 对话摘要\n\n无早期对话需要摘要。",
                "compressed_from": 0
            }
        
        # 提取关键信息
        key_moments = self.identify_key_moments(messages)
        code_blocks = self.extract_code_blocks(messages)
        configs = self.extract_configs(messages)
        todos = self.extract_todos(messages)
        preferences = self.extract_preferences(messages)
        
        # 生成结构化摘要
        summary_parts = ["## 📋 早期对话摘要\n"]
        
        if preferences:
            summary_parts.append("### 👤 用户偏好\n")
            for pref in preferences[:5]:
                summary_parts.append(f"- {pref[:100]}...\n")
        
        if key_moments:
            summary_parts.append("\n### 🎯 关键决策\n")
            for moment in key_moments[:5]:
                summary_parts.append(f"- {moment[:150]}...\n")
        
        if code_blocks:
            summary_parts.append(f"\n### 💻 代码块 ({len(code_blocks)} 个)\n")
            summary_parts.append("已保留关键代码，详见完整备份。\n")
        
        if configs:
            summary_parts.append(f"\n### ⚙️ 配置变更 ({len(configs)} 处)\n")
            for config in configs[:3]:
                summary_parts.append(f"- {config[:100]}...\n")
        
        if todos:
            summary_parts.append(f"\n### ✅ 待办事项 ({len(todos)} 项)\n")
            for todo in todos[:5]:
                summary_parts.append(f"- {todo[:100]}...\n")
        
        summary_parts.append(f"\n---\n*摘要自 {len(messages)} 轮对话，完整版本已备份*\n")
        
        return {
            "role": "system",
            "content": "".join(summary_parts),
            "compressed_from": len(messages),
            "compressed_at": datetime.now().isoformat()
        }
    
    def get_compression_recommendation(self, tokens: int) -> str:
        """获取压缩建议"""
        if tokens < 30000:
            return "无需压缩"
        elif tokens < 50000:
            return "建议压缩（中等优先级）"
        elif tokens < 100000:
            return "推荐压缩（高优先级）"
        else:
            return "立即压缩（紧急）"
    
    # ============ 辅助方法 ============
    
    def count_tokens(self, messages: List[Dict]) -> int:
        """估算 token 数量（简化版）"""
        total_chars = sum(len(m.get("content", "")) for m in messages)
        # 粗略估算：中文平均每字符 0.5 tokens，英文平均每字符 0.25 tokens
        return int(total_chars * 0.5)
    
    def identify_key_moments(self, history: List[Dict]) -> List[str]:
        """识别关键时刻"""
        key_moments = []
        keywords = ["记住", "重要", "决定", "结论", "完成", "配置", "确定", "最终"]
        
        for msg in history:
            content = msg.get("content", "")
            if any(kw in content for kw in keywords):
                # 提取前后文
                key_moments.append(content[:200])
        
        return key_moments[:20]  # 最多保留 20 个
    
    def extract_code_blocks(self, history: List[Dict]) -> List[str]:
        """提取代码块"""
        codes = []
        for msg in history:
            content = msg.get("content", "")
            if "```" in content:
                # 简单提取代码块
                start = content.find("```")
                while start != -1:
                    end = content.find("```", start + 3)
                    if end != -1:
                        code = content[start:end + 3]
                        if len(code) < 500:  # 只保留短代码块
                            codes.append(code)
                    start = content.find("```", end + 3) if end != -1 else -1
        
        return codes
    
    def extract_configs(self, history: List[Dict]) -> List[str]:
        """提取配置变更"""
        configs = []
        config_keywords = ["config", "配置", "设置", "settings", "enable", "disable"]
        
        for msg in history:
            content = msg.get("content", "")
            if any(kw in content.lower() for kw in config_keywords):
                configs.append(content[:150])
        
        return configs[:10]
    
    def extract_todos(self, history: List[Dict]) -> List[str]:
        """提取待办事项"""
        todos = []
        todo_keywords = ["待办", "todo", "需要", "稍后", "接下来", "记得", "别忘了"]
        
        for msg in history:
            content = msg.get("content", "")
            if any(kw in content.lower() for kw in todo_keywords):
                todos.append(content[:150])
        
        return todos[:15]
    
    def extract_preferences(self, history: List[Dict]) -> List[str]:
        """提取用户偏好"""
        preferences = []
        pref_keywords = ["我喜欢", "我不喜欢", "总是", "从不", "偏好", "习惯"]
        
        for msg in history:
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if any(kw in content for kw in pref_keywords):
                    preferences.append(content[:150])
        
        return preferences[:10]


def backup_history(history: List[Dict], output_dir: str = "~/.openclaw/backups") -> str:
    """备份对话历史"""
    backup_dir = Path(output_dir).expanduser()
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = backup_dir / f"session-{timestamp}.json"
    
    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    return str(backup_file)


def main():
    parser = argparse.ArgumentParser(description="对话上下文压缩工具")
    parser.add_argument("--threshold", type=int, default=50000, help="压缩阈值 tokens")
    parser.add_argument("--ratio", type=float, default=0.7, help="目标压缩比例")
    parser.add_argument("--analyze", action="store_true", help="仅分析，不压缩")
    parser.add_argument("--dry-run", action="store_true", help="试运行，显示预览")
    parser.add_argument("--backup-dir", default="~/.openclaw/backups", help="备份目录")
    
    args = parser.parse_args()
    
    # 读取输入
    try:
        history = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"错误：无法解析输入 JSON - {e}", file=sys.stderr)
        sys.exit(1)
    
    compressor = ContextCompressor(threshold_tokens=args.threshold, compression_ratio=args.ratio)
    
    # 分析
    analysis = compressor.analyze(history)
    
    if args.analyze:
        # 仅分析模式
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
        return
    
    # 检查是否需要压缩
    if not analysis["exceeds_threshold"]:
        print(json.dumps({
            "status": "skipped",
            "reason": analysis["compression_recommendation"],
            "current_tokens": analysis["total_tokens"],
            "threshold": args.threshold
        }, ensure_ascii=False, indent=2))
        return
    
    if args.dry_run:
        # 试运行模式
        compressed, report = compressor.compress(history)
        print("=== 压缩预览 ===")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        print("\n=== 压缩后前 3 条消息 ===")
        for msg in compressed[:3]:
            print(f"[{msg.get('role')}] {msg.get('content', '')[:100]}...")
        return
    
    # 执行压缩
    compressed, report = compressor.compress(history)
    
    # 备份
    backup_file = backup_history(history, args.backup_dir)
    report["backup_file"] = backup_file
    
    # 输出结果
    output = {
        "report": report,
        "compressed_history": compressed
    }
    
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
