#!/usr/bin/env python3
"""
酒店教育课件生成系统 v2.0
Hotel Education Courseware Generator — GHE Aligned (Cornell + EHL + HK PolyU)

GHE = Global Hospitality Education — 全球酒店管理教育标杆知识体系
- Cornell: 运营卓越 + 数据驱动
- EHL (洛桑): 奢华服务 + 欧洲标准  
- HK PolyU: 亚洲市场 + 中国元素

支持 24/7 持续生成，模块化架构，Subagent 并行开发
"""

import os
import sys
import json
import time
import yaml
import hashlib
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# ============ 配置 ============

BASE_DIR = Path.home() / "hotel-education"
COURSES_DIR = BASE_DIR / "courses"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "templates"
STATE_FILE = BASE_DIR / "generation_state.json"
CONFIG_FILE = BASE_DIR / "config.yaml"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / "generator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============ 设计系统常量 ============

# Stripe-inspired 极简顶奢风格
STRIKE_THEME = {
    "name": "stripe",
    "bg": "#ffffff",
    "heading": "#061b31",
    "body": "#64748b",
    "label": "#273951",
    "accent": "#533afd",
    "accent_hover": "#4434d4",
    "border": "#e5edf5",
    "shadow": "rgba(50,50,93,0.25)",
    "radius": "4px",
    "font_primary": "'Source Sans 3', system-ui, sans-serif",
    "font_mono": "'Source Code Pro', monospace",
    "font_weight_light": 300,
    "font_weight_normal": 400,
}

# Linear-inspired 深色精准风格
LINEAR_THEME = {
    "name": "linear",
    "bg": "#08090a",
    "surface": "#0f1011",
    "surface_elevated": "#191a1b",
    "heading": "#f7f8f8",
    "body": "#d0d6e0",
    "muted": "#8a8f98",
    "accent": "#7170ff",
    "accent_bg": "#5e6ad2",
    "border": "rgba(255,255,255,0.08)",
    "border_subtle": "rgba(255,255,255,0.05)",
    "font_primary": "'Inter', system-ui, sans-serif",
    "font_mono": "'JetBrains Mono', monospace",
    "font_weight": 400,
    "font_weight_bold": 510,
}

# 酒店教育专用配色
HOTEL_THEME = {
    "primary": "#1B4D3E",      # 酒店绿
    "secondary": "#C9A962",   # 香槟金
    "accent": "#2C5F2D",       # 深绿
    "dark": "#0A1628",         # 深蓝黑
    "light": "#F5F1E8",        # 米白
    "warm": "#8B4513",         # 暖棕
    "alert": "#C41E3A",        # 警示红
}

# ============ 数据结构 ============

@dataclass
class SlideContent:
    """单页幻灯片内容"""
    slide_id: str
    title: str
    subtitle: Optional[str] = None
    content_type: str = "default"  # title, text, list, image, chart, quote, comparison
    body: str = ""
    items: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    notes: Optional[str] = None
    transition: str = "fade"

@dataclass
class Module:
    """课程模块"""
    module_id: str
    title: str
    duration_minutes: int
    lesson_type: str = "theory"  # theory, practice, case
    slides: List[SlideContent] = field(default_factory=list)
    objectives: List[str] = field(default_factory=list)
    assessment: str = "quiz"

@dataclass
class Course:
    """完整课程"""
    course_id: str
    title: str
    level: str = "intermediate"  # beginner, intermediate, advanced
    modules: List[Module] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    duration_hours: float = 0
    language: str = "zh-CN"
    theme: str = "hotel"  # hotel, stripe, linear

# ============ 核心生成器 ============

class SlideRenderer(ABC):
    """幻灯片渲染器抽象基类"""
    
    @abstractmethod
    def render(self, slide: SlideContent, theme: Dict) -> str:
        pass
    
    def wrap_in_html(self, slides_html: List[str], title: str, theme: Dict) -> str:
        """包装为完整 HTML 文档"""
        fonts_link = self._get_fonts_link(theme)
        css = self._get_theme_css(theme)
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {fonts_link}
    <style>
    {css}
    </style>
</head>
<body>
    <div class="presentation">
        {''.join(slides_html)}
    </div>
</body>
</html>"""
        return html
    
    @abstractmethod
    def _get_fonts_link(self, theme: Dict) -> str:
        pass
    
    @abstractmethod
    def _get_theme_css(self, theme: Dict) -> str:
        pass

class StripeSlideRenderer(SlideRenderer):
    """Stripe 风格幻灯片渲染器 - 极简顶奢"""
    
    def _get_fonts_link(self, theme: Dict) -> str:
        return """<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;500;600&family=Source+Code+Pro:wght@400;500&display=swap" rel="stylesheet">"""
    
    def _get_theme_css(self, theme: Dict) -> str:
        return """
        :root {
            --bg: #ffffff;
            --heading: #061b31;
            --body: #64748b;
            --label: #273951;
            --accent: #533afd;
            --accent-hover: #4434d4;
            --border: #e5edf5;
            --gold: #A88B52;
            --gold-light: #C9A962;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Source Sans 3', system-ui, sans-serif; background: var(--bg); color: var(--body); line-height: 1.6; }
        .presentation { width: 100%; max-width: 1200px; margin: 0 auto; }
        .slide { min-height: 720px; padding: 80px 100px; display: flex; flex-direction: column; position: relative; border-bottom: 1px solid var(--border); }
        .slide--title { justify-content: center; align-items: center; text-align: center; background: linear-gradient(135deg, var(--heading) 0%, #1a2a4a 100%); color: white; }
        .slide--title h1 { font-size: 56px; font-weight: 300; letter-spacing: -1.4px; line-height: 1.03; margin-bottom: 24px; }
        .slide--title .subtitle { font-size: 20px; font-weight: 300; opacity: 0.8; }
        .slide--section { justify-content: center; background: var(--heading); color: white; }
        .slide--section h2 { font-size: 48px; font-weight: 300; letter-spacing: -0.96px; }
        .slide--content { justify-content: flex-start; padding-top: 60px; }
        .slide h3 { font-size: 32px; font-weight: 300; letter-spacing: -0.64px; color: var(--heading); margin-bottom: 40px; }
        .slide .body-text { font-size: 18px; font-weight: 300; line-height: 1.7; color: var(--body); max-width: 800px; }
        .slide .items-list { list-style: none; margin-top: 20px; }
        .slide .items-list li { font-size: 18px; font-weight: 300; line-height: 1.8; padding: 12px 0; border-bottom: 1px solid var(--border); display: flex; align-items: flex-start; gap: 16px; }
        .slide .items-list li::before { content: "—"; color: var(--gold); font-weight: 400; flex-shrink: 0; }
        .slide .quote { font-size: 24px; font-weight: 300; font-style: italic; color: var(--heading); border-left: 3px solid var(--gold); padding-left: 30px; margin: 40px 0; line-height: 1.6; }
        .slide .highlight-box { background: rgba(168,139,82,0.08); border: 1px solid rgba(168,139,82,0.2); border-radius: 4px; padding: 30px; margin: 20px 0; }
        .slide .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; margin-top: 30px; }
        .slide .col h4 { font-size: 18px; font-weight: 500; color: var(--heading); margin-bottom: 16px; }
        .slide .col p { font-size: 16px; font-weight: 300; color: var(--body); }
        .slide .meta { position: absolute; bottom: 30px; right: 40px; font-size: 12px; color: var(--muted, #999); }
        .slide .logo { position: absolute; top: 30px; left: 40px; font-size: 14px; font-weight: 500; color: var(--gold); letter-spacing: 1px; }
        .slide .page-num { position: absolute; bottom: 30px; left: 40px; font-size: 12px; color: var(--muted, #999); }
        """
    
    def render(self, slide: SlideContent, theme: Dict = None) -> str:
        t = STRIKE_THEME
        
        if slide.content_type == "title":
            return f"""<div class="slide slide--title">
    <div class="logo">HOTEL EDUCATION</div>
    <h1>{slide.title}</h1>
    <div class="subtitle">{slide.subtitle or ''}</div>
</div>"""
        
        if slide.content_type == "section":
            return f"""<div class="slide slide--section">
    <h2>{slide.title}</h2>
</div>"""
        
        if slide.content_type == "list":
            items_html = ''.join(f"<li>{item}</li>" for item in slide.items)
            return f"""<div class="slide slide--content">
    <h3>{slide.title}</h3>
    <p class="body-text">{slide.body}</p>
    <ul class="items-list">{items_html}</ul>
    <span class="page-num">{slide.slide_id}</span>
</div>"""
        
        if slide.content_type == "quote":
            return f"""<div class="slide slide--content">
    <h3>{slide.title}</h3>
    <blockquote class="quote">{slide.body}</blockquote>
    <span class="page-num">{slide.slide_id}</span>
</div>"""
        
        if slide.content_type == "comparison":
            cols_html = ''
            for item in slide.items:
                cols_html += f'<div class="col"><h4>{item.get("title","")}</h4><p>{item.get("content","")}</p></div>'
            return f"""<div class="slide slide--content">
    <h3>{slide.title}</h3>
    <div class="two-col">{cols_html}</div>
    <span class="page-num">{slide.slide_id}</span>
</div>"""
        
        # default
        return f"""<div class="slide slide--content">
    <h3>{slide.title}</h3>
    <p class="body-text">{slide.body}</p>
    <span class="page-num">{slide.slide_id}</span>
</div>"""

class LinearSlideRenderer(SlideRenderer):
    """Linear 风格幻灯片渲染器 - 深色精准"""
    
    def _get_fonts_link(self, theme: Dict) -> str:
        return """<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">"""
    
    def _get_theme_css(self, theme: Dict) -> str:
        return """
        :root {
            --bg: #08090a;
            --surface: #0f1011;
            --surface-el: #191a1b;
            --heading: #f7f8f8;
            --body: #d0d6e0;
            --muted: #8a8f98;
            --accent: #7170ff;
            --accent-bg: #5e6ad2;
            --border: rgba(255,255,255,0.08);
            --border-subtle: rgba(255,255,255,0.05);
            --green: #10b981;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--body); line-height: 1.6; }
        .presentation { width: 100%; max-width: 1200px; margin: 0 auto; }
        .slide { min-height: 720px; padding: 80px 100px; display: flex; flex-direction: column; position: relative; border-bottom: 1px solid var(--border); }
        .slide--title { justify-content: center; align-items: center; text-align: center; background: var(--bg); }
        .slide--title h1 { font-size: 56px; font-weight: 510; letter-spacing: -1.4px; line-height: 1.05; color: var(--heading); margin-bottom: 24px; }
        .slide--title .subtitle { font-size: 18px; font-weight: 400; color: var(--muted); }
        .slide--section { justify-content: center; background: var(--surface); border-left: 3px solid var(--accent); padding-left: 60px; }
        .slide--section h2 { font-size: 40px; font-weight: 510; letter-spacing: -0.96px; color: var(--heading); }
        .slide--content { justify-content: flex-start; padding-top: 60px; background: var(--bg); }
        .slide h3 { font-size: 28px; font-weight: 590; letter-spacing: -0.5px; color: var(--heading); margin-bottom: 30px; }
        .slide .body-text { font-size: 17px; font-weight: 400; line-height: 1.7; color: var(--body); max-width: 800px; }
        .slide .items-list { list-style: none; margin-top: 20px; }
        .slide .items-list li { font-size: 16px; font-weight: 400; line-height: 1.7; padding: 14px 0; border-bottom: 1px solid var(--border-subtle); color: var(--body); display: flex; align-items: center; gap: 16px; }
        .slide .items-list li::before { content: ""; width: 6px; height: 6px; background: var(--accent); border-radius: 50%; flex-shrink: 0; }
        .slide .stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-top: 40px; }
        .slide .stat-card { background: var(--surface-el); border: 1px solid var(--border); border-radius: 8px; padding: 30px; }
        .slide .stat-card .number { font-size: 42px; font-weight: 510; color: var(--heading); letter-spacing: -1px; }
        .slide .stat-card .label { font-size: 14px; color: var(--muted); margin-top: 8px; }
        .slide .code-block { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 20px; font-family: 'JetBrains Mono', monospace; font-size: 14px; color: var(--body); }
        .slide .meta { position: absolute; bottom: 30px; right: 40px; font-size: 12px; color: var(--muted); }
        .slide .page-num { position: absolute; bottom: 30px; left: 40px; font-size: 12px; color: var(--muted); }
        """
    
    def render(self, slide: SlideContent, theme: Dict = None) -> str:
        if slide.content_type == "title":
            return f"""<div class="slide slide--title">
    <h1>{slide.title}</h1>
    <div class="subtitle">{slide.subtitle or ''}</div>
</div>"""
        
        if slide.content_type == "section":
            return f"""<div class="slide slide--section">
    <h2>{slide.title}</h2>
</div>"""
        
        if slide.content_type == "stats":
            cards = ''.join(f'<div class="stat-card"><div class="number">{s["value"]}</div><div class="label">{s["label"]}</div></div>' for s in slide.data.get("stats", []))
            return f"""<div class="slide slide--content">
    <h3>{slide.title}</h3>
    <p class="body-text">{slide.body}</p>
    <div class="stat-grid">{cards}</div>
    <span class="page-num">{slide.slide_id}</span>
</div>"""
        
        if slide.content_type == "list":
            items_html = ''.join(f"<li>{item}</li>" for item in slide.items)
            return f"""<div class="slide slide--content">
    <h3>{slide.title}</h3>
    <p class="body-text">{slide.body}</p>
    <ul class="items-list">{items_html}</ul>
    <span class="page-num">{slide.slide_id}</span>
</div>"""
        
        # default
        return f"""<div class="slide slide--content">
    <h3>{slide.title}</h3>
    <p class="body-text">{slide.body}</p>
    <span class="page-num">{slide.slide_id}</span>
</div>"""

class HotelEducationRenderer(SlideRenderer):
    """酒店教育专用风格"""
    
    def _get_fonts_link(self, theme: Dict) -> str:
        return """<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=Inter:wght@300;400;500&family=Noto+Sans+SC:wght@300;400;500&display=swap" rel="stylesheet">"""
    
    def _get_theme_css(self, theme: Dict) -> str:
        hotel = HOTEL_THEME
        return f"""
        :root {{
            --bg: {hotel['light']};
            --heading: {hotel['dark']};
            --body: #4a5568;
            --accent: {hotel['primary']};
            --gold: {hotel['secondary']};
            --border: rgba(27,77,62,0.15);
            --surface: rgba(27,77,62,0.05);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Noto Sans SC', 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--body); line-height: 1.8; }}
        .presentation {{ width: 100%; max-width: 1200px; margin: 0 auto; }}
        .slide {{ min-height: 720px; padding: 80px 100px; display: flex; flex-direction: column; position: relative; border-bottom: 1px solid var(--border); }}
        .slide--title {{ justify-content: center; align-items: center; text-align: center; background: linear-gradient(135deg, {hotel['dark']} 0%, {hotel['primary']} 100%); color: white; }}
        .slide--title h1 {{ font-family: 'Playfair Display', serif; font-size: 52px; font-weight: 500; letter-spacing: -0.5px; line-height: 1.2; margin-bottom: 24px; }}
        .slide--title .subtitle {{ font-size: 18px; font-weight: 300; opacity: 0.85; letter-spacing: 2px; text-transform: uppercase; }}
        .slide--section {{ justify-content: center; background: {hotel['primary']}; color: white; }}
        .slide--section h2 {{ font-family: 'Playfair Display', serif; font-size: 42px; font-weight: 500; }}
        .slide--content {{ justify-content: flex-start; padding-top: 60px; background: var(--bg); }}
        .slide h3 {{ font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 500; color: var(--heading); margin-bottom: 30px; border-left: 4px solid var(--gold); padding-left: 20px; }}
        .slide .body-text {{ font-size: 17px; font-weight: 300; line-height: 1.9; color: var(--body); max-width: 820px; }}
        .slide .items-list {{ list-style: none; margin-top: 20px; }}
        .slide .items-list li {{ font-size: 16px; font-weight: 400; line-height: 1.8; padding: 14px 0; border-bottom: 1px solid var(--border); display: flex; align-items: flex-start; gap: 16px; }}
        .slide .items-list li::before {{ content: "✦"; color: var(--gold); font-size: 12px; flex-shrink: 0; margin-top: 4px; }}
        .slide .highlight-box {{ background: var(--surface); border-left: 4px solid var(--gold); padding: 24px 30px; margin: 20px 0; border-radius: 0 4px 4px 0; }}
        .slide .highlight-box p {{ font-size: 16px; color: var(--heading); }}
        .slide .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 50px; margin-top: 30px; }}
        .slide .col {{ background: white; border: 1px solid var(--border); border-radius: 8px; padding: 28px; }}
        .slide .col h4 {{ font-family: 'Playfair Display', serif; font-size: 18px; color: var(--heading); margin-bottom: 14px; }}
        .slide .col p {{ font-size: 15px; }}
        .slide .process-step {{ display: flex; align-items: center; gap: 20px; margin: 16px 0; }}
        .slide .step-num {{ width: 36px; height: 36px; background: var(--accent); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 500; flex-shrink: 0; }}
        .slide .step-text {{ font-size: 16px; color: var(--heading); }}
        .slide .meta {{ position: absolute; bottom: 24px; right: 40px; font-size: 11px; color: var(--gold); letter-spacing: 1px; }}
        .slide .page-num {{ position: absolute; bottom: 24px; left: 40px; font-size: 11px; color: var(--gold); }}
        .slide .course-tag {{ position: absolute; top: 30px; right: 40px; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: var(--gold); }}
        """
    
    def render(self, slide: SlideContent, theme: Dict = None) -> str:
        if slide.content_type == "title":
            return f"""<div class="slide slide--title">
    <h1>{slide.title}</h1>
    <div class="subtitle">{slide.subtitle or ''}</div>
</div>"""
        
        if slide.content_type == "section":
            return f"""<div class="slide slide--section">
    <h2>{slide.title}</h2>
</div>"""
        
        if slide.content_type == "process":
            steps_html = ''.join(f'''<div class="process-step"><div class="step-num">{i+1}</div><div class="step-text">{s}</div></div>''' for i, s in enumerate(slide.items))
            return f"""<div class="slide slide--content">
    <h3>{slide.title}</h3>
    <p class="body-text">{slide.body}</p>
    <div>{steps_html}</div>
    <span class="page-num">{slide.slide_id}</span>
</div>"""
        
        if slide.content_type == "list":
            items_html = ''.join(f"<li>{item}</li>" for item in slide.items)
            return f"""<div class="slide slide--content">
    <h3>{slide.title}</h3>
    <p class="body-text">{slide.body}</p>
    <ul class="items-list">{items_html}</ul>
    <span class="page-num">{slide.slide_id}</span>
</div>"""
        
        if slide.content_type == "highlight":
            return f"""<div class="slide slide--content">
    <h3>{slide.title}</h3>
    <p class="body-text">{slide.body}</p>
    <div class="highlight-box"><p>{slide.items[0] if slide.items else ''}</p></div>
    <span class="page-num">{slide.slide_id}</span>
</div>"""
        
        return f"""<div class="slide slide--content">
    <h3>{slide.title}</h3>
    <p class="body-text">{slide.body}</p>
    <span class="page-num">{slide.slide_id}</span>
</div>"""

# ============ 课程生成器 ============

class CourseGenerator:
    """课程生成器 - 整合所有方法论"""
    
    def __init__(self, renderer: SlideRenderer = None):
        self.renderer = renderer or HotelEducationRenderer()
    
    def generate_course(self, course: Course) -> str:
        """生成完整课程 HTML"""
        slides_html = []
        
        # 封面
        slides_html.append(SlideContent(
            slide_id="01",
            title=course.title,
            subtitle=f"{course.level.upper()} · {course.language}",
            content_type="title"
        ))
        
        # 目录
        slides_html.append(SlideContent(
            slide_id="02",
            title="课程目录",
            content_type="section"
        ))
        
        module_titles = [m.title for m in course.modules]
        slides_html.append(SlideContent(
            slide_id="03",
            title="内容概览",
            body=f"本课程包含 {len(course.modules)} 个模块，总时长约 {course.duration_hours} 小时",
            content_type="list",
            items=module_titles
        ))
        
        # 各模块
        for i, module in enumerate(course.modules):
            # 模块标题页
            slides_html.append(SlideContent(
                slide_id=f"{i*10+10:02d}",
                title=module.title,
                subtitle=f"模块 {i+1} · {module.duration_minutes} 分钟 · {module.lesson_type}",
                content_type="title"
            ))
            
            # 学习目标
            if module.objectives:
                slides_html.append(SlideContent(
                    slide_id=f"{i*10+11:02d}",
                    title="学习目标",
                    content_type="list",
                    items=module.objectives
                ))
            
            # 模块内容幻灯片
            for j, slide in enumerate(module.slides):
                slide.slide_id = f"{i*10+12+j:02d}"
                slides_html.append(slide)
            
            # 模块小结
            slides_html.append(SlideContent(
                slide_id=f"{i*10+20:02d}",
                title=f"模块小结: {module.title}",
                body=f"完成本模块学习后，您应掌握: {', '.join(module.objectives[:2])}",
                content_type="highlight",
                items=[f"核心概念已理解 · 实操技能已练习 · 案例分析已完成"]
            ))
        
        # 课程总结
        slides_html.append(SlideContent(
            slide_id="99",
            title="课程总结",
            content_type="section"
        ))
        slides_html.append(SlideContent(
            slide_id="100",
            title="下一步学习",
            body="恭喜完成本课程！建议继续学习以下相关课程：",
            content_type="list",
            items=course.prerequisites if course.prerequisites else ["查看完整课程体系"]
        ))
        
        # 渲染所有幻灯片
        rendered = [self.renderer.render(s) for s in slides_html]
        return self.renderer.wrap_in_html(rendered, course.title, {})
    
    def save_course(self, course: Course, output_path: Path):
        """保存课程 HTML"""
        html = self.generate_course(course)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        logger.info(f"✅ 课程已保存: {output_path}")
        return str(output_path)

# ============ Git Push 配置 ============

GHE_CODE_REPO = "https://github.com/fengurt/hotel-education.git"
GHE_COURSES_REPO = "https://github.com/fengurt/hotel-education-courses.git"
GHE_CODE_REPO_DIR = Path.home() / "hotel-education"
GHE_COURSES_REPO_DIR = Path.home() / "hotel-education-courses-repo"

def git_push(repo_path: Path, message: str, remote_url: str = None) -> bool:
    """Git add + commit + push helper"""
    try:
        import subprocess
        repo = repo_path
        
        # Check if it's a git repo
        if not (repo / ".git").exists():
            logger.warning(f"⚠️ {repo} 不是 git 仓库，跳过 push")
            return False
        
        # Set identity if not set
        subprocess.run(["git", "config", "user.email", "pilopio@163.com"], 
                       cwd=repo, check=False, capture_output=True)
        subprocess.run(["git", "config", "user.name", "pilopio"], 
                       cwd=repo, check=False, capture_output=True)
        
        # Add remote if not exists
        result = subprocess.run(["git", "remote", "-v"], cwd=repo, 
                                capture_output=True, text=True)
        if "origin" not in result.stdout:
            if remote_url:
                subprocess.run(["git", "remote", "add", "origin", remote_url], 
                              cwd=repo, check=False, capture_output=True)
        
        # git add
        subprocess.run(["git", "add", "-A"], cwd=repo, capture_output=True)
        
        # Check if there are changes to commit
        result = subprocess.run(["git", "status", "--porcelain"], cwd=repo, 
                                capture_output=True, text=True)
        if not result.stdout.strip():
            logger.info("📦 没有新变化，跳过 commit")
            return True
        
        # git commit
        commit_result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=repo, capture_output=True, text=True
        )
        if commit_result.returncode != 0:
            logger.warning(f"⚠️ Commit 失败: {commit_result.stderr}")
            return False
        
        # git push
        push_result = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=repo, capture_output=True, text=True
        )
        if push_result.returncode == 0:
            logger.info(f"🚀 已推送到 GitHub: {message[:50]}...")
            return True
        else:
            logger.warning(f"⚠️ Push 失败: {push_result.stderr}")
            return False
    except Exception as e:
        logger.error(f"❌ Git push 出错: {e}")
        return False

def git_push_course(course_key: str, theme: str, course_id: str) -> bool:
    """推送单门课程到 courses repo"""
    # courses repo 在 slide_generator 同级目录的 hotel-education-courses-repo
    courses_repo = GHE_CODE_REPO_DIR.parent / "hotel-education-courses-repo"
    if not courses_repo.exists():
        logger.warning(f"⚠️ courses-repo 不存在: {courses_repo}")
        return False
    
    source_html = GHE_CODE_REPO_DIR / "output" / theme / f"{course_key}.html"
    if not source_html.exists():
        return False
    
    # Copy to courses repo
    dest_html = courses_repo / theme / f"{course_key}.html"
    dest_html.parent.mkdir(parents=True, exist_ok=True)
    
    # Only copy if different
    import shutil
    if dest_html.exists():
        if source_html.stat().st_mtime <= dest_html.stat().st_mtime:
            return True  # Already up to date
    
    shutil.copy2(source_html, dest_html)
    
    message = f"Course: {course_id} ({course_key}) — {theme} theme generated"
    return git_push(courses_repo, message, GHE_COURSES_REPO)

# ============ 预置课程模板 ============

COURSE_TEMPLATES = {
    "front-office": {
        "title": "前厅部运营管理",
        "level": "intermediate",
        "course_id": "HE.01.01",
        "modules": [
            {
                "module_id": "MOD-001",
                "title": "前厅部概述与组织架构",
                "duration_minutes": 45,
                "lesson_type": "theory",
                "objectives": [
                    "理解前厅部在酒店中的核心地位",
                    "掌握前厅部组织架构与岗位职责",
                    "熟悉前厅部与其他部门的协作关系"
                ],
                "slides": [
                    {"title": "前厅部的角色定位", "body": "前厅部是酒店的大脑和心脏，负责客人从入住到离店的整个体验旅程。", "content_type": "list", "items": ["客人第一印象和最后印象的创造者", "酒店信息流的中心枢纽", "收益管理的关键执行部门", "客户关系建立的起点"]},
                    {"title": "前厅部组织架构", "body": "现代酒店前厅部通常采用以下组织结构：", "content_type": "list", "items": ["前厅部经理 (Front Office Manager)", "大堂副理 (Assistant Front Office Manager)", "前台主管 (Front Desk Supervisor)", "前台接待员 (Front Desk Agent)", "礼宾部 (Concierge)", "预订部 (Reservation)"]},
                    {"title": "关键绩效指标 (KPI)", "body": "前厅部核心绩效考核指标：", "content_type": "list", "items": ["入住率 (Occupancy Rate)", "平均房价 (ADR - Average Daily Rate)", "每可用客房收益 (RevPAR)", "入住/退房效率", "客人满意度评分", "投诉处理及时率"]},
                ]
            },
            {
                "module_id": "MOD-002",
                "title": "入住流程管理",
                "duration_minutes": 60,
                "lesson_type": "practice",
                "objectives": [
                    "熟练掌握标准入住流程 (Check-in SOP)",
                    "能够处理特殊入住需求 (VIP, 团体, 长住)",
                    "熟练使用酒店管理系统 (PMS) 完成登记"
                ],
                "slides": [
                    {"title": "标准入住流程 (Check-in SOP)", "body": "以下为国际五星级酒店标准入住流程：", "content_type": "process", "items": ["客人抵达，欢迎问候 (30秒内)", "身份证件核查与登记", "付款方式确认与押金收取", "房卡制作与房间分配", "酒店设施与客房介绍", "行李送达与祝住宿愉快"]},
                    {"title": "VIP 入住处理", "body": "VIP 客人入住需要额外关注：", "content_type": "list", "items": ["提前确认房态与特殊需求", "管理层欢迎致辞", "房间升级评估与执行", "欢迎礼品与个性化布置", "快速办理与专属通道"]},
                    {"title": "常见问题处理", "body": "入住过程中可能遇到的特殊情况：", "content_type": "list", "items": ["预订信息不符 — 核查原始订单，必要时联系预订部", "房间已满 (Overbooking) — 升舱或协调附近合作酒店", "证件问题 — 按照治安管理规定执行", "信用卡预授权失败 — 寻求替代支付方式", "语言沟通障碍 — 使用翻译工具或寻求同事协助"]},
                ]
            },
            {
                "module_id": "MOD-003",
                "title": "收益管理基础",
                "duration_minutes": 50,
                "lesson_type": "theory",
                "objectives": [
                    "理解收益管理的基本原理",
                    "掌握 ADR、Occ、RevPAR 三大指标",
                    "能够进行简单的市场需求分析"
                ],
                "slides": [
                    {"title": "收益管理核心概念", "body": "收益管理 (Revenue Management) 是通过优化价格、库存和渠道，最大化酒店收入的管理科学。", "content_type": "highlight", "items": ["在正确的时间，将正确的房间，以正确的价格，销售给正确的客人"]},
                    {"title": "三大核心指标", "body": "衡量酒店收益绩效的三个关键指标：", "content_type": "list", "items": ["入住率 (Occupancy) = 已售客房数 / 可售客房数", "平均房价 (ADR) = 总客房收入 / 已售客房数", "每可用客房收益 (RevPAR) = 入住率 × 平均房价 或 总收入 / 可售客房数"]},
                    {"title": "价格弹性与细分市场", "body": "不同细分市场的价格敏感度分析：", "content_type": "list", "items": ["商务旅客 — 价格不敏感，但对位置和便利性要求高", "休闲旅客 — 价格敏感，但对体验和特色更在意", "团队客户 — 量大价低，需提前规划", "长住客人 — 追求性价比，稳定收入来源"]},
                ]
            },
        ]
    },
    "housekeeping": {
        "title": "客房部运营管理",
        "level": "intermediate",
        "course_id": "HE.01.02",
        "modules": [
            {
                "module_id": "MOD-001",
                "title": "客房清洁标准",
                "duration_minutes": 55,
                "lesson_type": "practice",
                "objectives": [
                    "掌握客房清洁的标准操作流程",
                    "理解客房清洁的质量检查体系",
                    "熟悉不同房型的清洁时间标准"
                ],
                "slides": [
                    {"title": "客房清洁流程 (SOP)", "body": "标准客房清洁分为以下步骤：", "content_type": "process", "items": ["进入前 — 敲门三次，确认无人", "撤除布草 — 床单、枕套、毛巾分类收集", "表面除尘 — 从上到下，从里到外", "卫生间清洁 — 消毒、擦干、补充用品", "地面清洁 — 先吸尘，后湿拖", "床铺整理 — 按标准折叠，枕头方向正确", "复查补缺 — 物品归位，检查遗留物"]},
                    {"title": "清洁质量检查", "body": "建立三级检查体系确保品质：", "content_type": "list", "items": ["第一级: 员工自检 — 完成清洁后自我检查", "第二级: 主管普查 — 楼层主管逐间检查", "第三级: 经理抽查 — 不定期质量抽查"]},
                    {"title": "退房清洁 vs 在住清洁", "body": "两种清洁场景的区别与注意事项：", "content_type": "comparison", "items": [
                        {"title": "退房清洁 (Check-out)", "content": "全面深度清洁，床单毛巾全部更换，垃圾彻底清除，所有表面消毒，检查维修问题"},
                        {"title": "在住清洁 (Stay-over)", "content": "基础清洁整理，更换使用过的毛巾，垃圾清理，床铺整理（不换床单除非客人要求），快速但保持标准"}
                    ]},
                ]
            },
            {
                "module_id": "MOD-002",
                "title": "布草与库存管理",
                "duration_minutes": 40,
                "lesson_type": "theory",
                "objectives": [
                    "理解布草的生命周期管理",
                    "掌握客房耗用品的库存控制方法",
                    "了解绿色可持续发展在客房管理的应用"
                ],
                "slides": [
                    {"title": "布草管理原则", "body": "布草（床单、毛巾等）的管理核心是平衡品质与成本：", "content_type": "list", "items": ["配置标准: 每间客房配置基数 × 轮换系数 = 最低库存量", "报废标准: 破损、变色、变薄达到一定程度必须淘汰", "洗涤标准: 高温消毒、专业洗涤剂、控制洗涤次数", "盘点制度: 每月盘点，记录损耗，分析原因"]},
                    {"title": "绿色客房管理", "body": "可持续发展理念在客房管理中的实践：", "content_type": "highlight", "items": ["减少布草洗涤: 客人可选择减少洗涤频率，既环保又延长布草寿命", "节能措施: 客房电源感应卡、空调节能模式、LED照明", "减少一次性用品: 大瓶装洗漱用品、纸质包装替代塑料"]},
                ]
            },
        ]
    },
    "fnb": {
        "title": "餐饮部运营管理",
        "level": "intermediate",
        "course_id": "HE.01.03",
        "modules": [
            {
                "module_id": "MOD-001",
                "title": "餐饮服务流程",
                "duration_minutes": 60,
                "lesson_type": "practice",
                "objectives": [
                    "掌握标准餐饮服务流程",
                    "理解中西餐服务差异",
                    "熟练处理客人投诉与特殊需求"
                ],
                "slides": [
                    {"title": "餐桌服务标准流程", "body": "西餐零点服务标准流程：", "content_type": "process", "items": ["迎宾 — 引领入座，递上菜单", "餐前服务 — 冰水/茶水，开胃酒询问", "点单 — 记录菜品，注意特殊需求", "上菜 — 按顺序，使用正确的餐具", "席间服务 — 及时撤盘，续水，询问需求", "甜点咖啡 — 清理餐具，递上甜点单", "结账 — 核对账单，礼貌送客"]},
                    {"title": "中餐服务特点", "body": "中餐服务与西餐的关键差异：", "content_type": "list", "items": ["圆桌合餐制 — 菜品共享，需配备公筷公勺", "热菜优先 — 对温度要求高，上菜节奏更快", "个性化需求 — 忌口、过敏、地方口味需提前沟通", "包厢文化 — 注重私密性，服务更个性化"]},
                    {"title": "食品安全标准", "body": "餐饮食品安全五大要点：", "content_type": "list", "items": ["温度控制: 热菜≥60°C，冷菜≤4°C", "交叉污染预防: 生熟分开，刀具砧板分类", "个人卫生: 洗手、穿戴干净工作服、健康证", "食材储存: 先进先出 (FIFO)，定期检查保质期", "清洁消毒: 餐具高温消毒，表面定期消毒"]},
                ]
            },
        ]
    },
    "banquet": {
        "title": "宴会与会议管理",
        "level": "intermediate",
        "course_id": "HE.01.04",
        "prerequisites": ["HE.01.01 前厅部运营管理"],
        "modules": [
            {
                "module_id": "MOD-001",
                "title": "宴会运营概述",
                "duration_minutes": 60,
                "lesson_type": "theory",
                "objectives": [
                    "理解宴会部在酒店运营中的战略地位",
                    "掌握宴会部的组织架构与岗位职责",
                    "熟悉宴会类型分类与市场定位"
                ],
                "slides": [
                    {"title": "宴会部的战略价值", "body": "宴会业务是酒店高溢价、高频次、高品牌展示价值的核心业务板块。", "content_type": "list", "items": ["客房+餐饮+场地的一站式高消费场景", "企业客户与高净值个人的重要入口", "酒店品牌形象的集中展示窗口", "非客房收入的主要来源"]},
                    {"title": "宴会类型分类", "body": "按业务性质划分，宴会部主要承接以下类型活动：", "content_type": "list", "items": ["婚宴与生日宴 — 高端私人聚会，注重氛围与私密", "商务会议与发布会 — 企业形象展示，追求效率与专业", "展览与宴会 — 大型活动，考验综合统筹能力", "主题晚宴与节庆活动 — 品牌营销与客户维护", "政府与国际会议 — 高规格、高标准、严要求"]},
                    {"title": "宴会部组织架构", "body": "典型五星级酒店宴会部组织结构：", "content_type": "list", "items": ["宴会总监 (Banquet Director)", "宴会经理 / 宴会主管 (Banquet Manager / Supervisor)", "宴会销售专员 (Banquet Sales Executive)", "会议统筹协调员 (Conference Coordinator)", "宴会服务领班 (Banquet Captain)", "宴会服务员 (Banquet Waiter)", "场务与技术支持 (Setup & AV Technician)"]},
                ]
            },
            {
                "module_id": "MOD-002",
                "title": "宴会预订与合同管理",
                "duration_minutes": 75,
                "lesson_type": "practice",
                "objectives": [
                    "熟练掌握宴会预订流程与报价方法",
                    "能够独立审核并签订宴会合同",
                    "理解宴会合同的风险管控要点"
                ],
                "slides": [
                    {"title": "宴会预订流程", "body": "从首次咨询到确认订单的标准流程：", "content_type": "process", "items": ["需求了解 — 活动类型、人数、日期、预算", "场地推荐 — 根据人数匹配宴会厅/会议室", "初步报价 — 提供标准菜单与场地报价", "现场踏勘 — 带客户参观，实际测量", "方案定制 — 个性化方案与详细报价", "合同签订 — 收取定金，锁定档期", "活动前确认 — 细节复核，最终确认"]},
                    {"title": "宴会报价策略", "body": "制定宴会报价需要综合考虑以下因素：", "content_type": "list", "items": ["场地使用费 — 非用餐时段的标准收费", "餐饮人均消费 — 最低消费与档次选择", "服务费与税费 — 通常加收15-20%", "附加服务 — 鲜花、灯光、AV设备、停车", "淡旺季浮动 — 旺日加价，淡日折扣", "企业协议价 — 长期客户享受折扣"]},
                    {"title": "宴会合同核心条款", "body": "宴会合同必须明确约定的关键条款：", "content_type": "list", "items": ["活动基本信息 — 名称、日期、时间、场地", "人数与结算方式 — 保证人数与超出收费", "菜单与酒水 — 具体品种、规格、数量", "场地布置与设备 — 搭建时间、用电负荷", "取消政策 — 取消日期与违约金比例", "定金与付款 — 定金金额、尾款结算时间", "意外条款 — 不可抗力、责任划分"]},
                    {"title": "合同风险管控", "body": "宴会合同常见风险及规避措施：", "content_type": "highlight", "items": ["主宴会日确认人数比预期少30%以上 → 收取保证人数费用或设置最低消费", "临时增加设备需求 → 合同中明确增项收费标准", "客户提前撤场 → 明确未消费部分的处理方式"]},
                ]
            },
            {
                "module_id": "MOD-003",
                "title": "宴会执行与服务标准",
                "duration_minutes": 90,
                "lesson_type": "practice",
                "objectives": [
                    "掌握宴会活动前的准备与检查清单",
                    "熟练执行宴会服务流程与标准",
                    "能够处理宴会现场突发状况"
                ],
                "slides": [
                    {"title": "宴会活动前准备", "body": "活动前24小时至开场的标准准备流程：", "content_type": "process", "items": ["T-24h: 最终人数确认，更新厨房备货量", "T-12h: 场地搭建开始，舞台/展台/签到台", "T-6h: 餐桌摆台、餐具准备、花艺布置", "T-3h: 音响灯光调试，AV设备测试", "T-1h: 服务人员到位，站位分工", "T-30min: 迎宾准备，冷餐/甜点准备就绪", "T-0: 嘉宾入场，活动正式开始"]},
                    {"title": "宴会摆台标准", "body": "不同宴会类型的摆台要求：", "content_type": "list", "items": ["西餐宴会 — 中心装饰、主盘、餐具按序摆放、面包盘左侧、水杯右上", "中式围餐 — 圆桌转盘、骨碟、筷子、酱油碟、牙签盅", "自助餐 — 热菜保温台、冷菜台、甜点台、饮料台、回收台", "茶歇 — 咖啡机、茶具、点心托盘、纸杯、纸巾"]},
                    {"title": "服务流程与节奏", "body": "宴会服务全程质量控制要点：", "content_type": "list", "items": ["迎宾 — 微笑问候，引导入座，递上湿巾", "开场 — 主人致辞前确保酒杯齐备，服务员就位", "上菜 — 按约定顺序，控制节奏，菜品温度", "敬酒 — 及时添酒，观察客人需求", "席间服务 — 撤盘及时，保持桌面整洁", "甜点与送客 — 咖啡茶点，送客至门口，致谢"]},
                    {"title": "突发状况处理", "body": "宴会现场常见突发情况及应对：", "content_type": "list", "items": ["设备故障 (AV/灯光) — 立即切换备用设备，致歉并延长休息时间", "食物安全问题 — 立即停止供应，更换菜品，必要时送医", "客人突发疾病 — 通知医护，保留现场，联系家属", "人数超出预期 — 紧急调拨食材与餐具，临时加座", "天气影响 (户外) — 启动备选方案，室内转移或延期"]},
                    {"title": "宴会后收尾与复盘", "body": "活动结束后的标准收尾流程：", "content_type": "list", "items": ["现场清点 — 统计实际人数、消费项目、物品损耗", "账单结算 — 出具最终账单，收取尾款或处理退款", "场地恢复 — 撤场、清洁、还原设施", "客户回访 — 24小时内致电感谢，收集反馈", "内部复盘 — 填写活动总结报告，记录问题与改进点"]},
                ]
            },
            {
                "module_id": "MOD-004",
                "title": "会议管理专题",
                "duration_minutes": 60,
                "lesson_type": "theory",
                "objectives": [
                    "理解会议管理的基本概念与服务流程",
                    "掌握会议类型与场地布置方式",
                    "熟悉会议技术支持与茶歇管理"
                ],
                "slides": [
                    {"title": "会议市场概况", "body": "会议业务 (MICE) 是酒店重要的收入来源：", "content_type": "list", "items": ["会议 (Meeting) — 小规模，讨论为主", "奖励旅游 (Incentive) — 团队激励，高体验感", "大会 (Convention) — 大规模，复杂统筹", "展览 (Exhibition) — 以展示展销为主"]},
                    {"title": "会议场地布置方式", "body": "根据会议性质选择合适的场地布置：", "content_type": "list", "items": ["剧院式 (Theatre) — 适合演讲、授课，舞台在前排", "课堂式 (Classroom) — 有课桌，适合培训，需要笔记", "U型 (U-Shape) — 便于互动讨论，适合小团队", "董事会式 (Boardroom) — 小型高端会议，面对面", "宴会式 (Banquet) — 圆桌用餐或晚宴活动", "鱼骨式 (Fishbone) — 分组讨论，便于展示"]},
                    {"title": "会议技术支持", "body": "现代会议离不开完善的技术支持：", "content_type": "list", "items": ["音响系统 — 麦克风数量、扬声器分布、回声控制", "投影显示 — 分辨率、亮度、幕布尺寸、多屏切换", "视频会议 — 远程参会、视频连线、同声传译", "网络保障 — 现场Wi-Fi带宽、备用网络方案", "灯光设计 — 舞台灯光、氛围灯光、日光灯模式"]},
                    {"title": "茶歇与餐饮管理", "body": "会议茶歇是提升参会体验的重要环节：", "content_type": "list", "items": ["茶歇时间 — 上午10:00、下午15:00各一次", "标准配置 — 咖啡、茶、矿泉水、曲奇、水果", "升级选项 — 鲜榨果汁、冷餐小食、主题甜点台", "人数确认 — 提前确认，准确备货，避免浪费", "摆台位置 — 休息区或走廊，不影响会议进行"]},
                ]
            },
        ]
    },
    "revenue": {
        "title": "收益管理基础",
        "level": "advanced",
        "course_id": "HE.02.01",
        "modules": [
            {
                "module_id": "MOD-001",
                "title": "收益管理理论框架",
                "duration_minutes": 90,
                "lesson_type": "theory",
                "objectives": [
                    "理解收益管理的理论基础",
                    "掌握市场需求预测方法",
                    "能够制定基础的定价策略"
                ],
                "slides": [
                    {"title": "收益管理的起源", "body": "收益管理 (Revenue Management) 起源于美国航空业，1980年代引入酒店业。", "content_type": "highlight", "items": ["1980年代: 美联航首次引入收益管理理念", "1987年: 希尔顿酒店集团大规模实施", "1990年代: 成为国际酒店集团标准配置", "21世纪: AI驱动的动态收益管理兴起"]},
                    {"title": "市场需求预测", "body": "进行需求预测需要考虑的因素：", "content_type": "list", "items": ["历史数据分析 — 去年同期、本月趋势", "市场事件 — 展会、演唱会、体育赛事", "季节性因素 — 旺季、淡季、节假日", "竞争对手动态 — 新开业、促销活动", "宏观经济 — 商务活动、汇率、旅游政策"]},
                    {"title": "动态定价策略", "body": "价格弹性矩阵：", "content_type": "comparison", "items": [
                        {"title": "高需求期", "content": "抬高房价，缩短提前预订期，设置最短入住晚数，关闭折扣渠道"},
                        {"title": "低需求期", "content": "降低底价，放宽限制，启动促销，加强团队销售，启动长住折扣"}
                    ]},
                ]
            },
            {
                "module_id": "MOD-002",
                "title": "分销渠道管理",
                "duration_minutes": 60,
                "lesson_type": "theory",
                "objectives": [
                    "理解酒店分销渠道体系",
                    "掌握渠道成本与收益分析",
                    "能够优化渠道组合策略"
                ],
                "slides": [
                    {"title": "主要分销渠道", "body": "现代酒店分销渠道可分为四大类：", "content_type": "list", "items": ["直销渠道: 官网、电话预订、微信小程序、会员体系", "OTA渠道: 携程、美团、Booking、Expedia (佣金3-25%)", "批发/团队: 旅行社、企业客户、会展公司 (协议价)", "GDS/联动: 全球分销系统、航空公司常旅客"]},
                    {"title": "渠道成本分析", "body": "评估渠道盈利能力的关键指标：", "content_type": "list", "items": ["佣金率 = 佣金金额 / 客房收入", "获客成本 = 总佣金 / 新增客人数量", "渠道贡献 = 该渠道收入占比 vs 利润占比", "长期价值 — 评估渠道带来的会员转化"]},
                ]
            },
        ]
    },
    "digital-marketing": {
        "title": "数字营销",
        "level": "intermediate",
        "course_id": "HE.02.02",
        "modules": [
            {
                "module_id": "MOD-001",
                "title": "酒店数字营销概述",
                "duration_minutes": 45,
                "lesson_type": "theory",
                "objectives": [
                    "理解数字营销在酒店业的重要性",
                    "掌握数字营销漏斗与客户旅程",
                    "熟悉酒店数字营销的主要渠道"
                ],
                "slides": [
                    {"title": "数字营销的定义", "body": "数字营销是指利用数字渠道、平台和技术来推广酒店产品和服务，吸引潜在客人并转化为预订。", "content_type": "highlight", "items": ["线上渠道: 官网、社交媒体、搜索引擎", "移动端: APP、小程序、短信营销", "数据分析: 用户行为、转化率、ROI"]},
                    {"title": "酒店数字营销漏斗", "body": "客人从认知到预订的转化路径：", "content_type": "process", "items": ["认知 — 品牌曝光，社交媒体/搜索引擎广告", "兴趣 — 内容营销，酒店攻略、用户评价", "考虑 — 官网浏览，比价，查看套餐", "预订 — 直接预订或通过OTA完成", "忠诚 — 会员体系，回头客营销"]},
                    {"title": "主要数字营销渠道", "body": "酒店常用的数字营销渠道分类：", "content_type": "list", "items": ["直销渠道: 官网、微信小程序、APP、电话预订", "OTA渠道: 携程、美团、Booking、Expedia", "社交媒体: 微信、微博、抖音、小红书", "搜索引擎: 百度SEO、Google Ads", "内容营销: KOL合作、旅游博主、UGC"]},
                ]
            },
            {
                "module_id": "MOD-002",
                "title": "官网与直销渠道管理",
                "duration_minutes": 60,
                "lesson_type": "practice",
                "objectives": [
                    "掌握酒店官网优化的核心要素",
                    "能够设计和优化直接预订体验",
                    "理解会员体系与CRM的整合策略"
                ],
                "slides": [
                    {"title": "官网的核心作用", "body": "酒店官网是直销渠道的核心，具备以下优势：", "content_type": "list", "items": ["零佣金 — 避免OTA 15-25% 的佣金成本", "品牌控制 — 完全自定义呈现品牌故事", "数据拥有 — 第一时间获取客户数据", "客户关系 — 直接与客人建立联系"]},
                    {"title": "官网用户体验优化", "body": "提升官网转化率的关键要素：", "content_type": "list", "items": ["快速加载 — 3秒内打开，移动端优先", "清晰CTA — 突出'立即预订'按钮", "简化流程 — 减少填写字段，一步预订", "信任建设 — 安全标识、评价展示、取消政策"]},
                    {"title": "会员体系与忠诚度计划", "body": "构建高效会员体系的核心策略：", "content_type": "list", "items": ["等级设计 — 普卡、银卡、金卡、钻石卡", "积分规则 — 住宿、消费、活动参与获取积分", "权益分层 — 升房、延迟退房、专属折扣", "会员日 — 每月会员日促销活动"]},
                ]
            },
            {
                "module_id": "MOD-003",
                "title": "OTA与分销渠道策略",
                "duration_minutes": 60,
                "lesson_type": "theory",
                "objectives": [
                    "理解OTA的运作机制与佣金结构",
                    "掌握OTA平台排名规则与优化方法",
                    "能够制定直销与OTA的平衡策略"
                ],
                "slides": [
                    {"title": "主要OTA平台分析", "body": "国内外主流OTA平台特点：", "content_type": "list", "items": ["携程 — 国内龙头，高端市场占有率高", "美团 — 本地生活流量强，大众市场", "飞猪 — 阿里系，年轻人用户多", "Booking — 国际客人多，英文界面", "Expedia — 北美市场为主，全球覆盖"]},
                    {"title": "OTA佣金结构", "body": "OTA佣金通常采用以下模式：", "content_type": "list", "items": ["抽佣模式 — 按预订金额的15-25%收取佣金", "竞价排名 — 酒店可付费提升曝光位置", "金牌独家 — 签署最惠国待遇，获取专属标识", "促销活动 — 平台补贴活动，酒店配合优惠"]},
                    {"title": "直销vs OTA平衡策略", "body": "渠道组合优化原则：", "content_type": "comparison", "items": [
                        {"title": "加大直销", "content": "高房价时段、会员客人、协议客户、回头客"},
                        {"title": "依赖OTA", "content": "低需求期、新开业市场拓展、品牌曝光需求"}
                    ]},
                ]
            },
            {
                "module_id": "MOD-004",
                "title": "社交媒体营销实战",
                "duration_minutes": 75,
                "lesson_type": "practice",
                "objectives": [
                    "掌握主流社交媒体平台的内容策略",
                    "能够策划有效的社交媒体营销活动",
                    "理解KOL合作与用户生成内容(UGC)的运用"
                ],
                "slides": [
                    {"title": "微信营销生态", "body": "微信是酒店数字营销的核心阵地：", "content_type": "list", "items": ["公众号 — 品牌内容输出，月度推送", "小程序 — 预订入口，即用即走", "视频号 — 短视频内容，直播带货", "朋友圈广告 — 精准投放，本地推广"]},
                    {"title": "小红书种草营销", "body": "小红书已成为酒店种草的重要渠道：", "content_type": "list", "items": ["酒店探店 — 邀请博主体验并分享", "攻略内容 — 周末度假、亲子游、情侣游", "真实评价 — 鼓励客人分享入住体验", "话题营销 — #周末去哪玩 #宝藏酒店"]},
                    {"title": "短视频与直播", "body": "抖音/视频号酒店营销策略：", "content_type": "list", "items": ["短视频 — 房间展示、设施介绍、周边攻略", "直播带货 — 房券预售、套餐秒杀", "挑战赛 — 品牌话题互动，用户参与", "本地商家 — 地理位置推广，附近用户触达"]},
                    {"title": "KOL合作策略", "body": "与关键意见领袖合作的关键步骤：", "content_type": "list", "items": ["筛选匹配 — 粉丝画像与目标客群匹配", "合作形式 — 探店、体验、植入、测评", "效果评估 — 曝光量、互动率、转化率", "长期合作 — 签约品牌大使，持续种草"]},
                ]
            },
            {
                "module_id": "MOD-005",
                "title": "数据分析与投放优化",
                "duration_minutes": 60,
                "lesson_type": "practice",
                "objectives": [
                    "掌握数字营销核心数据指标",
                    "能够分析渠道效果并优化预算分配",
                    "理解A/B测试与数据驱动的决策方法"
                ],
                "slides": [
                    {"title": "核心数据指标体系", "body": "酒店数字营销必须关注的关键指标：", "content_type": "list", "items": ["流量指标 — UV、PV、跳出率、页面停留时间", "转化指标 — 预订转化率、加购率、放弃率", "收益指标 — ADR、RevPAR、每订单成本", "客户指标 — 新客占比、复购率、LTV"]},
                    {"title": "数据分析工具", "body": "主流数据分析平台与应用场景：", "content_type": "list", "items": ["百度统计 — 官网流量分析，关键词效果", "Google Analytics — 国际网站分析，用户行为", "腾讯广告后台 — 微信生态投放数据", "OTA后台 — 各平台曝光、点击、转化"]},
                    {"title": "预算分配与ROI优化", "body": "数据驱动的渠道预算优化策略：", "content_type": "list", "items": ["效果归因 — 确定各渠道的贡献权重", "边际效益 — 找到各渠道最优投放规模", "A/B测试 — 创意、落地页、人群定向测试", "动态调整 — 周度/月度根据数据迭代"]},
                    {"title": "A/B测试实战", "body": "常见的A/B测试场景：", "content_type": "list", "items": ["官网 — 不同的Banner图、按钮颜色、定价展示", "广告 — 不同的创意文案、受众定向、落地页", "邮件 — 不同的标题、下发时间、优惠力度", "小程序 — 不同的预订流程、房型展示顺序"]},
                ]
            },
        ]
    },
    "brand-building": {
        "title": "酒店品牌建设与定位",
        "level": "intermediate",
        "course_id": "GHE.2.1.05",
        "modules": [
            {
                "module_id": "MOD-001",
                "title": "酒店品牌战略框架",
                "duration_minutes": 60,
                "lesson_type": "theory",
                "objectives": [
                    "理解品牌战略在酒店发展中的核心作用",
                    "掌握品牌定位与价值主张的构建方法",
                    "熟悉单体酒店与连锁品牌的架构差异"
                ],
                "slides": [
                    {"title": "品牌战略的定义", "body": "酒店品牌战略是通过独特的品牌定位和价值主张，在目标客群心智中建立差异化认知的系统性方法。", "content_type": "highlight", "items": ["品牌定位 — 在市场中的独特位置", "价值主张 — 超越竞争对手的核心利益", "品牌承诺 — 客人对品牌的合理期望"]},
                    {"title": "品牌定位三要素", "body": "酒店品牌定位需要明确三个核心问题：", "content_type": "list", "items": ["我们是谁 — 品牌身份与核心价值观", "我们为谁服务 — 目标客群画像与需求", "我们提供什么独特价值 — 差异化竞争优势"]},
                    {"title": "品牌价值主张金字塔", "body": "构建品牌价值主张的系统框架：", "content_type": "list", "items": ["品牌愿景 — 未来要成为什么", "品牌使命 — 存在的根本意义", "品牌价值观 — 指导行为的准则", "品牌承诺 — 对客人的具体利益"]},
                    {"title": "单体酒店 vs 连锁品牌", "body": "两种品牌模式的对比分析：", "content_type": "comparison", "items": [
                        {"title": "单体酒店", "content": "灵活度高，可完全个性化定制，但品牌认知局限在本地市场"},
                        {"title": "连锁品牌", "content": "依托集团背书，统一的品牌标准和完善的会员体系支持"}
                    ]}
                ]
            },
            {
                "module_id": "MOD-002",
                "title": "国际酒店集团品牌体系",
                "duration_minutes": 45,
                "lesson_type": "theory",
                "objectives": [
                    "了解 Marriott、Hilton、IHG、Accor 等国际酒店集团的品牌矩阵",
                    "掌握不同品牌档次的定位策略",
                    "学习品牌组合管理的方法"
                ],
                "slides": [
                    {"title": "万豪国际品牌矩阵", "body": "万豪国际是全球最大的酒店集团之一，旗下品牌覆盖各档次：", "content_type": "list", "items": ["Luxury — The Ritz-Carlton, St. Regis, W Hotels, Edition", "Premium — Marriott, Sheraton, Westin, Renaissance", "Select — Courtyard, Fairfield, Aloft", "Extended Stay — Residence Inn, TownePlace Suites"]},
                    {"title": "希尔顿品牌体系", "body": "希尔顿采用差异化的品牌定位策略：", "content_type": "list", "items": ["Luxury — Waldorf Astoria, Conrad, LXR", "Premium — Hilton, DoubleTree, Canopy", "Midscale — Hampton, Tru, Homewood Suites"]},
                    {"title": "洲际酒店集团品牌", "body": "IHG 拥有多个特色品牌：", "content_type": "list", "items": ["Luxury — InterContinental, Kimpton, Hotel Indigo", "Premium — Crowne Plaza, HUALUXE", "Select — Holiday Inn, Holiday Inn Express"]},
                    {"title": "雅高酒店集团", "body": "Accor 是欧洲最大的酒店集团，品牌覆盖全面：", "content_type": "list", "items": ["Luxury — Raffles, Fairmont, Sofitel", "Premium — Pullman, MGallery, Angsana", "Midscale — Novotel, Mercure, Ibis", "Budget — Ibis Budget, HotelF1"]}
                ]
            },
            {
                "module_id": "MOD-003",
                "title": "品牌一致性管理",
                "duration_minutes": 45,
                "lesson_type": "practice",
                "objectives": [
                    "掌握 VI 视觉识别系统的规范应用",
                    "理解服务标准与品牌承诺的一致性",
                    "能够通过培训落地品牌体验"
                ],
                "slides": [
                    {"title": "VI 视觉识别系统规范", "body": "酒店 VI 系统的主要构成与应用：", "content_type": "list", "items": ["Logo 使用规范 — 尺寸、颜色、背景、间距", "色彩系统 — 主色、辅色、渐变色的使用规则", "字体规范 — 中英文标准字体与禁用字体", "图形元素 — 辅助图形与纹样的应用场景"]},
                    {"title": "品牌标准的执行检查", "body": "确保品牌标准落地的方法：", "content_type": "list", "items": ["神秘访客审计 — 第三方以客人视角评估", "定期自查 — 部门内部标准化检查", "品牌审核 — 总部定期飞行检查", "客人反馈 — 通过点评分析品牌感知"]},
                    {"title": "服务标准与品牌承诺", "body": "将品牌承诺转化为可执行的服务标准：", "content_type": "list", "items": ["服务语言 — 标准话术与语调要求", "仪容仪表 — 工装、妆容、姿态标准", "服务流程 — 每个触点的标准动作", "个性化服务 — 根据客人类型灵活调整"]},
                    {"title": "品牌培训体系", "body": "通过系统培训落地品牌标准：", "content_type": "list", "items": ["新员工入职培训 — 品牌文化与基础标准", "在职强化培训 — 定期复训与技能提升", "标杆学习 — 参观优秀门店，学习最佳实践", "认证考核 — 品牌标准考核与认证"]}
                ]
            },
        ]
    },
    "leadership": {
        "title": "酒店领导力与团队管理",
        "level": "advanced",
        "course_id": "HE.04",
        "modules": [
            {
                "module_id": "MOD-001",
                "title": "服务文化与领导力",
                "duration_minutes": 75,
                "lesson_type": "theory",
                "objectives": [
                    "理解服务文化对酒店的重要性",
                    "掌握教练式领导力方法",
                    "能够建设高绩效服务团队"
                ],
                "slides": [
                    {"title": "服务利润链模型", "body": "服务企业的核心价值逻辑：", "content_type": "highlight", "items": ["内部服务质量 → 员工满意度 → 服务质量 → 顾客满意度 → 顾客忠诚度 → 利润增长"]},
                    {"title": "仆人式领导 (Servant Leadership)", "body": "酒店管理者的核心领导哲学：", "content_type": "list", "items": ["服务导向 — 把员工需求放在首位", "授权赋能 — 给予一线员工决策权", "倾听尊重 — 真正理解员工的想法", "善于预见 — 提前发现问题根源", "身体力行 — 与员工一起在现场工作"]},
                    {"title": "有效授权的原则", "body": "在酒店运营中实现有效授权：", "content_type": "list", "items": ["明确目标 — 设定清晰的预期结果", "提供资源 — 确保完成任务所需条件", "定期检查 — 过程监督而非微观管理", "及时反馈 — 表扬优秀，纠正偏差", "承担后果 — 接受团队决策的结果"]},
                ]
            }
        ]
    },
    "cost-control": {
        "title": "成本控制",
        "level": "advanced",
        "course_id": "HE.03.01",
        "modules": [
            {
                "module_id": "MOD-001",
                "title": "酒店成本结构分析",
                "duration_minutes": 60,
                "lesson_type": "theory",
                "objectives": [
                    "理解酒店成本分类体系",
                    "掌握各类成本的占比与控制重点",
                    "能够分析酒店成本结构报表"
                ],
                "slides": [
                    {"title": "酒店成本五大分类", "body": "酒店运营成本可分为五大类别：", "content_type": "list", "items": ["人工成本 (Labor Cost) — 占比约28-35%，最大单项成本", "食品成本 (Food Cost) — 占比约25-30%，包含原材料与损耗", "客房成本 (Rooms Cost) — 布草、清洁用品、客房耗用品", "能源成本 (Utility Cost) — 水电气，占比约3-5%", "营销成本 (Marketing Cost) — 广告、佣金、促销费用"]},
                    {"title": "成本结构占比分析", "body": "国际高星级酒店典型成本结构：", "content_type": "list", "items": ["人工成本: 30-35%", "食品与酒水: 25-30%", "客房成本: 8-12%", "能源与维护: 5-8%", "市场营销: 5-10%", "行政管理: 5-8%", "保险与税费: 3-5%"]},
                    {"title": "成本控制的关键指标", "body": "衡量成本控制效果的核心指标：", "content_type": "list", "items": ["GOP (Gross Operating Profit) — 经营毛利率", "GOPPAR — 每可用客房经营利润", "人工成本率 — 人工成本/总收入", "食品成本率 — 食品成本/食品收入", "坪效 — 每平方米创收能力"]},
                ]
            },
            {
                "module_id": "MOD-002",
                "title": "食品成本控制",
                "duration_minutes": 75,
                "lesson_type": "practice",
                "objectives": [
                    "掌握食品成本率计算方法",
                    "熟练使用标准成本卡 (Standard Recipe Card)",
                    "能够进行有效的厨房库存管理"
                ],
                "slides": [
                    {"title": "食品成本率计算", "body": "食品成本率是餐饮成本控制的核心指标：", "content_type": "list", "items": ["食品成本率 = 食品成本 ÷ 食品收入 × 100%", "标准食品成本率: 28-35% (高端酒店可控制在30%以内)", "理想目标: 毛利率达到65-72%", "影响因素: 食材价格、浪费率、盗窃、菜单定价"]},
                    {"title": "标准成本卡 (Standard Recipe Card)", "body": "标准成本卡是控制食品成本的核心工具：", "content_type": "list", "items": ["定义每道菜的标准配方与用量", "明确每种食材的单位成本", "规定出品份数与标准损耗率", "作为培训和绩效考核的依据", "定期更新以反映价格变动"]},
                    {"title": "厨房库存管理", "body": "有效的库存管理可以显著降低食品成本：", "content_type": "list", "items": ["先进先出 (FIFO) — 优先使用先购入食材", "最低/最高库存量 — 避免积压或缺货", "定期盘点 — 每周或每日收盘点", "验收标准 — 检查质量、数量、有效期", "安全库存 — 应对突发需求的缓冲量"]},
                    {"title": "减少食品浪费的策略", "body": "从源头到终端控制浪费：", "content_type": "list", "items": ["采购端 — 精准预估需求，避免过量采购", "储存端 — 正确储存条件，减少变质损耗", "加工端 — 培训切配技能，提高出成率", "出品端 — 标准份量，杜绝偷工减料", "销售端 — 分析点单率，优化菜单设计"]},
                ]
            },
            {
                "module_id": "MOD-003",
                "title": "人工成本管理",
                "duration_minutes": 60,
                "lesson_type": "theory",
                "objectives": [
                    "理解酒店人工成本的结构组成",
                    "掌握排班优化与劳动效率分析方法",
                    "能够制定人工成本控制方案"
                ],
                "slides": [
                    {"title": "人工成本的构成", "body": "酒店人工成本不仅包含基本工资：", "content_type": "list", "items": ["基本工资 — 合同约定的固定薪酬", "加班费 — 超标准工时的补偿", "绩效奖金 — 与营收或利润挂钩", "社会保险 — 五险一金单位部分", "食宿成本 — 员工餐、宿舍提供", "培训费用 — 新员工入职培训成本"]},
                    {"title": "劳动效率指标", "body": "衡量人工效率的关键指标：", "content_type": "list", "items": ["人房比 — 员工数/客房数 (行业标准: 1:0.5-1.2)", "GOPPAR — 每位员工创造的平均利润", "Revenue per FTE — 每全职员工创收", "Occupancy per FTE — 每员工处理的客房数", "Schedule Efficiency — 排班效率指数"]},
                    {"title": "排班优化策略", "body": "科学排班可以有效控制人工成本：", "content_type": "list", "items": ["需求预测 — 基于入住率、餐期预测工时需求", "弹性用工 — 灵活用工、临时工、实习生", "交叉培训 — 一人多岗，提高适应性", "错峰排班 — 符合实际运营高峰需求", "自班优先 — 减少外包和临时工依赖"]},
                ]
            },
            {
                "module_id": "MOD-004",
                "title": "采购与供应链管理",
                "duration_minutes": 60,
                "lesson_type": "practice",
                "objectives": [
                    "理解酒店采购的分类与流程",
                    "掌握供应商管理与评估方法",
                    "能够进行采购成本分析"
                ],
                "slides": [
                    {"title": "采购分类与管理", "body": "酒店采购可分为三大类型：", "content_type": "list", "items": ["资本性采购 (CapEx) — 设备、装修、家具，一次性大额支出", "运营性采购 (OpEx) — 食材、布草、日耗品，周期性支出", "服务性采购 — 保洁、安保、维保，外包服务"]},
                    {"title": "供应商管理策略", "body": "建立高效的供应商体系：", "content_type": "list", "items": ["供应商分级 — 战略、优选、备选、淘汰", "定期评估 — 质量、价格、交货、服务综合评分", "竞争机制 — 关键物料保持2-3家合格供应商", "长期协议 — 锁定价格与供货条件", "本地采购 — 减少运输成本与碳排放"]},
                    {"title": "采购成本分析方法", "body": "评估采购效益的工具：", "content_type": "list", "items": ["TCO (Total Cost of Ownership) — 总拥有成本分析", "招标议价 — 公开竞标获取最优价格", "联合采购 — 集团化采购获取规模优势", "价格指数 — 对比市场价格波动", "质量成本 — 评估低价替代品的长期成本"]},
                ]
            },
            {
                "module_id": "MOD-005",
                "title": "预算编制与监控",
                "duration_minutes": 60,
                "lesson_type": "practice",
                "objectives": [
                    "掌握酒店年度预算编制流程",
                    "理解预算执行监控与差异分析",
                    "能够进行预算调整与滚动预测"
                ],
                "slides": [
                    {"title": "预算编制流程", "body": "酒店年度预算编制遵循以下步骤：", "content_type": "list", "items": ["1. 设定目标 — 收入、GOP、利润率目标", "2. 环境分析 — 市场趋势、竞争对手、自身能力", "3. 收入预测 — 基于历史数据与未来预期", "4. 成本预算 — 各部门成本需求汇总", "5. 资本支出 — 投资计划与资金安排", "6. 审批确认 — 管理层与董事会审批"]},
                    {"title": "预算监控与差异分析", "body": "预算执行过程中的监控要点：", "content_type": "list", "items": ["周报/月报 — 实际 vs 预算对比分析", "差异率 — 超出或低于预算的百分比", "根本原因 — 分析差异产生的真实原因", "整改措施 — 针对负差异的改进计划", "预警机制 — 设置关键指标的预警阈值"]},
                    {"title": "滚动预测 (Rolling Forecast)", "body": "现代酒店预算管理趋势：", "content_type": "list", "items": ["季度滚动 — 每季度更新未来12个月预测", "动态调整 — 根据市场变化及时修正", "场景模拟 — 乐观/基准/悲观三种情景", "零基预算 — 从零开始论证每项支出", "参与式预算 — 部门负责人参与预算制定"]},
                ]
            }
        ]
    },
    "food-safety": {
        "title": "食品安全与卫生标准 (HACCP)",
        "level": "intermediate",
        "course_id": "GHE.1.3.06",
        "modules": [
            {
                "module_id": "MOD-1",
                "title": "食品安全基础理论",
                "duration_minutes": 45,
                "lesson_type": "theory",
                "objectives": [
                    "理解食品污染的主要类型及危害",
                    "掌握HACCP的起源与发展历程",
                    "熟悉HACCP七大原则的基本框架"
                ],
                "slides": [
                    {"title": "食品污染类型", "body": "食品污染是导致食品安全问题的主要原因，主要分为以下三类：", "content_type": "list", "items": ["生物污染 — 细菌、病毒、寄生虫、真菌", "化学污染 — 农药残留、重金属、添加剂滥用", "物理污染 — 异物、金属碎片、玻璃碎片"]},
                    {"title": "HACCP的起源与发展", "body": "HACCP (Hazard Analysis and Critical Control Points) 系统的发展历程：", "content_type": "highlight", "items": ["1960年代: 美国NASA与Pillsbury公司为太空任务开发", "1970年代: FDA开始在水产品行业推广", "1980年代: CAC正式批准HACCP作为国际标准", "1990年代: 美国强制要求肉禽类产品实施HACCP", "2000年代至今: 全球食品行业广泛采用"]},
                    {"title": "HACCP七大原则", "body": "HACCP体系建立在七大核心原则之上：", "content_type": "list", "items": ["进行危害分析 — 识别潜在的食品安全危害", "确定关键控制点(CCP) — 找出必须控制的点", "建立关键限值 — 设定可接受与不可接受的临界值", "建立监控程序 — 确保持续监测CCP状态", "建立纠正措施 — 当监控显示CCP偏离时采取行动", "建立验证程序 — 确认HACCP系统运作正常", "建立文档记录 — 维持完整的记录体系"]}
                ]
            },
            {
                "module_id": "MOD-2",
                "title": "温度控制与储存标准",
                "duration_minutes": 60,
                "lesson_type": "practice",
                "objectives": [
                    "掌握热链与冷链管理的基本要求",
                    "正确进行食品冷藏和解冻操作",
                    "熟练运用先进先出(FIFO)原则"
                ],
                "slides": [
                    {"title": "热链与冷链管理", "body": "温度控制是食品安全的生命线：", "content_type": "list", "items": ["热食储存 — 热菜保持≥60°C，凉了必须回锅加热", "冷藏储存 — 0-4°C，超过4小时必须废弃", "冷冻储存 — -18°C以下，解冻后不可再次冷冻", "温度监控 — 每4小时记录一次冷藏冷冻温度"]},
                    {"title": "冷藏解冻标准操作", "body": "正确的解冻方法可以防止细菌繁殖：", "content_type": "list", "items": ["冰箱解冻 — 在0-4°C冷藏室缓慢解冻，需提前12-24小时", "流水解冻 — 用流动冷水，需在2小时内完成烹饪", "微波解冻 — 仅适用于即时烹饪，不可保留", "室温解冻 — 严格禁止，细菌繁殖风险极高"]},
                    {"title": "先进先出(FIFO)管理", "body": "FIFO是库存管理的基本原则：", "content_type": "list", "items": ["入库日期标注 — 所有食材必须标注入库日期", "储存位置安排 — 新货放后部，旧货放前部", "定期检查保质期 — 每周检查，及时处理过期品", "记录台账管理 — 建立进出库记录，可追溯"]}
                ]
            },
            {
                "module_id": "MOD-3",
                "title": "个人卫生与操作规范",
                "duration_minutes": 45,
                "lesson_type": "practice",
                "objectives": [
                    "掌握正确的洗手方法和时机",
                    "熟悉工作服穿戴标准",
                    "了解健康证管理和疾病报告制度"
                ],
                "slides": [
                    {"title": "洗手规范", "body": "洗手是预防食品污染最简单有效的措施：", "content_type": "list", "items": ["洗手五时机 — 上班前、处理生食后、接触垃圾后、如厕后、进餐前", "正确步骤 — 用流水打湿、涂皂液、搓揉20秒、冲洗干净、干燥", "手部消毒 — 必要时使用手部消毒剂", "伤口处理 — 手部有伤口必须穿戴防水绷带和手套"]},
                    {"title": "工作服穿戴标准", "body": "规范的工作服穿戴可以减少污染风险：", "content_type": "list", "items": ["帽子/头巾 — 必须完全遮盖头发，防止异物落入", "工作服 — 每日更换，保持干净整洁", "围裙 — 食品处理时必须穿戴一次性或清洁围裙", "鞋子 — 防滑、防水的专用工作鞋"]},
                    {"title": "健康证与疾病报告", "body": "从业人员健康管理是食品安全的重要保障：", "content_type": "list", "items": ["健康证要求 — 从事食品操作人员必须持有效健康证", "定期体检 — 每年进行健康体检", "疾病报告 — 出现腹泻、呕吐、发热等症状必须上报", "调离岗位 — 患有传染性疾病期间必须离开食品处理区"]}
                ]
            },
            {
                "module_id": "MOD-4",
                "title": "卫生检查与应急预案",
                "duration_minutes": 45,
                "lesson_type": "practice",
                "objectives": [
                    "掌握日常卫生检查的方法和要点",
                    "熟悉食品召回流程",
                    "能够处理食物中毒等紧急情况"
                ],
                "slides": [
                    {"title": "日常卫生检查表", "body": "建立完善的日常检查体系：", "content_type": "list", "items": ["个人卫生 — 健康证、洗手、穿戴检查", "区域卫生 — 地面、墙壁、天花板清洁度", "设备卫生 — 冷藏设备温度、砧板刀具清洁度", "食材卫生 — 感官检查、保质期检查、储存规范", "记录完整性 — 温度记录、消毒记录、进货台账"]},
                    {"title": "食品召回流程", "body": "当发现食品安全问题时必须迅速召回：", "content_type": "process", "items": ["问题识别 — 发现异物、变质、污染等问题", "立即停止销售 — 第一时间下架问题产品", "隔离封存 — 防止与其他食品混合", "报告上级 — 及时向管理层和监管部门报告", "原因分析 — 查明问题根源", "整改预防 — 制定措施防止再次发生"]},
                    {"title": "食物中毒应急处理", "body": "发生食物中毒时的紧急处理程序：", "content_type": "list", "items": ["立即救治 — 拨打120，送医治疗", "保护现场 — 保留食品、患者排泄物等证据", "报告上级 — 2小时内向管理层报告", "配合调查 — 提供菜单、食谱、操作记录", "善后处理 — 与患者家属沟通，处理赔偿事宜"]}
                ]
            }
        ]
    },
    "vip-reception": {
        "title": "VIP & 会员客人接待标准",
        "level": "intermediate",
        "course_id": "GHE.1.1.04",
        "prerequisites": ["HE.01.01 前厅部运营管理"],
        "modules": [
            {
                "module_id": "MOD-001",
                "title": "VIP 客人接待理念",
                "duration_minutes": 45,
                "lesson_type": "theory",
                "objectives": [
                    "理解 VIP 客人在酒店运营中的战略价值",
                    "掌握 VIP 分级标准与识别方法",
                    "熟悉 VIP 接待的核心原则与期望管理"
                ],
                "slides": [
                    {"title": "VIP 的战略价值", "body": "VIP 客人是酒店最宝贵的资产，他们不仅贡献高收入，更是品牌口碑的核心传播者。", "content_type": "highlight", "items": ["高消费能力 — VIP 客人平均消费是普通客人的 3-5 倍", "口碑传播 — 一位不满意 VIP 会影响 25+ 潜在客户", "品牌大使 — 忠诚 VIP 是酒店最有力的推荐人", "竞争壁垒 — 优质 VIP 关系形成对手难以复制的关系网络"]},
                    {"title": "VIP 分级标准", "body": "酒店 VIP 客人通常分为以下等级：", "content_type": "list", "items": ["钻石会员 / Diamond — 年度消费 top 0.1%，专属管家服务", "金卡会员 / Gold — 年度消费 top 1%，优先排队与升舱", "银卡会员 / Silver — 季度消费达到标准，基础权益保障", "商务 VIP — 企业协议客户，差旅管家服务", "政府 VIP — 政府机关与事业单位，政务接待标准", "名人 VIP — 演艺明星、社会名流，严格隐私保护"]},
                    {"title": "VIP 识别与预警", "body": "提前识别 VIP 客人至关重要：", "content_type": "list", "items": ["预订来源 — OTA 高端产品、官网直销、企业协议", "历史记录 — 入住频次、累计消费、特殊备注", "特殊标签 — PMS 系统中的 VIP 标识与偏好", "同行人员 — 随行助理、司机、保镖团队", "预订行为 — 临时取消后重新预订、连续多晚连住"]},
                    {"title": "VIP 接待核心原则", "body": "VIP 接待的五大黄金原则：", "content_type": "list", "items": ["预见需求 — 在客人开口之前就满足其需求", "专属关注 — 称呼姓名，让客人感受唯一性", "毫不打扰 — 保持距离感的同时提供周到服务", "快速响应 — VIP 问题优先处理，限时反馈", "超越期望 — 每次都给客人一点小惊喜"]}
                ]
            },
            {
                "module_id": "MOD-002",
                "title": "VIP 入住流程与个性化服务",
                "duration_minutes": 75,
                "lesson_type": "practice",
                "objectives": [
                    "熟练掌握 VIP 入住标准流程 (VIP Check-in SOP)",
                    "能够根据 VIP 级别制定个性化房间准备方案",
                    "掌握升舱决策的评估标准与话术技巧"
                ],
                "slides": [
                    {"title": "VIP 入住标准流程 (VIP Check-in SOP)", "body": "VIP 入住流程比普通入住更加精细化和个性化：", "content_type": "process", "items": ["预订确认 — 入住前一天再次确认预订，发送欢迎短信", "房态核查 — 提前检查房间状态，确认 VIP 特殊布置", "提前准备 — 提前 30 分钟完成登记，预留最佳房间", "欢迎仪式 — 管理人员或专属管家亲自迎接", "快速办理 — 简化前台流程，专属通道或柜台办理", "房间导览 —管家陪同介绍房间设施与特色服务", "跟进关怀 — 入住 15 分钟后电话询问满意度"]},
                    {"title": "房间准备检查清单", "body": "根据 VIP 级别，房间准备有不同的标准：", "content_type": "list", "items": ["基础准备 — 房间清洁、鲜花水果、MINI 吧补充", "高端定制 — 进口气泡酒、精美甜点、定制欢迎卡", "贵宾特供 — 套房/行政楼层、管家服务、专属礼宾", "特殊需求 — 无过敏房间、枕头菜单、按摩服务预约", "商务配置 — 打印机、会议室预约、高速网络测试", "隐私保护 — 匿名入住、楼层隔离、快递保密"]},
                    {"title": "欢迎礼品策略", "body": "精心设计的欢迎礼品让 VIP 感受尊贵：", "content_type": "list", "items": ["季节性礼品 — 根据入住季节提供时令水果/甜品", "本地特色 — 体现城市文化的文创产品", "个性化礼品 — 根据客人偏好准备的定制礼物", "品牌周边 — 酒店Logo精品、品牌香氛、定制用品", "儿童友好 — 有小朋友同行时准备玩具、绘本", "商务客人 — 精致咖啡豆、精美笔记本"]},
                    {"title": "升舱决策标准", "body": "升舱是一项艺术，需要综合评估：", "content_type": "comparison", "items": [
                        {"title": "升舱条件", "content": "高积分/高消费会员、同行人数多、特殊纪念日、预订了高价值房间但当日可免费升级、长期合作企业高管"},
                        {"title": "不升舱条件", "content": "高入住率时段、套房已满、预订本身就是套房、VIP已享受特殊折扣、客人明确表示不需要"}
                    ]},
                    {"title": "升舱话术技巧", "body": "当决定为 VIP 升舱时，使用以下话术：", "content_type": "list", "items": ["主动提议 — '先生/女士，我们为您准备了更好的房间，能否请您移步体验？'", "强调价值 — '免费升级至行政套房，价值 xxx 元'", "给予选择 — '如果您方便的话，我可以带您参观一下新房间'", "记录偏好 — '感谢您的入住，请问您对房间有什么特别偏好？'"]},
                    {"title": "特殊 VIP 处理", "body": "不同类型 VIP 的接待要点：", "content_type": "list", "items": ["演艺明星 — 秘密入住、楼层封锁、媒体屏蔽、优先通道", "政府官员 — 政务规格、安保配合、食品安全、严格保密", "企业高管 — 商务配置、行程私密、快速结账、专属服务", "长期住客 — 居住习惯记录、个性化空间、稳定性保障"]}
                ]
            },
            {
                "module_id": "MOD-003",
                "title": "会员计划与忠诚度管理",
                "duration_minutes": 60,
                "lesson_type": "theory",
                "objectives": [
                    "理解会员体系的设计逻辑与运营策略",
                    "掌握会员等级权益设计与积分策略",
                    "能够运用 CRM 数据进行个性化客人管理"
                ],
                "slides": [
                    {"title": "会员体系的价值", "body": "一个成功的会员体系是酒店最核心的竞争壁垒：", "content_type": "highlight", "items": ["提高复购率 — 会员复购率是非会员的 3 倍以上", "降低获客成本 — 会员获取成本仅为新客的 1/5", "数据资产 — 积累客人偏好、行为数据资产", "品牌忠诚 — 情感连接形成转移成本"]},
                    {"title": "会员等级设计", "body": "典型的酒店会员等级体系：", "content_type": "list", "items": ["普卡 / Classic — 注册即得，基本权益保障", "银卡 / Silver — 5晚/年或消费满额，优先入住", "金卡 / Gold — 20晚/年，客房升级、延迟退房", "白金 / Platinum — 50晚/年，专属礼宾、行政酒廊", "钻石卡 / Diamond — 100晚/年，套房升级、免费早餐", "终身成就 — 累计200晚，永恒尊荣身份"]},
                    {"title": "积分策略设计", "body": "积分是会员体系的核心激励机制：", "content_type": "list", "items": ["住宿积分 — 每消费1元得10-100积分不等", "双倍积分日 — 会员日、生日当月、特定时段", "等级加速 — 高等级会员积分加成 20-100%", "联名积分 — 航空公司、信用卡、合作伙伴", "积分兑换 — 免费房晚、增值服务、商品兑换", "积分到期 — 积分 24 个月有效，促进活跃"]},
                    {"title": "个性化数据管理", "body": "利用客人数据提供个性化服务：", "content_type": "list", "items": ["偏好记录 — 房间朝向、枕头软硬、MINI 吧喜好", "禁忌记录 — 过敏原、讨厌的物品、不喜欢的气味", "纪念日提醒 — 生日、结婚纪念日、入住纪念日", "历史服务 — 之前享受的服务、特殊要求", "反馈追踪 — 历史投诉、满意度评分、服务补救"]},
                    {"title": "CRM 系统应用", "body": "现代酒店 CRM 的核心功能：", "content_type": "list", "items": ["客人画像 — 360度整合客人信息与行为", "标签系统 — 消费能力、健康状况、服务偏好", "营销自动化 — 精准触达、时机把握、内容个性化", "价值预测 — RFM 模型预测客人终身价值", "流失预警 — 识别有流失风险的会员"]},
                    {"title": "会员生命周期管理", "body": "会员从获取到挽留的全程管理：", "content_type": "process", "items": ["获取 — 新会员注册奖励、首次入住优惠", "激活 — 入住提醒、服务介绍、期待值管理", "留存 — 权益升级、积分加赠、生日礼遇", "升级 — 定向激励、高价值活动邀请", "挽回 — 流失预警、专属回归offer、情感连接"]}
                ]
            }
        ]
    }
}

# ============ 状态管理 ============

def load_gen_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"generated": [], "pending": [], "failed": []}

def save_gen_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

# ============ 主生成循环 ============

def generate_all_courses(theme: str = "hotel"):
    """生成所有预置课程"""
    state = load_gen_state()
    
    if theme == "stripe":
        renderer = StripeSlideRenderer()
    elif theme == "linear":
        renderer = LinearSlideRenderer()
    else:
        renderer = HotelEducationRenderer()
    
    generator = CourseGenerator(renderer)
    
    for course_key, course_data in COURSE_TEMPLATES.items():
        if course_key in state["generated"]:
            logger.info(f"跳过已生成: {course_key}")
            continue
        
        try:
            # 构建 Course 对象
            course = Course(
                course_id=course_data["course_id"],
                title=course_data["title"],
                level=course_data["level"],
                modules=[]
            )
            
            for mod_data in course_data["modules"]:
                slides = []
                for slide_data in mod_data.get("slides", []):
                    slides.append(SlideContent(
                        slide_id="",
                        title=slide_data["title"],
                        body=slide_data.get("body", ""),
                        content_type=slide_data.get("content_type", "default"),
                        items=slide_data.get("items", []),
                        data=slide_data.get("data", {})
                    ))
                
                course.modules.append(Module(
                    module_id=mod_data["module_id"],
                    title=mod_data["title"],
                    duration_minutes=mod_data["duration_minutes"],
                    lesson_type=mod_data.get("lesson_type", "theory"),
                    objectives=mod_data.get("objectives", []),
                    slides=slides
                ))
            
            course.duration_hours = sum(m.duration_minutes for m in course.modules) / 60
            
            # 生成 HTML
            output_file = OUTPUT_DIR / theme / f"{course_key}.html"
            generator.save_course(course, output_file)

            state["generated"].append(course_key)
            save_gen_state(state)

            # 自动推送到 GitHub
            git_push_course(course_key, theme, course_data["course_id"])

        except Exception as e:
            logger.error(f"❌ 生成失败 {course_key}: {e}")
            state["failed"].append({"course": course_key, "error": str(e)})
            save_gen_state(state)

def continuous_generation(interval_hours: float = 1):
    """24/7 持续生成模式"""
    logger.info(f"🚀 启动持续生成模式 (间隔: {interval_hours}h)")
    
    while True:
        for theme in ["hotel", "stripe", "linear"]:
            logger.info(f"=== 生成主题: {theme} ===")
            generate_all_courses(theme)
        
        logger.info(f"⏰ 等待 {interval_hours}h 后下次生成...")
        time.sleep(interval_hours * 3600)

# ============ 入口 ============

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "once":
            theme = sys.argv[2] if len(sys.argv) > 2 else "hotel"
            generate_all_courses(theme)
        elif cmd == "continuous":
            interval = float(sys.argv[2]) if len(sys.argv) > 2 else 1
            continuous_generation(interval)
        elif cmd == "list":
            state = load_gen_state()
            print(f"已生成: {len(state['generated'])}")
            print(f"失败: {len(state['failed'])}")
            for c in COURSE_TEMPLATES.keys():
                status = "✅" if c in state["generated"] else "⏳"
                print(f"  {status} {c}")
        elif cmd == "push":
            # 手动推送所有未推送的课程到 GitHub
            theme = sys.argv[2] if len(sys.argv) > 2 else "hotel"
            courses_repo = GHE_CODE_REPO_DIR.parent / "hotel-education-courses-repo"
            if courses_repo.exists():
                git_push(courses_repo, "Manual push: update all courses", GHE_COURSES_REPO)
            git_push(GHE_CODE_REPO_DIR, "Update code repo", GHE_CODE_REPO)
        elif cmd == "demo":
            # 生成单个演示课程
            demo_course = Course(
                course_id="DEMO-001",
                title="前厅部运营管理 — 演示课程",
                level="intermediate"
            )
            demo_course.modules.append(Module(
                module_id="MOD-DEMO",
                title="入住流程详解",
                duration_minutes=30,
                objectives=["掌握标准入住流程", "处理VIP入住", "使用PMS系统"],
                slides=[
                    SlideContent(slide_id="1", title="前厅部的角色", body="前厅部是酒店运营的核心枢纽", content_type="default"),
                    SlideContent(slide_id="2", title="标准入住流程", body="六步标准流程", content_type="process", items=["欢迎问候", "证件核查", "付款确认", "房卡制作", "设施介绍", "祝住宿愉快"]),
                    SlideContent(slide_id="3", title="VIP接待要点", body="特殊客人的特别处理", content_type="highlight", items=["提前沟通特殊需求", "管理层参与欢迎", "房间升级评估"]),
                ]
            ))
            generator = CourseGenerator(HotelEducationRenderer())
            output_path = OUTPUT_DIR / "demo" / "demo.html"
            generator.save_course(demo_course, output_path)
            print(f"演示课程已生成: {output_path}")
    else:
        print("""
酒店教育课件生成器
====================

用法:
  python3 slide_generator.py once [theme]     # 生成所有课程 (一次)
  python3 slide_generator.py continuous [h]   # 持续生成模式
  python3 slide_generator.py list            # 查看生成状态
  python3 slide_generator.py demo            # 生成演示课程

主题 (theme):
  hotel   — 酒店教育专用风格 (默认)
  stripe  — Stripe 极简顶奢风格
  linear  — Linear 深色精准风格

示例:
  python3 slide_generator.py once hotel        # 生成酒店风格课程
  python3 slide_generator.py once stripe      # 生成 Stripe 风格
  python3 slide_generator.py continuous 4      # 每4小时持续生成
""")

if __name__ == "__main__":
    main()
