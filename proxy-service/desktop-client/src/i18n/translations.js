export const translations = {
  en: {
    hero: {
      eyebrow: 'Proxy Desktop',
      title: 'Connect to a free proxy with your activation key',
      text:
        'The desktop client talks directly to your FastAPI backend, requests a free virtual machine, and keeps the connection status fresh through WebSocket updates.',
      currentState: 'Current state'
    },
    language: {
      label: 'Language',
      english: 'EN',
      russian: 'RU'
    },
    panel: {
      connectionSettings: 'Connection Settings',
      desktopSession: 'Desktop Session',
      backendHint:
        'If the backend is running through docker compose, keep http://localhost:8000 as the Backend URL.'
    },
    fields: {
      backendUrl: 'Backend URL',
      activationKey: 'Activation Key'
    },
    placeholders: {
      backendUrl: 'http://localhost:8000',
      activationKey: 'Paste the one-time activation key from your profile'
    },
    buttons: {
      reset: 'Reset',
      connect: 'Connect',
      connecting: 'Connecting...',
      disconnect: 'Disconnect',
      disconnecting: 'Disconnecting...'
    },
    session: {
      desktopToken: 'Desktop token',
      issued: 'Issued',
      notIssued: 'Not issued yet',
      websocket: 'WebSocket',
      platform: 'Platform',
      electron: 'Electron',
      browser: 'browser',
      notAvailable: 'n/a'
    },
    proxy: {
      assignedProxy: 'Assigned Proxy',
      virtualMachine: 'Virtual Machine',
      noVm:
        'No virtual machine assigned yet. Connect with a valid activation key to reserve one.',
      reservedName: 'Reserved proxy'
    },
    details: {
      statusMessage: 'Status message',
      updatedAt: 'Updated at',
      notUpdatedYet: 'Not updated yet'
    },
    log: {
      liveFeed: 'Live Feed',
      activityLog: 'Activity Log'
    },
    status: {
      waiting: 'Waiting',
      connected: 'Connected',
      disconnected: 'Disconnected',
      no_free_vms: 'All Busy',
      error: 'Error',
      connecting: 'Connecting'
    },
    messages: {
      initial: 'Paste the activation key from the web profile and start a desktop session.',
      requestVm: 'Requesting a virtual machine from the backend...',
      noActiveDesktopSession: 'No active desktop session.',
      noActiveProxyConnection: 'No active proxy connection',
      statusUpdated: 'Status updated.',
      allBusy: 'All proxy servers are busy right now',
      invalidActivationKey: 'Invalid activation key',
      activationKeyExpired: 'Activation key expired',
      requestFailed: 'Request failed',
      networkError: 'Could not reach the backend service.',
      desktopReady: 'Desktop client is ready.',
      formReset: 'Input form was reset.',
      connectionRequestStarted: 'Connection request started.',
      proxyAssigned: ({ protocol, host, port }) => `Proxy assigned: ${protocol}://${host}:${port}`,
      connectionFailed: ({ detail }) => `Connection failed: ${detail}`,
      disconnectWithoutToken: 'Disconnect requested without an active token.',
      disconnectRequestStarted: 'Disconnect request started.',
      disconnectFailed: ({ detail }) => `Disconnect failed: ${detail}`,
      websocketOpening: 'Opening WebSocket channel.',
      websocketConnected: 'WebSocket connected.',
      websocketError: 'WebSocket reported an error.',
      websocketClosed: 'WebSocket closed.',
      nonJsonSocket: 'Received a non-JSON WebSocket message.',
      statusUpdate: ({ status, message }) => `Status update: ${status} - ${message}`,
      connectedTo: ({ name }) => `Connected to ${name}`,
      reconnectedTo: ({ name }) => `Reconnected to ${name}`,
      disconnectedFrom: ({ name }) => `Disconnected from ${name}`
    }
  },
  ru: {
    hero: {
      eyebrow: 'Proxy Desktop',
      title: 'Подключитесь к свободному прокси по ключу активации',
      text:
        'Десктоп-клиент напрямую обращается к вашему FastAPI backend, запрашивает свободную виртуальную машину и получает обновления статуса через WebSocket в реальном времени.',
      currentState: 'Текущее состояние'
    },
    language: {
      label: 'Язык',
      english: 'EN',
      russian: 'RU'
    },
    panel: {
      connectionSettings: 'Настройки подключения',
      desktopSession: 'Десктоп-сессия',
      backendHint:
        'Если backend запущен через docker compose, оставьте http://localhost:8000 в поле URL backend.'
    },
    fields: {
      backendUrl: 'URL backend',
      activationKey: 'Ключ активации'
    },
    placeholders: {
      backendUrl: 'http://localhost:8000',
      activationKey: 'Вставьте одноразовый ключ из личного кабинета'
    },
    buttons: {
      reset: 'Сбросить',
      connect: 'Подключиться',
      connecting: 'Подключение...',
      disconnect: 'Отключиться',
      disconnecting: 'Отключение...'
    },
    session: {
      desktopToken: 'Десктоп-токен',
      issued: 'Выдан',
      notIssued: 'Еще не выдан',
      websocket: 'WebSocket',
      platform: 'Платформа',
      electron: 'Electron',
      browser: 'браузер',
      notAvailable: 'н/д'
    },
    proxy: {
      assignedProxy: 'Выданный прокси',
      virtualMachine: 'Виртуальная машина',
      noVm:
        'Виртуальная машина пока не выделена. Подключитесь с валидным ключом активации, чтобы зарезервировать прокси.',
      reservedName: 'Зарезервированный прокси'
    },
    details: {
      statusMessage: 'Сообщение статуса',
      updatedAt: 'Обновлено',
      notUpdatedYet: 'Еще не обновлялось'
    },
    log: {
      liveFeed: 'Лента событий',
      activityLog: 'Журнал активности'
    },
    status: {
      waiting: 'Ожидание',
      connected: 'Подключено',
      disconnected: 'Отключено',
      no_free_vms: 'Все заняты',
      error: 'Ошибка',
      connecting: 'Подключение'
    },
    messages: {
      initial: 'Вставьте ключ активации из веб-профиля и запустите десктоп-сессию.',
      requestVm: 'Запрашиваем виртуальную машину у backend...',
      noActiveDesktopSession: 'Нет активной десктоп-сессии.',
      noActiveProxyConnection: 'Нет активного подключения к прокси',
      statusUpdated: 'Статус обновлен.',
      allBusy: 'Все прокси-серверы сейчас заняты',
      invalidActivationKey: 'Неверный ключ активации',
      activationKeyExpired: 'Срок действия ключа активации истек',
      requestFailed: 'Запрос завершился ошибкой',
      networkError: 'Не удалось связаться с backend',
      desktopReady: 'Десктоп-клиент готов к работе.',
      formReset: 'Поля формы сброшены.',
      connectionRequestStarted: 'Начат запрос на подключение.',
      proxyAssigned: ({ protocol, host, port }) => `Прокси выдан: ${protocol}://${host}:${port}`,
      connectionFailed: ({ detail }) => `Подключение не удалось: ${detail}`,
      disconnectWithoutToken: 'Запрошено отключение без активного токена.',
      disconnectRequestStarted: 'Начат запрос на отключение.',
      disconnectFailed: ({ detail }) => `Отключение не удалось: ${detail}`,
      websocketOpening: 'Открываем WebSocket-канал.',
      websocketConnected: 'WebSocket подключен.',
      websocketError: 'WebSocket сообщил об ошибке.',
      websocketClosed: 'WebSocket закрыт.',
      nonJsonSocket: 'Получено сообщение WebSocket не в формате JSON.',
      statusUpdate: ({ status, message }) => `Обновление статуса: ${status} - ${message}`,
      connectedTo: ({ name }) => `Подключено к ${name}`,
      reconnectedTo: ({ name }) => `Повторно подключено к ${name}`,
      disconnectedFrom: ({ name }) => `Отключено от ${name}`
    }
  }
}
