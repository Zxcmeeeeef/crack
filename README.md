# CRACK - Social Network

Социальная сеть, похожая на Telegram, на Python.

## Возможности

- 👤 Регистрация и аутентификация пользователей
- 💬 Создание каналов и отправка сообщений
- 🔍 Поиск пользователей
- 👥 Присоединение к каналам
- ✏️ Редактирование и удаление сообщений
- 🔐 JWT токены для безопасности

## Установка

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend запустится на `http://localhost:5000`

### Frontend

```bash
cd frontend
pip install -r requirements.txt
python main.py
```

## API Endpoints

### Аутентификация
- `POST /api/auth/register` - Регистрация
- `POST /api/auth/login` - Вход
- `POST /api/auth/logout` - Выход
- `GET /api/auth/me` - Получить текущего пользователя

### Каналы
- `GET /api/channels` - Список каналов пользователя
- `POST /api/channels` - Создать канал
- `POST /api/channels/<id>/join` - Присоединиться к каналу
- `POST /api/channels/<id>/leave` - Покинуть канал

### Сообщения
- `GET /api/messages/channel/<id>` - Получить сообщения канала
- `POST /api/messages/send` - Отправить сообщение
- `PUT /api/messages/<id>` - Редактировать сообщение
- `DELETE /api/messages/<id>` - Удалить сообщение

### Пользователи
- `GET /api/users/<id>` - Получить профиль пользователя
- `GET /api/users/search` - Поиск пользователей
- `PUT /api/users/me` - Обновить профиль

## Структура БД

- **Users** - пользователи
- **Channels** - каналы
- **Messages** - сообщения
- **channel_members** - связь пользователей и каналов

## Использование

1. Запустите backend
2. Запустите frontend
3. Зарегистрируйтесь или войдите
4. Создавайте каналы и общайтесь!

## Технологии

- Backend: Flask, SQLAlchemy, JWT
- Frontend: Tkinter
- БД: SQLite

---

Разработано как демонстрационный проект социальной сети 🚀
