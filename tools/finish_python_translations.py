from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

CATALOG_DIR = Path("src/reco_box/translations")

SOURCES = [
    "代理地址必须是主机:端口或 HTTP/HTTPS 地址",
    "代理地址不能包含账号密码",
    "代理地址不能包含路径、查询参数或片段",
    "仍有直播间正在录制或转换，请先全部暂停并等待收尾完成",
    "找不到直播间",
    "直播间地址不能为空",
    "该直播间地址已经存在",
    "保存目录不能为空",
    "检测间隔必须是正整数",
    "检测间隔不能低于 30 秒",
    "分段分钟数必须是正整数",
    "不支持该输出格式",
    "默认录制目录不能为空",
    "轮询秒数和分段分钟数必须是正整数",
    "轮询间隔不能低于 30 秒",
    "磁盘保护阈值必须是 1 至 1024 GB",
    "设置保存后校验失败，请重试",
    "选择文件夹",
    "预检失败：{error}",
    "导入失败：{error}",
    "找不到已锁定的解析源码：{path}",
    "暂不支持该直播间链接",
    "当前锁定版淘宝解析器要求登录会话，Reco Box 不导入账号或 Cookie，因此暂不尝试绕过；后续需要实现匿名公开接口后才能启用。",
    "该 TwitCasting 直播间要求登录，匿名模式不可用",
    "该 TwitCasting 页面无法匿名读取，可能需要登录或已受访问限制",
    "TwitCasting 未返回可录制的公开播放地址",
    "未找到 FFmpeg；开发版需要设置 RECO_BOX_FFMPEG",
    "磁盘剩余空间低于 {minimum_free_gb:g} GB，已阻止开始录制",
    "未找到可用直播线路",
    "未找到 ffprobe",
    "录制目录中没有媒体文件",
    "直播预览",
    "尚未取得直播流，请先点击“立即检查并录制”",
    "ffprobe 验证失败",
    "ffprobe 返回了无效 JSON",
    "文件中没有可识别的音视频流",
    "必须先设置录制保存目录",
    "输出格式必须是简单扩展名",
]

TRANSLATIONS = {
    "zh-TW": [
        "代理位址必須是主機:連接埠或 HTTP/HTTPS 位址", "代理位址不能包含帳號密碼", "代理位址不能包含路徑、查詢參數或片段",
        "仍有直播間正在錄製或轉換，請先全部暫停並等待收尾完成", "找不到直播間", "直播間位址不能為空", "該直播間位址已經存在", "儲存目錄不能為空",
        "偵測間隔必須是正整數", "偵測間隔不能低於 30 秒", "分段分鐘數必須是正整數", "不支援該輸出格式", "預設錄製目錄不能為空",
        "輪詢秒數和分段分鐘數必須是正整數", "輪詢間隔不能低於 30 秒", "磁碟保護門檻必須是 1 至 1024 GB", "設定儲存後驗證失敗，請重試", "選擇資料夾",
        "預檢失敗：{error}", "匯入失敗：{error}", "找不到已鎖定的解析原始碼：{path}", "暫不支援該直播間連結",
        "目前鎖定版淘寶解析器要求登入工作階段，Reco Box 不匯入帳號或 Cookie，因此不嘗試繞過；實作匿名公開介面後才能啟用。",
        "該 TwitCasting 直播間要求登入，匿名模式不可用", "該 TwitCasting 頁面無法匿名讀取，可能需要登入或已受存取限制", "TwitCasting 未傳回可錄製的公開播放位址",
        "找不到 FFmpeg；開發版需要設定 RECO_BOX_FFMPEG", "磁碟剩餘空間低於 {minimum_free_gb:g} GB，已阻止開始錄製", "找不到可用直播線路", "找不到 ffprobe",
        "錄製目錄中沒有媒體檔案", "直播預覽", "尚未取得直播串流，請先點擊「立即檢查並錄製」", "ffprobe 驗證失敗", "ffprobe 傳回無效 JSON",
        "檔案中沒有可識別的音訊或視訊串流", "必須先設定錄製儲存目錄", "輸出格式必須是簡單副檔名",
    ],
    "en": [
        "The proxy must be host:port or an HTTP/HTTPS URL", "The proxy cannot contain a username or password", "The proxy cannot contain a path, query, or fragment",
        "A room is still recording or converting. Pause all rooms and wait for finalization", "Room not found", "The room URL cannot be empty", "This room URL already exists", "The save folder cannot be empty",
        "The check interval must be a positive integer", "The check interval cannot be less than 30 seconds", "Segment minutes must be a positive integer", "Unsupported output format", "The default recording folder cannot be empty",
        "Polling seconds and segment minutes must be positive integers", "The polling interval cannot be less than 30 seconds", "The disk protection threshold must be 1–1024 GB", "Saved settings failed verification. Try again", "Select folder",
        "Preflight failed: {error}", "Import failed: {error}", "Pinned resolver source not found: {path}", "This livestream URL is not supported yet",
        "The pinned Taobao resolver requires a signed-in session. Reco Box does not import accounts or cookies and will not bypass this restriction; it can be enabled after a public anonymous interface is implemented.",
        "This TwitCasting room requires login; anonymous mode is unavailable", "This TwitCasting page cannot be read anonymously; it may require login or be access-restricted", "TwitCasting returned no public recordable playback URL",
        "FFmpeg not found; development builds must set RECO_BOX_FFMPEG", "Free disk space is below {minimum_free_gb:g} GB; recording was blocked", "No usable livestream route found", "ffprobe not found",
        "No media files were found in the recording folder", "Livestream preview", "No livestream is available yet. Click ‘Check and record now’ first", "ffprobe validation failed", "ffprobe returned invalid JSON",
        "No recognizable audio or video stream was found", "Set the recording folder first", "The output format must be a simple extension",
    ],
    "es": [
        "El proxy debe ser host:puerto o una URL HTTP/HTTPS", "El proxy no puede contener usuario ni contraseña", "El proxy no puede contener ruta, consulta ni fragmento",
        "Una sala sigue grabando o convirtiendo. Pause todas y espere a que finalicen", "No se encontró la sala", "La URL de la sala no puede estar vacía", "Esta URL ya existe", "La carpeta de guardado no puede estar vacía",
        "El intervalo debe ser un entero positivo", "El intervalo no puede ser inferior a 30 segundos", "Los minutos por segmento deben ser un entero positivo", "Formato de salida no compatible", "La carpeta predeterminada no puede estar vacía",
        "Los segundos de consulta y minutos de segmento deben ser enteros positivos", "El sondeo no puede ser inferior a 30 segundos", "El límite de protección debe ser de 1 a 1024 GB", "Falló la verificación de los ajustes guardados; inténtelo de nuevo", "Seleccionar carpeta",
        "Falló la comprobación: {error}", "Falló la importación: {error}", "No se encontró el código del analizador fijado: {path}", "Esta URL de directo aún no es compatible",
        "El analizador de Taobao fijado exige una sesión iniciada. Reco Box no importa cuentas ni cookies ni elude la restricción; se habilitará tras implementar una interfaz pública anónima.",
        "Esta sala de TwitCasting requiere inicio de sesión; el modo anónimo no está disponible", "Esta página de TwitCasting no puede leerse anónimamente; puede exigir inicio de sesión o estar restringida", "TwitCasting no devolvió una URL pública grabable",
        "No se encontró FFmpeg; la versión de desarrollo debe definir RECO_BOX_FFMPEG", "El espacio libre es inferior a {minimum_free_gb:g} GB; se bloqueó la grabación", "No se encontró una ruta de directo utilizable", "No se encontró ffprobe",
        "No hay archivos multimedia en la carpeta de grabación", "Vista previa del directo", "Aún no hay flujo; pulse «Comprobar y grabar ahora»", "Falló la validación de ffprobe", "ffprobe devolvió JSON no válido",
        "No hay flujos de audio o vídeo reconocibles", "Configure primero la carpeta de grabación", "El formato de salida debe ser una extensión simple",
    ],
    "fr": [
        "Le proxy doit être hôte:port ou une URL HTTP/HTTPS", "Le proxy ne peut pas contenir d’identifiant ni de mot de passe", "Le proxy ne peut pas contenir de chemin, requête ou fragment",
        "Une salle enregistre ou convertit encore. Mettez tout en pause et attendez la fin", "Salle introuvable", "L’URL de la salle ne peut pas être vide", "Cette URL existe déjà", "Le dossier de destination ne peut pas être vide",
        "L’intervalle doit être un entier positif", "L’intervalle ne peut pas être inférieur à 30 secondes", "La durée des segments doit être un entier positif", "Format de sortie non pris en charge", "Le dossier d’enregistrement par défaut ne peut pas être vide",
        "Les secondes de scrutation et minutes de segment doivent être positives", "La scrutation ne peut pas être inférieure à 30 secondes", "Le seuil disque doit être compris entre 1 et 1024 Go", "Échec de la vérification des réglages enregistrés. Réessayez", "Choisir un dossier",
        "Échec du contrôle : {error}", "Échec de l’import : {error}", "Source du résolveur verrouillé introuvable : {path}", "Cette URL de direct n’est pas encore prise en charge",
        "Le résolveur Taobao verrouillé exige une session connectée. Reco Box n’importe ni compte ni cookie et ne contourne pas cette restriction ; une interface publique anonyme est nécessaire.",
        "Cette salle TwitCasting exige une connexion ; le mode anonyme est indisponible", "Cette page TwitCasting n’est pas lisible anonymement ; connexion ou restriction possible", "TwitCasting n’a renvoyé aucune URL publique enregistrable",
        "FFmpeg introuvable ; la version de développement doit définir RECO_BOX_FFMPEG", "Espace libre inférieur à {minimum_free_gb:g} Go ; enregistrement bloqué", "Aucune route de direct utilisable", "ffprobe introuvable",
        "Aucun fichier multimédia dans le dossier d’enregistrement", "Aperçu du direct", "Aucun flux disponible. Cliquez d’abord sur « Vérifier et enregistrer »", "Échec de validation ffprobe", "ffprobe a renvoyé un JSON invalide",
        "Aucun flux audio ou vidéo reconnaissable", "Définissez d’abord le dossier d’enregistrement", "Le format de sortie doit être une extension simple",
    ],
    "de": [
        "Der Proxy muss Host:Port oder eine HTTP/HTTPS-URL sein", "Der Proxy darf keinen Benutzernamen oder Passwort enthalten", "Der Proxy darf keinen Pfad, keine Abfrage und kein Fragment enthalten",
        "Ein Raum zeichnet noch auf oder konvertiert. Alles pausieren und Abschluss abwarten", "Raum nicht gefunden", "Die Raum-URL darf nicht leer sein", "Diese Raum-URL existiert bereits", "Der Speicherordner darf nicht leer sein",
        "Das Prüfintervall muss eine positive Ganzzahl sein", "Das Prüfintervall darf nicht unter 30 Sekunden liegen", "Segmentminuten müssen eine positive Ganzzahl sein", "Ausgabeformat nicht unterstützt", "Der Standard-Aufnahmeordner darf nicht leer sein",
        "Abfragesekunden und Segmentminuten müssen positiv sein", "Das Abfrageintervall darf nicht unter 30 Sekunden liegen", "Der Festplattengrenzwert muss 1–1024 GB betragen", "Gespeicherte Einstellungen konnten nicht geprüft werden. Erneut versuchen", "Ordner auswählen",
        "Vorprüfung fehlgeschlagen: {error}", "Import fehlgeschlagen: {error}", "Fixierter Resolver-Quellcode nicht gefunden: {path}", "Diese Livestream-URL wird noch nicht unterstützt",
        "Der fixierte Taobao-Resolver benötigt eine angemeldete Sitzung. Reco Box importiert keine Konten oder Cookies und umgeht die Sperre nicht; zuerst ist eine öffentliche anonyme Schnittstelle nötig.",
        "Dieser TwitCasting-Raum erfordert eine Anmeldung; anonymer Modus ist nicht verfügbar", "Diese TwitCasting-Seite ist anonym nicht lesbar; Anmeldung oder Zugriffsbeschränkung möglich", "TwitCasting lieferte keine öffentlich aufnehmbare URL",
        "FFmpeg nicht gefunden; Entwicklungsbuilds müssen RECO_BOX_FFMPEG setzen", "Freier Speicher unter {minimum_free_gb:g} GB; Aufnahme wurde blockiert", "Keine nutzbare Livestream-Route gefunden", "ffprobe nicht gefunden",
        "Keine Mediendateien im Aufnahmeordner", "Livestream-Vorschau", "Noch kein Stream verfügbar. Zuerst „Jetzt prüfen und aufnehmen“ wählen", "ffprobe-Prüfung fehlgeschlagen", "ffprobe lieferte ungültiges JSON",
        "Kein erkennbarer Audio- oder Videostream", "Zuerst den Aufnahmeordner festlegen", "Das Ausgabeformat muss eine einfache Erweiterung sein",
    ],
    "pt": [
        "O proxy deve ser anfitrião:porta ou um URL HTTP/HTTPS", "O proxy não pode conter utilizador ou palavra-passe", "O proxy não pode conter caminho, consulta ou fragmento",
        "Uma sala ainda está a gravar ou converter. Pause todas e aguarde a conclusão", "Sala não encontrada", "O URL da sala não pode estar vazio", "Este URL já existe", "A pasta de destino não pode estar vazia",
        "O intervalo deve ser um inteiro positivo", "O intervalo não pode ser inferior a 30 segundos", "Os minutos por segmento devem ser um inteiro positivo", "Formato de saída não suportado", "A pasta predefinida não pode estar vazia",
        "Segundos de consulta e minutos de segmento devem ser positivos", "A consulta não pode ser inferior a 30 segundos", "O limite de proteção deve ser de 1 a 1024 GB", "Falha ao verificar as definições guardadas. Tente novamente", "Selecionar pasta",
        "Falha na pré-verificação: {error}", "Falha na importação: {error}", "Código do resolvedor fixado não encontrado: {path}", "Este URL de transmissão ainda não é suportado",
        "O resolvedor Taobao fixado exige sessão iniciada. O Reco Box não importa contas ou cookies nem contorna a restrição; é necessária uma interface pública anónima.",
        "Esta sala TwitCasting exige início de sessão; o modo anónimo está indisponível", "Esta página TwitCasting não pode ser lida anonimamente; pode exigir sessão ou estar restrita", "O TwitCasting não devolveu URL público gravável",
        "FFmpeg não encontrado; a versão de desenvolvimento deve definir RECO_BOX_FFMPEG", "Espaço livre inferior a {minimum_free_gb:g} GB; gravação bloqueada", "Não foi encontrada rota utilizável", "ffprobe não encontrado",
        "Não há ficheiros multimédia na pasta de gravação", "Pré-visualização da transmissão", "Ainda não há fluxo. Clique primeiro em «Verificar e gravar agora»", "Falha na validação do ffprobe", "O ffprobe devolveu JSON inválido",
        "Não foi encontrado fluxo de áudio ou vídeo reconhecível", "Defina primeiro a pasta de gravação", "O formato de saída deve ser uma extensão simples",
    ],
    "ru": [
        "Прокси должен иметь вид хост:порт или URL HTTP/HTTPS", "Прокси не должен содержать логин или пароль", "Прокси не должен содержать путь, запрос или фрагмент",
        "Одна из комнат ещё записывается или конвертируется. Приостановите всё и дождитесь завершения", "Комната не найдена", "URL комнаты не может быть пустым", "Такой URL уже существует", "Папка сохранения не может быть пустой",
        "Интервал проверки должен быть положительным целым", "Интервал не может быть меньше 30 секунд", "Минуты сегмента должны быть положительным целым", "Формат вывода не поддерживается", "Папка записи по умолчанию не может быть пустой",
        "Секунды опроса и минуты сегмента должны быть положительными", "Опрос не может быть реже 30 секунд", "Порог диска должен быть 1–1024 ГБ", "Проверка сохранённых настроек не удалась. Повторите", "Выбрать папку",
        "Предварительная проверка не удалась: {error}", "Импорт не удался: {error}", "Исходный код закреплённого анализатора не найден: {path}", "Этот URL трансляции пока не поддерживается",
        "Закреплённый анализатор Taobao требует авторизованную сессию. Reco Box не импортирует учётные записи или cookies и не обходит ограничение; нужен публичный анонимный интерфейс.",
        "Эта комната TwitCasting требует входа; анонимный режим недоступен", "Страница TwitCasting недоступна анонимно; возможен вход или ограничение доступа", "TwitCasting не вернул публичный URL для записи",
        "FFmpeg не найден; в сборке разработчика задайте RECO_BOX_FFMPEG", "Свободно меньше {minimum_free_gb:g} ГБ; запись заблокирована", "Не найден доступный маршрут трансляции", "ffprobe не найден",
        "В папке записи нет медиафайлов", "Предпросмотр трансляции", "Поток ещё не получен. Сначала нажмите «Проверить и записать»", "Проверка ffprobe не удалась", "ffprobe вернул недопустимый JSON",
        "Не найден распознаваемый аудио- или видеопоток", "Сначала задайте папку записи", "Формат вывода должен быть простым расширением",
    ],
    "ja": [
        "プロキシは ホスト:ポート または HTTP/HTTPS URL で指定してください", "プロキシにユーザー名やパスワードは含められません", "プロキシにパス、クエリ、フラグメントは含められません",
        "録画または変換中のルームがあります。すべて一時停止して完了を待ってください", "ルームが見つかりません", "ルーム URL は空にできません", "このルーム URL は既に存在します", "保存先は空にできません",
        "確認間隔は正の整数で指定してください", "確認間隔は 30 秒未満にできません", "分割時間は正の整数で指定してください", "未対応の出力形式です", "既定の録画先は空にできません",
        "確認秒数と分割分数は正の整数で指定してください", "ポーリング間隔は 30 秒未満にできません", "ディスク保護しきい値は 1～1024 GB です", "保存後の設定検証に失敗しました。再試行してください", "フォルダーを選択",
        "事前確認に失敗：{error}", "インポートに失敗：{error}", "固定リゾルバーのソースが見つかりません：{path}", "このライブ URL はまだ対応していません",
        "固定された Taobao リゾルバーはログイン済みセッションを要求します。Reco Box はアカウントや Cookie を取り込まず制限も回避しません。公開匿名 API の実装後に有効化できます。",
        "この TwitCasting ルームはログインが必要なため匿名モードを使用できません", "この TwitCasting ページは匿名で読めません。ログインまたはアクセス制限の可能性があります", "TwitCasting から録画可能な公開 URL が返されませんでした",
        "FFmpeg が見つかりません。開発版では RECO_BOX_FFMPEG を設定してください", "空き容量が {minimum_free_gb:g} GB 未満のため録画を開始しません", "利用可能な配信ルートが見つかりません", "ffprobe が見つかりません",
        "録画フォルダーにメディアファイルがありません", "ライブプレビュー", "配信を取得していません。先に「今すぐ確認して録画」を押してください", "ffprobe 検証に失敗", "ffprobe が無効な JSON を返しました",
        "認識可能な音声・映像ストリームがありません", "先に録画保存先を設定してください", "出力形式は単純な拡張子で指定してください",
    ],
    "ko": [
        "프록시는 호스트:포트 또는 HTTP/HTTPS URL이어야 합니다", "프록시에 사용자 이름이나 비밀번호를 포함할 수 없습니다", "프록시에 경로, 쿼리 또는 조각을 포함할 수 없습니다",
        "녹화 또는 변환 중인 방이 있습니다. 모두 일시 중지하고 마무리를 기다리세요", "방을 찾을 수 없습니다", "방 URL은 비워 둘 수 없습니다", "이 방 URL은 이미 존재합니다", "저장 폴더는 비워 둘 수 없습니다",
        "확인 간격은 양의 정수여야 합니다", "확인 간격은 30초보다 짧을 수 없습니다", "분할 시간은 양의 정수여야 합니다", "지원하지 않는 출력 형식입니다", "기본 녹화 폴더는 비워 둘 수 없습니다",
        "폴링 초와 분할 분은 양의 정수여야 합니다", "폴링 간격은 30초보다 짧을 수 없습니다", "디스크 보호 임계값은 1~1024GB여야 합니다", "저장된 설정 검증에 실패했습니다. 다시 시도하세요", "폴더 선택",
        "사전 검사 실패: {error}", "가져오기 실패: {error}", "고정된 리졸버 소스를 찾을 수 없음: {path}", "이 라이브 URL은 아직 지원되지 않습니다",
        "고정된 Taobao 리졸버는 로그인 세션을 요구합니다. Reco Box는 계정이나 Cookie를 가져오거나 제한을 우회하지 않으며 공개 익명 인터페이스 구현 후 활성화할 수 있습니다.",
        "이 TwitCasting 방은 로그인이 필요하여 익명 모드를 사용할 수 없습니다", "이 TwitCasting 페이지는 익명으로 읽을 수 없습니다. 로그인 또는 접근 제한이 있을 수 있습니다", "TwitCasting에서 녹화 가능한 공개 URL을 반환하지 않았습니다",
        "FFmpeg를 찾을 수 없습니다. 개발 빌드에서는 RECO_BOX_FFMPEG를 설정하세요", "남은 공간이 {minimum_free_gb:g}GB 미만이어서 녹화를 시작하지 않았습니다", "사용 가능한 라이브 경로를 찾을 수 없습니다", "ffprobe를 찾을 수 없습니다",
        "녹화 폴더에 미디어 파일이 없습니다", "라이브 미리보기", "아직 스트림을 받지 못했습니다. 먼저 ‘지금 확인 및 녹화’를 누르세요", "ffprobe 검증 실패", "ffprobe가 잘못된 JSON을 반환했습니다",
        "인식 가능한 오디오 또는 비디오 스트림이 없습니다", "먼저 녹화 저장 폴더를 설정하세요", "출력 형식은 단순 확장자여야 합니다",
    ],
}


def main() -> None:
    for code, values in TRANSLATIONS.items():
        if len(values) != len(SOURCES):
            raise RuntimeError(f"{code}: expected {len(SOURCES)} translations, got {len(values)}")
        path = CATALOG_DIR / f"reco_box_{code}.ts"
        tree = ET.parse(path)
        for context in tree.findall("context"):
            name = context.find("name")
            if name is not None and not (name.text or "").strip():
                name.text = "RecoBox"
        mapping = dict(zip(SOURCES, values, strict=True))
        found: set[str] = set()
        for context in tree.findall("context"):
            if context.findtext("name", "") != "RecoBox":
                continue
            for message in context.findall("message"):
                source = message.findtext("source", "")
                if source not in mapping:
                    continue
                found.add(source)
                translation = message.find("translation")
                if translation is None:
                    translation = ET.SubElement(message, "translation")
                translation.attrib.pop("type", None)
                translation.text = mapping[source]
        if found != set(SOURCES):
            raise RuntimeError(f"{code}: missing Python messages: {set(SOURCES) - found}")
        ET.indent(tree, space="    ")
        tree.write(path, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
