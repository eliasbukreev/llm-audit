# Анализ безопасности по ГОСТ 5131 (из удалённого репозитория)

Этот workflow анализирует репозиторий по указанному URL: клонирует его, выполняет анализ по ГОСТ и сохраняет результат в корень рабочего пространства.

## Инструкция по выполнению

### 1. Запросить адрес репозитория

Спроси пользователя URL репозитория для анализа (GitHub, GitLab и т.п.). Примеры форматов:
- `https://github.com/org/repo-name`
- `https://github.com/org/repo-name.git`
- `https://gitlab.com/org/repo-name`

Извлеки имя репозитория из URL (например, `repo-name` из `https://github.com/org/repo-name.git`).

### 2. Клонировать репозиторий

- Создай папку `repos-for-analysis`, если её нет.
- Выполни: `git clone <url> repos-for-analysis/<repo-name>`
- Если клонирование не удалось — сообщи пользователю об ошибке и не переходи к следующим шагам.

### 3. Прочитать план и выполнить анализ

- Прочитай детальный план из `.kilocode/workflows/gost5639/5131/plan.md`
- Выполни анализ **внутри** `repos-for-analysis/<repo-name>/`, следуя инструкциям из плана
- Создай итоговый документ `security-analysis-<repo-name>.md` в корне склонированного репозитория (т.е. в `repos-for-analysis/<repo-name>/security-analysis-<repo-name>.md`)

### 4. Сохранить результат в корень workspace

Скопируй `repos-for-analysis/<repo-name>/security-analysis-<repo-name>.md` в корень рабочего пространства (например, `./security-analysis-<repo-name>.md`), чтобы документ сохранился после удаления репозитория.

### 5. Удалить репозиторий

Удали папку `repos-for-analysis/<repo-name>` (через `rm -rf` или аналог), чтобы освободить место.
