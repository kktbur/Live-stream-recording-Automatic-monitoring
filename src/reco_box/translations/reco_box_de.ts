<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="de" sourcelanguage="zh_CN">
    <context>
        <name>RecoBox</name>
        <message>
            <location filename="../network.py" line="16" />
            <source>代理地址必须是主机:端口或 HTTP/HTTPS 地址</source>
            <translation>Der Proxy muss Host:Port oder eine HTTP/HTTPS-URL sein</translation>
        </message>
        <message>
            <location filename="../network.py" line="18" />
            <source>代理地址不能包含账号密码</source>
            <translation>Der Proxy darf keinen Benutzernamen oder Passwort enthalten</translation>
        </message>
        <message>
            <location filename="../network.py" line="20" />
            <source>代理地址不能包含路径、查询参数或片段</source>
            <translation>Der Proxy darf keinen Pfad, keine Abfrage und kein Fragment enthalten</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="200" />
            <source>仍有直播间正在录制或转换，请先全部暂停并等待收尾完成</source>
            <translation>Ein Raum zeichnet noch auf oder konvertiert. Alles pausieren und Abschluss abwarten</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="274" />
            <source>找不到直播间</source>
            <translation>Raum nicht gefunden</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="277" />
            <source>直播间地址不能为空</source>
            <translation>Die Raum-URL darf nicht leer sein</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="280" />
            <source>该直播间地址已经存在</source>
            <translation>Diese Raum-URL existiert bereits</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="283" />
            <source>保存目录不能为空</source>
            <translation>Der Speicherordner darf nicht leer sein</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="291" />
            <source>检测间隔必须是正整数</source>
            <translation>Das Prüfintervall muss eine positive Ganzzahl sein</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="293" />
            <source>检测间隔不能低于 30 秒</source>
            <translation>Das Prüfintervall darf nicht unter 30 Sekunden liegen</translation>
        </message>
        <message>
            <location filename="../ffmpeg.py" line="28" />
            <location filename="../room_model.py" line="299" />
            <location filename="../room_model.py" line="301" />
            <location filename="../view_models.py" line="200" />
            <source>分段分钟数必须是正整数</source>
            <translation>Segmentminuten müssen eine positive Ganzzahl sein</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="305" />
            <source>不支持该输出格式</source>
            <translation>Ausgabeformat nicht unterstützt</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="187" />
            <source>默认录制目录不能为空</source>
            <translation>Der Standard-Aufnahmeordner darf nicht leer sein</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="198" />
            <source>轮询间隔不能低于 30 秒</source>
            <translation>Das Abfrageintervall darf nicht unter 30 Sekunden liegen</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="202" />
            <source>磁盘保护阈值必须是 1 至 1024 GB</source>
            <translation>Der Festplattengrenzwert muss 1–1024 GB betragen</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="243" />
            <source>设置保存后校验失败，请重试</source>
            <translation>Gespeicherte Einstellungen konnten nicht geprüft werden. Erneut versuchen</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="288" />
            <source>选择文件夹</source>
            <translation>Ordner auswählen</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="356" />
            <source>预检失败：{error}</source>
            <translation>Vorprüfung fehlgeschlagen: {error}</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="372" />
            <source>导入失败：{error}</source>
            <translation>Import fehlgeschlagen: {error}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="94" />
            <source>找不到已锁定的解析源码：{path}</source>
            <translation>Fixierter Resolver-Quellcode nicht gefunden: {path}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="133" />
            <source>暂不支持该直播间链接</source>
            <translation>Diese Livestream-URL wird noch nicht unterstützt</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="165" />
            <source>当前锁定版淘宝解析器要求登录会话，Reco Box 不导入账号或 Cookie，因此暂不尝试绕过；后续需要实现匿名公开接口后才能启用。</source>
            <translation>Der fixierte Taobao-Resolver benötigt eine angemeldete Sitzung. Reco Box importiert keine Konten oder Cookies und umgeht die Sperre nicht; zuerst ist eine öffentliche anonyme Schnittstelle nötig.</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="212" />
            <source>该 TwitCasting 直播间要求登录，匿名模式不可用</source>
            <translation>Dieser TwitCasting-Raum erfordert eine Anmeldung; anonymer Modus ist nicht verfügbar</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="219" />
            <source>该 TwitCasting 页面无法匿名读取，可能需要登录或已受访问限制</source>
            <translation>Diese TwitCasting-Seite ist anonym nicht lesbar; Anmeldung oder Zugriffsbeschränkung möglich</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="243" />
            <source>TwitCasting 未返回可录制的公开播放地址</source>
            <translation>TwitCasting lieferte keine öffentlich aufnehmbare URL</translation>
        </message>
        <message>
            <location filename="../recording.py" line="206" />
            <source>未找到 FFmpeg；开发版需要设置 RECO_BOX_FFMPEG</source>
            <translation>FFmpeg nicht gefunden; Entwicklungsbuilds müssen RECO_BOX_FFMPEG setzen</translation>
        </message>
        <message>
            <location filename="../recording.py" line="236" />
            <source>磁盘剩余空间低于 {minimum_free_gb:g} GB，已阻止开始录制</source>
            <translation>Freier Speicher unter {minimum_free_gb:g} GB; Aufnahme wurde blockiert</translation>
        </message>
        <message>
            <location filename="../recording.py" line="330" />
            <source>未找到可用直播线路</source>
            <translation>Keine nutzbare Livestream-Route gefunden</translation>
        </message>
        <message>
            <location filename="../recording.py" line="487" />
            <source>未找到 ffprobe</source>
            <translation>ffprobe nicht gefunden</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="95" />
            <location filename="../recording.py" line="492" />
            <source>录制目录中没有媒体文件</source>
            <translation>Keine Mediendateien im Aufnahmeordner</translation>
        </message>
        <message>
            <location filename="../preview.py" line="16" />
            <location filename="../preview.py" line="36" />
            <location filename="../preview.py" line="41" />
            <source>直播预览</source>
            <translation>Livestream-Vorschau</translation>
        </message>
        <message>
            <location filename="../preview.py" line="37" />
            <source>尚未取得直播流，请先点击“立即检查并录制”</source>
            <translation>Noch kein Stream verfügbar. Zuerst „Jetzt prüfen und aufnehmen“ wählen</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="85" />
            <source>ffprobe 验证失败</source>
            <translation>ffprobe-Prüfung fehlgeschlagen</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="89" />
            <source>ffprobe 返回了无效 JSON</source>
            <translation>ffprobe lieferte ungültiges JSON</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="112" />
            <source>文件中没有可识别的音视频流</source>
            <translation>Kein erkennbarer Audio- oder Videostream</translation>
        </message>
        <message>
            <location filename="../ffmpeg.py" line="26" />
            <source>必须先设置录制保存目录</source>
            <translation>Zuerst den Aufnahmeordner festlegen</translation>
        </message>
        <message>
            <location filename="../output_paths.py" line="46" />
            <location filename="../output_paths.py" line="53" />
            <source>输出格式必须是简单扩展名</source>
            <translation>Das Ausgabeformat muss eine einfache Erweiterung sein</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="418" />
            <source>Resolver 调度限制</source>
            <translation>Resolver-Zeitplanlimits</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="421" />
            <source>最大并发</source>
            <translation>Maximale Parallelität</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="422" />
            <source>单平台并发</source>
            <translation>Parallelität pro Plattform</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="423" />
            <source>平台冷却（秒）</source>
            <translation>Plattform-Abklingzeit (Sekunden)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="425" />
            <source>用于分散解析请求；修改后立即影响新的监控请求。</source>
            <translation>Dient zur Verteilung von Resolver-Anfragen; Änderungen wirken sofort auf neue Überwachungsanfragen.</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="196" />
            <source>轮询、分段和解析限制参数必须是整数</source>
            <translation>Abfrage-, Segmentierungs- und Resolver-Limitparameter müssen Ganzzahlen sein</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="204" />
            <source>Resolver 最大并发必须是 1 至 32</source>
            <translation>Die maximale Resolver-Parallelität muss zwischen 1 und 32 liegen</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="206" />
            <source>单平台并发必须是 1 至 16</source>
            <translation>Die Parallelität pro Plattform muss zwischen 1 und 16 liegen</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="208" />
            <source>平台冷却必须是 0 至 3600 秒</source>
            <translation>Die Plattform-Abklingzeit muss zwischen 0 und 3600 Sekunden liegen</translation>
        </message>
    </context>
    <context>
        <name>Main</name>
        <message>
            <location filename="../ui/Main.qml" line="35" />
            <source>全部状态</source>
            <translation>Alle Status</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="36" />
            <location filename="../ui/Main.qml" line="241" />
            <location filename="../ui/Main.qml" line="448" />
            <source>录制中</source>
            <translation>Aufnahme</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="37" />
            <location filename="../ui/Main.qml" line="241" />
            <source>监控中</source>
            <translation>Überwachung</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="38" />
            <location filename="../ui/Main.qml" line="241" />
            <source>未开始</source>
            <translation>Nicht gestartet</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="41" />
            <source>默认排序</source>
            <translation>Standardsortierung</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="42" />
            <source>名称正序</source>
            <translation>Namensfolge</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="43" />
            <source>名称倒序</source>
            <translation>Name in umgekehrter Reihenfolge</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="46" />
            <source>原画</source>
            <translation>Originalgemälde</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="47" />
            <source>蓝光</source>
            <translation>Blu-ray</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="48" />
            <source>超清</source>
            <translation>Ultra HD</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="49" />
            <source>高清</source>
            <translation>HD</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="50" />
            <source>标清</source>
            <translation>SD</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="51" />
            <source>流畅</source>
            <translation>Glatt</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="54" />
            <source>线路1</source>
            <translation>Zeile 1</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="55" />
            <source>线路2</source>
            <translation>Zeile 2</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="56" />
            <source>线路3</source>
            <translation>Zeile 3</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="57" />
            <source>线路4</source>
            <translation>Zeile 4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="58" />
            <source>线路5</source>
            <translation>Zeile 5</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="163" />
            <location filename="../ui/Main.qml" line="280" />
            <location filename="../ui/Main.qml" line="287" />
            <source>添加直播间</source>
            <translation>Live-Übertragungsraum hinzufügen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="166" />
            <source>一键全部开始录屏 / 监控</source>
            <translation>Starten Sie die Aufzeichnung/Überwachung mit einem Klick</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="167" />
            <source>已启用全部直播间并立即检查</source>
            <translation>Alle Live-Übertragungsräume wurden jetzt aktiviert und überprüft</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="170" />
            <source>一键全部暂停录屏 / 监控</source>
            <translation>Unterbrechen Sie die gesamte Bildschirmaufzeichnung/-überwachung mit einem Klick</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="171" />
            <source>已请求全部暂停；正在录制的文件会先安全收尾</source>
            <translation>Alle Pausen wurden angefordert; Die aufgezeichneten Dateien werden zunächst sicher beendet</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="173" />
            <location filename="../ui/Main.qml" line="370" />
            <source>删除全部直播间</source>
            <translation>Alle Live-Übertragungsräume löschen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="175" />
            <source>全局设置、录制历史和运行日志</source>
            <translation>Globale Einstellungen, Aufzeichnungsverlauf und laufende Protokolle</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="181" />
            <source>搜索主播、标题或链接…</source>
            <translation>Nach Anker, Titel oder Link suchen…</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="189" />
            <source>直播间</source>
            <translation>Live-Übertragungsraum</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="241" />
            <source>转 MP4</source>
            <translation>auf MP4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="241" />
            <source>检查中</source>
            <translation>Prüfung</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source>暂无直播间标题</source>
            <translation>Noch kein Live-Übertragungsraumtitel</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>分段：</source>
            <translation>Segmentierung:</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>每 </source>
            <translation>Alle</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source> 分钟</source>
            <translation>Minuten</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>关闭</source>
            <translation>Schließen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source> · 完成后转 MP4</source>
            <translation>· Nach Abschluss in MP4 konvertieren</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="250" />
            <source>检测间隔 </source>
            <translation>Erkennungsintervall</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="250" />
            <source> 秒</source>
            <translation>Sekunden</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="254" />
            <source>错误：</source>
            <translation>Fehler:</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>停止并暂停</source>
            <translation>Stoppen und innehalten</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>暂停监控</source>
            <translation>Überwachung pausieren</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>开始监控</source>
            <translation>Überwachung starten</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="264" />
            <source>检查并录制</source>
            <translation>Prüfen und aufzeichnen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="268" />
            <source>预览</source>
            <translation>Vorschau</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="269" />
            <source>编辑</source>
            <translation>Bearbeiten</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="271" />
            <source>删除</source>
            <translation>Löschen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>还没有直播间</source>
            <translation>Es gibt noch keinen Live-Übertragungsraum</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>没有符合当前筛选条件的直播间</source>
            <translation>Es gibt keine Live-Übertragungsräume, die die aktuellen Filterbedingungen erfüllen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="279" />
            <source>添加公开直播间地址后，Reco Box 会自动开始监控</source>
            <translation>Nachdem die Adresse des öffentlichen Live-Übertragungsraums hinzugefügt wurde, beginnt Reco Box automatisch mit der Überwachung</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="279" />
            <source>调整状态筛选或搜索关键词后重试</source>
            <translation>Passen Sie den Statusfilter an oder suchen Sie nach Schlüsselwörtern und versuchen Sie es erneut</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="290" />
            <source>直播间添加成功</source>
            <translation>Live-Übertragungsraum erfolgreich hinzugefügt</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="293" />
            <location filename="../ui/Main.qml" line="322" />
            <source>直播间地址</source>
            <translation>Adresse des Live-Übertragungsraums</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="294" />
            <source>粘贴公开直播间链接</source>
            <translation>Fügen Sie den Link zum öffentlichen Live-Übertragungsraum ein</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="295" />
            <source>主播名字（可稍后自动识别）</source>
            <translation>Ankername (kann später automatisch erkannt werden)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="296" />
            <source>待识别主播</source>
            <translation>Anker muss identifiziert werden</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="297" />
            <location filename="../ui/Main.qml" line="335" />
            <source>保存目录</source>
            <translation>Verzeichnis speichern</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="298" />
            <location filename="../ui/Main.qml" line="336" />
            <location filename="../ui/Main.qml" line="410" />
            <source>选择目录</source>
            <translation>Verzeichnis auswählen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="299" />
            <source>格式、画质、检测间隔和分段使用已保存的全局默认设置。</source>
            <translation>Format, Qualität, Erkennungsintervall und Segmentierung verwenden gespeicherte globale Standardeinstellungen.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="306" />
            <source>编辑直播间</source>
            <translation>Live-Übertragungsraum bearbeiten</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="321" />
            <source>基础编辑</source>
            <translation>Grundlegende Bearbeitung</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="324" />
            <source>主播名字</source>
            <translation>Ankername</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="326" />
            <source>直播间标题</source>
            <translation>Titel des Live-Übertragungsraums</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="327" />
            <source>可以留空，开播后自动更新</source>
            <translation>kann leer gelassen werden und wird nach der Ausstrahlung automatisch aktualisiert.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="329" />
            <source>录制设置</source>
            <translation>Aufnahmeeinstellungen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="332" />
            <source>文件名（不分段时使用）</source>
            <translation>Dateiname (wird verwendet, wenn nicht segmentiert)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="332" />
            <source>留空则使用 1</source>
            <translation>Lassen Sie das Feld leer, um 1 zu verwenden</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="333" />
            <location filename="../ui/Main.qml" line="415" />
            <source>检测间隔（秒）</source>
            <translation>Erkennungsintervall (Sekunden)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="337" />
            <source>代理地址（可选）</source>
            <translation>Proxy-Adresse (optional)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="338" />
            <source>例如 127.0.0.1:7890；留空表示直连</source>
            <translation>Zum Beispiel 127.0.0.1:7890; Lassen Sie das Feld leer, um eine direkte Verbindung anzuzeigen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="341" />
            <source>录制清晰度</source>
            <translation>Klarheit der Aufnahme</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="342" />
            <source>录制路线</source>
            <translation>Aufzeichnungsroute</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="346" />
            <source>输出格式</source>
            <translation>Ausgabeformat</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="347" />
            <source>分段时长（分钟）</source>
            <translation>Segmentdauer (Minuten)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="347" />
            <source>启用</source>
            <translation>Aktivieren</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="349" />
            <source>分段文件固定按 1、2、3… 排列，最后一段按实际剩余时长保存。</source>
            <translation>Segmentierte Dateien werden fest in 1, 2, 3... angeordnet und das letzte Segment wird entsprechend der tatsächlich verbleibenden Dauer gespeichert.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="350" />
            <source>录制完成后转为 MP4（成功后删除 TS）</source>
            <translation>Nach Abschluss der Aufnahme in MP4 konvertieren (TS nach Erfolg löschen)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="351" />
            <source>纯音频模式</source>
            <translation>Nur-Audio-Modus</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="352" />
            <source>录制弹幕（仅在平台适配完成后生效）</source>
            <translation>Rekordsperren (wird erst wirksam, nachdem die Plattformanpassung abgeschlossen ist)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="359" />
            <location filename="../ui/Main.qml" line="378" />
            <source>取消</source>
            <translation>Abbrechen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="361" />
            <source>保存</source>
            <translation>Speichern</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="362" />
            <source>直播间设置已保存</source>
            <translation>Die Einstellungen des Live-Übertragungsraums wurden gespeichert</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="376" />
            <source>确定从 Reco Box 中删除全部直播间吗？
录制文件和历史记录不会删除。</source>
            <translation>Sind Sie sicher, dass Sie alle Live-Übertragungsräume aus Reco Box löschen möchten?
Aufnahmedateien und Verlauf werden nicht gelöscht.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="378" />
            <source>确认全部删除</source>
            <translation>Bestätigen Sie das Löschen aller</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="378" />
            <source>已删除全部直播间</source>
            <translation>Alle Live-Übertragungsräume wurden gelöscht</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="384" />
            <location filename="../ui/Main.qml" line="389" />
            <source>全局设置</source>
            <translation>Globale Einstellungen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="389" />
            <source>录制历史</source>
            <translation>Aufzeichnungsverlauf</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="389" />
            <source>运行日志</source>
            <translation>Protokoll ausführen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="396" />
            <source>新直播间默认设置</source>
            <translation>Standardeinstellungen für neuen Live-Übertragungsraum</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="396" />
            <source>导入旧配置</source>
            <translation>Alte Konfiguration importieren</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="397" />
            <source>界面语言</source>
            <translation>Schnittstellensprache</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="404" />
            <source>界面语言已切换</source>
            <translation>Die Sprache der Benutzeroberfläche wurde geändert</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="408" />
            <source>只影响以后新增或导入的直播间；已有直播间在卡片中单独编辑。</source>
            <translation>betrifft nur Live-Übertragungsräume, die in Zukunft hinzugefügt oder importiert werden; Vorhandene Live-Übertragungsräume können separat in der Karte bearbeitet werden.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="409" />
            <source>默认录制目录</source>
            <translation>Standardaufnahmeverzeichnis</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="413" />
            <source>默认格式</source>
            <translation>Standardformat</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="414" />
            <source>默认画质</source>
            <translation>Standardqualität</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="416" />
            <source>磁盘保护（GB）</source>
            <translation>Festplattenschutz (GB)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="426" />
            <source>默认代理地址（可选）</source>
            <translation>Standard-Proxy-Adresse (optional)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="427" />
            <source>新直播间继承；留空表示直连</source>
            <translation>Neuer Live-Übertragungsraum übernimmt; Lassen Sie das Feld leer, um eine direkte Verbindung anzuzeigen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="428" />
            <source>新直播间默认启用分段</source>
            <translation>Neue Live-Übertragungsräume ermöglichen standardmäßig die Segmentierung</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="428" />
            <location filename="../ui/Main.qml" line="429" />
            <source>设置已更改，请点击保存设置</source>
            <translation>Einstellungen wurden geändert. Klicken Sie bitte, um die Einstellungen zu speichern</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="429" />
            <source>每段</source>
            <translation>Jeder Absatz</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="429" />
            <source>分钟，最后一段按实际时长保存</source>
            <translation>Minuten, das letzte Segment wird entsprechend der tatsächlichen Dauer gespeichert</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="432" />
            <source>启动后自动监控 · 关闭窗口最小化到托盘 · 不随 Windows 开机启动</source>
            <translation>Automatische Überwachung nach dem Start · Schließen Sie das Fenster und minimieren Sie es in der Taskleiste. · Starten Sie nicht mit dem Windows-Start</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>保存设置</source>
            <translation>Einstellungen speichern</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>已保存并确认：以后新增直播间默认每 </source>
            <translation>Gespeichert und bestätigt: die Standardeinstellung für jeden neuen Live-Übertragungsraum in der Zukunft</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source> 分钟分段</source>
            <translation>Minutensegmente</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>已保存并确认：以后新增直播间默认不分段</source>
            <translation>Gespeichert und bestätigt: Neue Live-Übertragungsräume werden in Zukunft nicht standardmäßig segmentiert.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="436" />
            <source>已保存并确认</source>
            <translation>Gespeichert und bestätigt</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="436" />
            <source>设置已更改</source>
            <translation>Einstellungen geändert</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>可播放</source>
            <translation>Kann gespielt werden</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>转 MP4 中</source>
            <translation>In MP4 konvertieren</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>已完成</source>
            <translation>Abgeschlossen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>失败</source>
            <translation>ist fehlgeschlagen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="449" />
            <location filename="../ui/Main.qml" line="514" />
            <source>播放</source>
            <translation>Spielen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="450" />
            <source>目录</source>
            <translation>Verzeichnis</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="455" />
            <source>这里只显示脱敏后的状态和错误，不保存完整临时播放地址。</source>
            <translation>Hier werden nur der Status und Fehler nach der Desensibilisierung angezeigt und die vollständige temporäre Wiedergabeadresse wird nicht gespeichert.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="480" />
            <source>直播流播放失败</source>
            <translation>Live-Stream-Wiedergabe fehlgeschlagen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="484" />
            <source>直播流格式无效或播放器无法解码</source>
            <translation>Das Live-Stream-Format ist ungültig oder der Player kann es nicht dekodieren</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="508" />
            <source>正在准备预览……</source>
            <translation>Vorbereitung für die Vorschau...</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="509" />
            <source>正在连接直播流并等待首帧……</source>
            <translation>Verbindung zum Live-Stream herstellen und auf den ersten Frame warten ...</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="514" />
            <source>暂停</source>
            <translation>Pause</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="514" />
            <source>静音</source>
            <translation>Stumm</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="520" />
            <source>导入 DouyinLiveRecorder 旧配置</source>
            <translation>Alte DouyinLiveRecorder-Konfiguration importieren</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="524" />
            <source>选择旧程序根目录或其中的 config 文件夹。</source>
            <translation>Wählen Sie das alte Programmstammverzeichnis oder den Konfigurationsordner darin aus.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="525" />
            <source>选择文件夹</source>
            <translation>Ordner auswählen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>1. 预检</source>
            <translation>1. Vorab prüfen</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>2. 确认导入</source>
            <translation>2. Bestätigen Sie den Import</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>可导入直播间</source>
            <translation>kann in den Live-Übertragungsraum importiert werden</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="528" />
            <source>不会修改旧配置；Cookie、令牌、账号、密码和推送凭据不会导入。</source>
            <translation>Alte Konfigurationen werden nicht geändert; Cookies, Token, Konten, Passwörter und Push-Anmeldeinformationen werden nicht importiert.</translation>
        </message>
    </context>
</TS>