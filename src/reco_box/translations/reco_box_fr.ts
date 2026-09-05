<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="fr" sourcelanguage="zh_CN">
    <context>
        <name>RecoBox</name>
        <message>
            <location filename="../network.py" line="16" />
            <source>代理地址必须是主机:端口或 HTTP/HTTPS 地址</source>
            <translation>Le proxy doit être hôte:port ou une URL HTTP/HTTPS</translation>
        </message>
        <message>
            <location filename="../network.py" line="18" />
            <source>代理地址不能包含账号密码</source>
            <translation>Le proxy ne peut pas contenir d’identifiant ni de mot de passe</translation>
        </message>
        <message>
            <location filename="../network.py" line="20" />
            <source>代理地址不能包含路径、查询参数或片段</source>
            <translation>Le proxy ne peut pas contenir de chemin, requête ou fragment</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="200" />
            <source>仍有直播间正在录制或转换，请先全部暂停并等待收尾完成</source>
            <translation>Une salle enregistre ou convertit encore. Mettez tout en pause et attendez la fin</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="274" />
            <source>找不到直播间</source>
            <translation>Salle introuvable</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="277" />
            <source>直播间地址不能为空</source>
            <translation>L’URL de la salle ne peut pas être vide</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="280" />
            <source>该直播间地址已经存在</source>
            <translation>Cette URL existe déjà</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="283" />
            <source>保存目录不能为空</source>
            <translation>Le dossier de destination ne peut pas être vide</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="291" />
            <source>检测间隔必须是正整数</source>
            <translation>L’intervalle doit être un entier positif</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="293" />
            <source>检测间隔不能低于 30 秒</source>
            <translation>L’intervalle ne peut pas être inférieur à 30 secondes</translation>
        </message>
        <message>
            <location filename="../ffmpeg.py" line="28" />
            <location filename="../room_model.py" line="299" />
            <location filename="../room_model.py" line="301" />
            <location filename="../view_models.py" line="200" />
            <source>分段分钟数必须是正整数</source>
            <translation>La durée des segments doit être un entier positif</translation>
        </message>
        <message>
            <location filename="../room_model.py" line="305" />
            <source>不支持该输出格式</source>
            <translation>Format de sortie non pris en charge</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="187" />
            <source>默认录制目录不能为空</source>
            <translation>Le dossier d’enregistrement par défaut ne peut pas être vide</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="198" />
            <source>轮询间隔不能低于 30 秒</source>
            <translation>La scrutation ne peut pas être inférieure à 30 secondes</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="202" />
            <source>磁盘保护阈值必须是 1 至 1024 GB</source>
            <translation>Le seuil disque doit être compris entre 1 et 1024 Go</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="243" />
            <source>设置保存后校验失败，请重试</source>
            <translation>Échec de la vérification des réglages enregistrés. Réessayez</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="288" />
            <source>选择文件夹</source>
            <translation>Choisir un dossier</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="356" />
            <source>预检失败：{error}</source>
            <translation>Échec du contrôle : {error}</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="372" />
            <source>导入失败：{error}</source>
            <translation>Échec de l’import : {error}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="94" />
            <source>找不到已锁定的解析源码：{path}</source>
            <translation>Source du résolveur verrouillé introuvable : {path}</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="133" />
            <source>暂不支持该直播间链接</source>
            <translation>Cette URL de direct n’est pas encore prise en charge</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="165" />
            <source>当前锁定版淘宝解析器要求登录会话，Reco Box 不导入账号或 Cookie，因此暂不尝试绕过；后续需要实现匿名公开接口后才能启用。</source>
            <translation>Le résolveur Taobao verrouillé exige une session connectée. Reco Box n’importe ni compte ni cookie et ne contourne pas cette restriction ; une interface publique anonyme est nécessaire.</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="212" />
            <source>该 TwitCasting 直播间要求登录，匿名模式不可用</source>
            <translation>Cette salle TwitCasting exige une connexion ; le mode anonyme est indisponible</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="219" />
            <source>该 TwitCasting 页面无法匿名读取，可能需要登录或已受访问限制</source>
            <translation>Cette page TwitCasting n’est pas lisible anonymement ; connexion ou restriction possible</translation>
        </message>
        <message>
            <location filename="../resolver.py" line="243" />
            <source>TwitCasting 未返回可录制的公开播放地址</source>
            <translation>TwitCasting n’a renvoyé aucune URL publique enregistrable</translation>
        </message>
        <message>
            <location filename="../recording.py" line="206" />
            <source>未找到 FFmpeg；开发版需要设置 RECO_BOX_FFMPEG</source>
            <translation>FFmpeg introuvable ; la version de développement doit définir RECO_BOX_FFMPEG</translation>
        </message>
        <message>
            <location filename="../recording.py" line="236" />
            <source>磁盘剩余空间低于 {minimum_free_gb:g} GB，已阻止开始录制</source>
            <translation>Espace libre inférieur à {minimum_free_gb:g} Go ; enregistrement bloqué</translation>
        </message>
        <message>
            <location filename="../recording.py" line="330" />
            <source>未找到可用直播线路</source>
            <translation>Aucune route de direct utilisable</translation>
        </message>
        <message>
            <location filename="../recording.py" line="487" />
            <source>未找到 ffprobe</source>
            <translation>ffprobe introuvable</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="95" />
            <location filename="../recording.py" line="492" />
            <source>录制目录中没有媒体文件</source>
            <translation>Aucun fichier multimédia dans le dossier d’enregistrement</translation>
        </message>
        <message>
            <location filename="../preview.py" line="16" />
            <location filename="../preview.py" line="36" />
            <location filename="../preview.py" line="41" />
            <source>直播预览</source>
            <translation>Aperçu du direct</translation>
        </message>
        <message>
            <location filename="../preview.py" line="37" />
            <source>尚未取得直播流，请先点击“立即检查并录制”</source>
            <translation>Aucun flux disponible. Cliquez d’abord sur « Vérifier et enregistrer »</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="85" />
            <source>ffprobe 验证失败</source>
            <translation>Échec de validation ffprobe</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="89" />
            <source>ffprobe 返回了无效 JSON</source>
            <translation>ffprobe a renvoyé un JSON invalide</translation>
        </message>
        <message>
            <location filename="../media_probe.py" line="112" />
            <source>文件中没有可识别的音视频流</source>
            <translation>Aucun flux audio ou vidéo reconnaissable</translation>
        </message>
        <message>
            <location filename="../ffmpeg.py" line="26" />
            <source>必须先设置录制保存目录</source>
            <translation>Définissez d’abord le dossier d’enregistrement</translation>
        </message>
        <message>
            <location filename="../output_paths.py" line="46" />
            <location filename="../output_paths.py" line="53" />
            <source>输出格式必须是简单扩展名</source>
            <translation>Le format de sortie doit être une extension simple</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="418" />
            <source>Resolver 调度限制</source>
            <translation>Limites de planification du Resolver</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="421" />
            <source>最大并发</source>
            <translation>Concurrence maximale</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="422" />
            <source>单平台并发</source>
            <translation>Concurrence par plateforme</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="423" />
            <source>平台冷却（秒）</source>
            <translation>Délai d’attente de la plateforme (secondes)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="425" />
            <source>用于分散解析请求；修改后立即影响新的监控请求。</source>
            <translation>Utilisé pour répartir les requêtes du resolver ; les modifications s’appliquent immédiatement aux nouvelles requêtes de surveillance.</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="196" />
            <source>轮询、分段和解析限制参数必须是整数</source>
            <translation>Les paramètres de sondage, de segmentation et de limites du resolver doivent être des entiers</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="204" />
            <source>Resolver 最大并发必须是 1 至 32</source>
            <translation>La concurrence maximale du Resolver doit être comprise entre 1 et 32</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="206" />
            <source>单平台并发必须是 1 至 16</source>
            <translation>La concurrence par plateforme doit être comprise entre 1 et 16</translation>
        </message>
        <message>
            <location filename="../view_models.py" line="208" />
            <source>平台冷却必须是 0 至 3600 秒</source>
            <translation>Le délai d’attente de la plateforme doit être compris entre 0 et 3600 secondes</translation>
        </message>
    </context>
    <context>
        <name>Main</name>
        <message>
            <location filename="../ui/Main.qml" line="35" />
            <source>全部状态</source>
            <translation>Tous les statuts</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="36" />
            <location filename="../ui/Main.qml" line="241" />
            <location filename="../ui/Main.qml" line="448" />
            <source>录制中</source>
            <translation>Enregistrement</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="241" />
            <source>卡顿收尾</source>
            <translation>Finalisation après blocage</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="37" />
            <location filename="../ui/Main.qml" line="241" />
            <source>监控中</source>
            <translation>Surveillance</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="38" />
            <location filename="../ui/Main.qml" line="241" />
            <source>未开始</source>
            <translation>Non démarré</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="41" />
            <source>默认排序</source>
            <translation>Tri par défaut</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="42" />
            <source>名称正序</source>
            <translation>Séquence de noms</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="43" />
            <source>名称倒序</source>
            <translation>Nom dans l'ordre inverse</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="46" />
            <source>原画</source>
            <translation>Peinture originale</translation>
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
            <translation>Lisse</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="54" />
            <source>线路1</source>
            <translation>Ligne 1</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="55" />
            <source>线路2</source>
            <translation>Ligne 2</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="56" />
            <source>线路3</source>
            <translation>Ligne 3</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="57" />
            <source>线路4</source>
            <translation>Ligne 4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="58" />
            <source>线路5</source>
            <translation>Ligne 5</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="163" />
            <location filename="../ui/Main.qml" line="280" />
            <location filename="../ui/Main.qml" line="287" />
            <source>添加直播间</source>
            <translation>Ajouter une salle de diffusion en direct</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="166" />
            <source>一键全部开始录屏 / 监控</source>
            <translation>Démarrez l'enregistrement/la surveillance en un seul clic</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="167" />
            <source>已启用全部直播间并立即检查</source>
            <translation>Toutes les salles de diffusion en direct ont été activées et vérifiées maintenant</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="170" />
            <source>一键全部暂停录屏 / 监控</source>
            <translation>Suspendre tous les enregistrements/surveillances d'écran en un seul clic</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="171" />
            <source>已请求全部暂停；正在录制的文件会先安全收尾</source>
            <translation>Toutes les pauses ont été demandées ; les fichiers en cours d'enregistrement seront d'abord terminés en toute sécurité</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="173" />
            <location filename="../ui/Main.qml" line="370" />
            <source>删除全部直播间</source>
            <translation>Supprimer toutes les salles de diffusion en direct</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="175" />
            <source>全局设置、录制历史和运行日志</source>
            <translation>Paramètres globaux, historique d'enregistrement et journaux d'exécution</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="181" />
            <source>搜索主播、标题或链接…</source>
            <translation>Rechercher une ancre, un titre ou un lien…</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="189" />
            <source>直播间</source>
            <translation>Salle de diffusion en direct</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="241" />
            <source>转 MP4</source>
            <translation>en MP4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="241" />
            <source>检查中</source>
            <translation>Vérification</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="244" />
            <source>暂无直播间标题</source>
            <translation>Aucun titre de salle de diffusion en direct pour l'instant</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>分段：</source>
            <translation>Segmentation :</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>每 </source>
            <translation>Chaque</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source> 分钟</source>
            <translation>minutes</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source>关闭</source>
            <translation>Fermer</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="245" />
            <source> · 完成后转 MP4</source>
            <translation>· Convertir en MP4 une fois terminé</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="250" />
            <source>检测间隔 </source>
            <translation>Intervalle de détection</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="250" />
            <source> 秒</source>
            <translation>secondes</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="254" />
            <source>错误：</source>
            <translation>Erreur :</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>停止并暂停</source>
            <translation>Arrêter et mettre en pause</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>暂停监控</source>
            <translation>Suspension suspendue</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="259" />
            <source>开始监控</source>
            <translation>Démarrer la surveillance</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="264" />
            <source>检查并录制</source>
            <translation>Vérifier et enregistrer</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="268" />
            <source>预览</source>
            <translation>Aperçu</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="269" />
            <source>编辑</source>
            <translation>Modifier</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="271" />
            <source>删除</source>
            <translation>Supprimer</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>还没有直播间</source>
            <translation>Il n'y a pas encore de salle de diffusion en direct</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="278" />
            <source>没有符合当前筛选条件的直播间</source>
            <translation>Aucune salle de diffusion en direct ne répond aux conditions de filtrage actuelles.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="279" />
            <source>添加公开直播间地址后，Reco Box 会自动开始监控</source>
            <translation>Après avoir ajouté l'adresse de la salle de diffusion publique en direct, Reco Box démarrera automatiquement la surveillance</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="279" />
            <source>调整状态筛选或搜索关键词后重试</source>
            <translation>Ajustez le filtre d'état ou recherchez des mots-clés et réessayez</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="290" />
            <source>直播间添加成功</source>
            <translation>Salle de diffusion en direct ajoutée avec succès</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="293" />
            <location filename="../ui/Main.qml" line="322" />
            <source>直播间地址</source>
            <translation>Adresse de la salle de diffusion en direct</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="294" />
            <source>粘贴公开直播间链接</source>
            <translation>Coller le lien de la salle de diffusion publique en direct</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="295" />
            <source>主播名字（可稍后自动识别）</source>
            <translation>Nom de l'ancre (peut être automatiquement reconnu ultérieurement)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="296" />
            <source>待识别主播</source>
            <translation>Ancre à identifier</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="297" />
            <location filename="../ui/Main.qml" line="335" />
            <source>保存目录</source>
            <translation>Enregistrer le répertoire</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="298" />
            <location filename="../ui/Main.qml" line="336" />
            <location filename="../ui/Main.qml" line="410" />
            <source>选择目录</source>
            <translation>Sélectionner le répertoire</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="299" />
            <source>格式、画质、检测间隔和分段使用已保存的全局默认设置。</source>
            <translation>Le format, la qualité, l'intervalle de détection et la segmentation utilisent les paramètres globaux par défaut enregistrés.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="306" />
            <source>编辑直播间</source>
            <translation>Modifier la salle de diffusion en direct</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="321" />
            <source>基础编辑</source>
            <translation>Édition de base</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="324" />
            <source>主播名字</source>
            <translation>Nom de l'ancre</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="326" />
            <source>直播间标题</source>
            <translation>Titre de la salle de diffusion en direct</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="327" />
            <source>可以留空，开播后自动更新</source>
            <translation>peut être laissé vide et sera automatiquement mis à jour après la diffusion.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="329" />
            <source>录制设置</source>
            <translation>Paramètres d'enregistrement</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="332" />
            <source>文件名（不分段时使用）</source>
            <translation>Nom du fichier (utilisé lorsqu'il n'est pas segmenté)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="332" />
            <source>留空则使用 1</source>
            <translation>Laisser vide pour utiliser 1</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="333" />
            <location filename="../ui/Main.qml" line="415" />
            <source>检测间隔（秒）</source>
            <translation>Intervalle de détection (secondes)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="337" />
            <source>代理地址（可选）</source>
            <translation>Adresse proxy (facultatif)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="338" />
            <source>例如 127.0.0.1:7890；留空表示直连</source>
            <translation>Par exemple, 127.0.0.1:7890 ; laisser vide pour indiquer une connexion directe</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="341" />
            <source>录制清晰度</source>
            <translation>Clarté d'enregistrement</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="342" />
            <source>录制路线</source>
            <translation>Itinéraire d'enregistrement</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="346" />
            <source>输出格式</source>
            <translation>Format de sortie</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="347" />
            <source>分段时长（分钟）</source>
            <translation>Durée du segment (minutes)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="347" />
            <source>启用</source>
            <translation>Activer</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="349" />
            <source>分段文件固定按 1、2、3… 排列，最后一段按实际剩余时长保存。</source>
            <translation>Les fichiers segmentés sont organisés de manière fixe en 1, 2, 3..., et le dernier segment est enregistré en fonction de la durée restante réelle.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="350" />
            <source>录制完成后转为 MP4（成功后删除 TS）</source>
            <translation>Convertir en MP4 une fois l'enregistrement terminé (supprimer TS après succès)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="351" />
            <source>纯音频模式</source>
            <translation>Mode audio uniquement</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="352" />
            <source>录制弹幕（仅在平台适配完成后生效）</source>
            <translation>Barrages records (ne prendront effet qu'une fois l'adaptation de la plateforme terminée)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="359" />
            <location filename="../ui/Main.qml" line="378" />
            <source>取消</source>
            <translation>Annuler</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="361" />
            <source>保存</source>
            <translation>Enregistrer</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="362" />
            <source>直播间设置已保存</source>
            <translation>Les paramètres de la salle de diffusion en direct ont été enregistrés</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="376" />
            <source>确定从 Reco Box 中删除全部直播间吗？
录制文件和历史记录不会删除。</source>
            <translation>Êtes-vous sûr de vouloir supprimer toutes les salles de diffusion en direct de Reco Box ?
Les fichiers d'enregistrement et l'historique ne seront pas supprimés.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="378" />
            <source>确认全部删除</source>
            <translation>Confirmer la suppression de tous</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="378" />
            <source>已删除全部直播间</source>
            <translation>Toutes les salles de diffusion en direct ont été supprimées</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="384" />
            <location filename="../ui/Main.qml" line="389" />
            <source>全局设置</source>
            <translation>Paramètres globaux</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="389" />
            <source>录制历史</source>
            <translation>Historique des enregistrements</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="389" />
            <source>运行日志</source>
            <translation>Journal d'exécution</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="396" />
            <source>新直播间默认设置</source>
            <translation>Paramètres par défaut pour la nouvelle salle de diffusion en direct</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="396" />
            <source>导入旧配置</source>
            <translation>Importer l'ancienne configuration</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="397" />
            <source>界面语言</source>
            <translation>Langage de l'interface</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="404" />
            <source>界面语言已切换</source>
            <translation>La langue de l'interface a été changée</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="408" />
            <source>只影响以后新增或导入的直播间；已有直播间在卡片中单独编辑。</source>
            <translation>affecte uniquement les salles de diffusion en direct qui seront ajoutées ou importées à l'avenir ; Les salles de diffusion en direct existantes peuvent être modifiées séparément dans la carte.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="409" />
            <source>默认录制目录</source>
            <translation>Répertoire d'enregistrement par défaut</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="413" />
            <source>默认格式</source>
            <translation>Format par défaut</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="414" />
            <source>默认画质</source>
            <translation>Qualité par défaut</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="416" />
            <source>磁盘保护（GB）</source>
            <translation>Protection du disque (Go)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="426" />
            <source>默认代理地址（可选）</source>
            <translation>Adresse proxy par défaut (facultatif)</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="427" />
            <source>新直播间继承；留空表示直连</source>
            <translation>Héritage d'une nouvelle salle de diffusion en direct ; laisser vide pour indiquer une connexion directe</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="428" />
            <source>新直播间默认启用分段</source>
            <translation>Les nouvelles salles de diffusion en direct activent la segmentation par défaut</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="428" />
            <location filename="../ui/Main.qml" line="429" />
            <source>设置已更改，请点击保存设置</source>
            <translation>Les paramètres ont été modifiés, veuillez cliquer pour enregistrer les paramètres</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="429" />
            <source>每段</source>
            <translation>Chaque paragraphe</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="429" />
            <source>分钟，最后一段按实际时长保存</source>
            <translation>minutes, le dernier segment est sauvegardé en fonction de la durée réelle</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="432" />
            <source>启动后自动监控 · 关闭窗口最小化到托盘 · 不随 Windows 开机启动</source>
            <translation>Surveiller automatiquement après le démarrage · Fermez la fenêtre et réduisez-la dans la barre d'état · Ne démarrez pas au démarrage de Windows</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>保存设置</source>
            <translation>Enregistrer les paramètres</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>已保存并确认：以后新增直播间默认每 </source>
            <translation>Enregistré et confirmé : valeur par défaut pour chaque nouvelle salle de diffusion en direct à l'avenir</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source> 分钟分段</source>
            <translation>segments de minutes</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="434" />
            <source>已保存并确认：以后新增直播间默认不分段</source>
            <translation>Enregistré et confirmé : les nouvelles salles de diffusion en direct ne seront plus segmentées par défaut à l'avenir.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="436" />
            <source>已保存并确认</source>
            <translation>Enregistré et confirmé</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="436" />
            <source>设置已更改</source>
            <translation>Paramètres modifiés</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>可播放</source>
            <translation>Peut être joué</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>转 MP4 中</source>
            <translation>Convertir en MP4</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>已完成</source>
            <translation>Terminé</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="448" />
            <source>失败</source>
            <translation>a échoué</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="449" />
            <location filename="../ui/Main.qml" line="514" />
            <source>播放</source>
            <translation>Jouer</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="450" />
            <source>目录</source>
            <translation>Répertoire</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="455" />
            <source>这里只显示脱敏后的状态和错误，不保存完整临时播放地址。</source>
            <translation>Seuls l'état et les erreurs après désensibilisation sont affichés ici, et l'adresse de lecture temporaire complète n'est pas enregistrée.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="480" />
            <source>直播流播放失败</source>
            <translation>Échec de la lecture du flux en direct</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="484" />
            <source>直播流格式无效或播放器无法解码</source>
            <translation>Le format du flux en direct n'est pas valide ou le lecteur ne peut pas le décoder</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="508" />
            <source>正在准备预览……</source>
            <translation>Préparation de l'aperçu...</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="509" />
            <source>正在连接直播流并等待首帧……</source>
            <translation>Connexion au flux en direct et attente de la première image...</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="514" />
            <source>暂停</source>
            <translation>Pause</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="514" />
            <source>静音</source>
            <translation>Sourdine</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="520" />
            <source>导入 DouyinLiveRecorder 旧配置</source>
            <translation>Importer l'ancienne configuration de DouyinLiveRecorder</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="524" />
            <source>选择旧程序根目录或其中的 config 文件夹。</source>
            <translation>Sélectionnez l'ancien répertoire racine du programme ou le dossier de configuration qu'il contient.</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="525" />
            <source>选择文件夹</source>
            <translation>Sélectionner un dossier</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>1. 预检</source>
            <translation>1. Pré-vérification</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>2. 确认导入</source>
            <translation>2. Confirmer l'importation</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="526" />
            <source>可导入直播间</source>
            <translation>peut être importé dans la salle de diffusion en direct</translation>
        </message>
        <message>
            <location filename="../ui/Main.qml" line="528" />
            <source>不会修改旧配置；Cookie、令牌、账号、密码和推送凭据不会导入。</source>
            <translation>Les anciennes configurations ne seront pas modifiées ; les cookies, jetons, comptes, mots de passe et informations d'identification push ne seront pas importés.</translation>
        </message>
    </context>
</TS>
