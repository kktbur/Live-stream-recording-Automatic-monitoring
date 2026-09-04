<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="ru" sourcelanguage="zh_CN">
    <context>
        <name>RecoBox</name>
        <message>
            <location filename="../network.py" line="16" />
            <source>代理地址必须是主机:端口或 HTTP/HTTPS 地址</source>
            <translation>Прокси должен иметь вид хост:порт или URL HTTP/HTTPS</translation>
        </message>
        <message>
            <location filename="../network.py" line="18" />
            <source>代理地址不能包含账号密码</source>
            <translation>Прокси не должен содержать логин или пароль</translation>
        </message>
        <message>
            <location filename="../network.py" line="20" />
            <source>代理地址不能包含路径、查询参数或片段</source>
            <translation>Прокси не должен содержать путь, запрос или фрагмент</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="200" />
            <source>仍有直播间正在录制或转换，请先全部暂停并等待收尾完成</source>
            <translation>Одна из комнат ещё записывается или конвертируется. Приостановите всё и дождитесь завершения</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="274" />
            <source>找不到直播间</source>
            <translation>Комната не найдена</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="277" />
            <source>直播间地址不能为空</source>
            <translation>URL комнаты не может быть пустым</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="280" />
            <source>该直播间地址已经存在</source>
            <translation>Такой URL уже существует</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="283" />
            <source>保存目录不能为空</source>
            <translation>Папка сохранения не может быть пустой</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="291" />
            <source>检测间隔必须是正整数</source>
            <translation>Интервал проверки должен быть положительным целым</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="293" />
            <source>检测间隔不能低于 30 秒</source>
            <translation>Интервал не может быть меньше 30 секунд</translation>
        </message>
        <message>
            <location filename="../ffmpeg.py" line="28" />
            <location filename="../room_model.py" line="299" />
            <location filename="../room_model.py" line="301" />
            <location filename="../view_models.py" line="200" />
            <source>分段分钟数必须是正整数</source>
            <translation>Минуты сегмента должны быть положительным целым</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="305" />
            <source>不支持该输出格式</source>
            <translation>Формат вывода не поддерживается</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="187" />
            <source>默认录制目录不能为空</source>
            <translation>Папка записи по умолчанию не может быть пустой</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="198" />
            <source>轮询间隔不能低于 30 秒</source>
            <translation>Опрос не может быть реже 30 секунд</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="202" />
            <source>磁盘保护阈值必须是 1 至 1024 GB</source>
            <translation>Порог диска должен быть 1–1024 ГБ</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="243" />
            <source>设置保存后校验失败，请重试</source>
            <translation>Проверка сохранённых настроек не удалась. Повторите</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="288" />
            <source>选择文件夹</source>
            <translation>Выбрать папку</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="356" />
            <source>预检失败：{error}</source>
            <translation>Предварительная проверка не удалась: {error}</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="372" />
            <source>导入失败：{error}</source>
            <translation>Импорт не удался: {error}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="94" />
            <source>找不到已锁定的解析源码：{path}</source>
            <translation>Исходный код закреплённого анализатора не найден: {path}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="133" />
            <source>暂不支持该直播间链接</source>
            <translation>Этот URL трансляции пока не поддерживается</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="165" />
            <source>当前锁定版淘宝解析器要求登录会话，Reco Box 不导入账号或 Cookie，因此暂不尝试绕过；后续需要实现匿名公开接口后才能启用。</source>
            <translation>Закреплённый анализатор Taobao требует авторизованную сессию. Reco Box не импортирует учётные записи или cookies и не обходит ограничение; нужен публичный анонимный интерфейс.</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="212" />
            <source>该 TwitCasting 直播间要求登录，匿名模式不可用</source>
            <translation>Эта комната TwitCasting требует входа; анонимный режим недоступен</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="219" />
            <source>该 TwitCasting 页面无法匿名读取，可能需要登录或已受访问限制</source>
            <translation>Страница TwitCasting недоступна анонимно; возможен вход или ограничение доступа</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="243" />
            <source>TwitCasting 未返回可录制的公开播放地址</source>
            <translation>TwitCasting не вернул публичный URL для записи</translation>
        </message>
        <message>
            <location filename="../recording.py" line="206" />
            <source>未找到 FFmpeg；开发版需要设置 RECO_BOX_FFMPEG</source>
            <translation>FFmpeg не найден; в сборке разработчика задайте RECO_BOX_FFMPEG</translation>
        </message>
        <message>
            <location filename="../recording.py" line="236" />
            <source>磁盘剩余空间低于 {minimum_free_gb:g} GB，已阻止开始录制</source>
            <translation>Свободно меньше {minimum_free_gb:g} ГБ; запись заблокирована</translation>
        </message>
        <message>
            <location filename="../recording.py" line="330" />
            <source>未找到可用直播线路</source>
            <translation>Не найден доступный маршрут трансляции</translation>
        </message>
        <message>
            <location filename="../recording.py" line="487" />
            <source>未找到 ffprobe</source>
            <translation>ffprobe не найден</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="95" />
            <location filename="../recording.py" line="492" />
            <source>录制目录中没有媒体文件</source>
            <translation>В папке записи нет медиафайлов</translation>
        </message>
        <message>
            <location filename="../preview.py" line="16" />
            <location filename="../preview.py" line="36" />
            <location filename="../preview.py" line="41" />
            <source>直播预览</source>
            <translation>Предпросмотр трансляции</translation>
        </message>
        <message>
            <location filename="../preview.py" line="37" />
            <source>尚未取得直播流，请先点击“立即检查并录制”</source>
            <translation>Поток ещё не получен. Сначала нажмите «Проверить и записать»</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="85" />
            <source>ffprobe 验证失败</source>
            <translation>Проверка ffprobe не удалась</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="89" />
            <source>ffprobe 返回了无效 JSON</source>
            <translation>ffprobe вернул недопустимый JSON</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="112" />
            <source>文件中没有可识别的音视频流</source>
            <translation>Не найден распознаваемый аудио- или видеопоток</translation>
        </message>
        <message>
            <location filename="../ffmpeg.py" line="26" />
            <source>必须先设置录制保存目录</source>
            <translation>Сначала задайте папку записи</translation>
        </message>
        <message>
            <location filename="../output_paths.py" line="46" />
            <location filename="../output_paths.py" line="53" />
            <source>输出格式必须是简单扩展名</source>
            <translation>Формат вывода должен быть простым расширением</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="418" />
            <source>Resolver 调度限制</source>
            <translation>Ограничения планировщика Resolver</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="421" />
            <source>最大并发</source>
            <translation>Максимальная параллельность</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="422" />
            <source>单平台并发</source>
            <translation>Параллельность для платформы</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="423" />
            <source>平台冷却（秒）</source>
            <translation>Задержка платформы (секунды)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="425" />
            <source>用于分散解析请求；修改后立即影响新的监控请求。</source>
            <translation>Используется для распределения запросов Resolver; изменения сразу применяются к новым запросам мониторинга.</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="196" />
            <source>轮询、分段和解析限制参数必须是整数</source>
            <translation>Параметры проверки, сегментации и ограничений Resolver должны быть целыми числами</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="204" />
            <source>Resolver 最大并发必须是 1 至 32</source>
            <translation>Максимальная параллельность Resolver должна быть от 1 до 32</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="206" />
            <source>单平台并发必须是 1 至 16</source>
            <translation>Параллельность для платформы должна быть от 1 до 16</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="208" />
            <source>平台冷却必须是 0 至 3600 秒</source>
            <translation>Задержка платформы должна быть от 0 до 3600 секунд</translation>
        </message>
    </context>
    <context>
        <name>Main</name>
        <message>
            <location filename="../ui/Main.qml" line="35" />
            <source>全部状态</source>
            <translation>Все статусы</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="36" />
            <location filename="../ui/Main.qml" line="241" />
            <location filename="../ui/Main.qml" line="448" />
            <source>录制中</source>
            <translation>Запись</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="37" />
            <location filename="../ui/Main.qml" line="241" />
            <source>监控中</source>
            <translation>Мониторинг</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="38" />
            <location filename="../ui/Main.qml" line="241" />
            <source>未开始</source>
            <translation>Не запущено</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="41" />
            <source>默认排序</source>
            <translation>Сортировка по умолчанию</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="42" />
            <source>名称正序</source>
            <translation>Последовательность имен</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="43" />
            <source>名称倒序</source>
            <translation>Имя в обратном порядке</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="46" />
            <source>原画</source>
            <translation>Оригинальная картина</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="47" />
            <source>蓝光</source>
            <translation>Blu-ray</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="48" />
            <source>超清</source>
            <translation>Ультра HD</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="49" />
            <source>高清</source>
            <translation>HD</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="50" />
            <source>标清</source>
            <translation>СД</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="51" />
            <source>流畅</source>
            <translation>Гладкий</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="54" />
            <source>线路1</source>
            <translation>Строка 1</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="55" />
            <source>线路2</source>
            <translation>Строка 2</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="56" />
            <source>线路3</source>
            <translation>Строка 3</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="57" />
            <source>线路4</source>
            <translation>Строка 4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="58" />
            <source>线路5</source>
            <translation>Строка 5</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="163" />
            <location filename="../ui/Main.qml" line="280" />
            <location filename="../ui/Main.qml" line="287" />
            <source>添加直播间</source>
            <translation>Добавить комнату прямой трансляции</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="166" />
            <source>一键全部开始录屏 / 监控</source>
            <translation>Начните запись/мониторинг всего одним щелчком мыши</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="167" />
            <source>已启用全部直播间并立即检查</source>
            <translation>Все комнаты прямых трансляций включены и проверены.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="170" />
            <source>一键全部暂停录屏 / 监控</source>
            <translation>Приостановите запись/мониторинг экрана одним щелчком мыши.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="171" />
            <source>已请求全部暂停；正在录制的文件会先安全收尾</source>
            <translation>Все паузы запрошены; записываемые файлы сначала будут благополучно завершены</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="173" />
            <location filename="../ui/Main.qml" line="370" />
            <source>删除全部直播间</source>
            <translation>Удалить все комнаты прямых трансляций</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="175" />
            <source>全局设置、录制历史和运行日志</source>
            <translation>Глобальные настройки, история записи и журналы ведения</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="181" />
            <source>搜索主播、标题或链接…</source>
            <translation>Выполните поиск по якорю, заголовку или ссылке…</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="189" />
            <source>直播间</source>
            <translation>Комната прямой трансляции</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="241" />
            <source>转 MP4</source>
            <translation>в MP4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="241" />
            <source>检查中</source>
            <translation>Проверка</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source>暂无直播间标题</source>
            <translation>Названия комнаты прямой трансляции пока нет</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>分段：</source>
            <translation>Сегментация:</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>每 </source>
            <translation>Каждый</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source> 分钟</source>
            <translation>минут</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>关闭</source>
            <translation>Закрыть</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source> · 完成后转 MP4</source>
            <translation>· Конвертировать в MP4 после завершения</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="250" />
            <source>检测间隔 </source>
            <translation>Интервал обнаружения</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="250" />
            <source> 秒</source>
            <translation>секунд</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="254" />
            <source>错误：</source>
            <translation>Ошибка:</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>停止并暂停</source>
            <translation>Стоп и пауза</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>暂停监控</source>
            <translation>Приостановить мониторинг</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>开始监控</source>
            <translation>Начать мониторинг</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="264" />
            <source>检查并录制</source>
            <translation>Проверьте и запишите</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="268" />
            <source>预览</source>
            <translation>Предварительный просмотр</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="269" />
            <source>编辑</source>
            <translation>Править</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="271" />
            <source>删除</source>
            <translation>Удалить</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>还没有直播间</source>
            <translation>Комнаты для прямых трансляций пока нет</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>没有符合当前筛选条件的直播间</source>
            <translation>Нет комнат прямых трансляций, соответствующих текущим условиям фильтра.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="279" />
            <source>添加公开直播间地址后，Reco Box 会自动开始监控</source>
            <translation>После добавления адреса комнаты публичной прямой трансляции Reco Box автоматически начнет мониторинг</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="279" />
            <source>调整状态筛选或搜索关键词后重试</source>
            <translation>Настройте фильтр статуса или выполните поиск по ключевым словам и повторите попытку.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="290" />
            <source>直播间添加成功</source>
            <translation>Комната прямой трансляции успешно добавлена</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="293" />
            <location filename="../ui/Main.qml" line="322" />
            <source>直播间地址</source>
            <translation>Адрес комнаты прямой трансляции</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="294" />
            <source>粘贴公开直播间链接</source>
            <translation>Вставьте ссылку на комнату общедоступной прямой трансляции</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="295" />
            <source>主播名字（可稍后自动识别）</source>
            <translation>Имя привязки (позже может быть распознано автоматически)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="296" />
            <source>待识别主播</source>
            <translation>Якорь, который необходимо идентифицировать</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="297" />
            <location filename="../ui/Main.qml" line="335" />
            <source>保存目录</source>
            <translation>Сохранить каталог</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="298" />
            <location filename="../ui/Main.qml" line="336" />
            <location filename="../ui/Main.qml" line="410" />
            <source>选择目录</source>
            <translation>Выберите каталог</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="299" />
            <source>格式、画质、检测间隔和分段使用已保存的全局默认设置。</source>
            <translation>Формат, качество, интервал обнаружения и сегментация используют сохраненные глобальные настройки по умолчанию.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="306" />
            <source>编辑直播间</source>
            <translation>Редактировать комнату прямой трансляции</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="321" />
            <source>基础编辑</source>
            <translation>Базовое редактирование</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="324" />
            <source>主播名字</source>
            <translation>Имя привязки</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="326" />
            <source>直播间标题</source>
            <translation>Название комнаты прямой трансляции</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="327" />
            <source>可以留空，开播后自动更新</source>
            <translation>можно оставить пустым, оно будет автоматически обновляться после трансляции.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="329" />
            <source>录制设置</source>
            <translation>Настройки записи</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="332" />
            <source>文件名（不分段时使用）</source>
            <translation>Имя файла (используется, если он не сегментирован)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="332" />
            <source>留空则使用 1</source>
            <translation>Оставьте поле пустым, чтобы использовать 1</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="333" />
            <location filename="../ui/Main.qml" line="415" />
            <source>检测间隔（秒）</source>
            <translation>Интервал обнаружения (секунды)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="337" />
            <source>代理地址（可选）</source>
            <translation>Адрес прокси (необязательно)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="338" />
            <source>例如 127.0.0.1:7890；留空表示直连</source>
            <translation>Например, 127.0.0.1:7890; оставьте пустым, чтобы указать прямое соединение</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="341" />
            <source>录制清晰度</source>
            <translation>Четкость записи</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="342" />
            <source>录制路线</source>
            <translation>Маршрут записи</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="346" />
            <source>输出格式</source>
            <translation>Формат вывода</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="347" />
            <source>分段时长（分钟）</source>
            <translation>Продолжительность сегмента (минуты)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="347" />
            <source>启用</source>
            <translation>Включить</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="349" />
            <source>分段文件固定按 1、2、3… 排列，最后一段按实际剩余时长保存。</source>
            <translation>Сегментированные файлы фиксированно располагаются по позициям 1, 2, 3..., а последний сегмент сохраняется в соответствии с фактической оставшейся продолжительностью.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="350" />
            <source>录制完成后转为 MP4（成功后删除 TS）</source>
            <translation>Конвертировать в MP4 после завершения записи (удалить TS после успеха)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="351" />
            <source>纯音频模式</source>
            <translation>Режим только аудио</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="352" />
            <source>录制弹幕（仅在平台适配完成后生效）</source>
            <translation>Записи (вступят в силу только после завершения адаптации платформы)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="359" />
            <location filename="../ui/Main.qml" line="378" />
            <source>取消</source>
            <translation>Отмена</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="361" />
            <source>保存</source>
            <translation>Сохранить</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="362" />
            <source>直播间设置已保存</source>
            <translation>Настройки комнаты прямой трансляции сохранены</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="376" />
            <source>确定从 Reco Box 中删除全部直播间吗？
录制文件和历史记录不会删除。</source>
            <translation>Вы уверены, что хотите удалить все комнаты прямых трансляций из Reco Box?
Файлы записи и история не будут удалены.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="378" />
            <source>确认全部删除</source>
            <translation>Подтвердите удаление всех</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="378" />
            <source>已删除全部直播间</source>
            <translation>Все комнаты прямых трансляций удалены</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="384" />
            <location filename="../ui/Main.qml" line="389" />
            <source>全局设置</source>
            <translation>Глобальные настройки</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="389" />
            <source>录制历史</source>
            <translation>История записи</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="389" />
            <source>运行日志</source>
            <translation>Журнал выполнения</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="396" />
            <source>新直播间默认设置</source>
            <translation>Настройки по умолчанию для новой комнаты прямой трансляции</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="396" />
            <source>导入旧配置</source>
            <translation>Импортировать старую конфигурацию</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="397" />
            <source>界面语言</source>
            <translation>Язык интерфейса</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="404" />
            <source>界面语言已切换</source>
            <translation>Язык интерфейса переключен</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="408" />
            <source>只影响以后新增或导入的直播间；已有直播间在卡片中单独编辑。</source>
            <translation>влияет только на комнаты прямых трансляций, которые будут добавлены или импортированы в будущем; существующие комнаты прямых трансляций можно редактировать отдельно в карточке.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="409" />
            <source>默认录制目录</source>
            <translation>Каталог для записи по умолчанию</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="413" />
            <source>默认格式</source>
            <translation>Формат по умолчанию</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="414" />
            <source>默认画质</source>
            <translation>Качество по умолчанию</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="416" />
            <source>磁盘保护（GB）</source>
            <translation>Защита диска (ГБ)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="426" />
            <source>默认代理地址（可选）</source>
            <translation>Адрес прокси-сервера по умолчанию (необязательно)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="427" />
            <source>新直播间继承；留空表示直连</source>
            <translation>Новая комната прямых трансляций унаследована; оставьте пустым, чтобы указать прямое соединение</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="428" />
            <source>新直播间默认启用分段</source>
            <translation>В новых комнатах прямых трансляций сегментация включена по умолчанию.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="428" />
            <location filename="../ui/Main.qml" line="429" />
            <source>设置已更改，请点击保存设置</source>
            <translation>Настройки изменены, нажмите, чтобы сохранить настройки.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="429" />
            <source>每段</source>
            <translation>Каждый абзац</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="429" />
            <source>分钟，最后一段按实际时长保存</source>
            <translation>минут, последний сегмент сохраняется в соответствии с фактической длительностью</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="432" />
            <source>启动后自动监控 · 关闭窗口最小化到托盘 · 不随 Windows 开机启动</source>
            <translation>Автоматически отслеживать после запуска · Закрыть окно и свернуть его в трей · Не запускать при запуске Windows</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>保存设置</source>
            <translation>Сохранить настройки</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>已保存并确认：以后新增直播间默认每 </source>
            <translation>Сохранено и подтверждено: значение по умолчанию для каждой новой комнаты прямой трансляции в будущем.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source> 分钟分段</source>
            <translation>минутные сегменты</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>已保存并确认：以后新增直播间默认不分段</source>
            <translation>Сохранено и подтверждено: новые комнаты прямых трансляций в будущем не будут сегментироваться по умолчанию.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="436" />
            <source>已保存并确认</source>
            <translation>Сохранено и подтверждено.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="436" />
            <source>设置已更改</source>
            <translation>Настройки изменены</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>可播放</source>
            <translation>Можно играть</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>转 MP4 中</source>
            <translation>Конвертировать в MP4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>已完成</source>
            <translation>Завершено</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>失败</source>
            <translation>не удалось</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="449" />
            <location filename="../ui/Main.qml" line="514" />
            <source>播放</source>
            <translation>Играть</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="450" />
            <source>目录</source>
            <translation>Каталог</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="455" />
            <source>这里只显示脱敏后的状态和错误，不保存完整临时播放地址。</source>
            <translation>Здесь отображаются только статус и ошибки после десенсибилизации, а полный временный адрес воспроизведения не сохраняется.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="480" />
            <source>直播流播放失败</source>
            <translation>Не удалось воспроизвести прямую трансляцию</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="484" />
            <source>直播流格式无效或播放器无法解码</source>
            <translation>Формат прямой трансляции недействителен или проигрыватель не может его декодировать.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="508" />
            <source>正在准备预览……</source>
            <translation>Подготовка к предварительной версии...</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="509" />
            <source>正在连接直播流并等待首帧……</source>
            <translation>Подключаюсь к прямой трансляции и ожидаю первого кадра...</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="514" />
            <source>暂停</source>
            <translation>Пауза</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="514" />
            <source>静音</source>
            <translation>Отключить звук</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="520" />
            <source>导入 DouyinLiveRecorder 旧配置</source>
            <translation>Импортировать старую конфигурацию DouyinLiveRecorder</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="524" />
            <source>选择旧程序根目录或其中的 config 文件夹。</source>
            <translation>Выберите корневой каталог старой программы или папку конфигурации в нем.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="525" />
            <source>选择文件夹</source>
            <translation>Выбрать папку</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>1. 预检</source>
            <translation>1. Предварительная проверка</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>2. 确认导入</source>
            <translation>2. Подтвердить импорт</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>可导入直播间</source>
            <translation>можно импортировать в комнату прямой трансляции</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="528" />
            <source>不会修改旧配置；Cookie、令牌、账号、密码和推送凭据不会导入。</source>
            <translation>Старые конфигурации не будут изменены; файлы cookie, токены, учетные записи, пароли и push-учетные данные не будут импортированы.</translation>
        </message>
    </context>
</TS>