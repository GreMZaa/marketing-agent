# 🤖 AI Marketing Agent

Прототип агента-маркетолога с искусственным интеллектом для автоматизации и оптимизации рекламных кампаний.

## 🚀 Возможности

- **Мультиплатформенность** — управление кампаниями Яндекс.Директ, Google Ads, Instagram, Telegram
- **Автоматический расчёт метрик** — CPC, CPO, CPM, конверсии (CR)
- **AI-оптимизация бюджета** — автоматическое перераспределение бюджета по ROI
- **AI-ассистент (Cohere)** — чат с ИИ для рекомендаций по маркетингу
- **Интерактивный дашборд** — визуализация всех кампаний в стиле Craft

## 📦 Установка

```bash
git clone https://github.com/GreMZaa/marketing-agent.git
cd marketing-agent
pip install -r requirements.txt
```

## ▶️ Запуск

```bash
streamlit run app.py
```

## 🔑 Переменные окружения

| Переменная | Описание |
|---|---|
| `COHERE_API_KEY` | API-ключ Cohere для AI-ассистента |

Создайте файл `.env` в корне проекта:
```
COHERE_API_KEY=ваш_ключ
```

## 🛠 Технологии

- Python 3.10+
- Streamlit
- Pandas
- Cohere API
- python-dotenv

## 📸 Скриншот

![Marketing Agent Dashboard](https://img.shields.io/badge/Status-Active-brightgreen)

## 📄 Лицензия

MIT
