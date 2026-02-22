# 🚀 Деплой Moneycat Bot на Railway

## Что нужно до старта
- Аккаунт на [railway.app](https://railway.app) (вход через GitHub)
- Аккаунт на [github.com](https://github.com)
- Токен бота от [@BotFather](https://t.me/BotFather)
- Твой Telegram User ID (узнать у @userinfobot)
- Бот добавлен в канал как **администратор** с правом публикации

---

## Шаг 1 — Подготовь файлы локально

```bash
# Создай папку проекта
mkdir moneycat_bot && cd moneycat_bot

# Скопируй все файлы из архива в эту папку
# Также положи сюда template.png (шаблон без цифр!)
```

Структура папки должна быть:
```
moneycat_bot/
├── bot.py
├── image_generator.py
├── requirements.txt
├── Procfile
├── .gitignore
├── .env.example
└── template.png        ← твой шаблон БЕЗ цифр
```

Если Inter Semibold не системный — создай папку fonts/:
```
moneycat_bot/
└── fonts/
    └── Inter-SemiBold.ttf
```
Скачать шрифт: https://fonts.google.com/specimen/Inter

---

## Шаг 2 — Залей на GitHub

```bash
cd moneycat_bot
git init
git add .
git commit -m "init"
git branch -M main

# Создай репозиторий на github.com (можно приватный!)
git remote add origin https://github.com/ТВОЙ_ЮЗЕР/moneycat_bot.git
git push -u origin main
```

---

## Шаг 3 — Деплой на Railway

1. Зайди на [railway.app](https://railway.app) → **New Project**
2. Выбери **Deploy from GitHub repo** → выбери `moneycat_bot`
3. Railway автоматически начнёт деплой

---

## Шаг 4 — Переменные окружения

В Railway → твой проект → **Variables** добавь:

| Переменная | Значение |
|---|---|
| `BOT_TOKEN` | токен от BotFather |
| `CHANNEL_ID` | `@moneycat_cargo` или `-100xxxxxxxxx` |
| `ADMIN_IDS` | твой user_id, например `123456789` |
| `WEBHOOK_URL` | оставь пустым пока |

---

## Шаг 5 — Получи URL и добавь в переменные

1. В Railway → **Settings** → **Domains** → Generate Domain
2. Скопируй URL вида `https://moneycat-bot-xxx.railway.app`
3. Добавь его в переменную `WEBHOOK_URL`
4. Railway перезапустит бот автоматически

---

## Шаг 6 — Проверь

Напиши боту `/start` → потом `/rates` → вводи курсы по одному.

---

## Как обновлять курсы с телефона

Просто открой Telegram на телефоне → найди своего бота → `/rates`.
Бот попросит ввести 4 числа по очереди, сгенерирует картинку и предложит опубликовать.

---

## Частые проблемы

**Бот не отвечает** — проверь переменные в Railway → Variables  
**Картинка без текста** — шрифт не найден, положи `Inter-SemiBold.ttf` в папку `fonts/`  
**Текст не на том месте** — напиши мне, подправим координаты  
**Бот не может публиковать в канал** — убедись что бот добавлен как admin в канал
