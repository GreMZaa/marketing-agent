import cohere
import pandas as pd
from typing import Dict, List, Any, Tuple
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MarketingAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("COHERE_API_KEY", "")
        # Initialize client if API key is provided
        if self.api_key:
            self.co = cohere.Client(api_key=self.api_key)
        else:
            self.co = None

    def calculate_metrics(self, campaign: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates CPC, CPM, CPO, and CR (conversion rate).
        """
        spend = float(campaign.get("spend", 0.0))
        impressions = int(campaign.get("impressions", 0))
        clicks = int(campaign.get("clicks", 0))
        conversions = int(campaign.get("conversions", 0))
        
        cpc = spend / clicks if clicks > 0 else 0.0
        cpm = (spend / impressions) * 1000 if impressions > 0 else 0.0
        cpo = spend / conversions if conversions > 0 else 0.0
        cr = (conversions / clicks) * 100 if clicks > 0 else 0.0
        
        metrics = campaign.copy()
        metrics.update({
            "cpc": round(cpc, 2),
            "cpm": round(cpm, 2),
            "cpo": round(cpo, 2),
            "cr": round(cr, 2)
        })
        return metrics

    def optimize_budget(self, campaign_metrics: Dict[str, Any], kpi_cpo: float) -> Tuple[Dict[str, Any], str]:
        """
        Applies rules:
        - If CPO > KPI: Decrease budget by 50%
        - If CPO <= KPI: Increase budget by 50%
        """
        cpo = campaign_metrics["cpo"]
        current_budget = float(campaign_metrics["budget"])
        
        if cpo > kpi_cpo:
            new_budget = current_budget * 0.5
            action = "reduce"
            reason = f"CPO ({cpo:.2f} руб.) превышает KPI ({kpi_cpo:.2f} руб.). Снижаем бюджет на 50% для сокращения расходов и генерируем новые креативы."
        else:
            new_budget = current_budget * 1.5
            action = "increase"
            reason = f"CPO ({cpo:.2f} руб.) в пределах нормы/ниже KPI ({kpi_cpo:.2f} руб.). Кампания эффективна, увеличиваем бюджет на 50% для масштабирования."
            
        optimized = campaign_metrics.copy()
        optimized["new_budget"] = round(new_budget, 2)
        optimized["action"] = action
        optimized["reason"] = reason
        return optimized, action

    def generate_analysis_and_creatives(self, campaign: Dict[str, Any], kpi_cpo: float) -> Dict[str, Any]:
        """
        Calls Cohere API to get analysis and new ad creatives.
        """
        if not self.co:
            return {
                "analysis": "Cohere API key не задан. Анализ недоступен.",
                "new_creatives": []
            }
            
        platform = campaign["platform"]
        cpo = campaign["cpo"]
        cpc = campaign["cpc"]
        cr = campaign["cr"]
        spend = campaign["spend"]
        clicks = campaign["clicks"]
        conversions = campaign["conversions"]
        impressions = campaign["impressions"]
        current_text = campaign["current_text"]
        action = campaign["action"]
        
        # 1. Analytical Summary
        analysis_prompt = f"""
        Ты профессиональный ИИ-аналитик в маркетинге. Проанализируй рекламную кампанию на платформе '{platform}'.
        Метрики:
        - Расход: {spend} руб.
        - Показы: {impressions}
        - Клики: {clicks}
        - Конверсии: {conversions}
        - Стоимость клика (CPC): {cpc} руб.
        - Конверсия (CR): {cr}%
        - Стоимость лида/покупки (CPO): {cpo} руб.
        - Целевой CPO (KPI): {kpi_cpo} руб.
        - Решение по бюджету: {campaign['reason']}
        
        Напиши краткое аналитическое резюме на русском языке (2-3 предложения): объясни, почему кампания успешна или неуспешна, и дай одну конкретную рекомендацию. Будь краток, профессионален и пиши по делу. Не используй общие фразы.
        """
        
        try:
            # Let's try standard v5+ client first
            try:
                response = self.co.chat(
                    message=analysis_prompt,
                    model="command-r-plus-08-2024"
                )
                analysis_text = response.text.strip()
            except AttributeError:
                # Older SDK fallback
                response = self.co.generate(
                    prompt=analysis_prompt,
                    model="command",
                    max_tokens=200
                )
                analysis_text = response.generations[0].text.strip()
        except Exception as e:
            analysis_text = f"Не удалось сгенерировать анализ: {str(e)}"
            
        new_creatives = []
        if action == "reduce":
            # 2. Creative copy generation
            creatives_prompt = f"""
            Ты профессиональный копирайтер. Рекламная кампания на платформе '{platform}' неэффективна (CPO {cpo} руб. выше целевого {kpi_cpo} руб.).
            Текущий текст объявления: "{current_text}"
            
            Напиши 2 новых цепляющих варианта рекламного текста на русском языке для этой платформы, которые исправят ситуацию и повысят конверсию. Тексты должны быть короткими, адаптированными под формат площадки и содержать привлекательное предложение и четкий призыв к действию (CTA).
            Выведи строго два варианта. Не пиши никаких вводных фраз или пояснений. Напиши каждый вариант на новой строке, без нумерации.
            """
            
            try:
                try:
                    response_creatives = self.co.chat(
                        message=creatives_prompt,
                        model="command-r-plus-08-2024"
                    )
                    creatives_raw = response_creatives.text.strip()
                except AttributeError:
                    response_creatives = self.co.generate(
                        prompt=creatives_prompt,
                        model="command",
                        max_tokens=250
                    )
                    creatives_raw = response_creatives.generations[0].text.strip()
                
                # Split lines and filter empty ones
                lines = [line.strip() for line in creatives_raw.split("\n") if line.strip()]
                # Clean up any potential markdown numbers or list signs like "1. ", "- ", etc.
                for line in lines:
                    cleaned = line
                    if cleaned.startswith(("1.", "2.", "3.", "4.", "-", "*")):
                        # strip prefix
                        for prefix in ["1.", "2.", "3.", "4.", "-", "*"]:
                            if cleaned.startswith(prefix):
                                cleaned = cleaned[len(prefix):].strip()
                                break
                    if cleaned:
                        new_creatives.append(cleaned)
                
                # Ensure we have at least some elements
                new_creatives = new_creatives[:2]
            except Exception as e:
                new_creatives = [f"Не удалось сгенерировать креативы: {str(e)}"]
                
        return {
            "analysis": analysis_text,
            "new_creatives": new_creatives
        }
