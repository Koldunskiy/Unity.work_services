```markdown
# Unity.work_services

**Unity.work_services** — это набор утилит и сервисов для Unity, упрощающих работу с асинхронными операциями, DI, событиями и другими часто используемыми паттернами в проектах на Unity.

[![Unity Version](https://img.shields.io/badge/Unity-2021.3%2B-blue.svg)](https://unity.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## Содержание

- [Описание](#описание)
- [Установка](#установка)
- [Быстрый старт](#быстрый-старт)
- [Основные компоненты](#основные-компоненты)
- [Примеры использования](#примеры-использования)
- [Контрибьютинг](#контрибьютинг)
- [Лицензия](#лицензия)

## Описание

Репозиторий содержит готовые к использованию сервисы для Unity-проектов:

- **AsyncService** — управление асинхронными задачами с поддержкой отмены и прогресса.
- **EventBus** — легковесная система событий без зависимостей от MonoBehaviour.
- **ServiceLocator** — простой DI-контейнер для регистрации и получения сервисов.
- **CoroutineHelper** — обёртка над корутинами с возможностью ожидания условий.
- **PoolManager** — пул объектов с поддержкой префабов и автоматическим возвратом.

Все сервисы написаны с учетом производительности и удобства интеграции в существующие проекты.

## Установка

### Через Unity Package Manager (Git URL)

1. Откройте **Window → Package Manager**.
2. Нажмите **+ → Add package from git URL**.
3. Вставьте:

```
https://github.com/Koldunskiy/Unity.work_services.git
```

4. Дождитесь загрузки.

### Вручную

```bash
git clone https://github.com/Koldunskiy/Unity.work_services.git Assets/Unity.work_services
```

> Рекомендуется размещать в папке `Assets/Plugins/` или `Assets/Packages/`.

## Быстрый старт

```csharp
using Unity.work_services.Core;

// Регистрация сервиса
ServiceLocator.Register(new PlayerDataService());

// Получение сервиса
var playerData = ServiceLocator.Get<PlayerDataService>();

// Отправка события
EventBus.Publish(new PlayerDiedEvent());

// Подписка на событие
EventBus.Subscribe<PlayerDiedEvent>(OnPlayerDied);
```

## Основные компоненты

| Компонент          | Назначение                                      |
|--------------------|-------------------------------------------------|
| `AsyncService`     | Асинхронные операции с прогрессом и отменой     |
| `EventBus`         | Глобальная система событий                      |
| `ServiceLocator`   | Регистрация и внедрение зависимостей            |
| `CoroutineHelper`  | Удобные корутины с условиями ожидания           |
| `PoolManager`      | Пул объектов с поддержкой префабов              |

## Примеры использования

### Пример: Асинхронная загрузка с прогрессом

```csharp
var asyncOp = AsyncService.Run(async (progress, token) =>
{
    for (int i = 0; i <= 100; i += 10)
    {
        await Task.Delay(100, token);
        progress.Report(i / 100f);
    }
});

asyncOp.ProgressChanged += (p) => Debug.Log($"Прогресс: {p * 100}%");
await asyncOp;
```

### Пример: Пул объектов

```csharp
var pool = new ObjectPool<Bullet>(CreateBullet, 10);

Bullet bullet = pool.Get();
bullet.Fire();

// Возврат в пул
pool.Release(bullet);
```

## Контрибьютинг

Мы приветствуем вклад в развитие проекта!

1. Форкните репозиторий.
2. Создайте ветку: `git checkout -b feature/awesome-feature`.
3. Зафиксируйте изменения: `git commit -m 'Add awesome feature'`.
4. Запушьте: `git push origin feature/awesome-feature`.
5. Создайте Pull Request.

Подробные правила — в [CONTRIBUTING.md](CONTRIBUTING.md).

## Лицензия

Распространяется под лицензией [MIT](LICENSE).

---

**Автор:** [Koldunskiy](https://github.com/Koldunskiy)  
**Поддержка:** Открывайте [Issues](https://github.com/Koldunskiy/Unity.work_services/issues) при возникновении проблем.
```

---

### Как использовать:
1. Скопируй **весь текст выше** (от `# Unity.work_services` до конца).
2. В корне репозитория создай файл:  
   `README.md`
3. Вставь содержимое.
4. Зафиксируй и запушь:

```bash
git add README.md
git commit -m "Add README.md"
git push
```

Готово! README появится на главной странице GitHub.

Если нужно — могу адаптировать под реальную структуру папок/классов. Просто пришли список файлов.
